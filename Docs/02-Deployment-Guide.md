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
  → detect.py    → reads registry.json, runs checks per tool
  → sync.py      → builds canonical body from distill/canon/, writes to detected tools
  → verify.py    → read-backs every written file, checks marker present
```

- Only **detected** tools get synced. Undetected tools are skipped (not fabricated).
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
| `--global` | Also write global entry files (`~/.claude/CLAUDE.md`, `~/.codex/instructions.md`, `~/.gemini/AGENTS.md`, `~/.config/devin/AGENTS.md`). The harness then applies to *all* your projects, not just this repo. |
| `--tools X,Y` | Sync only listed tool ids. Example: `--tools claude_code,codex`. |
| `--dry-run` | Detect + report only. No writes. Safe for inspection. |
| `--canon` | Regenerate the repo's own `AGENTS.md` canon body from `distill/canon/`. Use after editing canon. |

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
