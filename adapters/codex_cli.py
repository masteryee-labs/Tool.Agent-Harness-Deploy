"""Adapter for Codex CLI.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
Codex CLI shares the .codex/ layout with the Codex tool — sync dedupes by target path.
"""
from .base import BaseAdapter


class CodexCliAdapter(BaseAdapter):
    tool_id = "codex_cli"


ADAPTER = CodexCliAdapter
