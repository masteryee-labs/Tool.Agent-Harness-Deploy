# 13 — Glossary

> Term definitions and source references. Read when a term is unclear.

## Terms

### Harness
The system around an AI model — context management, tools, memory, permissions, workflow,
validation, feedback. The model is the horse; the harness is the bridle/saddle/reins. The
harness doesn't change the model's capability; it determines how that capability is
directed, bounded, and verified.

### Harness Engineering
Designing the harness (not the prompt, not the model). The third layer after Prompt
Engineering and Context Engineering. See `08-Harness-Engineering.md`.

### Caveman (mode)
Token-compressed agent communication. Strip filler words; keep code/paths/errors verbatim.
~65% token reduction. See `05-Caveman-Optimization.md`.

### Commander + Workers
The orchestration pattern: one Commander (main thread) decides/dispatches/integrates; many
Workers (sub-agents) do focused tasks with clean context. See `04-Orchestrator-Design.md`.

### Maker ≠ Checker
The agent that produces output never verifies it. Verification is a separate act by a
fresh-context agent or deterministic CLI. See `distill/canon/VERIFICATION_PROTOCOL.md`.

### Three-layer memory
Hot (`loop_state.md`, <3KB), Knowledge (`knowledge_distill.md`, <8KB), Cold (archive, grep.
The model forgets between runs; the repo doesn't. See `06-Memory-System.md`.

### Loop Engineering
Designing systems where the AI iterates autonomously — prompting itself, verifying,
recording state — until a stop condition. See `distill/canon/LOOP_PROTOCOL.md`.

### Multi-thinking modes
Switching reasoning angles (Skeptic, Architect, Auditor, Devil's Advocate, ...) to
triangulate and cut hallucination. See `09-Multi-Thinking-Modes.md`.

### Gap-scan
Differential blind-spot scan after BOOT. Scans 1-2 scope angles, not all six. See
`distill/skills/gap-scan.md`.

### Harness-sensor
Computational verification sensor — structural/build/syntax checks after code changes. See
`distill/skills/harness-sensor.md`.

### Auditor (skill)
Adversarial seven-angle audit. Run every 5 iterations, after large outputs, before
declaring done. See `distill/skills/auditor.md`.

### Loop-memory (skill)
Three-layer memory read/write. Read at BOOT, write at end of every iteration. See
`distill/skills/loop-memory.md`.

### Judgment rubrics
Externalized decision criteria — each criterion paired with positive/negative examples.
The model matches against the rubric instead of judging subjectively. See
`distill/canon/JUDGMENT_RUBRICS.md`.

### Handoff letter
A letter from past sessions to future sessions. Captures decisions, warnings, and context
that doesn't fit in structured state files. See `distill/canon/HANDOFF_LETTER.md`.

### Using-skills (meta-skill)
Enforces skill-first methodology: before responding to any request, check if a skill
matches and invoke it first. Inspired by obra/superpowers. See
`distill/skills/using-skills.md`.

### Deep-memory (skill)
Hybrid retrieval (BM25 + ChromaDB vector + BGE-Reranker) over `~/.deep-memory/` hot and
cold stores. Ships in-repo at `distill/skills/chroma-hybrid-search/`. See
`06-Memory-System.md`.

### Distill (the pipeline)
detect → sync → verify. The main entry point is `scripts/distill.py`. See
`02-Deployment-Guide.md`.

### Canon
The tool-agnostic source of truth in `distill/canon/`. Every tool's entry file is generated
from it. Edit canon, not entry files.

### Adapter
A thin Python module per tool that knows how to detect the tool and where/how to write its
config. See `03-Tool-Adapters.md`.

### Registry
`adapters/registry.json` — the single source of tool-specific data (detect checks, config
paths, format).

### GoalSpec
A structured task declaration (goal, complexity, scope, subtasks, acceptance criteria)
written to `loop_state.md` at BOOT. Required for L/XL tasks.

### Red lines
Hard stops in `distill/canon/REDLINES.md`. Violating any → stop, ask human.

### Honest clause
The harness explicitly states what it can and cannot do. Can't do → say so, list options,
don't fabricate.

### Heretic (referenced for understanding only)
An open-source project (p-e-w/heretic) that removes an open-source model's refusal concept
via steering-vector surgery. **Agent Harness Deploy does NOT use, bundle, or endorse Heretic for
bypassing safety.** It is referenced here only because the user's source material mentioned
it as part of the interpretability landscape. Agent Harness Deploy is a defensive harness tool: it
configures AI coding assistants, it does not modify model weights or remove safety
guardrails. Understanding steering vectors is useful for harness design (see the emotional
dimension in `08-Harness-Engineering.md`); using them to strip safety is not what this repo
does.

### RIA++
Six-section canonical extraction format for harness concepts (source: kangarooking/cangjie-skill). R = Reading (source quote), I = Interpretation (own words), A1 = Past Application (source cases), A2 = Activation triggers (when to use), A2- = Anti-activation (when NOT to use), B = Boundary (what it doesn't cover). A concept without all six sections will be over- or under-applied. See `distill/canon/HARNESS_ENGINEERING.md`.

### Cognitive angle
A distilled thinking framework (e.g., Munger inversion, Feynman first-principles, Taleb antifragility) that the Commander assigns to a Worker to provide cognitive diversity beyond functional diversity. Workers with different cognitive angles think differently about the same problem, catching blind spots that uniform-thinking workers miss. See `Docs/Agents/nuwa.md`.

### Fresh-context verification
The maker≠checker principle in practice: the agent that produces output never verifies it. A fresh-context agent (no prior investment in the answer) or a CLI tool (deterministic, no bias) does the verification. Prevents confirmation bias and rationalization. See `distill/canon/VERIFICATION_PROTOCOL.md`.

### Idle-yank
When an agent has not produced output or written `loop_state.md` for N consecutive polling intervals, the harness re-injects the GoalSpec and forces a state write. Prevents silent stalls in unattended loops. See `distill/canon/LOOP_PROTOCOL.md`.

## Source references

The concepts in this harness synthesize ideas from many sources. Key ones:

| Concept | Source |
|---------|--------|
| Caveman token optimization | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| Multi-agent agency | msitarzewski/agency-agents |
| Auto-memory | ekcheungai (Threads) |
| Loopkit Vault | govin999999 (Threads) |
| Multi-thinking modes | alchaincyf/nuwa-skill, jacob_cp314 (Threads) |
| Codebase memory | DeusData/codebase-memory-mcp, lawrenceteh_ (Threads) |
| Deep memory | deep-memory pattern (hybrid BM25 + vector + reranker retrieval); implemented in-repo at `distill/skills/chroma-hybrid-search/` |
| Loop Engineering | Addy Osmani, Boris Cherny, Karpathy autoresearch, loops.elorm.xyz |
| Loop kickoff templates | loops.elorm.xyz (kickoff prompt structure) |
| Harness Engineering | OpenAI blog (Ryan Lopopolo), Anthropic Harness Design, Mitchell Hashimoto |
| Harness five dimensions | 温灁?"Harness Engineering — AI 工程師第一維度 |
| 80-word instruction experiment | 控制平面大課題 |
| Control-plane pattern | Ryan Carson, Wisely Chen 見解 |
| CLAUDE.md discipline | Karpathy's CLAUDE.md, Boris Cherny |
| Cross-tool entry sync | Yee-World-Life `.agent/scripts/sync_cross_tool_entries.py` pattern |
| Skills format | Codex/Claude Code SKILL.md convention, obra/superpowers ("Use when..." pattern) |
| Meta-skill enforcement | obra/superpowers `using-superpowers` pattern |
| Worker frontmatter (color/emoji/services) | msitarzewski/agency-agents |
| Judgment externalization | Fable 5 skills discipline (Iwo's Rigor Pack, kpab's Fable-5-native skills) |
| Sub-agent templates | Yee-World-Life `AI_Subagent_Templates.md` v7.6 |

> These sources inspired the design. Agent Harness Deploy is an independent implementation; it does not
> copy their code. Each concept is adapted and cited where relevant in the Docs.
