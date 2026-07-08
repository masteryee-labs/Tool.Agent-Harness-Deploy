---
name: loop-memory
description: "Use when BOOTing a session (read hot + knowledge layers) or at the end of every iteration (write hot layer). Keeps state persistent across runs — the model forgets, the repo doesn't."
---

# Skill: loop-memory

> Thin wrapper over `../canon/MEMORY_PROTOCOL.md`. Read at BOOT, write at end of every iteration.
> The model forgets; the repo doesn't.

## Trigger
- BOOT: read hot + knowledge layers.
- End of every iteration: write hot layer.
- Keywords: update memory, loop_state, iteration end, distill.

## What to do

Follow `../canon/MEMORY_PROTOCOL.md` for the full three-layer spec. Quick reference:

| Action | Rule |
|--------|------|
| Read at BOOT | `.agent/loop_state.md` (<3KB) + `.agent/knowledge_distill.md` (<8KB) |
| Write every iteration | Update `.agent/loop_state.md` with: date, phase, last_action, active GoalSpec, subtasks, deferred/human_required, memory flags |
| Distill when >8KB | Merge duplicate anti-patterns, abstract concrete cases into patterns, archive originals to `loop_state_archive.md`. Dispatch Memory Keeper if judgment needed. |
| Cold layer | Append-only. Never edit; only archive. |
| Secrets | Never write secrets/keys/API tokens to any layer. |
| Skipping write | Red line #7 (canon). |

## Optional: deep-memory

If `~/.deep-memory/.venv` exists, run cross-project retrieval via `chroma-hybrid-search` skill.
If not, set `deep_memory_offline: true` in loop_state. Do not fabricate memory.
