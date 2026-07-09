#!/usr/bin/env python3
"""Tests for loop_memory_sync.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "loop_memory_sync.py"


def run_sync(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


def test_loop_memory_sync_creates_registry():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        # Seed a session_state
        state = {
            "session_id": "s-xyz",
            "goal": "test goal",
            "status": "in_progress",
            "complexity": "M",
            "last_heartbeat": "2026-07-09T10:00:00+00:00",
        }
        ss_dir = cwd / ".agent" / "session_state"
        ss_dir.mkdir(parents=True)
        (ss_dir / "s-xyz.json").write_text(json.dumps(state), encoding="utf-8")

        r = run_sync(["--session", "s-xyz", "--status", "completed"], cwd)
        assert r.returncode == 0, r.stderr

        registry = cwd / ".agent" / "loop_state.md"
        assert registry.exists()
        text = registry.read_text(encoding="utf-8")
        assert "s-xyz" in text
        assert "test goal" in text

        # session_state should have been updated
        updated = json.loads((ss_dir / "s-xyz.json").read_text(encoding="utf-8"))
        assert updated["status"] == "completed"


def test_loop_memory_sync_marks_stale_sessions():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        state = {
            "session_id": "s-stale",
            "goal": "stale goal",
            "status": "in_progress",
            "complexity": "M",
            "last_heartbeat": "2000-01-01T00:00:00+00:00",
            "last_state_write": "",
        }
        ss_dir = cwd / ".agent" / "session_state"
        ss_dir.mkdir(parents=True)
        (ss_dir / "s-stale.json").write_text(json.dumps(state), encoding="utf-8")

        r = run_sync([], cwd)
        assert r.returncode == 0, r.stderr

        registry = cwd / ".agent" / "loop_state.md"
        assert registry.exists()
        text = registry.read_text(encoding="utf-8")
        assert "suspected_crashed" in text
        assert "active_sessions" in text

        updated = json.loads((ss_dir / "s-stale.json").read_text(encoding="utf-8"))
        assert updated["status"] == "suspected_crashed"


def test_loop_memory_sync_enforces_max_active_sessions():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        ss_dir = cwd / ".agent" / "session_state"
        ss_dir.mkdir(parents=True)
        base = datetime.now(timezone.utc)
        for i in range(4):
            ts = (base + timedelta(seconds=i)).isoformat(timespec="seconds")
            state = {
                "session_id": f"s-{i}",
                "goal": f"goal {i}",
                "status": "in_progress",
                "last_heartbeat": ts,
                "last_state_write": ts,
                "owned_files": [f"scripts/{i}.py"],
                "tags": ["test"],
            }
            (ss_dir / f"s-{i}.json").write_text(json.dumps(state), encoding="utf-8")

        r = run_sync([], cwd)
        assert r.returncode == 0, r.stderr

        registry = cwd / ".agent" / "loop_state.md"
        text = registry.read_text(encoding="utf-8")
        assert "## Queued sessions" in text, text
        # The oldest (s-0) should be queued
        queued = json.loads((ss_dir / "s-0.json").read_text(encoding="utf-8"))
        assert queued["status"] == "queued", queued
        # The newest 3 should remain active
        for i in range(1, 4):
            s = json.loads((ss_dir / f"s-{i}.json").read_text(encoding="utf-8"))
            assert s["status"] == "in_progress", s


if __name__ == "__main__":
    test_loop_memory_sync_creates_registry()
    test_loop_memory_sync_marks_stale_sessions()
    test_loop_memory_sync_enforces_max_active_sessions()
    print("loop_memory_sync tests passed")
