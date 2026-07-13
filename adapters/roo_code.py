"""Adapter for Roo Code.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class RooCodeAdapter(BaseAdapter):
    tool_id = "roo_code"


ADAPTER = RooCodeAdapter
