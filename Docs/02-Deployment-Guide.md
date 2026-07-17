# 02 — Deployment Guide

> How "幫恁部署：[url]" works, step by step. This is the Doc the receiving AI reads first.

## The one-line deploy

Tell any AI coding assistant:

> 幫恁部署：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy

(English equivalent: "deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy")

That's it. The AI does the rest.

## What the AI does (the contract)

When the AI receives that instruction, it MUST:

1. **Clone or enter the repo.**
   ```
   git clone https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
   cd Tool.Agent-Harness-Deploy
   ```
   (If already cloned, just `cd` into it.)

2. **Read `AGENTS.md`.** This is the entry file. It routes the AI to the deploy flow
   (this Doc) and the canon.

3. **Run the deployer.**
   ```
   python scripts/distill.py
   ```
   This runs detect → sync → verify in one shot.

4. **Report results.** The AI tells the user:
   - Which tools were detected (with evidence).
   - Which tools were synced (with file paths).
   - Verification PASS/FAIL.
   - "Open any of your AI tools now — they share the same harness."

5. **If verification FAILS**, the AI does NOT claim success. It reports the failures and
   points to `12-Troubleshooting.md`.

## What the deployer does internally

```
distill.py
  → migrate.py   → scans global MCP files for legacy pollution, safe-restores from .bak
  → detect.py    → reads registry.json, runs checks per tool
  → sync.py      → builds canonical body from distill/canon/, writes to detected tools
  → verify.py    → read-backs every written file, checks marker present
```

- **Step 0 (legacy cleanup):** scans 4 global MCP locations for `.bak` files from old
  deploys. Safe-restores if no user changes since. Skips + warns if user changed MCP
  servers. See "Legacy cleanup" below.
- Only **detected** tools get synced. Undetected tools are skipped (not fabricated).
- **Project-scoped** configs (`.mcp.json`, `.claude/settings.json`, hooks) are always
  written. **Global-scoped** configs (`~/.codeium/windsurf/mcp_config.json`, etc.) are
  only written with `--global`. This prevents cross-project pollution.
- Existing configs are backed up to `.bak` before overwrite.
- Dedupes by target path (AGY CLI + Antigravity — one `AGENTS.md` write).

## After deploy

The harness is now in every detected tool. When you open any of them in this repo (or
globally, if you ran with `--global`), they read their entry file, which contains the
canonical body. They all behave the same: caveman comms, commander+workers, three-layer
memory, loop discipline, maker≠checker verification.

## Prerequisites

- Python 3.9+ on PATH (`python --version` or `python3 --version`).
- The repo cloned locally.
- At least one AI coding tool installed (otherwise there's nothing to sync to).

## Manual deploy (no AI)

If you want to deploy without an AI driving it:

### Quick start

**Windows (PowerShell):**
```powershell
cd C:\path\to\Tool.Agent-Harness-Deploy
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1
```

**Linux / macOS (bash):**
```bash
cd /path/to/Tool.Agent-Harness-Deploy
bash scripts/deploy.sh
```

**Direct (any OS):**
```bash
cd /path/to/Tool.Agent-Harness-Deploy
python scripts/distill.py
```

All three do the same thing: detect → sync → verify.

### Step by step (the long way)

If you want to see each stage separately:

**1. Detect — see what's installed**
```bash
python scripts/detect.py
```
Output lists detected tools (with evidence) and not-detected tools. This step makes no
changes to your system.

**2. Sync — write the harness to detected tools**
```bash
python scripts/sync.py
```
For each detected tool, writes the canonical body to the tool's native entry file. Backs
up any existing file to `.bak` first.

**3. Verify — confirm writes are intact**
```bash
python scripts/verify.py
```
Reads back every written file and confirms the canonical marker is present. Reports
PASS/FAIL per file.

## Flags

| Flag | Effect |
|------|--------|
| `--global` | Also write global entry files (`~/.claude/CLAUDE.md`, `~/.codex/instructions.md`, `~/.gemini/AGENTS.md`, `~/.config/devin/AGENTS.md`) **and** global MCP files (`~/.codeium/windsurf/mcp_config.json`, `~/.cline/...`, `~/.roo/...`). The harness then applies to *all* your projects, not just this repo. Without this flag, only project-level configs are written — different projects are fully isolated. |
| `--tools X,Y` | Sync only listed tool ids. Example: `--tools claude_code,codex`. |
| `--dry-run` | Detect + report only. No writes. Safe for inspection. |
| `--no-migrate` | Skip Step 0 (legacy global MCP cleanup). Use if you want to skip the auto-cleanup. |
| `--canon` | Regenerate the repo's own `AGENTS.md` canon body from `distill/canon/`. Use after editing canon. |

## Project vs global scope

The deployer separates **project-scoped** and **global-scoped** runtime configs:

| Config type | Project-scoped (always written) | Global-scoped (--global only) |
|-------------|--------------------------------|-------------------------------|
| Entry file | `.claude/CLAUDE.md`, `.codex/instructions.md`, etc. | `~/.claude/CLAUDE.md`, `~/.codex/instructions.md`, etc. |
| MCP | `.mcp.json`, `.cursor/mcp.json`, `.devin/mcp.json`, etc. | `~/.codeium/windsurf/mcp_config.json`, `~/.cline/...`, `~/.roo/...`, `${APPDATA}/Claude/...` |
| Settings | `.claude/settings.json`, `.codex/config.toml`, etc. | (none — settings are always project-scoped) |
| Hooks | `.claude/hooks/`, `.codex/hooks/`, etc. | (none — hooks are always project-scoped) |

**Settings and hooks are always project-scoped** — they contain permissions and hook
scripts that reference project-relative paths. Global settings would be dangerous
(e.g., globally allowing `git push --force`).

**MCP is mixed**: most tools have per-project MCP (Claude Code, Codex, Cursor, Devin,
etc.), but 4 tools only have a global MCP file (Claude Desktop, Cline, Roo Code,
Windsurf). For those 4, global MCP is only written with `--global`.

## Legacy cleanup

Old versions of Agent Harness Deploy (before the scope fix) wrote to global MCP files
even without `--global`, polluting configs for Claude Desktop, Cline, Roo Code, and
Windsurf. The deployer now auto-cleans this on every run (Step 0):

1. **Scans** the 4 global MCP locations for `.bak` files from old deploys.
2. **Safe-restores** from `.bak` if the current file's `mcpServers` matches the `.bak`
   (after stripping `_`-prefixed keys, which old AHD removed) — meaning no user changes
   were made since the old deploy.
3. **Skips + warns** if you added/removed MCP servers after the old deploy. The `.bak`
   is kept for manual review.

Standalone usage:
```bash
python scripts/migrate.py --report    # check only, no writes
python scripts/migrate.py             # auto-restore where safe
python scripts/migrate.py --restore   # force-restore from .bak (destructive)
```

## Re-deploying after canon changes

If you change rules in `distill/canon/`:

1. Regenerate the repo entry:
   ```bash
   python scripts/sync.py --canon
   ```
2. Push to all detected tools:
   ```bash
   python scripts/distill.py
   ```
3. (Optional) Push globally:
   ```bash
   python scripts/distill.py --global
   ```

## Rolling back

Every sync backs up existing files to `.bak`. To roll back a tool:

```bash
# Example: roll back Claude Code project entry
mv .claude/CLAUDE.md.bak .claude/CLAUDE.md
```

The `.bak` files are your undo. Don't delete them until you've confirmed the new config works.

## What you'll see in each tool after deploy

| Tool | File written | What the tool reads |
|------|--------------|---------------------|
| Claude Code | `.claude/CLAUDE.md` | Rules at project start |
| Antigravity | `AGENTS.md` | Rules at repo entry |
| Codex | `.codex/instructions.md` | Instructions |
| Devin | `.devin/AGENTS.md` | Rules |
| Cursor | `.cursor/rules/Agent Harness Deploy.mdc` | Rule with `alwaysApply: true` |
| Claude Desktop | `claude_desktop_config.json` | `_Agent Harness Deploy` pointer key |

## Verifying it worked

1. Run `python scripts/verify.py` — all PASS.
2. Open one of your detected tools in this repo.
3. Ask it "what rules are you following?" — it should describe the Agent Harness Deploy harness
   (caveman comms, commander+workers, three-layer memory, maker≠checker).

## What the AI must NOT do

- Do not start "improving" or "extending" the deployer. It's a tool, not a codebase to hack.
- Do not write configs for tools that weren't detected.
- Do not skip verification.
- Do not claim success if verify FAILS.
- Do not edit `distill/canon/` during a deploy (canon edits are a separate human-approved action).
