"""Adapter for Claude Code for VS Code.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class ClaudeCodeVSCodeAdapter(BaseAdapter):
    tool_id = "claude_code_vscode"


ADAPTER = ClaudeCodeVSCodeAdapter
