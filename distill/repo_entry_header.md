# Agent Harness Deploy — Agent Entry File

> You are reading this because an AI coding assistant cloned this repo after a user said
> "幫我部屬：[github link]" / "deploy: [github link]" / "set up this harness".
> This file is the **single source of truth** that every AGENTS.md-aware tool reads first.

---

## 0. What this repo is (read this before doing anything)

Agent Harness Deploy is a **self-deploying, cross-tool AI harness deployer**.

It does **one job**: detect which AI coding tools are installed on this machine, then generate
and sync a single canonical harness (caveman-optimized, multi-agent, memory-enabled,
loop-engineered, session-concurrent) into every detected tool's native config location — so that whichever tool
the user opens next, they get the **same** rules, memory, skills, and orchestrator.

**This repo is the deployer, not the product.** The product is the harness it writes into
your tools. Do not start building features. Do not refactor the deployer. Run the deployer.

---

## 1. BOOT protocol (order is mandatory)

1. `read(".agent/loop_state.md")` — read the session registry (<3KB).
   - If the file does not exist, create an empty registry:
     ```yaml
     ---
     context_fill_pct: 0
     caveman_level: full
     active_sessions: []
     active_session: null
     ---
     ```
2. `read(".agent/knowledge_distill.md")` — load anti-patterns (<8KB).
3. `read(".agent/user_profile.md")` — load profile (<2KB).
4. If `.agent/loop_state.md` has an `active_session` that is `in_progress`, `crashed`, or `suspected_crashed`,
   `read(".agent/session_state/<session_id>.json")` and `.agent/loop_state/<session_id>.md` **only for audit**.
   Do not read all `session_state/*.json` or `loop_state/*.md` files. If the previous session's
   `owned_files`/`affected_files`/`tags` overlap the new task, ask the human whether to continue.
   **Never auto-resume.**
5. Read per-session context flags — `.agent/context_flags/<session_id>.json` if it exists.
6. Output a GoalSpec (see `distill/canon/BOOT_PROTOCOL.md`) and write it to:
   - `.agent/loop_state/<session_id>.md`
   - `.agent/session_state/<session_id>.json`
7. Call `python scripts/loop_memory_sync.py` to update `.agent/loop_state.md` registry.
8. Read `Docs/02-Deployment-Guide.md` — the exact deploy flow.
9. Run the deployer: `python scripts/distill.py` (or follow `Docs/02-Deployment-Guide.md §Manual deploy`).

> Do NOT read every Doc. Read `Docs/02-Deployment-Guide.md` first, then load others on demand
> via the index in `Docs/00-Overview.md`.

---

## 2. The deploy contract (what "幫我部屬" means)

When the user says **"幫我部屬：[this repo's URL]"**, the receiving AI must:

1. Clone / enter the repo.
2. Read this `AGENTS.md`.
3. Run `python scripts/distill.py` (auto-detect installed tools → generate → sync).
4. Report which tools were detected and synced, with file paths as evidence.
5. Tell the user: "open any of your AI tools now — they share the same harness."

The deployer **only deploys sync pipelines for tools that are actually installed**. It will
never write configs for a tool that is not present. See `Docs/03-Tool-Adapters.md`.

Manual deploy is also supported — see `Docs/02-Deployment-Guide.md §Manual deploy`.

---

## 3. Red lines (violating any → stop and ask the human)

1. Do not modify `distill/canon/` without human approval — it is the canonical source.
2. Do not delete or overwrite an existing tool config without first creating a `.bak`.
3. Do not write configs for tools that are not detected as installed.
4. Do not self-verify — verification is done by `scripts/verify.py` or a fresh-context agent.
5. Do not hardcode tool paths — use `adapters/registry.json`.
6. Do not skip the detection step. Detection is the whole point.
7. Do not start "improving" or "extending" the deployer unless explicitly asked.
8. Do not auto-resume a previous session — ask the human first.
9. Do not read all `loop_state/*.md` files at BOOT; only read the registry + the one matching session.
10. Do not write secrets into `session_state`, `journal.jsonl`, or tool logs.

Full red lines → `distill/canon/REDLINES.md`.

---

## 4. Index (load on demand)

| What you need | Where to look |
|---------------|---------------|
| Overview & concept | `Docs/00-Overview.md` |
| Deploy flow (auto + manual) | `Docs/02-Deployment-Guide.md` |
| Per-tool config locations | `Docs/03-Tool-Adapters.md` |
| Commander + workers design | `Docs/04-Orchestrator-Design.md` |
| Caveman token optimization | `distill/canon/CAVEMAN_PROTOCOL.md` |
| Memory system (registry + per-session state) | `distill/canon/MEMORY_PROTOCOL.md` |
| Loop engineering | `distill/canon/LOOP_PROTOCOL.md` |
| Harness engineering | `distill/canon/HARNESS_ENGINEERING.md` |
| Multi-thinking modes | `Docs/09-Multi-Thinking-Modes.md` |
| Verification protocol | `distill/canon/VERIFICATION_PROTOCOL.md` |
| Manual deployment | `Docs/02-Deployment-Guide.md §Manual deploy` |
| Troubleshooting | `Docs/12-Troubleshooting.md` |
| Glossary | `Docs/13-Glossary.md` |
| Orchestrator design + self-orchestration | `Docs/04-Orchestrator-Design.md` |
| Commander-Worker delegation + 派工三件套 | `distill/orchestrator/COMMANDER.md` |
| Nuwa system + Nuwa Team (cognitive diversity) | `Docs/Agents/nuwa.md` |
| Worktree manager (parallel Worker isolation) | `scripts/worktree.py` |
| Dispatch planner (file ownership + conflict detection) | `scripts/plan_dispatch.py` |
| Loop/memory sync (registry regeneration) | `scripts/loop_memory_sync.py` |
| Memory audit (candidate -> knowledge) | `scripts/memory_audit.py` |
| Red lines + control plane (8-step lifecycle) | `distill/canon/REDLINES.md` |
| Judgment rubrics (positive/negative examples) | `distill/canon/JUDGMENT_RUBRICS.md` |
| Canonical rules (tool-agnostic) | `distill/canon/` |
| Orchestrator prompts | `distill/orchestrator/` |
| Reusable skills | `distill/skills/` |
| Tool adapters | `adapters/` |
| Detection + sync scripts | `scripts/` |
| **Anti-link-rot embedded asset vault** | `core/assets/vault/` |
| **Vendored external skills** | `core/assets/skills/nuwa-skill/` |

---

## 5. Cross-tool adaptation

| Tool family | Entry file the deployer writes | Config root |
|-------------|----------------------------------|-------------|
| Antigravity / Gemini CLI | `AGENTS.md` | repo root + `~/.gemini/` |
| Codex / Codex CLI | `.codex/instructions.md` | `.codex/` + `~/.codex/` |
| Claude Code | `.claude/CLAUDE.md` | `.claude/` + `~/.claude/` |
| Devin / Devin CLI | `.devin/AGENTS.md` | `.devin/` + `~/.config/devin/` |
| Cursor | `.cursor/rules/*.mdc` | `.cursor/` |
| Claude Desktop | `claude_desktop_config.json` | `%APPDATA%\Claude\` |
| OpenCode / OpenClaw / Hermes / ZCode / Kimi Code | tool-specific | see `adapters/registry.json` |

> The deployer generates a **canonical body** once, then each adapter translates it into the
> tool's native format and writes it to the tool's native location. One source, many sinks.

---

## 6. Honest clause

- The deployer **can** do: detection, config generation, file sync, verification, backup.
- The deployer **cannot** do: taste/aesthetic decisions, guessing what a user wants beyond
  the deploy contract, writing configs for tools it cannot detect.
- When uncertain: detect, don't guess. When detection fails: report, don't fabricate.

*This file is the entry point. The canonical rules live in `distill/canon/`. Modify there,
not here. After modifying, run `python scripts/sync.py --canon`.*
