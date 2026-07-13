"""Adapter for Cline.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class ClineAdapter(BaseAdapter):
    tool_id = "cline"


ADAPTER = ClineAdapter
