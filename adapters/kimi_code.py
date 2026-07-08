"""Adapter for Kimi Code.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class KimiCodeAdapter(BaseAdapter):
    tool_id = "kimi_code"


ADAPTER = KimiCodeAdapter
