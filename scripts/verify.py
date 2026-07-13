#!/usr/bin/env python3
"""verify.py ??Read back every file written by sync.py and confirm integrity.

Verification is never self-assertion. This script reads the actual files on disk and
checks that the canonical body marker is present. A sync that skips verify is a failed
sync (red line #10).

Usage:
    python scripts/verify.py
    python scripts/verify.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from adapters import get_adapter, all_tool_ids  # noqa: E402
from adapters.verify_links import check_file, DEFAULT_ALLOWED_MISSING  # noqa: E402

# References that are commands or docs, not necessarily present in a deployed project.
# `scripts/worktree.py` and `scripts/plan_dispatch.py` are rewritten to `<config_root>/scripts/`
# during sync; other `scripts/` entries are repo/deployer-only commands.
BASE_ALLOWED_MISSING = DEFAULT_ALLOWED_MISSING + [
    "Docs/",
    # .agents/ files are runtime-generated (loop_state, session_state, handoff_letter, knowledge_distill)
    ".agents/",
    # Deployer-repo directories not present in a deployed project
    "adapters/",
    "scripts/verify.py",
    "scripts/distill.py",
    "scripts/detect.py",
    "scripts/sync.py",
    "scripts/verify_links.py",
]

# Tool config roots used by registry.json. A tool's entry file may reference other tools
# as examples, but it should not reference missing files inside its own root.
_TOOL_ROOTS = [
    ".claude/", ".codex/", ".devin/", ".agents/", ".cursor/",
    ".open/", ".openclaw/", ".hermes/", ".zcode/", ".kimi/", ".opencode/",
    ".github/", ".gemini/", ".clinerules/", ".roo/", ".continue/", ".windsurf/",
]

# Runtime-generated subpaths within a tool's config root. These are created at runtime
# by hooks and scripts, not at deploy time, so missing links to them are not errors.
_RUNTIME_GENERATED_SUBPATHS = [
    "loop_state.md",
    "loop_state/",
    "session_state/",
    "loop_state_archive.md",
    "loop_state_archive/",
    "context_flags/",
    "knowledge_distill.md",
    "handoff_letter.md",
    "user_profile.md",
    "tmp/",
]


def _allowed_missing_for(adapter) -> list[str]:
    """Build allowed-missing list for a given tool.

    The current tool's own config root is excluded from the allow list so that broken
    internal links (e.g. `.codex/COMMANDER.md` instead of `.codex/agents/COMMANDER.md`)
    are still flagged. All other tool roots are allowed because they are examples.

    Runtime-generated paths within the current tool's root (loop_state, session_state,
    knowledge_distill, etc.) are added to the allow list because they don't exist at
    deploy time — they're created by hooks and scripts at runtime.
    """
    current_root = adapter._config_root_rel()
    allowed = list(BASE_ALLOWED_MISSING)
    for root in _TOOL_ROOTS:
        # Exclude the tool's own config root so internal links are verified.
        if current_root and root.rstrip("/") == current_root.rstrip("/"):
            continue
        allowed.append(root)
    # Allow runtime-generated paths within the current tool's config root
    if current_root:
        for sub in _RUNTIME_GENERATED_SUBPATHS:
            allowed.append(current_root + sub)
    return allowed


def _verify_session_runtime(project_root: Path, runtime_root: str, tool_id: str) -> list[dict]:
    """Check session concurrency directories and helper scripts for a given runtime root.

    Each tool has its own config root (e.g. .agents/ for Antigravity, .claude/ for
    Claude Code). The runtime scripts and session state dirs live inside that root.
    """
    results = []
    root_dir = project_root / runtime_root
    for label, path in (
        ("session_state", root_dir / "session_state"),
        ("loop_state", root_dir / "loop_state"),
        ("loop_state_archive", root_dir / "loop_state_archive"),
    ):
        exists = path.exists()
        results.append({
            "tool_id": tool_id,
            "name": "session_runtime",
            "target": f"dir:{path}",
            "ok": exists,
            "evidence": f"{label} dir present" if exists else f"{label} dir missing",
        })
    # Critical helper scripts
    scripts_dir = root_dir / "scripts"
    for script in ("worktree.py", "plan_dispatch.py", "session_manager.py", "loop_memory_sync.py", "memory_audit.py", "pre_task_audit.py", "ahd_session.py"):
        path = scripts_dir / script
        exists = path.exists()
        results.append({
            "tool_id": tool_id,
            "name": "session_runtime",
            "target": f"script:{path}",
            "ok": exists,
            "evidence": f"{script} present" if exists else f"{script} missing",
        })
    return results


def verify_all(project_root: str = ".") -> dict:
    results = []
    project_root_path = Path(project_root).resolve()

    # First pass: detect tools and check per-tool session runtime dirs.
    # Each tool's runtime root is tool-specific (e.g. .agents/ for Antigravity).
    detected_adapters = []
    for tid in all_tool_ids():
        adapter = get_adapter(tid, project_root=project_root)
        det = adapter.detect()
        if not det.detected:
            continue
        detected_adapters.append(adapter)
        runtime_root = adapter._runtime_root_rel()
        results.extend(_verify_session_runtime(project_root_path, runtime_root, tid))

    # Second pass: per-tool entry file + asset verification + link checks.
    for adapter in detected_adapters:
        tid = adapter.tool_id
        checks = adapter.verify()
        for label, ok, evidence in checks:
            results.append({
                "tool_id": tid,
                "name": adapter.name,
                "target": label,
                "ok": ok,
                "evidence": evidence,
            })

        # Link/format check for the tool's entry file and config root
        entry_path = adapter.project_entry_path()
        if entry_path and entry_path.exists():
            allowed_missing = _allowed_missing_for(adapter)
            link_report = check_file(entry_path, project_root_path, allowed_missing)
            if not link_report.ok:
                for missing in link_report.missing:
                    results.append({
                        "tool_id": tid,
                        "name": adapter.name,
                        "target": f"link:{missing.target}",
                        "ok": False,
                        "evidence": f"missing from {entry_path}",
                    })
            results.append({
                "tool_id": tid,
                "name": adapter.name,
                "target": f"links:{entry_path}",
                "ok": link_report.ok,
                "evidence": f"{len(link_report.missing)} missing, {len(link_report.allowed)} allowed",
            })

    return {"checks": results, "pass": all(r["ok"] for r in results) if results else True}


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify synced config integrity.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--project-root", default=".")
    args = ap.parse_args()

    result = verify_all(args.project_root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["pass"] else 1

    print("== Agent Harness Deploy ??Verification ==")
    print()
    if not result["checks"]:
        print("No detected tools with written entries to verify.")
        return 0
    for r in result["checks"]:
        mark = "PASS" if r["ok"] else "FAIL"
        print(f"  [{mark}] {r['name']:<22} {r['target']}  ({r['evidence']})")
    print()
    print(f"Overall: {'PASS' if result['pass'] else 'FAIL'}  ({sum(1 for r in result['checks'] if r['ok'])}/{len(result['checks'])} checks)")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
