"""Adapter for Continue.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class ContinueDevAdapter(BaseAdapter):
    tool_id = "continue_dev"


ADAPTER = ContinueDevAdapter
