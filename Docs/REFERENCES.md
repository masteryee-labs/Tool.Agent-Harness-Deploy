# Reference Links

Source references for the 5 pillars of Agent Harness Deploy.

### Pillar 1 — Caveman token compression
- https://vocus.cc/article/6a10254ffd897800017eaac1
- https://www.reddit.com/r/ClaudeAI/comments/1sble09/taught_claude_to_talk_like_a_caveman_to_use_75/
- https://github.com/JuliusBrussee/caveman
- https://github.com/cheeseonamonkey/Lean-Caveman-originall-
- https://github.com/JuliusBrussee/caveman-code

### Pillar 2 — Commander-Worker hierarchy
- https://github.com/msitarzewski/agency-agents
- https://www.threads.com/@krumjahn/post/DaZuvrPm6Fw
- https://substack.com/@rumjahn
- https://github.com/obra/superpowers

### Pillar 3 — Loop engineering + Vault control
- https://loops.elorm.xyz/
- https://www.threads.com/@govin999999/post/DaXprW2GFbT
- https://www.threads.com/@govin999999/post/DZwNh9oGC-l
- https://www.threads.com/@aiposthub/post/DZpiC-FAWZR
- https://www.threads.com/@noktvng/post/DZuYFVWDw_E

### Pillar 4 — Deep repo memory
- https://github.com/DeusData/codebase-memory-mcp
- https://github.com/kevintsai1202/deep-memory
- https://kevintsai1202.github.io/deep-memory/
- https://www.threads.com/@ekcheungai/post/DaZ8cfjjHUP
- https://www.threads.com/@lawrenceteh_/post/DaPtdrBCNdO
- https://www.threads.com/@cai.chengkai/post/DaVIELxEni9
- https://www.threads.com/@jsfiend32/post/DaTUVldEzIL

### Pillar 5 — Sandbox boundary realignment
- https://github.com/p-e-w/heretic
- https://www.threads.com/@ray.realms/post/DZkWgzXgQZQ

### Vault asset sources
- https://github.com/usestrix/strix
- https://github.com/safishamsi/graphify

---

## Source architecture — masteryee-labs `Docs/Agents/`

The Commander + Workers pattern in Agent Harness Deploy is a generalized, tool-agnostic
distillation of the orchestrator architecture used in the masteryee-labs project.

| Subdirectory | Role | Agent Harness Deploy equivalent |
|--------------|------|---------------------|
| `指揮官Orchestrator_Prompt.md` | Dual-pipeline commander: BOOT → dependency graph → wave dispatch → verify → checkpoint | `distill/orchestrator/COMMANDER.md` + `DISPATCH_TEMPLATES.md` |
| `指揮官Bug_Fixer_Agent_Prompt.md` | Focused fixer worker | `workers/BUILDER.md` |
| `指揮官Agy_QA_Agent_Prompt.md` | Independent QA dispatcher | `workers/AUDITOR.md` + `workers/VERIFIER.md` |
| `故事寫/Story_Session_Prompts/*.md` | Per-session task prompts (one file = one Worker task) | `DISPATCH_TEMPLATES.md` (the fill-in templates that generate per-task prompts) |
| `遊戲QA/QA_Session_Prompts/*.md` | Per-system QA sub-prompts | `workers/VERIFIER.md` (acceptance-criteria checklists) |
| `Docs/Agents/README.md` | "These are human-authored prompt specs, not AI slop" | `distill/orchestrator/` is the same: human-authored, canon-protected |

**Kept** (the load-bearing ideas): Commander never works; three-piece dispatch; maker ≠ checker; state on disk; model escalation; recovery mode.

**Dropped** (project-specific): hardcoded session dependency graph; tool-specific dispatch mechanisms; concurrency caps and rate-limit workarounds.

The masteryee-labs orchestrator is a specific, large-scale instance (153 sessions, dual pipeline). Agent Harness Deploy is the general, portable core.

### Orchestrator source references
- masteryee-labs `Docs/Agents/` — the reference architecture (指揮官 / 故事寫 / 遊戲QA / 圖書管理員)
- msitarzewski/agency-agents — independent agents with distinct personalities (the "vibe" + frontmatter pattern)
- OpenAI "Harness Engineering" / Anthropic "Harness Design" — commander-never-works and maker/checker separation
- Karpathy / Boris Cherny — "humans steer, agents execute"; loops where the AI prompts, verifies, and records state itself
