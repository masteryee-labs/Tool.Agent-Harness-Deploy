#!/usr/bin/env python3
"""Fetch nuwa-skill repo files into core/assets/skills/nuwa-skill/ (vendored)."""
import urllib.request
import urllib.parse
import os
import sys
from pathlib import Path

# Fix Windows console encoding for Chinese output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE = "https://raw.githubusercontent.com/alchaincyf/nuwa-skill/main"
ROOT = Path(__file__).resolve().parent.parent / "core" / "assets" / "skills" / "nuwa-skill"

# (relative_path, is_text) — skip images/promo/README translations/wechat QR
FILES = [
    # Core
    ("SKILL.md", True),
    ("LICENSE", True),
    ("README.md", True),          # main README (zh)
    ("README_EN.md", True),       # English README
    # References (extraction framework, fidelity scorecard, skill template)
    ("references/extraction-framework.md", True),
    ("references/fidelity-scorecard.md", True),
    ("references/skill-template.md", True),
    # Scripts
    ("scripts/download_subtitles.sh", True),
    ("scripts/merge_research.py", True),
    ("scripts/quality_check.py", True),
    ("scripts/srt_to_transcript.py", True),
    # Community / contributing
    ("COMMUNITY.md", True),
    ("CONTRIBUTING.md", True),
    # Example perspectives — 3 referenced in nuwa.md (munger/feynman/taleb)
    ("examples/munger-perspective/SKILL.md", True),
    ("examples/munger-perspective/FIDELITY.md", True),
    ("examples/munger-perspective/references/25-biases.md", True),
    ("examples/munger-perspective/references/research.md", True),
    ("examples/munger-perspective/references/查理芒格思想体系深度调研-20260404.md", True),
    ("examples/munger-perspective/references/芒格表达风格DNA分析.md", True),
    ("examples/feynman-perspective/SKILL.md", True),
    ("examples/feynman-perspective/FIDELITY.md", True),
    ("examples/feynman-perspective/references/research.md", True),
    ("examples/feynman-perspective/references/费曼外部评价调研.md", True),
    ("examples/feynman-perspective/references/费曼著作与系统思考调研-20260404.md", True),
    ("examples/feynman-perspective/references/费曼表达风格调研.md", True),
    ("examples/feynman-perspective/references/费曼重大决策调研-20260404.md", True),
    ("examples/feynman-perspective/references/费曼长对话与即兴思考方式调研-20260404.md", True),
    ("examples/taleb-perspective/SKILL.md", True),
    ("examples/taleb-perspective/FIDELITY.md", True),
    ("examples/taleb-perspective/references/research.md", True),
    ("examples/taleb-perspective/references/塔勒布外部批评调研.md", True),
    ("examples/taleb-perspective/references/塔勒布思想体系调研.md", True),
    ("examples/taleb-perspective/references/塔勒布深度对话调研.md", True),
    ("examples/taleb-perspective/references/塔勒布碎片表达与社交媒体人格调研.md", True),
    ("examples/taleb-perspective/references/塔勒布重大决策与实际行动调研-20260404.md", True),
]

def fetch(rel: str) -> bool:
    # URL-encode each path segment (Chinese filenames)
    parts = rel.split("/")
    encoded = "/".join(urllib.parse.quote(p, safe="") for p in parts)
    url = f"{BASE}/{encoded}"
    dst = ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size > 0:
        print(f"  SKIP {rel:70s} (exists, {dst.stat().st_size} bytes)")
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Agent-Harness-Deploy/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        dst.write_bytes(data)
        print(f"  OK  {rel:70s} {len(data):>7d} bytes")
        return True
    except Exception as e:
        print(f"  FAIL {rel:70s} {e}")
        return False

def main():
    print(f"Vendoring nuwa-skill into {ROOT}")
    ok = 0
    fail = 0
    for rel, _ in FILES:
        if fetch(rel):
            ok += 1
        else:
            fail += 1
    print(f"\nDone: {ok} OK, {fail} FAIL, {len(FILES)} total")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
