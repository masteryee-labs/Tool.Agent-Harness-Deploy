# 04 — Orchestrator Design

> The "AI prompts itself" pattern: one Commander + many focused Workers.
> Reference: agency-agents (msitarzewski) + masteryee-labs Docs/Agents architecture.

## The core idea

A single LLM thread has limited attention and context. When you ask it to scan a repo,
write code, and verify the result all in one conversation, it gets sloppy. The solution:
**split the work across focused agents with clean context windows.**

- **Commander** — the main conversation. Decomposes, dispatches, integrates, verifies. Never
  does the actual scanning/building/writing.
- **Workers** — focused sub-agents. Each gets one task, one clean context, one acceptance
  criteria set. Reports back in a strict format.

This is "AI prompts itself": the Commander writes prompts for Workers, the Workers execute,
the Commander integrates. The human only talks to the Commander.

## Why this is the signature feature

Most "AI coding" setups are one thread doing everything: scanning, writing, verifying,
reporting. The thread's context fills with file contents and error logs; by the time it
needs to judge, it has lost the big picture. Output quality degrades as context fills.

Self-orchestration fixes this structurally, not by prompt-tuning:
- **Commander's context stays clean** — it carries the plan, not the data. Workers carry
  the data; the Commander carries the judgment.
- **Workers get clean context** — each Worker sees only its task. Less distraction, fewer
  hallucinations.
- **Maker ≠ checker is enforced by structure** — a fresh-context Verifier has no
  investment in the answer. It catches what the author talked themselves past.

This is the single highest-value structural rule in production agent systems (OpenAI,
Anthropic, Cloudflare, Stripe all converge on it). Agent Harness Deploy ships it as canon,
into every detected tool, so whichever tool you open next already has it.

## Why it works

1. **Clean context** — a Worker doesn't carry the Commander's whole conversation. It sees
   only its task. Less distraction, fewer hallucinations.
2. **Specialization** — a Scout (read-only) doesn't accidentally edit files. A Verifier
   (fresh context) doesn't inherit the author's biases.
3. **Parallelism** — multiple Workers can run in parallel (worktrees prevent file clashes).
4. **Maker ≠ checker** — the Worker that writes doesn't verify. A different Worker verifies.
   This is the single highest-value rule for output quality.

## The cast

### Commander (`distill/orchestrator/COMMANDER.md`)
- **vibe**: 鷹眼指揮官 — sees the field, sends orders, reads reports, never leaves the tent.
- Does: BOOT, decompose, dispatch (three-piece set), integrate, verify, update state, report.
- Does NOT: grep whole repo, read 10+ files, batch-edit, self-verify, produce images.
- Exception: S-tier tasks (<5 lines, 1 file, no verify chain) — Commander does directly.

### Workers (`distill/orchestrator/workers/`)

| Worker | vibe | Role | Context |
|--------|------|------|---------|
| Scout | 鷹眼獵人 | Search & research, read-only, reports evidence | Can be same context, read-only tools |
| Builder | 精準工匠 | Implements to spec, edits files, runs build | Fresh or same; never self-verifies |
| Auditor | 找碴者 | Adversarial review, assumes broken | **Fresh context required** |
| Verifier | 鐵面審判官 | Acceptance-criteria read-back, item-by-item | **Fresh context required** |
| Memory Keeper | 圖書管理員 | Distills experience into cold memory | Same context OK |

## The dispatch contract (three-piece set)

Every dispatch MUST include all three (see `distill/orchestrator/DISPATCH_TEMPLATES.md`):

1. **Goal & motivation** — one-line goal, why now, inputs (paths/lines/data).
2. **Acceptance criteria** — 3-5 checkable results, each verifiable by read/grep/exec.
3. **Report format** — conclusion + file:line evidence + unfinished items. No long prose.

Missing any → do not dispatch. The Worker will flail.

## Model dispatch (escalation)

| Situation | Action |
|-----------|--------|
| Small model: tool/syntax error 1× | Upgrade to mid, attach error trace |
| Mid model: same task fails 2× | Upgrade to high, attach full failure trace |
| High model: fails 2× | Stop. `human_required`. Ask human. |
| High model solves a pattern | Template it, hand to cheap model for batch |

Same task, max 2 retry rounds (including model swaps). Then defer or escalate.

## Multi-thinking modes (the Commander switches these)

The Commander states its active mode in output and switches when task character changes:

- **Skeptic** (default) — every claim needs evidence. Analysis, debugging.
- **Architect** — decompose, design. Planning, refactoring scope.
- **Auditor** — find flaws. Verification, completion checks.
- **Devil's Advocate** — argue the opposite. Before declaring done.

See `09-Multi-Thinking-Modes.md`.

## The full flow

```
User request
    │
    ▼
Commander: BOOT → read state → GoalSpec
    │
    ├─ dispatch Scout ──→ Scout reports evidence
    ├─ dispatch Builder ──→ Builder writes code, reports paths
    ├─ dispatch Auditor ──→ Auditor reviews (fresh context), reports issues
    │       └─ if issues ──→ dispatch Builder to fix ──→ re-audit
    ├─ dispatch Verifier ──→ Verifier read-backs (fresh context), PASS/FAIL
    │       └─ if FAIL ──→ dispatch Builder to fix ──→ re-verify
    ├─ dispatch Memory Keeper ──→ distills experience to cold memory
    │
    ▼
Commander: integrate → update loop_state.md → report to user
```

## Deploy-time vs Runtime self-orchestration

Self-orchestration happens **twice**: once at deploy-time (one-shot, deterministic stop)
and once at runtime (recurring, per-task). Both follow the same rule: **the thread that
decides is not the thread that does.**

### 1. Deploy-time (the deployer itself is self-orchestrating)

When a user says `幫恁部署！<this repo's URL>` to any AI tool, the receiving AI becomes a
Commander and the deployer's three stages are its Workers:

| Stage | Worker role | What it does | Fresh context? |
|-------|-------------|--------------|----------------|
| `detect.py` | Scout | Read `registry.json`, run checks per tool, report evidence | n/a (deterministic) |
| `sync.py` | Builder | Build canonical body from `distill/canon/`, write to detected tools, `.bak` first | n/a (deterministic) |
| `verify.py` | Verifier | Read back every written file, confirm marker present, PASS/FAIL | yes (cold read-back) |

The receiving AI (Commander) does NOT write configs itself. It runs the pipeline and
reports the verdict. `distill.py` chains the three stages; the Commander reports the
result with file paths as evidence. **The deploy is a self-orchestrating loop with a
deterministic stop condition: `verify.py` PASS.**

This is why the deploy contract in `AGENTS.md` is short: the Commander's job is to run
the pipeline and report, not to understand the deployer's internals. The deployer is a
tool the Commander dispatches; the Commander does not modify it (Red Line #7).

### 2. Runtime (after deploy, inside each synced tool)

Once the harness is installed, the tool's main conversation becomes a Commander following
`distill/orchestrator/COMMANDER.md`. It dispatches the five Workers (see "The cast" above)
and switches multi-thinking modes (see "Multi-thinking modes" above).

## The self-orchestrating loop, end to end

```
1. Human: "幫恁部署！<url>"
2. Receiving AI (Commander) reads AGENTS.md → runs distill.py
   → detect.py (Scout)   → 7/14 detected, evidence per tool
   → sync.py   (Builder) → 4 files written, 3 deduped, .bak for each
   → verify.py (Verifier) → 7/7 PASS (cold read-back)
3. Commander reports: detected, synced (paths), verify PASS
4. Human opens any synced tool — it is now a Commander (COMMANDER.md loaded)
5. Human gives a task → Commander dispatches Workers → integrates → reports
6. Every iteration: Commander writes loop_state.md (state spine)
7. Task done → Commander dispatches Verifier (fresh context) → PASS → report
8. Commander dispatches Memory Keeper → 1-3 takeaways to cold memory
```

Steps 1-3 are **deploy-time** self-orchestration (one-shot, deterministic stop).
Steps 4-8 are **runtime** self-orchestration (recurring, per-task).

## Why the Commander never works

If the Commander starts grepping and editing, its context fills with file contents and
error logs. By the time it needs to make a judgment, it's lost the big picture. The
discipline: **Commander's context is for decisions, not data.** Workers carry the data;
Commander carries the plan.

## How this maps to different tools

| Tool | How to spawn a Worker |
|------|----------------------|
| Devin | `run_subagent` (explore / general profiles) |
| Claude Code | internal subagent mechanism |
| Antigravity (agy) | internal mechanism / `exec "codex exec ..."` for cross-tool |
| Codex | internal mechanism / `exec "agy -p ..."` for cross-tool |

The canon is tool-agnostic; the dispatch mechanism is tool-specific. The Commander prompt
(`distill/orchestrator/COMMANDER.md`) tells the Commander to use whatever subagent mechanism
its host tool provides.

## Source architecture

The Commander + Workers pattern is a generalized distillation of the masteryee-labs
orchestrator architecture. See [`Docs/REFERENCES.md`](REFERENCES.md) §"Source architecture"
for the full mapping table and kept/dropped comparison.
