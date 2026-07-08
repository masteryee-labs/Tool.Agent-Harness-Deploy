"""Agent Harness Deploy tool adapters package.

Each module exports an `ADAPTER` callable (a BaseAdapter subclass). The sync script
imports them dynamically based on registry.json tool ids.
"""
from .base import BaseAdapter, load_registry, expand, get_tool_spec

# Map tool_id -> adapter class (lazy import avoids circulars and keeps imports explicit).
_TOOL_ID_TO_MODULE = {
    "claude_code": "claude_code",
    "antigravity": "antigravity",
    "codex": "codex",
    "devin": "devin",
    "cursor": "cursor",
    "claude_desktop": "claude_desktop",
    "opencode": "opencode",
    "openclaw": "openclaw",
    "hermes": "hermes",
    "zcode": "zcode",
    "kimi_code": "kimi_code",
    "agy_cli": "agy_cli",
    "codex_cli": "codex_cli",
    "devin_cli": "devin_cli",
}


def get_adapter(tool_id: str, project_root: str = "."):
    """Instantiate the adapter for a tool_id."""
    import importlib
    mod = importlib.import_module(f"adapters.{_TOOL_ID_TO_MODULE[tool_id]}")
    return mod.ADAPTER(project_root=project_root)


def all_tool_ids() -> list[str]:
    return list(_TOOL_ID_TO_MODULE.keys())
