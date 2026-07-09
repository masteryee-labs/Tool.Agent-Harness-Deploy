#!/usr/bin/env python3
"""Tests for ahd_session.py core helpers."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Import ahd_session from its source location
sys.path.insert(0, str(ROOT / "core" / "assets" / "runtime" / "hooks"))
import ahd_session


def test_slugify_session_id():
    assert ahd_session.slugify_session_id("a:b/c\\d e") == "a-b-c-d-e"
    assert ahd_session.slugify_session_id("---foo---") == "foo"
    assert ahd_session.slugify_session_id(":/") == "unknown"
    long_id = "x" * 100
    assert len(ahd_session.slugify_session_id(long_id)) == 64


def test_get_session_id_chain():
    # Direct data
    assert ahd_session.get_session_id({"session_id": "s-1"}) == "s-1"

    # Env var
    old = os.environ.get("AHD_SESSION_ID")
    os.environ["AHD_SESSION_ID"] = "s-env"
    try:
        assert ahd_session.get_session_id({}) == "s-env"
    finally:
        if old is None:
            os.environ.pop("AHD_SESSION_ID", None)
        else:
            os.environ["AHD_SESSION_ID"] = old

    # UUID fallback
    sid = ahd_session.get_session_id({})
    assert sid
    assert "unknown" not in sid or sid != "unknown"


def test_session_state_read_write():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        original = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: cwd
        try:
            sid = "s-test"
            ahd_session.write_session_state(sid, {"session_id": sid, "goal": "test"}, cwd, merge=False)
            data = ahd_session.read_session_state(sid, cwd)
            assert data["session_id"] == sid
            assert data["goal"] == "test"

            ahd_session.update_session_state(sid, {"last_heartbeat": "2026-07-09T00:00:00Z"}, cwd)
            data = ahd_session.read_session_state(sid, cwd)
            assert data["goal"] == "test"
            assert data["last_heartbeat"] == "2026-07-09T00:00:00Z"
        finally:
            ahd_session.get_repo_root = original


def test_concurrent_session_state_updates():
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(tmp)
        original = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: cwd
        try:
            sid = "s-concurrent"
            ahd_session.write_session_state(sid, {"session_id": sid}, cwd, merge=False)

            errors: list[str] = []

            def worker(n: int):
                for _ in range(20):
                    try:
                        # Update distinct keys per thread to test merge safety under concurrency.
                        ahd_session.update_session_state(sid, {f"counter_{n}": _ + 1}, cwd)
                    except Exception as e:
                        errors.append(f"worker {n}: {e}")

            threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            final = ahd_session.read_session_state(sid, cwd)
            for i in range(4):
                assert final.get(f"counter_{i}") == 20, f"counter_{i}={final.get(f'counter_{i}')}, errors={errors}"
            assert not errors
        finally:
            ahd_session.get_repo_root = original


if __name__ == "__main__":
    test_slugify_session_id()
    test_get_session_id_chain()
    test_session_state_read_write()
    test_concurrent_session_state_updates()
    print("session_state tests passed")
