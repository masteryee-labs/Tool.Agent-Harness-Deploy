"""Adapter for ChatGPT Desktop.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class ChatGPTDesktopAdapter(BaseAdapter):
    tool_id = "chatgpt_desktop"


ADAPTER = ChatGPTDesktopAdapter
