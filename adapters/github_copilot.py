"""Adapter for GitHub Copilot.

Thin wrapper around BaseAdapter; all tool-specific data lives in registry.json.
"""
from .base import BaseAdapter


class GitHubCopilotAdapter(BaseAdapter):
    tool_id = "github_copilot"


ADAPTER = GitHubCopilotAdapter
