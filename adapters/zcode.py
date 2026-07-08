"""Adapter for ZCode.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class ZCodeAdapter(BaseAdapter):
    tool_id = "zcode"


ADAPTER = ZCodeAdapter
