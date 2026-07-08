"""Adapter for Devin / Devin CLI.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class DevinAdapter(BaseAdapter):
    tool_id = "devin"


ADAPTER = DevinAdapter
