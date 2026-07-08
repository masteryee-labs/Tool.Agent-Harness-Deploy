#!/usr/bin/env bash
# Tool.Agent-Harness-Deploy — manual deploy (Linux/macOS).
# Detects installed AI tools, syncs the canonical harness into each, verifies.
# Equivalent to: python scripts/distill.py
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "== Tool.Agent-Harness-Deploy — Manual Deploy (bash) =="

if ! command -v python3 >/dev/null 2>&1; then
    if ! command -v python >/dev/null 2>&1; then
        echo "ERROR: python not found. Install Python 3.9+." >&2
        exit 1
    fi
    PY=python
else
    PY=python3
fi

ARGS=("scripts/distill.py")
while [[ $# -gt 0 ]]; do
    case "$1" in
        --global) ARGS+=("--global"); shift ;;
        --dry-run) ARGS+=("--dry-run"); shift ;;
        --tools) ARGS+=("--tools" "$2"); shift 2 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done

"$PY" "${ARGS[@]}"
