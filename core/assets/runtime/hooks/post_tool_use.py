#!/usr/bin/env python3
"""Post-tool-use hook — logs tool usage for audit trail.

Called by the AI tool after executing any tool. Receives JSON on stdin:
  {"tool_name": "Edit", "tool_input": {...}, "tool_response": {...}, "session_id": "..."}

Exit codes:
  0 = success (always — post-hooks never block)

Writes a JSONL line to .agent/tool_log.jsonl:
  {"ts": "2026-01-01T12:00:00", "tool": "Edit", "file": "path", "ok": true, "session": "..."}

This creates a persistent audit trail of what the agent did, which:
  - Helps the auditor skill review past actions
  - Provides evidence for verification (maker ≠ checker)
  - Enables debugging when something went wrong

The log is capped at 1000 lines (rotates to .tool_log.1.jsonl when exceeded).
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = Path(".agent/tool_log.jsonl")
MAX_LINES = 1000


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    tool_response = data.get("tool_response", {})
    session_id = data.get("session_id", "")

    # Extract relevant info based on tool type
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": tool_name,
        "session": session_id[:12] if session_id else "",
    }

    # Try to extract file path from common tools
    for key in ("file_path", "path", "notebook_path"):
        if key in tool_input:
            entry["file"] = tool_input[key]
            break

    # For Bash, log the command (truncated)
    if tool_name in ("Bash", "bash", "Shell", "Execute", "exec"):
        cmd = tool_input.get("command", "")
        entry["command"] = cmd[:200]
        if len(cmd) > 200:
            entry["command_truncated"] = True

    # Check if the tool succeeded
    if isinstance(tool_response, dict):
        entry["ok"] = "error" not in str(tool_response.get("content", "")).lower()
    elif isinstance(tool_response, str):
        entry["ok"] = "error" not in tool_response.lower()
    else:
        entry["ok"] = True

    # Write to log
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Rotate if log is too large
        if LOG_PATH.exists():
            lines = LOG_PATH.read_text(encoding="utf-8").count("\n")
            if lines >= MAX_LINES:
                backup = LOG_PATH.with_suffix(".1.jsonl")
                LOG_PATH.rename(backup)

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # Logging failure should never block the agent
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
