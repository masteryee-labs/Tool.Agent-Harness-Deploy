"""Adapter for OpenCode.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class OpenCodeAdapter(BaseAdapter):
    tool_id = "opencode"


ADAPTER = OpenCodeAdapter
