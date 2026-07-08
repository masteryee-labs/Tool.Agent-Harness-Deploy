# 00 — Overview

> Start here. This is the index. Load other Docs on demand, not all at once.

## What is Agent Harness Deploy?

A **self-deploying, cross-tool AI harness synchronizer**. You give an AI coding assistant
this repo's GitHub URL and say "幫我部屬：[url]" (or "deploy: [url]"). The AI clones the
repo, runs the deployer, and the deployer:

1. **Detects** which AI coding tools are installed on your machine.
2. **Generates** a single canonical harness (caveman-optimized, multi-agent, memory-enabled,
   loop-engineered) from `distill/canon/`.
3. **Syncs** that harness into every detected tool's native config location.
4. **Verifies** every written file by reading it back.

Result: whichever AI tool you open next — Claude Code, Antigravity, Codex, Devin, Cursor,
etc. — they all share the **same** rules, memory protocol, orchestrator, and skills. No more
re-explaining your workflow to each tool. No more drift between `.claude/`, `.codex/`,
`.devin/`, `AGENTS.md`.

## The problem it solves

Different AI tools store their config in different places and formats:

| Tool | Where its rules live |
|------|----------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` at repo root |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Claude Desktop | `claude_desktop_config.json` (JSON, not markdown) |

If you use three of these, you maintain three copies of your rules. They drift. You forget
which one is current. Agent Harness Deploy fixes this: **one source (`distill/canon/`), many sinks**.

## What it is NOT

- Not a coding agent. It's a harness *installer/synchronizer*.
- Not a prompt library. The canon is a *discipline*, not a prompt collection.
- Not a replacement for your tools. It configures the tools you already have.
- Not a jailbreak or safety-removal tool. (See `13-Glossary.md` on Heretic — referenced for
  understanding interpretability only; not used or endorsed for bypassing safety.)

## Key concepts (one-liners)

| Concept | Meaning | Deep dive |
|---------|---------|-----------|
| Caveman | Token-compressed agent comms (~65% cut, 4 levels) | `distill/canon/CAVEMAN_PROTOCOL.md` |
| Commander + Workers | One orchestrator dispatches focused workers | `04-Orchestrator-Design.md` |
| Three-layer memory | Hot / knowledge / cold state on disk | `distill/canon/MEMORY_PROTOCOL.md` |
| Loop engineering | Autonomous iteration with stop conditions + kickoff templates | `distill/canon/LOOP_PROTOCOL.md` |
| Harness engineering | The system around the model | `distill/canon/HARNESS_ENGINEERING.md` |
| Multi-thinking modes | Switch angles to cut hallucination | `09-Multi-Thinking-Modes.md` |
| Maker ≠ Checker | Author never verifies own output | `distill/canon/VERIFICATION_PROTOCOL.md` |
| Judgment rubrics | Externalized decision criteria with positive/negative examples | `distill/canon/JUDGMENT_RUBRICS.md` |
| Handoff letter | Context from past sessions to future sessions | `distill/canon/HANDOFF_LETTER.md` |
| Deep-memory | Hybrid BM25+vector+reranker cross-project retrieval | `distill/skills/chroma-hybrid-search/` |

## Repo map

```
agent-harness-deploy/
├── AGENTS.md                  # Entry file for AGENTS.md-aware tools
├── README.md                  # English (default)
├── README_zh-TW.md            # 繁體中文
├── README_zh-CN.md            # 简体中文
├── Docs/                      # This directory — human-facing documentation
├── distill/
│   ├── canon/                 # Canonical rules (the source of truth)
│   │   ├── CORE_CANON.md
│   │   ├── BOOT_PROTOCOL.md
│   │   ├── MEMORY_PROTOCOL.md
│   │   ├── LOOP_PROTOCOL.md
│   │   ├── VERIFICATION_PROTOCOL.md
│   │   ├── CAVEMAN_PROTOCOL.md
│   │   ├── JUDGMENT_RUBRICS.md     # Externalized decision criteria
│   │   ├── HANDOFF_LETTER.md       # Letter to future sessions
│   │   └── REDLINES.md
│   ├── orchestrator/          # Commander + workers prompts
│   └── skills/                # Reusable skills (YAML frontmatter, "Use when..." format)
│       ├── gap-scan.md
│       ├── harness-sensor.md
│       ├── auditor.md
│       ├── loop-memory.md
│       ├── using-skills.md        # Meta-skill: enforces skill-first methodology
│       └── chroma-hybrid-search/  # Deep-memory hybrid retrieval (BM25+vector+reranker)
├── adapters/                  # Per-tool config adapters + registry.json
├── scripts/                   # detect.py, distill.py, sync.py, verify.py, deploy.*
└── .agent/                    # The deployer's own harness (dogfooded)
```

## Doc index

| # | Doc | When to read |
|---|-----|--------------|
| 00 | Overview (this) | First |
| 01 | Architecture | Want the full system design |
| 02 | Deployment Guide | Deploying (auto or manual) |
| 03 | Tool Adapters | Adding/fixing a tool's config location |
| 04 | Orchestrator Design | Understanding Commander + Workers + self-orchestration |
| 09 | Multi-Thinking Modes | Reducing hallucination via angle-switching |
| 12 | Troubleshooting | Something didn't work |
| 13 | Glossary | Term definitions + source references |
| — | References | Source links for the 5 pillars + vault assets + orchestrator architecture |
| — | Agents/nuwa.md | Nuwa verification system + Nuwa Team (cognitive diversity) |

### Canon replacements (for deleted Docs files)

| Canon file | Replaces | When to read |
|------------|----------|--------------|
| `distill/canon/CAVEMAN_PROTOCOL.md` | `05-Caveman-Optimization.md` | Why/how token compression |
| `distill/canon/MEMORY_PROTOCOL.md` | `06-Memory-System.md` | How state persists across runs |
| `distill/canon/LOOP_PROTOCOL.md` | `07-Loop-Engineering.md` | Autonomous iteration, 5+1 components, stop conditions |
| `distill/canon/HARNESS_ENGINEERING.md` | `08-Harness-Engineering.md` | The system-around-the-model philosophy |
| `distill/canon/VERIFICATION_PROTOCOL.md` | `10-Verification-Protocol.md` | Why maker ≠ checker, SHA discipline, multi-agent debate |
| `distill/orchestrator/COMMANDER.md` | `Agents/commander.md` | Commander dispatch workflow |
| `distill/canon/REDLINES.md` | `harness_control_plane.md` | Hard stops and red lines |
| `distill/canon/JUDGMENT_RUBRICS.md` | `harness_rubrics.md` | Externalized decision criteria |

## Honest clause

This deployer can reliably do: detection, config generation, file sync, verification,
backup. It cannot do: taste/aesthetic decisions, guessing what you want beyond the deploy
contract, writing configs for tools it can't detect. When uncertain, it reports — it does
not fabricate.
