"""Adapter for Claude Desktop.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
Claude Desktop uses a single JSON config — BaseAdapter._wrap_json injects a pointer
rather than dumping the full canon body into JSON.
"""
from .base import BaseAdapter


class ClaudeDesktopAdapter(BaseAdapter):
    tool_id = "claude_desktop"


ADAPTER = ClaudeDesktopAdapter
