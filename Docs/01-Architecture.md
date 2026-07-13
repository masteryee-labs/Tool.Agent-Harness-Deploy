# 01 — Architecture

> The full system design. Read if you want to understand or extend the deployer.

## Design goals

1. **One source, many sinks** — a single canonical rule set, translated into each tool's
   native format and location.
2. **Detect, don't guess** — only write to tools that are actually installed.
3. **Non-destructive** — back up before overwrite; never silently clobber existing config.
4. **Self-verifying** — every sync ends with a read-back verification.
5. **Tool-agnostic canon** — the rules don't mention specific tools; adapters handle format.
6. **Dogfooded** — the deployer ships with its own `.agents/` harness using the same canon.

## Layered architecture

```
+-----------------------------------------------------------+
|  distill/canon/         THE source of truth               |
|  (tool-agnostic rules: CORE, BOOT, MEMORY, LOOP, ...)     |
+---------------------------+-------------------------------+
                            |
                            | build_canonical_body()
                            v
+---------------------------+-------------------------------+
|  scripts/sync.py        generates one canonical body      |
+---------------------------+-------------------------------+
                            |
                            | per-tool adapter
                            v
+---------------------------+-------------------------------+
|  adapters/              14 tool adapters + registry       |
|  (claude_code, codex, devin, cursor, ...)                 |
|  Each knows: detect? where to write? what format?         |
+---------------------------+-------------------------------+
                            |
                            | write to native location
                            v
+---------------------------+-------------------------------+
|  Tool native locations  .claude/, .codex/, .devin/,       |
|  AGENTS.md, .cursor/rules/*.mdc, ...                      |
+---------------------------+-------------------------------+
                            |
                            | read-back
                            v
+---------------------------+-------------------------------+
|  scripts/verify.py      confirms marker present           |
+-----------------------------------------------------------+
```

## The three pipeline stages

### 1. Detect (`scripts/detect.py`)
Reads `adapters/registry.json`. For each tool, runs its detection checks (command version,
dir exists, file exists). Returns a list of detected/not-detected with evidence.

**Sacred rule**: a tool not detected is a tool not synced. No fabrication.

### 2. Sync (`scripts/sync.py`)
Concatenates `distill/canon/*.md` in defined order into one canonical body. For each
detected tool, the adapter writes the body to the tool's native entry file. Dedupes by
target path (so AGY CLI + Antigravity don't write `AGENTS.md` twice). Backs up existing
files to `.bak` before overwriting.

### 3. Verify (`scripts/verify.py`)
Reads back every written file. Confirms the canonical marker is present. Reports PASS/FAIL
per file. A sync that skips verify is a failed sync.

## The orchestrator (runtime, not deploy-time)

Once the harness is installed in a tool, that tool's main conversation becomes a
**Commander** (`distill/orchestrator/COMMANDER.md`). It dispatches focused sub-tasks to
**Workers** (`distill/orchestrator/workers/`):

| Worker | Role |
|--------|------|
| Scout | Search & research (read-only) |
| Builder | Implementation (edits files) |
| Auditor | Adversarial review (fresh context) |
| Verifier | Acceptance-criteria read-back (fresh context) |
| Memory Keeper | Distill experience into cold memory |

The Commander never works — it decides, dispatches, integrates, verifies. This is the
"AI prompts itself" pattern: one orchestrator + many doers.

## The canon (what gets synced)

| Canon file | Purpose |
|------------|---------|
| `CORE_CANON.md` | Identity, principles, what this harness optimizes for |
| `REDLINES.md` | Hard stops — violating → ask human |
| `BOOT_PROTOCOL.md` | Startup sequence (order mandatory) |
| `MEMORY_PROTOCOL.md` | Three-layer memory + optional deep-memory |
| `LOOP_PROTOCOL.md` | Convergent iteration with stop conditions |
| `VERIFICATION_PROTOCOL.md` | Maker ≠ checker, circuit breakers |
| `CAVEMAN_PROTOCOL.md` | Token compression communication style |

## Extension points

- **Add a tool**: add an entry to `adapters/registry.json` + a thin adapter module. See
  `03-Tool-Adapters.md`.
- **Change the rules**: edit `distill/canon/*.md`, then run `python scripts/sync.py --canon`
  to regenerate the repo's `AGENTS.md` canon body, and re-run `distill.py` to push to tools.
- **Add a skill**: drop a `.md` into `distill/skills/`. Skills are loaded on demand by the
  orchestrator.

## Why this design

- **Decoupled**: canon doesn't know about tools; tools don't know about canon. Adapters bridge.
- **Idempotent**: running `distill.py` twice produces the same result (dedupe + backup).
- **Auditable**: every write has a path; every verify has evidence; detection has evidence.
- **Reversible**: `.bak` files let you roll back any sync.
