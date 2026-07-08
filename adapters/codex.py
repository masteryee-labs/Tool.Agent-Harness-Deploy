"""Adapter for Codex / Codex CLI.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class CodexAdapter(BaseAdapter):
    tool_id = "codex"


ADAPTER = CodexAdapter
