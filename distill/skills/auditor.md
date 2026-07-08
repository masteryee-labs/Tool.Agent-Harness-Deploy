---
name: auditor
description: "Use when 5 iterations have passed, or after a large output (>5 files or >200 lines changed), or before declaring a task complete. Seven-angle adversarial audit to catch self-persuasion blind spots."
---

# Skill: auditor

> Adversarial audit. Run every 5 iterations, after large outputs, and before declaring done.
> Seven-angle audit to catch self-persuasion blind spots.

## Trigger
- Every 5 iterations (mandatory).
- After a large output (>5 files or >200 lines changed).
- Before declaring a task complete.
- Keywords: auditor, adversarial audit, AUDITOR MODE.

## The seven audit angles

1. **Self-persuasion** — did the agent talk itself into "done" without evidence?
2. **Scope creep** — did work exceed what was asked?
3. **Red-line breach** — any `canon/REDLINES.md` line violated?
4. **Unverified claims** — claims stated as fact without file:line evidence?
5. **Fabricated detection** — any "synced"/"found" claim without a tool run?
6. **State drift** — `loop_state.md` not updated last iteration?
7. **Honest-clause violation** — taste/aesthetic decision made without escalating?

## How

For each angle: ask the adversarial question. If yes → P0/P1 finding with evidence.
If no → one-line "clean" note. No angle skipped.

## Output
```
## Audit [CLEAN/ISSUES] iteration:N
## Findings
| angle | severity | evidence | fix |
## Clean angles
- [angle]: clean — [why]
## Escalation needed [yes/no + reason]
```

## Rule
Auditor is fresh-context when possible. If same context, switch to Devil's Advocate mode
explicitly and state it. Same-context audit is weaker — note this in output.
