# Docs/Agents/nuwa.md — 女媧系統 (Nuwa Skill)

> The Nuwa System is a parallel-reasoning verification layer that prevents mock-completion
> errors. Named after 女媧 (Nüwa), the mythological creator who patched the sky — Nuwa
> patches the gaps in a single reasoning thread by running multiple alternative reasoning
> trees in parallel and cross-checking their conclusions.
>
> Origin: proven in the Yee-World-Life project as a skill that catches edge cases,
> dependency conflicts, and regression risks that a single-threaded agent misses. The
> Agent Harness Deploy generalizes it into a tool-agnostic verification skill.

---

## 1. The problem Nuwa solves

A single reasoning thread has blind spots. The agent thinks "this change is safe" because
its reasoning path didn't encounter the edge case, the dependency conflict, or the
regression risk. It's not hallucinating — it's **reasoning incompletely**. The blind spot
is structural: one thread, one path, one conclusion.

**Mock-completion error:** the agent declares "done" based on its single reasoning path,
but an alternative reasoning path would have found a blocker. The agent isn't lying — it
genuinely didn't see the problem. But the problem exists.

**Nuwa's approach:** run 3 parallel alternative reasoning trees, each looking at the
problem from a different angle. If all 3 agree with the primary thread → high confidence.
If any diverges → investigate the divergence before declaring done.

---

## 2. The three parallel reasoning trees

### Tree 1: Edge Case Breaker (邊界破壞者)

| Field | Value |
|-------|-------|
| Question | "What input, state, or condition would break this?" |
| Mindset | Adversarial — actively try to find the breaking case |
| Looks for | Empty inputs, null/undefined, boundary values (0, -1, MAX_INT), concurrent access, race conditions, Unicode/encoding edge cases, timezone/date boundary, permission denied, disk full, network timeout |
| Output | List of edge cases that would break the change, each with: trigger condition + expected failure mode + severity |
| Pass condition | No P0 edge cases found. P1 edge cases documented as known limitations. |

### Tree 2: Dependency Inspector (依賴檢查員)

| Field | Value |
|-------|-------|
| Question | "What else depends on what I'm changing, and will it break?" |
| Mindset | Structural — trace the dependency graph, not the logic |
| Looks for | Import chains, function call sites, type dependencies, config key references, shared state, database schema dependencies, API contract consumers, test dependencies |
| Output | Blast radius map: every file/function that depends on the changed entity, with risk assessment per dependency |
| Pass condition | No critical dependency would break. High-risk dependencies have mitigation plans. |

### Tree 3: Regression Prophet (回歸預言者)

| Field | Value |
|-------|-------|
| Question | "Has this pattern of change caused regressions before? What tests would catch it?" |
| Mindset | Historical — use memory (knowledge_distill.md, deep-memory) to find prior regression patterns |
| Looks for | Similar changes that caused regressions in this project or prior projects, missing test coverage for the changed code path, tests that would need updating, integration tests that might break |
| Output | Regression risk assessment: prior incidents matching this pattern + test coverage gaps + recommended test additions |
| Pass condition | No unmitigated high-risk regression pattern. Test coverage exists for the changed path. |

---

## 3. Physical read-back checks (防止 mock-completion)

The parallel reasoning trees catch **logical** blind spots. Physical read-back checks
catch **mechanical** mock-completion — the agent says "I wrote the file" but the file is
truncated, empty, or missing the critical section.

### Read-back protocol

After any file write, the agent (or a fresh-context Verifier) must:

1. **Read the file back** using a read tool (not the write buffer — the actual disk file).
2. **Check for the canonical marker** — a known string that MUST be present in the file.
   For harness entry files, the marker is `<!-- CANON-BODY-START -->`. For other files,
   the marker is the last line of the intended content.
3. **Check the byte count** — compare actual file size against expected. If the file is
   significantly smaller than expected, it's likely truncated.
4. **Check the last line** — does the file end with the expected final line, or does it
   cut off mid-content?
5. **Report:** "Read-back: PASS (file:line confirmed, N bytes, ends with expected line)"
   or "Read-back: FAIL (truncated at line X, missing Y, Z bytes vs expected W)."

### Why physical read-back matters

Models sometimes report success based on the write buffer, not the disk state. The write
buffer is what the model intended to write. The disk file is what actually got written.
They can differ due to:
- Filesystem errors (disk full, permission denied silently swallowed)
- Encoding issues (UTF-8 BOM, line ending conversion, codepage mismatch)
- Tool truncation (the write tool cut off at a length limit)
- Race conditions (another process modified the file after write)

**The agent's confidence that it wrote the file is NOT evidence that the file is correct
on disk.** Physical read-back is the only reliable check.

---

## 4. Nuwa activation protocol

### When to activate Nuwa

| Trigger | Action |
|---------|--------|
| Before declaring a task "done" | Run all 3 reasoning trees + physical read-back |
| After a large output (5+ files changed) | Run all 3 reasoning trees + physical read-back on every file |
| Before a commit / PR | Run Dependency Inspector + physical read-back |
| When the agent feels confident | Run Edge Case Breaker (confidence is a signal to check for blind spots) |
| Every 5 iterations (with Auditor) | Nuwa runs alongside the Auditor's 7-angle review |

### When NOT to activate Nuwa

| Situation | Reason |
|-----------|--------|
| S-tier task (<5 lines, 1 file, no verify chain) | Overkill — the task is too small for parallel reasoning |
| Read-only exploration (Scout) | No write to verify — Nuwa is for write/complete decisions |
| User explicitly says "just do it" | Respect user intent, but still do physical read-back |

---

## 5. Nuwa execution flow

```
┌─────────────────────────────────────────────────────┐
│  Agent declares "done" (or Commander pre-declare)   │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
     ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
     │ Edge   │  │ Dep    │  │ Reg    │  ← parallel reasoning trees
     │ Case   │  │ Inspect│  │ Prophet│     (fresh context per tree)
     │ Breaker│  │        │  │        │
     └────┬───┘  └────┬───┘  └────┬───┘
          │            │            │
          └────────────┼────────────┘
                       │
              ┌────────▼────────┐
              │  Convergence     │  ← do all 3 agree?
              │  Check           │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  All agree?      │
              │  YES → proceed   │
              │  NO  → investigate divergence │
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  Physical       │  ← read files back from disk
              │  Read-back      │     check markers, byte count, last line
              └────────┬────────┘
                       │
              ┌────────▼────────┐
              │  Read-back PASS? │
              │  YES → declare done │
              │  NO  → re-write + re-check │
              └─────────────────┘
```

---

## 6. Convergence rules

| Tree result | Action |
|-------------|--------|
| All 3 trees: no issues found | High confidence. Proceed to physical read-back. |
| 1 tree: issue found; 2 trees: clean | Investigate the issue. If P0/P1 → fix before declaring done. If P2 → document as known limitation. |
| 2+ trees: issues found | Stop. Do not declare done. Fix issues, re-run Nuwa. |
| Trees disagree on whether something is an issue | The disagreement itself is a finding. Investigate why the trees diverge. The divergence often reveals an ambiguous spec or an unstated assumption. |

---

## 7. Integration with the harness

| Component | How Nuwa integrates |
|-----------|---------------------|
| Commander | Commander dispatches Nuwa as a pre-declaration gate. Nuwa is not a separate worker — it's a verification mode that the Verifier or Auditor worker enters. |
| Verifier | The Verifier runs physical read-back as part of its standard checks. Nuwa's reasoning trees extend the Verifier's scope from "is the file correct?" to "is the change safe?" |
| Auditor | The Auditor's 7-angle review and Nuwa's 3-tree reasoning are complementary. Auditor checks the output; Nuwa checks the blind spots around the output. Run both before declaring done. |
| Memory | The Regression Prophet tree queries `knowledge_distill.md` and deep-memory for prior regression patterns. If a pattern matches, it's a finding. |
| Loop state | Nuwa results are written to `loop_state.md`: "Nuwa: 3 trees run, N issues found (P0:x, P1:y, P2:z), read-back PASS/FAIL." |

---

## 8. Nuwa skill prompt template

When activating Nuwa, the Commander dispatches with this template:

```
Dispatch → Verifier (Nuwa mode)

Goal: Run Nuwa parallel-reasoning verification on the completed task.
Why now: Task is about to be declared done. Pre-declaration gate.
Inputs:
  - GoalSpec + acceptance criteria
  - List of files changed (paths + line numbers)
  - Session transcript (or summary)

Run 3 parallel reasoning trees:

Tree 1 — Edge Case Breaker:
  What input, state, or condition would break this change?
  Check: empty inputs, null/undefined, boundary values, concurrent access,
  encoding edge cases, permission errors, resource exhaustion.

Tree 2 — Dependency Inspector:
  What else depends on what was changed? Will it break?
  Check: import chains, call sites, type dependencies, config references,
  shared state, API consumers, test dependencies.

Tree 3 — Regression Prophet:
  Has this pattern caused regressions before?
  Query: knowledge_distill.md, deep-memory (if available).
  Check: prior incidents, missing test coverage, tests needing updates.

Then: physical read-back on every changed file.
  Read from disk (not write buffer). Check canonical marker, byte count, last line.

Report:
  Tree 1 findings: [P0/P1/P2 edge cases or "none found"]
  Tree 2 findings: [blast radius + risk per dependency or "no critical deps"]
  Tree 3 findings: [regression patterns + coverage gaps or "no patterns match"]
  Convergence: [all agree / divergence on X]
  Read-back: [PASS/FAIL per file with evidence]
  Verdict: [SAFE TO DECLARE DONE / BLOCKED — list blockers]
```

---

## 9. Honest clause

- Nuwa **can** do: find edge cases, trace dependencies, match regression patterns,
  verify files on disk.
- Nuwa **cannot** do: guarantee zero bugs (it reduces blind spots, doesn't eliminate
  them), replace human review for critical changes, verify external system behavior
  (only what's in the repo).
- If all 3 trees find nothing but the agent still feels uncertain → trust the uncertainty.
  Flag for human review. Nuwa reduces false confidence, it doesn't create false alarms.

---

## 10. Relationship to other components

| Component | Relationship |
|-----------|-------------|
| `distill/canon/VERIFICATION_PROTOCOL.md` | Nuwa extends verification from "is the output correct?" to "is the change safe from blind spots?" |
| `distill/skills/auditor.md` | Auditor = adversarial output review. Nuwa = parallel reasoning blind-spot check. Complementary. |
| `distill/canon/JUDGMENT_RUBRICS.md` | R1 (is the task done?) uses Nuwa as a pre-declaration gate. |
| `core/assets/vault/memory_mcp_schema.json` | Regression Prophet tree queries the memory system. |
| `distill/canon/JUDGMENT_RUBRICS.md` | Nuwa results feed into the completion criteria rubric. |

---

*Nuwa is a verification mode, not a separate worker. It runs inside the Verifier or
Auditor worker when the Commander dispatches a pre-declaration gate check. The 3
reasoning trees can run as parallel sub-agents (if the tool supports it) or sequentially
in a single fresh-context agent.*

---

## 11. The two Nuwas

There are two systems that share the Nuwa name. They are complementary, not competing.

| Aspect | Project-internal Nuwa | nuwa-skill (vendored) |
|--------|----------------------|----------------------|
| **What it is** | Parallel-reasoning verification layer | Thinking-framework distillation factory |
| **What it does** | Runs 3 reasoning trees to catch blind spots | Distills anyone's cognitive OS into a Skill |
| **Output** | PASS/BLOCKED verdict + blocker list | `.claude/skills/[person]-perspective/SKILL.md` |
| **Parallelism** | 3 trees (edge/dependency/regression) | 6 research agents (writings/conversations/expression/external/decisions/timeline) |
| **Name origin** | 女媧補天 = patch reasoning blind spots | 女媧造人 = create cognitive clones |
| **Relationship** | Uses cognitive angles to verify | Creates new cognitive angles to use |

The project-internal Nuwa (this file, sections 1-10) provides the verification scaffolding
(3 trees, convergence rules, read-back). nuwa-skill provides the cognitive diversity (new
thinking frameworks to plug into those trees).

---

## 12. nuwa-skill integration: self-distillation + cognitive diversity

**nuwa-skill is vendored** at `core/assets/skills/nuwa-skill/` (anti-link-rot guarantee).
`python scripts/distill.py` copies it into every detected tool's skills directory. Three
pre-distilled perspectives (Munger, Feynman, Taleb) ship with it. Attribution:
`core/assets/skills/nuwa-skill/ATTRIBUTION.md` (upstream: `alchaincyf/nuwa-skill`, MIT).

Users can distill anyone — no install step:
```
> 蒸餾一次芒格         # uses vendored munger-perspective directly
> 使用費曼視角Skill    # uses vendored feynman-perspective directly
> 蒸餾一次Karpathy     # runs the distillation factory to create a new one
```

Each distilled skill becomes a **cognitive angle** the Commander can assign to Nuwa
verification trees.

### Why nuwa-skill fills the cognitive diversity gap

The project's Worker cast has **functional diversity** but no **cognitive diversity** —
all Workers think the same way, just do different things. Fine for mechanical tasks, weak
for judgment-heavy tasks (architecture, risk, strategy).

| Worker | Without nuwa-skill | With cognitive angle |
|--------|-------------------|---------------------|
| Scout | neutral | (neutral — search doesn't need angles) |
| Builder-A | neutral | 芒格逆向思考 — "What would fail first? Invert." |
| Builder-B | neutral | 費曼式第一性原理 — "What's the simplest explanation?" |
| Auditor | assumes broken | 塔勒布反脆弱 — "Is this fragile to tail risks?" |
| Verifier | item-by-item | 波普爾證偽 — "Actively try to disprove" |
| Memory Keeper | neutral | (neutral — distill doesn't need angles) |

This is the **Nuwa Team** — functional roles × cognitive angles = a team where workers
don't just do different things, they **think differently**.

---

## 13. The Nuwa Team architecture

```
User request
    │
    ▼
Commander: BOOT → read state → GoalSpec
    │
    ├─ plan_dispatch.py --analyze
    │     → file ownership map (disjoint sets)
    │     → conflict detection
    │     → Nuwa angle suggestions (edge/dependency/regression)
    │
    ├─ worktree.py create builder-a, builder-b, ...
    │
    ├─ dispatch Scout (functional: search)
    │
    ├─ dispatch Builder-A (functional: build + cognitive: 芒格 逆向)
    │     → works in .worktrees/builder-a/, owns [files-A]
    ├─ dispatch Builder-B (functional: build + cognitive: 費曼 第一性原理)
    │     → works in .worktrees/builder-b/, owns [files-B]
    │     (parallel — no file overlap, no clash)
    │
    ├─ dispatch Auditor (functional: review + cognitive: 塔勒布 反脆弱)
    │     → fresh context, reviews both builders' output
    │
    ├─ dispatch Nuwa verification (3 cognitive angles)
    │     → Tree 1: Edge Case Breaker (functional angle)
    │     → Tree 2: Dependency Inspector (functional angle)
    │     → Tree 3: Regression Prophet (functional angle)
    │     → Extended: 芒格 逆向 + 費曼 簡化 (if user distilled these)
    │
    ├─ worktree.py merge builder-a, builder-b
    ├─ worktree.py clean
    │
    ▼
Commander: integrate → update loop_state.md → report to user
```

---

## 14. How the Commander assigns cognitive angles

### Step 1: Check what perspective skills are installed

Before dispatching, the Commander scans the tool's skills directory:

```bash
# Check for distilled perspective skills
ls .claude/skills/*-perspective/ 2>/dev/null
ls .codex/skills/*-perspective/ 2>/dev/null
ls .devin/skills/*-perspective/ 2>/dev/null
ls .agents/skills/*-perspective/ 2>/dev/null
```

If perspective skills exist, they're available as cognitive angles.

### Step 2: Match angles to subtask character

| Subtask character | Built-in angle | Extended angle (if available) |
|-------------------|---------------|------------------------------|
| Bug fix, input handling | `edge-case` | 費曼 (simplify — what's the minimal case?) |
| Multi-file refactor | `dependency` | 芒格 (invert — what breaks if I'm wrong?) |
| API/contract change | `regression` | 塔勒布 (fragility — what's the tail risk?) |
| Architecture decision | (all 3) | 芒格 + 費曼 + 塔勒布 (full cognitive diversity) |
| Security review | `edge-case` + `dependency` | 波普爾 (falsification — try to break it) |

### Step 3: Inject into Worker dispatch

```
## Cognitive angle (for this task)
Think like 芒格: invert the problem. Don't ask "will this work?" — ask "what would
make this fail catastrophically?" Then check if that failure mode exists.
```

The Worker applies this cognitive frame ON TOP of its functional role. A Builder with
芒格 angle still builds — but it builds with inversion in mind.

---

## 15. Parallel dispatch workflow

### 15.1 Analyze

```bash
# Commander writes subtasks.json, then runs the planner
python scripts/plan_dispatch.py --analyze --subtasks subtasks.json --json
```

Output tells the Commander:
- Which files each Worker owns (disjoint)
- Which files are shared (need serialization)
- Which Nuwa angles apply to each subtask
- How many worktrees to create

### 15.2 Create worktrees

```bash
python scripts/worktree.py create builder-a
python scripts/worktree.py create builder-b
```

### 15.3 Dispatch Workers

The Commander dispatches Builder-A and Builder-B in parallel, each with:
- `owned_files` from the plan
- `worktree_path` pointing to their worktree
- `nuwa_angles` from the plan
- Optional `perspective_skills` if the user has distilled any

### 15.4 Merge

After both Workers report:

```bash
python scripts/worktree.py merge builder-a
python scripts/worktree.py merge builder-b
python scripts/worktree.py clean
```

### 15.5 Verify

The Commander dispatches a Nuwa verification with the suggested cognitive angles.
If perspective skills are installed, they're added as extended angles.

---

## 16. Conflict resolution

When `plan_dispatch.py` detects a file conflict (two subtasks touching the same file):

1. **Serialize** — the first subtask owns the file; the second must wait
2. **Split** — if the file is large, the Commander may split it (rare, needs human approval)
3. **Escalate** — if both subtasks critically need the same file, escalate to human

The `shared_files` field in the dispatch template tells a Worker: "you may NOT edit this
file — report `needs_escalation` if you need to." The Commander then serializes.

---

## 17. When to use the Nuwa Team (and when not to)

### Use it when:
- Multiple Builders need to work in parallel (file ownership prevents clashes)
- The task involves judgment-heavy decisions (cognitive diversity catches blind spots)
- The task is L/XL complexity (worth the overhead of worktree + planning)
- The user has distilled perspective skills and wants cognitive diversity

### Don't use it when:
- S-tier task (<5 lines, 1 file) — just do it directly
- Single Builder, no parallelism — worktree is overhead, skip it
- Mechanical task with no judgment — cognitive angles add noise, not signal
- No perspective skills installed — the 3 built-in angles are sufficient

### The overhead calculation:
- `plan_dispatch.py` analysis: ~2 seconds
- `worktree.py create` per worker: ~1 second
- `worktree.py merge` per worker: ~2 seconds
- Total overhead for 2 parallel Builders: ~8 seconds

This is negligible compared to the cost of file clashes (which can corrupt hours of work).

---

## 18. Nuwa Team relationship to other components

| Component | Relationship |
|-----------|-------------|
| `distill/orchestrator/COMMANDER.md` | The Commander's dispatch workflow includes worktree creation + file ownership + Nuwa angle assignment. |
| `distill/orchestrator/DISPATCH_TEMPLATES.md` | Templates include `owned_files`, `shared_files`, `worktree_path`, `nuwa_angles`, `perspective_skills` fields. |
| `scripts/worktree.py` | Git worktree manager — creates/isolates/merges parallel Worker checkouts. |
| `scripts/plan_dispatch.py` | Pre-dispatch analyzer — file ownership, conflict detection, Nuwa angle suggestions. |
| `core/assets/vault/agency_framework.toml` | The agency framework defines Worker personas. Nuwa Team extends personas with cognitive angles. |
| `core/assets/skills/nuwa-skill/` (vendored) | The distillation factory, vendored from `alchaincyf/nuwa-skill` (MIT). Deployed automatically. See `core/assets/skills/nuwa-skill/ATTRIBUTION.md`. |

---

*The Nuwa Team is functional diversity × cognitive diversity. Workers do different things
AND think differently. Worktrees prevent file clashes. File ownership prevents edit
conflicts. Cognitive angles prevent reasoning blind spots. The result: a team that is
mechanically safe (no clashes) and cognitively diverse (no groupthink).*
