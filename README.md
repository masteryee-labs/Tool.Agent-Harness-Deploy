# Agent Harness Deploy

**Self-deploying cross-tool AI harness — one canonical source deployed to Claude Code, Codex, Cursor, Devin, Antigravity & 9 more.**

> Loop engineering · Context engineering · Harness engineering · Agent memory — one command deploys the complete harness to all your AI coding tools.

> Languages: **English** (this file) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md)

---

## What it does

You give any AI coding assistant this repo's GitHub URL and say:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

The AI clones the repo, runs the deployer, and it:

1. **Detects** which AI coding tools are installed on your machine (Claude Code, Codex, Cursor, Devin, Antigravity, etc.).
2. **Generates** one canonical harness — caveman-optimized, multi-agent, memory-enabled, loop-engineered — from `distill/canon/`.
3. **Deploys** it into every detected tool's native config location (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Verifies** every written file by reading it back (zero-truncation check).

**Result:** whichever AI tool you open next — they all share the **same** rules, memory protocol, orchestrator, skills, hooks, and MCP config. No more maintaining three copies of your rules. No more drift between `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Only tools that are **actually installed** get deployed. Nothing is written for tools that aren't detected. You can also deploy manually — no AI required.

## Why

Every AI coding tool stores its config in a different place and format:

| Tool | Where its rules live |
|------|----------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Claude Desktop | `claude_desktop_config.json` |

Use three of these and you maintain three copies. They drift. You forget which is current. **Agent Harness Deploy fixes it: one source (`distill/canon/`), many sinks.**

Unlike simple rules-sync tools that only copy text between config files, this deploys a **complete agent harness**: rules + skills + worker personas + memory protocol + loop engineering + hooks + MCP + vault assets.

## The one-line deploy

Tell any AI coding assistant:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

The AI reads `AGENTS.md`, runs `python scripts/distill.py`, reports what it deployed. Done.

See [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) for the full contract.

## Manual deploy (no AI)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Any OS, direct
python scripts/distill.py
```

See [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Cross-platform support

This project works on **Windows, macOS, and Linux**.

| Platform | Requirements | Deploy command |
|----------|-------------|----------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| Any OS | Python 3.9+ | `python scripts/distill.py` |

### How cross-platform works

- All Python scripts use `pathlib` (no hardcoded `\` or `/` separators).
- Tool paths in `adapters/registry.json` use env expansion: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- On macOS/Linux, Windows-only env vars (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) automatically fall back to XDG-style paths (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` is for Windows; `deploy.sh` is for macOS/Linux. Both call the same `python scripts/distill.py`.

### Platform-specific tools

| Tool | Windows | macOS | Linux | Note |
|------|---------|-------|-------|------|
| Claude Desktop | ✓ | — | — | Windows-only app; detection skips on macOS/Linux |
| Cursor | ✓ | ✓ | ✓ | Detects `${APPDATA}/Cursor` (Win) or `~/Library/Application Support/Cursor` (macOS) |
| All other tools | ✓ | ✓ | ✓ | Detected via CLI command on PATH |

## What's in the harness — 5 technical pillars

The deployer syncs a canonical rule set built on 5 pillars of agent harness engineering:

| Pillar | What it gives you | Vault file | Doc |
|--------|-------------------|------------|-----|
| **1. Caveman token compression** | ~65% token cut, more usable context | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Commander-Worker hierarchy** | AI prompts itself — one orchestrator, many focused workers; dispatch three-piece set | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Loop engineering + Vault control** | `/loop` (monitoring) vs `/goal` (convergent); maker ≠ checker; SHA discipline | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. Deep repo memory** | Three-layer disk memory (hot <3KB, knowledge <8KB, cold ∞); optional deep-memory hybrid retrieval | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. Sandbox boundary realignment** | Non-critical path 100% yield; critical-file JSON risk contract | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Additional concepts layered on top: **harness engineering** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **multi-thinking modes** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **judgment rubrics** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)).

## Anti-link-rot architecture (Embedded Vault)

All external technical configuration mechanisms are **embedded and locally cached** in `core/assets/vault/`. The deployer does **not** fetch schemas from external repos at runtime. This is an immutable local template database:

| Vault file | Embedded source |
|-----------|-----------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

See [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Supported tools (14)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude
Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI

Adding a tool is a registry entry + a 6-line adapter. See
[`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Repo layout

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # Entry file for AGENTS.md-aware tools
├── CLAUDE.md                  # Entry file for CLAUDE.md-aware tools
├── README.md / README_zh-TW.md / README_zh-CN.md
├── core/assets/               # Vault, skills, runtime (hooks, settings, MCP)
├── Docs/                      # Documentation
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # Tool adapters + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                    # The deployer's own harness (dogfooded)
```

See [`Docs/00-Overview.md`](Docs/00-Overview.md) for detailed directory descriptions.

## Quick commands

```bash
python scripts/detect.py            # see which tools are installed
python scripts/distill.py           # full deploy: detect → sync → verify
python scripts/distill.py --global  # also sync global entry files
python scripts/distill.py --dry-run # detect only, no writes
python scripts/verify.py            # re-verify after a sync
python scripts/sync.py --canon      # regenerate AGENTS.md after editing canon
```

## How it works (30-second version)

1. `detect.py` reads `adapters/registry.json`, runs each tool's detection checks (CLI binary, env path, app data).
2. `sync.py` concatenates `distill/canon/*.md` into one canonical body, writes it to each detected tool's native entry file (backing up existing files to `.bak` first). Only detected tools get written.
3. `verify.py` reads back every written file and confirms the canonical marker is present (zero-truncation check).

Full design: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## Honest clause

The deployer can reliably do: detection, config generation, file sync, verification, backup. It cannot do: taste/aesthetic decisions, guessing what you want beyond the deploy contract, writing configs for tools it can't detect. When uncertain, it reports — it does not fabricate. Full statement in [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Safety note

This repo is a **defensive** harness tool. It configures AI coding assistants' rule files. It does **not** modify model weights, does **not** remove safety guardrails, and does **not** bundle or endorse jailbreak/safety-removal tools. The Heretic project is referenced in the glossary only as part of the interpretability landscape that informed the harness's understanding of steering vectors — it is not used here. See [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Requirements

- Python 3.9+
- At least one supported AI coding tool installed (otherwise there's nothing to deploy to)

## License

MIT — see [LICENSE](LICENSE).

## References

See [`Docs/REFERENCES.md`](Docs/REFERENCES.md) for source references by pillar.

## Documentation index

| Doc | Topic |
|-----|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Overview & index |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Full system design |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | How "deploy:" works |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Per-tool config locations |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Commander + Workers + self-orchestration |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Hallucination reduction |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Common issues |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Terms & sources |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Nuwa system + Nuwa Team (parallel reasoning, cognitive diversity) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Token compression (was Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Three-layer memory (was Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Loop engineering, 5+1 components (was Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | System around the model (was Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, SHA discipline (was Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Hard stops + control plane (was Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Externalized decision criteria (was Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Commander-Worker delegation (was Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Anti-link-rot embedded asset vault |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Runtime layer: hooks, settings, MCP templates |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Vendored nuwa-skill attribution & file inventory |
