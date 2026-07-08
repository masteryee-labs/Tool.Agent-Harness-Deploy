"""Adapter for AGY CLI.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
AGY CLI shares the AGENTS.md entry with Antigravity — sync dedupes by target path.
"""
from .base import BaseAdapter


class AgyCliAdapter(BaseAdapter):
    tool_id = "agy_cli"


ADAPTER = AgyCliAdapter
