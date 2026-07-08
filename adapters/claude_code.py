"""Adapter for Claude Code.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class ClaudeCodeAdapter(BaseAdapter):
    tool_id = "claude_code"


ADAPTER = ClaudeCodeAdapter
