"""Adapter for OpenClaw.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class OpenClawAdapter(BaseAdapter):
    tool_id = "openclaw"


ADAPTER = OpenClawAdapter
