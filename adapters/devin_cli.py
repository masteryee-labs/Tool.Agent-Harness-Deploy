"""Adapter for Devin CLI.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
Devin CLI shares the .devin/ layout with the Devin tool — sync dedupes by target path.
"""
from .base import BaseAdapter


class DevinCliAdapter(BaseAdapter):
    tool_id = "devin_cli"


ADAPTER = DevinCliAdapter
