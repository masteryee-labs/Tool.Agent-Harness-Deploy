#!/usr/bin/env python3
"""plan_dispatch.py ??Dependency graph analysis + file ownership allocation + conflict detection.

The Commander calls this BEFORE dispatching parallel Workers. It:

  1. Analyzes which files each subtask touches (from grep/AST scan)
  2. Detects file ownership conflicts (two subtasks touching the same file)
  3. Allocates files to workers (disjoint sets ??no overlap)
  4. Suggests Nuwa cognitive angles for each subtask (from the deployer's
     Nuwa 3-tree system + any user-distilled perspective skills)
  5. Outputs a JSON dispatch plan the Commander can paste into Worker prompts

Usage:
  python scripts/plan_dispatch.py --analyze --subtasks subtasks.json
  python scripts/plan_dispatch.py --analyze --subtasks subtasks.json --json

subtasks.json format:
  [
    {
      "id": "st-1",
      "goal": "Fix backup logic in sync.py",
      "files_hint": ["scripts/sync.py", "adapters/base.py"]
    },
    {
      "id": "st-2",
      "goal": "Add new adapter for tool X",
      "files_hint": ["adapters/tool_x.py", "adapters/registry.json"]
    }
  ]

Output (JSON):
  {
    "subtasks": [
      {
        "id": "st-1",
        "owned_files": ["scripts/sync.py"],
        "shared_files": ["adapters/base.py"],   # needs serialization
        "conflicts": [],
        "nuwa_angles": ["edge-case", "dependency"],
        "parallel_safe": true,
        "worktree": "builder-a"
      },
      ...
    ],
    "conflicts": [
      {
        "file": "adapters/base.py",
        "subtasks": ["st-1", "st-2"],
        "resolution": "serialize",
        "suggested_order": ["st-1", "st-2"]
      }
    ],
    "worktrees": ["builder-a", "builder-b"],
    "summary": "2 subtasks, 1 conflict (adapters/base.py), 2 worktrees needed"
  }
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent

# Nuwa's 3 cognitive angles (from Docs/Agents/nuwa.md)
NUWA_ANGLES = {
    "edge-case": {
        "name": "Edge Case Breaker",
        "question": "What input, state, or condition would break this?",
        "mindset": "adversarial",
    },
    "dependency": {
        "name": "Dependency Inspector",
        "question": "What else depends on what I'm changing, and will it break?",
        "mindset": "structural",
    },
    "regression": {
        "name": "Regression Prophet",
        "question": "What previously-working behavior will this change break?",
        "mindset": "historical",
    },
}


def _grep_files(pattern: str, path: str = ".") -> list[str]:
    """Find files matching a pattern (import/reference grep)."""
    try:
        r = subprocess.run(
            ["rg", "-l", "--no-heading", pattern, path],
            capture_output=True, text=True, timeout=10, cwd=str(ROOT)
        )
        if r.returncode == 0:
            return [f.strip() for f in r.stdout.strip().split("\n") if f.strip()]
    except Exception:
        pass
    return []


def _expand_file_hints(files_hint: list[str]) -> set[str]:
    """Given explicit file hints, expand to include files that import/reference them.

    For each file in the hint, grep for its module name to find dependents.
    This catches the "I'm changing base.py but 10 files import it" case.
    """
    touched = set(files_hint)

    for f in files_hint:
        # Derive module name from path (e.g. adapters/base.py ??"base" or "from .base")
        p = Path(f)
        if p.suffix == ".py":
            mod_name = p.stem
            # Find files that import this module
            importers = _grep_files(
                rf"(from \. import {mod_name}|from \.{mod_name}|import {mod_name}|from \.\.\.{mod_name})",
            )
            touched.update(importers)
        elif f.endswith(".json"):
            # Find files that reference this JSON path
            ref = p.name
            refs = _grep_files(re.escape(ref))
            touched.update(refs)

    return touched


def _detect_conflicts(subtasks: list[dict]) -> list[dict]:
    """Detect files touched by multiple subtasks."""
    file_to_subtasks: dict[str, list[str]] = defaultdict(list)

    for st in subtasks:
        for f in st.get("_expanded_files", []):
            file_to_subtasks[f].append(st["id"])

    conflicts = []
    for f, sts in file_to_subtasks.items():
        if len(sts) > 1:
            conflicts.append({
                "file": f,
                "subtasks": sts,
                "resolution": "serialize",
                "suggested_order": sts,  # first-listed goes first
            })

    return conflicts


def _allocate_ownership(subtasks: list[dict], conflicts: list[dict]) -> dict:
    """Allocate files to workers as disjoint sets.

    Files in conflict ??assigned to the first subtask that touches them (serialized).
    Other subtasks must wait for that subtask to finish before touching the file.
    Files not in conflict ??owned by the single subtask that touches them.
    """
    conflict_files = {c["file"] for c in conflicts}
    conflict_owner = {}
    for c in conflicts:
        # First subtask in suggested_order owns the file
        conflict_owner[c["file"]] = c["suggested_order"][0]

    allocation = {}
    for st in subtasks:
        owned = []
        shared = []
        for f in st.get("_expanded_files", []):
            if f in conflict_files:
                if conflict_owner[f] == st["id"]:
                    owned.append(f)  # This subtask owns the conflicting file
                else:
                    shared.append(f)  # Must wait for the owner
            else:
                owned.append(f)
        allocation[st["id"]] = {
            "owned_files": sorted(set(owned)),
            "shared_files": sorted(set(shared)),
        }

    return allocation


def _suggest_nuwa_angles(st: dict) -> list[str]:
    """Suggest which Nuwa cognitive angles to apply to this subtask.

    Heuristics:
    - If the subtask touches >2 files ??dependency angle (check blast radius)
    - If the subtask goal mentions "fix", "bug", "error", "edge" ??edge-case angle
    - If the subtask goal mentions "refactor", "change", "update", "modify" ??regression angle
    - Default: all 3 angles (full Nuwa)
    """
    goal = st.get("goal", "").lower()
    files = st.get("_expanded_files", [])

    angles = []

    if any(kw in goal for kw in ["fix", "bug", "error", "edge", "crash", "fail"]):
        angles.append("edge-case")

    if len(files) > 2 or any(kw in goal for kw in ["refactor", "change", "update", "modify", "rename"]):
        angles.append("dependency")
        angles.append("regression")

    if not angles:
        angles = ["edge-case", "dependency", "regression"]

    return list(dict.fromkeys(angles))  # dedupe, preserve order


def _assign_worktrees(subtasks: list[dict], allocation: dict) -> dict:
    """Assign a worktree (builder-a, builder-b, ...) to each parallel-safe subtask."""
    worktree_map = {}
    wt_idx = 0
    for st in subtasks:
        wt_name = f"builder-{chr(ord('a') + wt_idx)}"
        worktree_map[st["id"]] = wt_name
        wt_idx += 1
    return worktree_map


def analyze(subtasks: list[dict]) -> dict:
    """Full analysis: expand files, detect conflicts, allocate, suggest angles."""
    # Step 1: Expand file hints (find dependents via grep)
    for st in subtasks:
        st["_expanded_files"] = sorted(_expand_file_hints(st.get("files_hint", [])))

    # Step 2: Detect conflicts
    conflicts = _detect_conflicts(subtasks)

    # Step 3: Allocate ownership
    allocation = _allocate_ownership(subtasks, conflicts)

    # Step 4: Suggest Nuwa angles
    for st in subtasks:
        st["_nuwa_angles"] = _suggest_nuwa_angles(st)

    # Step 5: Assign worktrees
    worktree_map = _assign_worktrees(subtasks, allocation)

    # Build output
    result_subtasks = []
    for st in subtasks:
        alloc = allocation[st["id"]]
        has_conflict = any(
            st["id"] in c["subtasks"] for c in conflicts
        )
        result_subtasks.append({
            "id": st["id"],
            "goal": st["goal"],
            "owned_files": alloc["owned_files"],
            "shared_files": alloc["shared_files"],
            "conflicts": [c for c in conflicts if st["id"] in c["subtasks"]],
            "nuwa_angles": st["_nuwa_angles"],
            "parallel_safe": len(alloc["shared_files"]) == 0,
            "worktree": worktree_map[st["id"]],
        })

    summary = (
        f"{len(subtasks)} subtasks, "
        f"{len(conflicts)} conflict(s)"
        f"{', ' + str(len(set(w for w in worktree_map.values()))) + ' worktrees needed' if subtasks else ''}"
    )

    return {
        "subtasks": result_subtasks,
        "conflicts": conflicts,
        "worktrees": sorted(set(worktree_map.values())),
        "summary": summary,
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Analyze subtasks for file ownership, conflicts, and Nuwa angle assignment."
    )
    ap.add_argument("--analyze", action="store_true", help="Run analysis")
    ap.add_argument("--subtasks", required=True, help="Path to subtasks.json")
    ap.add_argument("--json", action="store_true", help="Output as JSON")
    args = ap.parse_args()

    if not args.analyze:
        ap.print_help()
        return 1

    subtask_path = Path(args.subtasks)
    if not subtask_path.exists():
        print(f"  [!] Subtasks file not found: {subtask_path}")
        return 1

    subtasks = json.loads(subtask_path.read_text(encoding="utf-8-sig"))
    result = analyze(subtasks)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("== Agent Harness Deploy Dispatch Planner ==")
        print()
        for st in result["subtasks"]:
            tag = "PARALLEL" if st["parallel_safe"] else "SERIAL"
            print(f"  [{tag}] {st['id']}: {st['goal']}")
            print(f"         Worktree: {st['worktree']}")
            print(f"         Owned:    {st['owned_files']}")
            if st["shared_files"]:
                print(f"         Shared:   {st['shared_files']} (wait for owner)")
            print(f"         Nuwa:     {st['nuwa_angles']}")
            if st["conflicts"]:
                for c in st["conflicts"]:
                    print(f"         Conflict: {c['file']} (with {c['subtasks']})")
            print()

        if result["conflicts"]:
            print("  Conflicts:")
            for c in result["conflicts"]:
                print(f"    {c['file']}: {c['subtasks']} ??{c['resolution']}")
            print()

        print(f"  Worktrees: {result['worktrees']}")
        print(f"  Summary:   {result['summary']}")
        print()
        print("  Next:")
        for wt in result["worktrees"]:
            print(f"    python scripts/worktree.py create {wt}")
        print("    (dispatch Workers with owned_files from above)")
        print("    (after all report: merge each worktree, then clean)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
