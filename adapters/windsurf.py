"""Adapter for Windsurf.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class WindsurfAdapter(BaseAdapter):
    tool_id = "windsurf"


ADAPTER = WindsurfAdapter
