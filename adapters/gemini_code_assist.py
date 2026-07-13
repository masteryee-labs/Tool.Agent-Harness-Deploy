"""Adapter for Gemini Code Assist.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class GeminiCodeAssistAdapter(BaseAdapter):
    tool_id = "gemini_code_assist"


ADAPTER = GeminiCodeAssistAdapter
