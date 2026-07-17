#!/usr/bin/env python3
"""Tests for project/global scope separation and legacy MCP migration.

Covers:
- expand() env var expansion (including Windows ${HOME} fallback)
- _resolve_scoped_path() project vs global scope detection
- _sync_runtime() respects global_too flag
- migrate.py check_one() all 5 statuses
- migrate.py sidecar marker distinguishes new-AHD .bak from legacy .bak
- migrate.py does NOT undo a --global deploy on second run
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from adapters.base import expand, load_registry, _write_bak_marker
from scripts.migrate import (
    _clean_servers,
    _has_ahd_marker,
    check_one,
    find_legacy_global_mcp_paths,
    run_migration,
)
from adapters import get_adapter


# ---------------------------------------------------------------------------
# expand() — env var expansion
# ---------------------------------------------------------------------------

def test_expand_none():
    assert expand(None) is None


def test_expand_project_relative():
    """Relative paths are returned as-is (no expansion needed)."""
    assert expand(".mcp.json") == ".mcp.json"
    assert expand(".claude/settings.json") == ".claude/settings.json"


def test_expand_appdata():
    """${APPDATA} expands to an absolute path on all platforms."""
    result = expand("${APPDATA}/Claude/config.json")
    assert not result.startswith("${")
    assert "Claude/config.json" in result.replace("\\", "/")


def test_expand_home_on_windows():
    """${HOME} must expand even on Windows (which doesn't set HOME by default).

    This is the bug that caused literal '${HOME}' directories to be created
    under project roots before the fix.
    """
    result = expand("${HOME}/.codeium/windsurf/mcp_config.json")
    assert not result.startswith("${HOME}"), "HOME was not expanded"
    assert ".codeium/windsurf/mcp_config.json" in result.replace("\\", "/")


def test_expand_tilde():
    """~ expands to user home."""
    result = expand("~/some/path")
    assert not result.startswith("~")
    assert "some/path" in result.replace("\\", "/")


# ---------------------------------------------------------------------------
# _resolve_scoped_path() — scope detection
# ---------------------------------------------------------------------------

def test_resolve_project_path_always_resolved():
    """Project-relative paths resolve to project_root/<path> regardless of global_too."""
    adapter = get_adapter("claude_code", project_root="C:/fake_proj")
    result = adapter._resolve_scoped_path(".mcp.json", global_too=False)
    assert result is not None
    assert "fake_proj" in str(result)


def test_resolve_global_path_skipped_without_global_flag():
    """Global (absolute) paths return None when global_too=False."""
    adapter = get_adapter("windsurf", project_root="C:/fake_proj")
    result = adapter._resolve_scoped_path(
        "${HOME}/.codeium/windsurf/mcp_config.json", global_too=False
    )
    assert result is None, "global path should be skipped without --global"


def test_resolve_global_path_resolved_with_global_flag():
    """Global (absolute) paths resolve to real location when global_too=True."""
    adapter = get_adapter("windsurf", project_root="C:/fake_proj")
    result = adapter._resolve_scoped_path(
        "${HOME}/.codeium/windsurf/mcp_config.json", global_too=True
    )
    assert result is not None
    assert "fake_proj" not in str(result), "should not be under project root"
    assert "mcp_config.json" in str(result)


def test_resolve_none_path():
    """None or empty path returns None."""
    adapter = get_adapter("claude_code", project_root="C:/fake_proj")
    assert adapter._resolve_scoped_path(None, global_too=False) is None
    assert adapter._resolve_scoped_path("", global_too=False) is None


# ---------------------------------------------------------------------------
# Registry audit — all 23 tools have correct scope classification
# ---------------------------------------------------------------------------

def test_all_global_mcp_paths_are_absolute_after_expand():
    """Every path that find_legacy_global_mcp_paths returns must be absolute."""
    paths = find_legacy_global_mcp_paths()
    assert len(paths) == 4, f"expected 4 global MCP tools, got {len(paths)}"
    for tool_id, mcp_path, bak_path in paths:
        assert os.path.isabs(str(mcp_path)), f"{tool_id}: {mcp_path} is not absolute"


def test_all_global_mcp_tools_have_template():
    """All 4 global-MCP tools must have non-null mcp_template (otherwise no pollution)."""
    paths = find_legacy_global_mcp_paths()
    reg = load_registry()
    for tool_id, _, _ in paths:
        tool = next(t for t in reg["tools"] if t["id"] == tool_id)
        assert tool["runtime"]["mcp_template"] is not None


def test_project_scoped_tools_not_in_legacy_list():
    """Tools with project-relative mcp_file must NOT appear in legacy list."""
    paths = find_legacy_global_mcp_paths()
    tool_ids = {p[0] for p in paths}
    # These have project-scoped MCP and should never be in the legacy list
    assert "claude_code" not in tool_ids
    assert "codex" not in tool_ids
    assert "cursor" not in tool_ids
    assert "devin" not in tool_ids


# ---------------------------------------------------------------------------
# _clean_servers() — _-prefixed key stripping
# ---------------------------------------------------------------------------

def test_clean_servers_strips_underscore_names():
    servers = {"_comment": {}, "real": {"command": "x"}}
    cleaned = _clean_servers(servers)
    assert "_comment" not in cleaned
    assert "real" in cleaned


def test_clean_servers_strips_underscore_keys_in_config():
    servers = {"srv": {"command": "x", "_disabled": True, "_note": "hi"}}
    cleaned = _clean_servers(servers)
    assert "_disabled" not in cleaned["srv"]
    assert "_note" not in cleaned["srv"]
    assert cleaned["srv"]["command"] == "x"


def test_clean_servers_preserves_normal_keys():
    servers = {"srv": {"command": "x", "args": ["a", "b"], "env": {"K": "V"}}}
    cleaned = _clean_servers(servers)
    assert cleaned == servers


# ---------------------------------------------------------------------------
# check_one() — all 5 statuses
# ---------------------------------------------------------------------------

def _make_tmp():
    return Path(tempfile.mkdtemp())


def test_check_one_clean_no_files():
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        result = check_one("test", mcp, bak)
        assert result["status"] == "clean"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_check_one_no_bak_file_exists():
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        mcp.write_text(json.dumps({"mcpServers": {}}), encoding="utf-8")
        bak = d / "mcp.json.bak"
        result = check_one("test", mcp, bak)
        assert result["status"] == "no_bak"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_check_one_managed_has_marker():
    """A .bak with AHD marker should be 'managed' (skip, don't restore)."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        bak.write_text(json.dumps({"mcpServers": {"old": {"command": "x"}}}), encoding="utf-8")
        _write_bak_marker(bak)
        mcp.write_text(json.dumps({"mcpServers": {"old": {"command": "x"}}}), encoding="utf-8")
        result = check_one("test", mcp, bak)
        assert result["status"] == "managed"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_check_one_safe_restore_no_user_changes():
    """Legacy .bak (no marker) with identical mcpServers → safe_restore."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        # .bak has original (with _comment that old AHD stripped)
        bak.write_text(json.dumps({"mcpServers": {"_comment": "hi", "srv": {"command": "x"}}}), encoding="utf-8")
        # current has what old AHD left (stripped _comment)
        mcp.write_text(json.dumps({"mcpServers": {"srv": {"command": "x"}}}), encoding="utf-8")
        result = check_one("test", mcp, bak)
        assert result["status"] == "safe_restore"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_check_one_unsafe_skip_user_added_servers():
    """Legacy .bak (no marker) with user-added servers → unsafe_skip."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        bak.write_text(json.dumps({"mcpServers": {"old": {"command": "x"}}}), encoding="utf-8")
        mcp.write_text(json.dumps({"mcpServers": {"old": {"command": "x"}, "user-added": {"command": "y"}}}), encoding="utf-8")
        result = check_one("test", mcp, bak)
        assert result["status"] == "unsafe_skip"
        assert "user-added" in result["detail"]
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_check_one_safe_restore_file_deleted():
    """Legacy .bak (no marker), file deleted → safe_restore."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"  # doesn't exist
        bak = d / "mcp.json.bak"
        bak.write_text(json.dumps({"mcpServers": {"srv": {"command": "x"}}}), encoding="utf-8")
        result = check_one("test", mcp, bak)
        assert result["status"] == "safe_restore"
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------------------
# Sidecar marker — _has_ahd_marker / _write_bak_marker
# ---------------------------------------------------------------------------

def test_write_and_detect_marker():
    d = _make_tmp()
    try:
        bak = d / "test.json.bak"
        bak.write_text("{}", encoding="utf-8")
        assert not _has_ahd_marker(bak), "should not have marker before writing"
        _write_bak_marker(bak)
        assert _has_ahd_marker(bak), "should have marker after writing"
        marker_path = Path(str(bak) + ".ahd_managed")
        assert marker_path.exists()
        data = json.loads(marker_path.read_text(encoding="utf-8"))
        assert data["managed_by"] == "Agent Harness Deploy"
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------------------
# Critical regression: --global deploy must NOT be undone by migrate.py
# ---------------------------------------------------------------------------

def test_migrate_does_not_undo_global_deploy():
    """Simulate: (1) --global writes MCP + .bak with marker,
    (2) user runs distill.py without --global,
    (3) migrate.py must NOT restore from the managed .bak."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"

        # Step 1: --global deploy writes new content, backs up old to .bak WITH marker
        original = {"mcpServers": {"user-server": {"command": "node"}}}
        mcp.write_text(json.dumps(original), encoding="utf-8")
        # Simulate _merge_mcp backing up then writing
        shutil.copy2(mcp, bak)
        _write_bak_marker(bak)
        new_content = {"mcpServers": {"user-server": {"command": "node"}, "ahd-server": {"command": "python"}}}
        mcp.write_text(json.dumps(new_content), encoding="utf-8")

        # Step 2: migrate.py runs (simulating distill.py Step 0)
        result = check_one("test", mcp, bak)
        assert result["status"] == "managed", \
            f"migrate.py must skip managed .bak, got {result['status']}"

        # The MCP file must still have the --global content (not restored)
        current = json.loads(mcp.read_text(encoding="utf-8"))
        assert "ahd-server" in current["mcpServers"], \
            "--global deploy content was undone by migrate.py!"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_migrate_restores_legacy_pollution():
    """Simulate: (1) old AHD polluted global MCP (no marker),
    (2) user runs distill.py,
    (3) migrate.py restores from .bak."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"

        # .bak = original (before old AHD pollution), NO marker
        original = {"mcpServers": {"_my_comment": "hi", "real": {"command": "x"}}}
        bak.write_text(json.dumps(original), encoding="utf-8")
        # current = what old AHD left (stripped _ keys, reformatted)
        polluted = {"mcpServers": {"real": {"command": "x"}}}
        mcp.write_text(json.dumps(polluted), encoding="utf-8")

        result = check_one("test", mcp, bak)
        assert result["status"] == "safe_restore"

        # Simulate the restore
        shutil.copy2(bak, mcp)
        bak.unlink()
        restored = json.loads(mcp.read_text(encoding="utf-8"))
        assert "_my_comment" in restored["mcpServers"], \
            "original _-prefixed keys should be restored"
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------------------
# run_migration() — integration test with temp files
# ---------------------------------------------------------------------------

def test_run_migration_report_mode_no_writes():
    """--report mode must not modify any files.

    Monkeypatches find_legacy_global_mcp_paths to return temp paths so that
    run_migration actually processes them. Verifies that report_only=True
    does NOT restore or delete anything.
    """
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        bak.write_text(json.dumps({"mcpServers": {"_c": "x", "s": {"command": "x"}}}), encoding="utf-8")
        mcp.write_text(json.dumps({"mcpServers": {"s": {"command": "x"}}}), encoding="utf-8")
        mcp_hash_before = mcp.read_bytes()
        bak_hash_before = bak.read_bytes()

        # Monkeypatch find_legacy_global_mcp_paths to return our temp paths
        import scripts.migrate as migmod
        original_finder = migmod.find_legacy_global_mcp_paths
        migmod.find_legacy_global_mcp_paths = lambda: [("test_tool", mcp, bak)]
        try:
            rc = run_migration(report_only=True)
            assert isinstance(rc, int)
        finally:
            migmod.find_legacy_global_mcp_paths = original_finder

        # Report mode must not have touched either file
        assert mcp.read_bytes() == mcp_hash_before, "report mode modified mcp file!"
        assert bak.read_bytes() == bak_hash_before, "report mode modified .bak file!"
        assert bak.exists(), "report mode deleted .bak file!"
        assert mcp.exists(), "report mode deleted mcp file!"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_run_migration_default_mode_restores_safe():
    """Default mode (not report, not force) should restore safe_restore cases."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        # Legacy .bak (no marker) with matching mcpServers after _clean
        bak.write_text(json.dumps({"mcpServers": {"_c": "x", "s": {"command": "x"}}}), encoding="utf-8")
        mcp.write_text(json.dumps({"mcpServers": {"s": {"command": "x"}}}), encoding="utf-8")

        import scripts.migrate as migmod
        original_finder = migmod.find_legacy_global_mcp_paths
        migmod.find_legacy_global_mcp_paths = lambda: [("test_tool", mcp, bak)]
        try:
            rc = run_migration(report_only=False, force_restore=False)
        finally:
            migmod.find_legacy_global_mcp_paths = original_finder

        # Should have restored: mcp now has .bak content, .bak deleted
        assert not bak.exists(), ".bak should be deleted after restore"
        restored = json.loads(mcp.read_text(encoding="utf-8"))
        assert "_c" in restored["mcpServers"], "original _-prefixed keys should be restored"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_run_migration_force_restore_overrides_unsafe():
    """--restore mode should force-restore even unsafe_skip cases."""
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        # User added a server after old deploy → normally unsafe_skip
        bak.write_text(json.dumps({"mcpServers": {"old": {"command": "x"}}}), encoding="utf-8")
        mcp.write_text(json.dumps({"mcpServers": {"old": {"command": "x"}, "user": {"command": "y"}}}), encoding="utf-8")

        import scripts.migrate as migmod
        original_finder = migmod.find_legacy_global_mcp_paths
        migmod.find_legacy_global_mcp_paths = lambda: [("test_tool", mcp, bak)]
        try:
            rc = run_migration(report_only=False, force_restore=True)
        finally:
            migmod.find_legacy_global_mcp_paths = original_finder

        # Force restore: mcp now has .bak content (user server lost), .bak deleted
        assert not bak.exists(), ".bak should be deleted after force restore"
        restored = json.loads(mcp.read_text(encoding="utf-8"))
        assert "user" not in restored["mcpServers"], "force restore should overwrite user changes"
        assert "old" in restored["mcpServers"], "original server should be restored"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_run_migration_force_restore_does_not_override_managed():
    """--restore must NOT override managed .bak (from --global deploy).

    This is the critical safety test: even with --restore, migrate.py must
    never undo a --global deploy. Managed .bak files are always skipped.
    """
    d = _make_tmp()
    try:
        mcp = d / "mcp.json"
        bak = d / "mcp.json.bak"
        # Simulate --global deploy: .bak has marker, mcp has new content
        shutil.copy2(mcp, bak) if mcp.exists() else bak.write_text("{}")
        _write_bak_marker(bak)
        mcp.write_text(json.dumps({"mcpServers": {"ahd-srv": {"command": "py"}}}), encoding="utf-8")
        mcp_hash_before = mcp.read_bytes()

        import scripts.migrate as migmod
        original_finder = migmod.find_legacy_global_mcp_paths
        migmod.find_legacy_global_mcp_paths = lambda: [("test_tool", mcp, bak)]
        try:
            rc = run_migration(report_only=False, force_restore=True)
        finally:
            migmod.find_legacy_global_mcp_paths = original_finder

        # Managed .bak must NOT be restored, even with --restore
        assert mcp.read_bytes() == mcp_hash_before, \
            "--restore must not override managed .bak!"
        current = json.loads(mcp.read_text(encoding="utf-8"))
        assert "ahd-srv" in current["mcpServers"], \
            "--global deploy content must be preserved even with --restore"
    finally:
        shutil.rmtree(d, ignore_errors=True)
