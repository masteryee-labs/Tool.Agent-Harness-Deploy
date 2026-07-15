# Agent Harness Deploy

**Self-deploying cross-tool AI harness — one canonical source deployed to Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot & 16 more.**

> Loop engineering · Context engineering · Harness engineering · Agent memory · Comment & version discipline — one command deploys the complete harness to all your AI coding tools.

> **Languages:** **English** (this file) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## What it does

You give any AI coding assistant this repo's GitHub URL and say:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

The AI clones the repo, runs the deployer, and it:

1. **Detects** which AI coding tools are installed on your machine (23 tools supported).
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
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

Use three of these and you maintain three copies. They drift. You forget which is current. **Agent Harness Deploy fixes it: one source (`distill/canon/`), many sinks.**

Unlike simple rules-sync tools that only copy text between config files, this deploys a **complete agent harness**: rules + skills + worker personas + memory protocol + loop engineering + hooks + MCP + vault assets + comment/version discipline sensors.

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
| ChatGPT Desktop | ✓ | — | — | Windows-only app; detection skips on macOS/Linux |
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

Additional concepts layered on top: **harness engineering** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **multi-thinking modes** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **judgment rubrics** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **comment & version discipline** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Comment & version discipline (AI slop prevention)

AI coding assistants produce two persistent forms of slop that survive in the repo:

1. **Explanation bloat** — comments that restate the code (`# loop through items` above `for x in items:`). Zero information, wastes tokens, rots when code changes.
2. **Version stacking** — in-file version markers accumulated across edits (`<!-- v2 -->`, `# v3 fixed X`). Context rot and recursive-depth debt.

This harness prevents both through a **three-layer defense**:

| Layer | Mechanism | File |
|-------|-----------|------|
| **Canon prevention** | REDLINES #16 (no explanatory comments) + #17 (no in-file version stacking) + CORE_CANON Comment/Version discipline | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **Skill detection** | `harness-sensor` SENSOR-4b (comment slop, graceful degradation) + SENSOR-4c (version stacking, always runs) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **Mechanical guard** | `sync.py` pre-sync gate rejects canon files with stacked version markers | [`scripts/sync.py`](scripts/sync.py) |

Research-backed: arXiv 2605.02741 (Volume-Quality Inverse Law), arXiv 2512.20334 (Comment Traps), arXiv 2606.09090 (Context Rot). See [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) for the full evaluation of 6 open-source CLI tools.

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

## Supported tools (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Adding a tool is a registry entry + a 6-line adapter. See [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Repo layout

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # Entry file for AGENTS.md-aware tools
├── CLAUDE.md                  # Entry file for CLAUDE.md-aware tools
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10 more languages
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

## FAQ

<details>
<summary><strong>What is Agent Harness Deploy?</strong></summary>

Agent Harness Deploy is a self-deploying, cross-tool AI harness deployer. It detects which AI coding tools you have installed, then generates and syncs a single canonical harness (caveman-optimized, multi-agent, memory-enabled, loop-engineered) into every detected tool's native config location — so all your AI tools share the same rules.
</details>

<details>
<summary><strong>How do I deploy the harness?</strong></summary>

Tell any AI coding assistant: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. Or run manually: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>Which AI coding tools are supported?</strong></summary>

23 tools: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Adding a tool takes one registry entry + a 6-line adapter.
</details>

<details>
<summary><strong>Does it write configs for tools I don't have installed?</strong></summary>

No. Detection is sacred — only tools actually installed on your machine get deployed. If a tool is not detected, it is reported as "not detected" and skipped. Zero unnecessary footprint.
</details>

<details>
<summary><strong>What is caveman token compression?</strong></summary>

Caveman mode strips filler (hedging, pleasantries, restating the question) from agent communications while keeping all evidence (code, paths, errors, exact values) verbatim. This achieves ~65% token reduction, effectively multiplying the usable context window. See `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>What is the Commander-Worker hierarchy?</strong></summary>

The main thread (Commander) decides, dispatches, and integrates. Workers scan and edit. This prevents the main context from filling with low-level details while keeping decision-making centralized. See `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>How does the memory system work?</strong></summary>

Three-layer disk memory: hot layer (registry <3KB, per-session state <8KB), knowledge layer (anti-patterns <8KB), cold layer (archive, grep-only). State persists on disk, not in context — so sessions survive across tool restarts. See `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>What is comment & version discipline?</strong></summary>

A three-layer defense against AI-generated comment slop (explanation bloat) and in-file version stacking. Layer 1: canon red lines (#16, #17). Layer 2: harness-sensor skill (SENSOR-4b/4c). Layer 3: sync.py mechanical guard. See `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>Is this a jailbreak or safety-removal tool?</strong></summary>

No. This is a defensive harness tool. It configures AI coding assistants' rule files. It does not modify model weights, does not remove safety guardrails, and does not bundle jailbreak tools. The sandbox boundary realignment works at the file level via JSON risk contracts, not at the model level by removing refusal loops.
</details>

<details>
<summary><strong>What license is this project under?</strong></summary>

MIT License — see [LICENSE](LICENSE). Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>Can I add my own AI tool?</strong></summary>

Yes. Adding a tool requires one entry in `adapters/registry.json` + a 6-line adapter class. See `Docs/03-Tool-Adapters.md`.
</details>

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
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI comment slop + version stacking: CLI tool evaluation |
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

---

<details>
<summary><em>SEO / AEO / GEO / LLMO metadata</em></summary>

**Project name:** Agent Harness Deploy

**One-line description:** Self-deploying cross-tool AI harness — one canonical source, 23 AI coding tool sinks.

**Keywords:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention

**Key facts for AI/LLM citation:**
- 23 AI coding tools supported (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot, etc.)
- One canonical source (`distill/canon/`), many tool-native sinks
- 5 technical pillars: caveman compression, Commander-Worker, loop engineering, deep memory, sandbox boundary
- Three-layer comment/version discipline: canon red lines + skill sensors + mechanical guard
- Cross-platform: Windows, macOS, Linux (Python 3.9+)
- MIT License, copyright masteryee-labs
- Anti-link-rot: all external schemas embedded in `core/assets/vault/`
- Deploy command: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Target audience:** Developers using multiple AI coding assistants who want consistent rules across all tools. Open-source contributors, AI-first engineering teams, solo developers using Claude Code + Cursor + Codex simultaneously.

**Category:** Developer tools > AI coding assistants > Configuration management > Agent harness engineering
</details>
