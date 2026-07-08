#!/usr/bin/env python3
"""Stop hook ??clean exit when the agent session ends.

Called by the AI tool when a session stops (agent finishes, user stops, or
context limit hit). Receives JSON on stdin:
  {"session_id": "...", "stop_hook_active": true}

Exit codes:
  0 = success (always ??stop hooks never block)

What it does:
  1. Checks if .agent/loop_state.md was written this session. If not, writes
     a minimal "session ended without state write" note (so the next session
     knows the previous one didn't crash cleanly).
  2. Cleans temporary files older than 24h in .agent/tmp/ (if exists).
  3. Appends a session-end marker to the cold archive.

This implements the canon's "state write is the heartbeat" rule at the runtime
layer ??even if the agent forgot to write state, the stop hook leaves a trace.
"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

STATE_PATH = Path(".agent/loop_state.md")
ARCHIVE_PATH = Path(".agent/loop_state_archive.md")
TMP_DIR = Path(".agent/tmp")
SESSION_MARKER = "<!-- Agent Harness Deploy-stop-hook -->"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # 1. Check if loop_state.md exists and was modified recently
    state_written = False
    if STATE_PATH.exists():
        mtime = STATE_PATH.stat().st_mtime
        # Consider "recent" if modified in last 30 minutes
        if time.time() - mtime < 1800:
            state_written = True

    if not state_written:
        # Agent ended without writing state ??leave a trace
        try:
            STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            note = (
                f"\n{SESSION_MARKER}\n"
                f"## Session ended {ts}\n"
                f"State was NOT written by the agent before session end.\n"
                f"This may indicate: agent crashed, context limit hit, or user stopped mid-task.\n"
                f"Next session: check the conversation log for what was in progress.\n"
            )
            with open(STATE_PATH, "a", encoding="utf-8") as f:
                f.write(note)
        except Exception:
            pass

    # 2. Clean old temp files
    if TMP_DIR.exists():
        cutoff = time.time() - 86400  # 24h
        for f in TMP_DIR.iterdir():
            try:
                if f.is_file() and f.stat().st_mtime < cutoff:
                    f.unlink()
            except Exception:
                pass

    # 3. Append session-end marker to cold archive
    try:
        ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(ARCHIVE_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{SESSION_MARKER} session_end ts={ts} state_written={state_written}\n")
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
