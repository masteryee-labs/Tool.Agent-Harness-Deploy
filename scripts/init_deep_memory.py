#!/usr/bin/env python3
"""init_deep_memory.py — One-command bootstrap for deep-memory storage.

Detects the Python interpreter, creates a venv in `~/.deep-memory/.venv`, installs the
`chroma-hybrid-search` skill requirements, and builds the initial empty index.

Usage:
    python scripts/init_deep_memory.py
    python scripts/init_deep_memory.py --project-root .
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def get_home() -> Path:
    return Path.home()


def get_repo_root() -> Path:
    """Return repo root assuming this script lives in scripts/."""
    return Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap deep-memory storage.")
    ap.add_argument("--project-root", default=".", help="Project root for relative paths")
    ap.add_argument("--no-index", action="store_true", help="Skip initial empty index build")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    repo_root = get_repo_root()
    home = get_home()
    venv_dir = home / ".deep-memory" / ".venv"
    venv_dir.mkdir(parents=True, exist_ok=True)

    # Determine paths
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"

    reqs = repo_root / "distill" / "skills" / "chroma-hybrid-search" / "requirements.txt"
    if not reqs.exists():
        print(f"[init_deep_memory] Requirements not found: {reqs}")
        return 1

    # 1. Create venv if interpreter not present
    if not venv_python.exists():
        print(f"[init_deep_memory] Creating venv at {venv_dir}")
        cmd = [sys.executable, "-m", "venv", str(venv_dir)]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[init_deep_memory] Failed to create venv: {e}")
            return 1
    else:
        print(f"[init_deep_memory] Venv already exists at {venv_dir}")

    # 2. Upgrade pip and install requirements
    print(f"[init_deep_memory] Installing requirements from {reqs}")
    try:
        subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(venv_pip), "install", "-r", str(reqs)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[init_deep_memory] Failed to install requirements: {e}")
        return 1

    # 3. Build empty index
    if not args.no_index:
        update_db = repo_root / "distill" / "skills" / "chroma-hybrid-search" / "scripts" / "update_db.py"
        if update_db.exists():
            print("[init_deep_memory] Building empty index")
            env = os.environ.copy()
            env["PROJECT_ROOT"] = str(project_root)
            try:
                subprocess.run(
                    [str(venv_python), str(update_db), "--project-root", str(project_root)],
                    check=True,
                    env=env,
                )
            except subprocess.CalledProcessError as e:
                print(f"[init_deep_memory] Index build failed: {e}")
                return 1
        else:
            print(f"[init_deep_memory] update_db.py not found at {update_db}, skipping index")

    print(f"[init_deep_memory] Deep memory ready at {venv_dir}")
    print(f"  Python: {venv_python}")
    print(f"  Activate: source {venv_dir}/bin/activate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
