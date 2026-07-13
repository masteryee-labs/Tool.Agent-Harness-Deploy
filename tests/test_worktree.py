#!/usr/bin/env python3
"""Tests for worktree.py session-aware prefix and session_state sync."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKTREE_SCRIPT = ROOT / "scripts" / "worktree.py"
SESSION_MANAGER_SCRIPT = ROOT / "scripts" / "session_manager.py"


def _git(*args, cwd: Path):
    r = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {args} failed: {r.stderr}")


def test_worktree_prefix_and_session_state_sync():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _git("init", "-b", "main", cwd=tmp)
        _git("config", "user.email", "test@test.com", cwd=tmp)
        _git("config", "user.name", "Test", cwd=tmp)
        (tmp / "init.txt").write_text("init", encoding="utf-8")
        _git("add", "init.txt", cwd=tmp)
        _git("commit", "-m", "init", cwd=tmp)

        session_id = "s-12345678"
        expected_prefix = f"wt-{session_id[:8]}-"
        expected_wid = f"{expected_prefix}builder-a"
        expected_path = tmp / ".worktrees" / expected_wid

        # Initialize session so worktree.py can update session_state.worktrees
        init = subprocess.run(
            [sys.executable, str(SESSION_MANAGER_SCRIPT), "init", session_id, "--goal", "test"],
            cwd=str(tmp), capture_output=True, text=True
        )
        if init.returncode != 0:
            print(init.stdout)
            print(init.stderr)
        assert init.returncode == 0, init.stderr

        create = subprocess.run(
            [sys.executable, str(WORKTREE_SCRIPT), "create", "builder-a", "--session", session_id],
            cwd=str(tmp), capture_output=True, text=True
        )
        if create.returncode != 0:
            print(create.stdout)
            print(create.stderr)
        assert create.returncode == 0, create.stderr

        assert expected_path.exists(), f"expected worktree path not found: {expected_path}"

        state_path = tmp / ".agents" / "session_state" / f"{session_id}.json"
        assert state_path.exists(), f"session_state not written: {state_path}"
        data = json.loads(state_path.read_text(encoding="utf-8"))
        assert expected_wid in data.get("worktrees", []), f"worktrees not updated: {data}"

        remove = subprocess.run(
            [sys.executable, str(WORKTREE_SCRIPT), "remove", expected_wid],
            cwd=str(tmp), capture_output=True, text=True
        )
        if remove.returncode != 0:
            print(remove.stdout)
            print(remove.stderr)
        assert remove.returncode == 0, remove.stderr
        assert not expected_path.exists(), "worktree path still exists after remove"

        data = json.loads(state_path.read_text(encoding="utf-8"))
        assert expected_wid not in data.get("worktrees", []), f"worktrees not removed: {data}"


if __name__ == "__main__":
    test_worktree_prefix_and_session_state_sync()
    print("worktree tests passed")
