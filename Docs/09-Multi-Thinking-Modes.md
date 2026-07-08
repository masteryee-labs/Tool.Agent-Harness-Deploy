# 09 ??Multi-Thinking Modes

> Switch thinking angles to cut hallucination. One perspective blinds; several triangulate.
> Inspired by alchaincyf/nuwa-skill and jacob_cp314 Threads.

## The problem

A model reasoning in one mode develops blind spots specific to that mode. The Skeptic
catches unverified claims but misses structural opportunities. The Architect sees structure
but skips evidence checks. The Auditor finds flaws but won't propose alternatives.

Single-mode reasoning is like looking through one eye ??no depth perception. The fix:
**deliberately switch modes** and state which is active. Different angles catch different
blind spots. Triangulation reduces hallucination.

## The modes

| Mode | Question it asks | Use when |
|------|------------------|----------|
| Skeptic (default) | "Where's the evidence?" | Analysis, debugging, evaluating claims |
| Architect | "How does this decompose?" | Planning, refactoring scope, system design |
| Auditor | "What's wrong here?" | Verification, completion checks, review |
| Devil's Advocate | "What's the strongest case against?" | Before declaring done, before a risky commit |
| Scout | "What's out there?" | Exploration, research, mapping unknowns |
| Builder | "How do I make this?" | Implementation, construction |

## How to use

The Commander states its active mode in output and switches when the task character
changes. Example:

```
[mode: Architect] Decomposing the sync bug into 3 subtasks...
[mode: Skeptic] Verifying each subtask has acceptance criteria with evidence...
[mode: Devil's Advocate] Before declaring done: what if the dedupe key is case-sensitive on Windows?
```

## Why it reduces hallucination

Hallucination often comes from **mode-lock** ??the model commits to one framing and
generates confident-sounding content within it, even when the framing is wrong. Forcing a
mode switch breaks the lock:

- After Architect proposes a plan ??switch to Devil's Advocate to attack it.
- After Builder writes code ??switch to Auditor to find flaws.
- After Skeptic verifies claims ??switch to Scout to check for unconsidered alternatives.

Each switch is a fresh pass with a different question. Hallucinations that survive one mode
rarely survive all.

## The nuwa-skill approach

The nuwa-skill (alchaincyf) formalizes this as a skill: a structured prompt that cycles
through thinking modes and integrates their outputs. The Agent Harness Deploy harness adopts the same
principle but lighter ??modes are stated in-line, not a separate skill invocation, to keep
context lean.

## Mode + multi-agent

The strongest combination: **different agents in different modes.** The Commander runs in
Architect mode to decompose. A Scout worker runs in Scout mode to map. An Auditor worker
runs in Auditor mode (fresh context) to review. A Verifier worker runs in Skeptic mode to
check acceptance. Cross-agent + cross-mode catches what same-agent same-mode misses.

## When NOT to switch

- Trivial tasks (S-tier) ??one mode is fine. Switching adds overhead.
- When the task is genuinely single-faceted (e.g., "update the date in a file").
- Mid-sentence. Switch between turns or sub-tasks, not mid-thought.

## Anti-patterns

- **Mode theater** ??stating a mode but not actually applying its question. If you say
  "Devil's Advocate" but don't raise the strongest objection, it's decoration.
- **Mode lock** ??staying in one mode for an entire complex task. Switch when character
  changes.
- **Mode as excuse** ??"I'm in Builder mode, I don't need to verify." No. Builder mode
  means you build; verification is a separate step regardless of mode.

## Implementation in this harness

- `distill/canon/BOOT_PROTOCOL.md` ??activates default mode set (Skeptic/Architect/Auditor)
  at BOOT.
- `distill/orchestrator/COMMANDER.md` ??Commander switches modes and states them.
- `distill/orchestrator/workers/AUDITOR.md` ??Auditor runs all three lenses (Skeptic,
  Devil's Advocate, Auditor) on output.
- `distill/skills/auditor.md` ??the seven-angle audit is a multi-mode sweep.

## Source references

- alchaincyf/nuwa-skill ??multi-thinking skill framework.
- jacob_cp314 Threads ??multi-thinking mode concept.
- The general principle: triangulation beats single-perspective reasoning for hallucination
  reduction.
