"""Adapter for Hermes.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class HermesAdapter(BaseAdapter):
    tool_id = "hermes"


ADAPTER = HermesAdapter
