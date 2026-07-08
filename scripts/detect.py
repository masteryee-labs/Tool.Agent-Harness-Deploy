#!/usr/bin/env python3
"""detect.py ??Detect which AI coding tools are installed on this machine.

Reads adapters/registry.json, runs each tool's detection checks, prints a report.
This is the first step of the distill pipeline. Detection is sacred: a tool not
detected is a tool not synced. Never fabricate detection results.

Usage:
    python scripts/detect.py
    python scripts/detect.py --json   # machine-readable output
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Make the repo root importable when run as a script.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from adapters import get_adapter, all_tool_ids  # noqa: E402


def detect_all(project_root: str = ".") -> list[dict]:
    results = []
    for tid in all_tool_ids():
        adapter = get_adapter(tid, project_root=project_root)
        det = adapter.detect()
        results.append({
            "tool_id": det.tool_id,
            "name": det.name,
            "detected": det.detected,
            "evidence": det.evidence,
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect installed AI coding tools.")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of human report")
    ap.add_argument("--project-root", default=".", help="project root (default: cwd)")
    args = ap.parse_args()

    results = detect_all(args.project_root)
    detected = [r for r in results if r["detected"]]
    not_detected = [r for r in results if not r["detected"]]

    if args.json:
        print(json.dumps({"detected": detected, "not_detected": not_detected}, indent=2,
                         ensure_ascii=False))
        return 0

    print("== Agent Harness Deploy ??Tool Detection ==")
    print()
    print(f"Detected ({len(detected)}):")
    for r in detected:
        print(f"  [+] {r['name']:<22} ({r['tool_id']})  {r['evidence']}")
    print()
    print(f"Not detected ({len(not_detected)}):")
    for r in not_detected:
        print(f"  [-] {r['name']:<22} ({r['tool_id']})")
    print()
    print(f"Summary: {len(detected)}/{len(results)} tools detected.")
    print("Next: python scripts/distill.py   (syncs to detected tools only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
