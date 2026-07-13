#!/usr/bin/env python3
"""Tests for post_tool_use.py hook."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOK = ROOT / "core" / "assets" / "runtime" / "hooks" / "post_tool_use.py"


def run_hook(payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def test_post_tool_use_writes_session_state():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        # Fake a repo root marker
        (cwd / ".git").mkdir()

        payload = {
            "tool_name": "Edit",
            "tool_input": {"file_path": "test.py"},
            "tool_response": {"content": "ok"},
            "session_id": "s-abc123",
        }
        r = run_hook(payload, cwd)
        assert r.returncode == 0, r.stderr

        state_path = cwd / ".agents" / "session_state" / "s-abc123.json"
        assert state_path.exists(), "session_state json not created"
        data = json.loads(state_path.read_text(encoding="utf-8"))
        assert data["session_id"] == "s-abc123"
        assert data["last_tool"] == "Edit"
        assert data["last_file"] == "test.py"


def test_post_tool_use_redacts_command():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        payload = {
            "tool_name": "Bash",
            "tool_input": {"command": "curl -H 'Authorization: token ghp_123456789012345678901234567890123456' https://api.github.com"},
            "tool_response": {"content": "error: not found"},
            "session_id": "s-redact",
        }
        r = run_hook(payload, cwd)
        assert r.returncode == 0, r.stderr

        journal_path = cwd / ".agents" / "session_state" / "s-redact" / "journal.jsonl"
        assert journal_path.exists()
        lines = journal_path.read_text(encoding="utf-8").strip().splitlines()
        assert lines
        entry = json.loads(lines[0])
        assert "token=***" in entry["command"] or "***" in entry["command"]


def test_post_tool_use_candidate_memory():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        payload = {
            "tool_name": "Bash",
            "tool_input": {"command": "ls /nonexistent"},
            "tool_response": {"content": "No such file or directory"},
            "session_id": "s-candidate",
        }
        # First failure is logged in the journal but not recorded as candidate memory.
        r = run_hook(payload, cwd)
        assert r.returncode == 0, r.stderr

        # Second identical failure creates a candidate memory entry.
        r = run_hook(payload, cwd)
        assert r.returncode == 0, r.stderr

        candidate_path = cwd / ".agents" / "session_state" / "s-candidate" / "candidate_memory.jsonl"
        assert candidate_path.exists()
        lines = candidate_path.read_text(encoding="utf-8").strip().splitlines()
        assert lines
        entry = json.loads(lines[0])
        assert entry["trigger"]
        assert entry["correct_action"]


def _import_post_tool_use_mod():
    import importlib.util
    sys.path.insert(0, str(HOOK.parent))
    spec = importlib.util.spec_from_file_location("post_tool_use", HOOK)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["post_tool_use"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_post_tool_use_journal_rotation():
    with tempfile.TemporaryDirectory() as tmp:
        journal_path = Path(tmp) / "journal.jsonl"
        journal_path.write_text("\n".join([f'{{"n": {i}}}' for i in range(5)]) + "\n", encoding="utf-8")

        mod = _import_post_tool_use_mod()
        mod._rotate(journal_path, max_lines=3)
        assert not journal_path.exists(), "journal should be rotated"
        backup = journal_path.with_suffix(".1.jsonl")
        assert backup.exists(), "backup should exist after rotation"


def test_post_tool_use_candidate_memory_bound():
    with tempfile.TemporaryDirectory() as tmp:
        candidate_path = Path(tmp) / "candidate_memory.jsonl"
        mod = _import_post_tool_use_mod()
        for i in range(55):
            mod._append_bounded_jsonl(candidate_path, {"n": i}, max_records=50)
        lines = candidate_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 50, f"expected 50, got {len(lines)}"


if __name__ == "__main__":
    test_post_tool_use_writes_session_state()
    test_post_tool_use_redacts_command()
    test_post_tool_use_candidate_memory()
    test_post_tool_use_journal_rotation()
    test_post_tool_use_candidate_memory_bound()
    print("post_tool_use tests passed")
