---
name: harness-sensor
description: "Use when code or files have been modified. Runs structural, build, and syntax checks deterministically. Code changes trigger full sensor; doc-only changes trigger SENSOR-3 only."
---

# Skill: harness-sensor

> Computational verification sensor. Run after code/file changes.
> Two modes: `code` (full sensor) / `doc` (SENSOR-3 only).
> Implements Q3 computational sensors per `distill/canon/HARNESS_ENGINEERING.md` and CLI gates per `distill/canon/VERIFICATION_PROTOCOL.md`.
> Every failure output must include `Fix: <specific action>` as the last line.

## Trigger
- After any code modification → `code` mode.
- After pure doc/markdown modification → `doc` mode.
- Keywords: harness-sensor, build check, sensor PASS.

## Sensors

### SENSOR-1: Structure (code mode)
- Files claimed changed actually exist at claimed paths.
- `read` each changed file, confirm content present.
- Fail → report path + what's missing.

### SENSOR-2: Build (code mode)
- Run the project's build/typecheck/lint command.
- Pass = green. Fail = report error verbatim + failing file:line.
- If no build system → skip with note "no build system."

### SENSOR-3: Syntax/links (both modes)
- Markdown: check internal links resolve, code fences balanced, headers well-formed.
- Code: syntax check (parse-only if no full build).
- Config files: valid JSON/YAML/TOML parse.

### SENSOR-4: SLOP (doc mode + code report)
- Run `slop-detector` on user-facing prose, naming, and abstractions in the changed set.
- Flag generic names, filler phrases, single-call wrappers, premature interfaces.

## Output
```
## Sensor [PASS/FAIL] mode:[code/doc]
## SENSOR-1 structure: [pass/fail] — evidence
## SENSOR-2 build: [pass/fail/n-a] — command + result
## SENSOR-3 syntax: [pass/fail] — evidence
## SENSOR-4 slop: [pass/fail] — count
## Failures
- sensor | file:line | issue | fix
Fix: <specific action>
```

## Rules
- Sensor is deterministic. It runs commands. It does not "feel" correctness.
- A sensor FAIL stops the loop. Fix before next iteration.
- Sensor does not replace fresh-context Verifier. Sensor = structural; Verifier = semantic.
- If SENSOR-4 fails, the next iteration should fix the SLOP before moving on.
