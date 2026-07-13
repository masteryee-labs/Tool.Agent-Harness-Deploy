#!/usr/bin/env python3
"""Tests for session_manager.py."""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import scripts.session_manager as session_manager


def make_args(**kwargs) -> argparse.Namespace:
    return argparse.Namespace(**kwargs)


def test_session_manager_init_and_status():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        # session_manager uses get_repo_root which walks up to .git
        ahd_session = session_manager.ahd_session
        original = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: cwd
        try:
            args = make_args(session_id="s-manage", goal="test", complexity="M", force=False)
            rc = session_manager.cmd_init(args)
            assert rc == 0

            state = json.loads((cwd / ".agents" / "session_state" / "s-manage.json").read_text(encoding="utf-8"))
            assert state["session_id"] == "s-manage"
            assert state["goal"] == "test"
            assert state["status"] == "in_progress"

            args = make_args(session_id="s-manage", status="completed")
            rc = session_manager.cmd_status(args)
            assert rc == 0

            state = json.loads((cwd / ".agents" / "session_state" / "s-manage.json").read_text(encoding="utf-8"))
            assert state["status"] == "completed"
            assert state["state_written"] is True
        finally:
            ahd_session.get_repo_root = original


def test_session_manager_heartbeat():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        ahd_session = session_manager.ahd_session
        original = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: cwd
        try:
            args = make_args(session_id="s-hb", goal="", complexity="M", force=False)
            session_manager.cmd_init(args)

            args = make_args(session_id="s-hb")
            rc = session_manager.cmd_heartbeat(args)
            assert rc == 0

            state = json.loads((cwd / ".agents" / "session_state" / "s-hb.json").read_text(encoding="utf-8"))
            assert state["last_heartbeat"] != ""
        finally:
            ahd_session.get_repo_root = original


def test_session_manager_max_active_sessions():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        (cwd / ".git").mkdir()

        ahd_session = session_manager.ahd_session
        original = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: cwd
        try:
            # Create 3 active sessions
            for i in range(3):
                args = make_args(session_id=f"s-{i}", goal="test", complexity="M", force=False)
                rc = session_manager.cmd_init(args)
                assert rc == 0, f"session {i} should initialize"

            # 4th without force should be rejected
            args = make_args(session_id="s-full", goal="test", complexity="M", force=False)
            rc = session_manager.cmd_init(args)
            assert rc == 1, "4th active session should be rejected"

            # 4th with force should become queued
            args = make_args(session_id="s-queued", goal="test", complexity="M", force=True)
            rc = session_manager.cmd_init(args)
            assert rc == 0, "4th session with --force should initialize as queued"
            state = json.loads((cwd / ".agents" / "session_state" / "s-queued.json").read_text(encoding="utf-8"))
            assert state["status"] == "queued"
        finally:
            ahd_session.get_repo_root = original


if __name__ == "__main__":
    test_session_manager_init_and_status()
    test_session_manager_heartbeat()
    test_session_manager_max_active_sessions()
    print("session_manager tests passed")
