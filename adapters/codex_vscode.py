"""Adapter for Codex IDE Extension.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class CodexVSCodeAdapter(BaseAdapter):
    tool_id = "codex_vscode"


ADAPTER = CodexVSCodeAdapter
