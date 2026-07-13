#!/usr/bin/env python3
"""Tests for memory_audit.py."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import scripts.memory_audit as memory_audit


def test_memory_audit_merges_candidates():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        ahd_session = memory_audit.ahd_session
        original = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: cwd
        try:
            sid = "s-memory"
            ss_dir = cwd / ".agents" / "session_state" / sid
            ss_dir.mkdir(parents=True)
            candidate_path = ss_dir / "candidate_memory.jsonl"
            candidate = {
                "trigger": "test error",
                "correct_action": "do this",
                "counter": "counter",
                "ts": "2026-07-09T00:00:00+00:00",
            }
            candidate_path.write_text(json.dumps(candidate) + "\n", encoding="utf-8")

            memory_audit.run(cwd, sid)

            knowledge = cwd / ".agents" / "knowledge_distill.md"
            assert knowledge.exists()
            text = knowledge.read_text(encoding="utf-8")
            assert "test error" in text
            assert "do this" in text

            # Candidate file should be cleared
            assert candidate_path.read_text(encoding="utf-8") == ""
        finally:
            ahd_session.get_repo_root = original


if __name__ == "__main__":
    test_memory_audit_merges_candidates()
    print("memory_audit tests passed")
