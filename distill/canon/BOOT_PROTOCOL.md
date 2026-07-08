# BOOT Protocol — Startup Sequence

> Order is mandatory. Do not skip or reorder. Total BOOT payload target: <16KB.

---

## Sequence

1. **Read entry file** — the file that brought you here (AGENTS.md / CLAUDE.md /
   instructions.md / .devin/AGENTS.md). It routes you to canon.
2. **Read hot layer** — `.agent/loop_state.md` (<3KB). Inherits prior state.
3. **Read knowledge layer** — `.agent/knowledge_distill.md` (<8KB). Anti-patterns.
4. **Read deploy guide** — `Docs/02-Deployment-Guide.md` (only if deploying).
5. **Output GoalSpec** — write to `loop_state.md`:
   ```yaml
   goal: "[one-line summary]"
   complexity: "S|M|L|XL"
   scope:
     angles_required: ["angle1", "angle2"]
     files_to_check: ["path1", "path2"]
     sensor_mode: "code" | "doc"
   subtasks: []  # L/XL required
   acceptance_criteria: []
   human_in_loop_triggers: []
   estimated_iterations: N
   ```
6. **Deep-memory check** (optional) — if `~/.deep-memory/.venv` exists, run retrieval.
   If not, set `deep_memory_offline: true`. Do not fabricate memory.
7. **Differential gap-scan** — scan 1-2 scope angles only. See `../skills/gap-scan.md`.

## Rules

- Do NOT read all Docs at BOOT. Load on demand via the index in `Docs/00-Overview.md`.
- Do NOT read full `context.md` if a quick-lookup variant exists.
- Do NOT start work without a GoalSpec for L/XL tasks.
- BOOT is for orientation. Work happens after.

## Multi-thinking mode activation

At BOOT, activate the default thinking mode set (see `Docs/09-Multi-Thinking-Modes.md`):
- **Skeptic** — default. Every claim needs evidence.
- **Architect** — for planning/decomposition tasks.
- **Auditor** — for verification/completion tasks.

Switch modes explicitly when the task changes character. State the active mode in output.

## Rule placement (Lost in the Middle)

> See `HARNESS_ENGINEERING.md §Rule placement and attention management` for the full principle.
> Short version: critical rules go at the top of the entry file (first 30 lines = "golden
> position"). Rules buried at line 300 of a 600-line file are effectively unwritten.
