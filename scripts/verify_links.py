#!/usr/bin/env python3
"""verify_links.py — CLI wrapper around adapters/verify_links.py.

Usage:
    python scripts/verify_links.py <file-or-dir>
    python scripts/verify_links.py <file-or-dir> --allow-missing "Docs/" --allow-missing "scripts/verify.py"
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from adapters.verify_links import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
