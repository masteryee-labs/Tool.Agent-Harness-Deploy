"""Adapter for Antigravity (AGY).

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class AntigravityAdapter(BaseAdapter):
    tool_id = "antigravity"


ADAPTER = AntigravityAdapter
