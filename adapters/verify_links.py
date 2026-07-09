"""verify_links.py — Check that referenced project files actually exist.

This is used by `scripts/verify.py` to verify deployed canonical files. It scans
markdown and config files for path-like references and confirms the target exists.

Rules:
- References are project-root relative.
- Paths in `allowed_missing` or starting with an `allowed_prefix` are reported but not flagged as failures.
- JSON/TOML/YAML are parsed and string values that look like paths are checked.
- The checker is intentionally conservative: tokens with wildcards, env vars, JSON/XML,
  or function-call syntax are skipped or must be explicitly allowed.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class LinkCheck:
    target: str
    exists: bool
    allowed: bool
    context: str = ""


@dataclass
class LinkReport:
    file: Path
    ok: bool
    missing: list[LinkCheck] = field(default_factory=list)
    allowed: list[LinkCheck] = field(default_factory=list)
    parse_error: Optional[str] = None


# Roots we consider resolvable. The rest of the string is captured until a delimiter.
_KNOWN_ROOTS = (
    r"distill/|core/|scripts/|Docs/|"
    r"\.agent/|\.agents/|\.claude/|\.codex/|\.devin/|\.cursor/|"
    r"\.open/|\.openclaw/|\.hermes/|\.zcode/|\.kimi/|\.opencode/"
)

# Markdown links, backticks, and bare paths with a known root.
# For bare paths, we require a leading space/bracket/punctuation to avoid matching
# in the middle of words.
_PATH_RE = re.compile(
    rf"""
    (?:\[([^\]]*)\]\(([^)]+)\))            # [text](path)
    |`([^`\n]+)`                            # `path`
    |(?:^|[\s\[\(<>:])
    ((?:{_KNOWN_ROOTS})
     [^\s\)\]\>`\n,]+)                     # path root
    """,
    re.VERBOSE,
)

# Characters that disqualify a token from being a resolvable path.
_INVALID_PATH_CHARS = set("<>*{}[]%|\\\"")

# Allowed file extensions for path checks.
_CHECK_EXTENSIONS = {".md", ".py", ".json", ".toml", ".yaml", ".yml", ".txt", ".mdc", ".mdx"}

# Common false positives that can be skipped automatically.
# These are prefixes, so `~` matches all `~/...` paths, etc.
DEFAULT_ALLOWED_MISSING = [
    "~",                       # home-relative paths (e.g. ~/.deep-memory/.venv)
    "%",                       # Windows env vars (e.g. %APPDATA%\Claude\)
    "read(",                   # read("...") calls
    "write(",                  # write("...") calls
    "{",                       # inline JSON strings
    "<",                       # XML/template tokens
    "/",                      # JSON pointers /goal /loop /correct/value
    "db/",                     # example schema
    "plans/",                  # template paths
    "rejected/",               # directory labels
    "distill/canon/",          # canonical directory references
    "core/assets/skills/nuwa-skill/",  # directory references
    "core/assets/vault/",      # vault directory references
    ".agent/loop_state_archive.md",
    ".agent/candidate_memory.jsonl",
    ".agent/context_flags.json",
    ".agent/knowledge_distill.md",
]


def _looks_like_path(token: str) -> bool:
    """Heuristic: strings with a slash and no invalid/wildcard characters."""
    if not token or "//" in token or "http" in token:
        return False
    if "/" not in token and "\\" not in token:
        return False
    if token.startswith("http://") or token.startswith("https://"):
        return False
    if any(c in token for c in _INVALID_PATH_CHARS):
        return False
    # Skip trailing punctuation
    if token[-1] in ".),;:":
        return False
    return True


def _extract_candidates(text: str) -> set[str]:
    """Extract path-like strings from a text block."""
    candidates = set()
    for m in _PATH_RE.finditer(text):
        for group in m.groups():
            if group is None:
                continue
            token = group.strip().strip("`'\"\n")
            token = token.split(" ")[0] if " " in token else token
            # Remove trailing punctuation likely introduced by markdown/ prose
            token = token.rstrip(".,;:)>")
            # Handle read("...") style: the whole token will start with read(
            if token.startswith("read(") or token.startswith("write("):
                candidates.add(token)
                continue
            if _looks_like_path(token):
                candidates.add(token)
    return candidates


def _normalize_path(target: str, project_root: Path) -> Path:
    """Resolve a project-root-relative path."""
    return (project_root / target.replace("\\", "/")).resolve()


def _is_allowed(target: str, allowed_missing: Optional[list[str]]) -> bool:
    """Return True if target is in allowed_missing or starts with an allowed prefix."""
    if not allowed_missing:
        return False
    for item in allowed_missing:
        if target == item or target.startswith(item):
            return True
    return False


def _check_text(text: str, file: Path, project_root: Path, allowed_missing: Optional[list[str]]) -> list[LinkCheck]:
    """Scan text for path references and return their existence status."""
    results = []
    for target in sorted(_extract_candidates(text)):
        target_path = _normalize_path(target, project_root)
        exists = target_path.exists()
        allowed = _is_allowed(target, allowed_missing)
        results.append(LinkCheck(target=target, exists=exists, allowed=allowed))
    return results


def _check_config_text(text: str, ext: str, file: Path, project_root: Path, allowed_missing: Optional[list[str]]) -> list[LinkCheck]:
    """Parse a JSON/TOML/YAML config and check string values that look like paths."""
    candidates = set()
    try:
        if ext == ".json":
            data = json.loads(text)
        elif ext == ".toml":
            try:
                import tomllib
                data = tomllib.loads(text)
            except Exception:
                try:
                    import tomli
                    data = tomli.loads(text)
                except Exception:
                    return []
        elif ext in (".yaml", ".yml"):
            try:
                import yaml
                data = yaml.safe_load(text)
            except Exception:
                return []
        else:
            return []
    except Exception:
        return []

    def _walk(obj):
        if isinstance(obj, dict):
            for v in obj.values():
                _walk(v)
        elif isinstance(obj, list):
            for v in obj:
                _walk(v)
        elif isinstance(obj, str):
            token = obj.strip().strip("`'\"")
            if _looks_like_path(token):
                candidates.add(token)

    _walk(data)

    results = []
    for target in sorted(candidates):
        target_path = _normalize_path(target, project_root)
        exists = target_path.exists()
        allowed = _is_allowed(target, allowed_missing)
        results.append(LinkCheck(target=target, exists=exists, allowed=allowed))
    return results


def check_file(file: Path, project_root: Path, allowed_missing: Optional[list[str]] = None) -> LinkReport:
    """Check a single file for path references and parse errors."""
    if allowed_missing is None:
        allowed_missing = DEFAULT_ALLOWED_MISSING

    report = LinkReport(file=file, ok=True)
    if not file.exists():
        report.ok = False
        report.parse_error = "file not found"
        return report

    try:
        text = file.read_text(encoding="utf-8")
    except Exception as e:
        report.ok = False
        report.parse_error = str(e)
        return report

    ext = file.suffix.lower()
    checks = _check_text(text, file, project_root, allowed_missing)

    if ext in {".json", ".toml", ".yaml", ".yml"}:
        try:
            config_checks = _check_config_text(text, ext, file, project_root, allowed_missing)
            checks.extend(config_checks)
        except Exception as e:
            report.parse_error = str(e)
            report.ok = False

    for check in checks:
        if check.allowed:
            report.allowed.append(check)
        elif not check.exists:
            report.missing.append(check)
            report.ok = False

    return report


def check_directory(
    directory: Path,
    project_root: Path,
    allowed_missing: Optional[list[str]] = None,
    extensions: Optional[set[str]] = None,
) -> list[LinkReport]:
    """Recursively check all files in a directory."""
    if allowed_missing is None:
        allowed_missing = DEFAULT_ALLOWED_MISSING
    if extensions is None:
        extensions = _CHECK_EXTENSIONS
    reports = []
    if not directory.exists():
        return reports
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions:
            reports.append(check_file(path, project_root, allowed_missing))
    return reports


def main() -> int:
    import argparse
    import sys

    ap = argparse.ArgumentParser(description="Verify referenced paths exist.")
    ap.add_argument("path", help="File or directory to check")
    ap.add_argument("--project-root", default=".", help="Project root for resolving paths")
    ap.add_argument("--allow-missing", action="append", default=[],
                    help="Path or prefix to allow missing (can repeat)")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    target = Path(args.path)

    allowed_missing = DEFAULT_ALLOWED_MISSING + args.allow_missing

    if target.is_file():
        reports = [check_file(target, project_root, allowed_missing)]
    elif target.is_dir():
        reports = check_directory(target, project_root, allowed_missing)
    else:
        print(f"[verify_links] not found: {target}")
        return 1

    failed = 0
    allowed_count = 0
    for r in reports:
        if r.missing:
            failed += len(r.missing)
            print(f"\nFAIL {r.file}")
            for m in r.missing:
                print(f"  missing: {m.target}")
            if r.parse_error:
                print(f"  parse error: {r.parse_error}")
        elif r.ok:
            print(f"PASS {r.file}")
        if r.allowed:
            allowed_count += len(r.allowed)

    if allowed_count:
        print(f"\n({allowed_count} references allowed missing)")

    if failed:
        print(f"\n{failed} missing reference(s)")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
