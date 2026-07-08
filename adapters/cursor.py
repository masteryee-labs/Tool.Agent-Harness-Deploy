"""Adapter for Cursor.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
Cursor uses .mdc files with YAML frontmatter — handled by BaseAdapter._wrap_mdc.
"""
from .base import BaseAdapter


class CursorAdapter(BaseAdapter):
    tool_id = "cursor"


ADAPTER = CursorAdapter
