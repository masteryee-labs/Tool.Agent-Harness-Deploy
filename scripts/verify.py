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


def verify_all(project_root: str = ".") -> dict:
    results = []
    for tid in all_tool_ids():
        adapter = get_adapter(tid, project_root=project_root)
        det = adapter.detect()
        if not det.detected:
            continue
        checks = adapter.verify()
        for label, ok, evidence in checks:
            results.append({
                "tool_id": tid,
                "name": adapter.name,
                "target": label,
                "ok": ok,
                "evidence": evidence,
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
