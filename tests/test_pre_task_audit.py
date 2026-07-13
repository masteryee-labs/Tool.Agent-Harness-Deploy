#!/usr/bin/env python3
"""Tests for pre_task_audit.py conflict detection."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "core" / "assets" / "runtime" / "hooks"))

import ahd_session
import pre_task_audit
import plan_dispatch


def _setup_active_session(tmp: Path, sid: str, owned: list[str], tags: list[str], status: str = "in_progress"):
    """Create a session_state and loop_state.md active table entry for a session."""
    state = {
        "session_id": sid,
        "goal": "test",
        "status": status,
        "owned_files": owned,
        "affected_files": [],
        "tags": tags,
        "last_heartbeat": ahd_session.now_utc(),
        "last_state_write": ahd_session.now_utc(),
    }
    ahd_session.write_session_state(sid, state, tmp, merge=False)


def test_pre_task_audit_no_conflict():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        original_get_repo_root = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: tmp
        plan_dispatch.ROOT = tmp
        try:
            _setup_active_session(tmp, "s-existing", ["scripts/old.py"], ["docs"])
            registry = tmp / ".agents" / "loop_state.md"
            registry.write_text(
                "---\nactive_sessions: []\nactive_session: null\n---\n"
                "## Active sessions\n| session_id | goal | status | tags | owned_files | last_heartbeat |\n"
                "|---|---|---|---|---|---|\n"
                f"| s-existing | test | in_progress | docs | scripts/old.py | {ahd_session.now_utc()} |\n",
                encoding="utf-8",
            )
            result = pre_task_audit.audit(tmp, ["scripts/new.py"], ["new"])
            assert result["ok"], f"expected no conflict, got {result}"
            assert result["active_sessions_count"] == 1
        finally:
            ahd_session.get_repo_root = original_get_repo_root
            plan_dispatch.ROOT = ROOT


def test_pre_task_audit_file_conflict():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        original_get_repo_root = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: tmp
        plan_dispatch.ROOT = tmp
        try:
            _setup_active_session(tmp, "s-existing", ["scripts/sync.py"], ["concurrency"])
            registry = tmp / ".agents" / "loop_state.md"
            registry.write_text(
                "---\nactive_sessions: []\nactive_session: null\n---\n"
                "## Active sessions\n| session_id | goal | status | tags | owned_files | last_heartbeat |\n"
                "|---|---|---|---|---|---|\n"
                f"| s-existing | test | in_progress | concurrency | scripts/sync.py | {ahd_session.now_utc()} |\n",
                encoding="utf-8",
            )
            result = pre_task_audit.audit(tmp, ["scripts/sync.py"], ["concurrency"])
            assert not result["ok"], f"expected conflict, got {result}"
            assert any(c["session_id"] == "s-existing" for c in result["conflicts"])
        finally:
            ahd_session.get_repo_root = original_get_repo_root
            plan_dispatch.ROOT = ROOT


def test_pre_task_audit_tag_conflict():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        original_get_repo_root = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: tmp
        plan_dispatch.ROOT = tmp
        try:
            _setup_active_session(tmp, "s-existing", ["scripts/other.py"], ["concurrency"])
            registry = tmp / ".agents" / "loop_state.md"
            registry.write_text(
                "---\nactive_sessions: []\nactive_session: null\n---\n"
                "## Active sessions\n| session_id | goal | status | tags | owned_files | last_heartbeat |\n"
                "|---|---|---|---|---|---|\n"
                f"| s-existing | test | in_progress | concurrency | scripts/other.py | {ahd_session.now_utc()} |\n",
                encoding="utf-8",
            )
            result = pre_task_audit.audit(tmp, ["scripts/new.py"], ["concurrency"])
            assert not result["ok"], f"expected tag conflict, got {result}"
            assert any(c["reason"] == "tag overlap" for c in result["conflicts"])
        finally:
            ahd_session.get_repo_root = original_get_repo_root
            plan_dispatch.ROOT = ROOT


def test_pre_task_audit_cli():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        original_get_repo_root = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: tmp
        plan_dispatch.ROOT = tmp
        try:
            _setup_active_session(tmp, "s-existing", ["scripts/sync.py"], ["concurrency"])
            registry = tmp / ".agents" / "loop_state.md"
            registry.write_text(
                "---\nactive_sessions: []\nactive_session: null\n---\n"
                "## Active sessions\n| session_id | goal | status | tags | owned_files | last_heartbeat |\n"
                "|---|---|---|---|---|---|\n"
                f"| s-existing | test | in_progress | concurrency | scripts/sync.py | {ahd_session.now_utc()} |\n",
                encoding="utf-8",
            )
            import subprocess
            r = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "pre_task_audit.py"),
                 "--files", "scripts/sync.py", "--tags", "concurrency"],
                cwd=str(tmp), capture_output=True, text=True
            )
            assert r.returncode == 1, f"expected exit 1, got {r.returncode}\n{r.stdout}\n{r.stderr}"
            assert "Conflict" in r.stdout
        finally:
            ahd_session.get_repo_root = original_get_repo_root
            plan_dispatch.ROOT = ROOT


def test_pre_task_audit_treats_stale_as_suspected_crashed():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        original_get_repo_root = ahd_session.get_repo_root
        ahd_session.get_repo_root = lambda _=None: tmp
        plan_dispatch.ROOT = tmp
        try:
            _setup_active_session(tmp, "s-stale", ["scripts/sync.py"], ["concurrency"])
            # backdate heartbeat
            state = ahd_session.read_session_state("s-stale", tmp)
            state["last_heartbeat"] = "2000-01-01T00:00:00+00:00"
            state["last_state_write"] = ""
            ahd_session.write_session_state("s-stale", state, tmp, merge=False)

            registry = tmp / ".agents" / "loop_state.md"
            registry.write_text(
                "---\nactive_sessions: []\nactive_session: null\n---\n"
                "## Active sessions\n| session_id | goal | status | tags | owned_files | last_heartbeat |\n"
                "|---|---|---|---|---|---|\n"
                "| s-stale | test | in_progress | concurrency | scripts/sync.py | 2000-01-01T00:00:00+00:00 |\n",
                encoding="utf-8",
            )
            result = pre_task_audit.audit(tmp, ["scripts/sync.py"], ["concurrency"])
            assert not result["ok"]
            assert any("stale" in c["reason"] for c in result["conflicts"])
            # session_state should have been updated to suspected_crashed
            updated = ahd_session.read_session_state("s-stale", tmp)
            assert updated["status"] == "suspected_crashed"
        finally:
            ahd_session.get_repo_root = original_get_repo_root
            plan_dispatch.ROOT = ROOT


if __name__ == "__main__":
    test_pre_task_audit_no_conflict()
    test_pre_task_audit_file_conflict()
    test_pre_task_audit_tag_conflict()
    test_pre_task_audit_cli()
    test_pre_task_audit_treats_stale_as_suspected_crashed()
    print("pre_task_audit tests passed")
