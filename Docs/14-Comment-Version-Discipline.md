# 14 — Comment & Version Discipline: CLI Tool Integration Evaluation

> Evaluates open-source CLI tools for detecting/removing AI-generated comment slop and
> in-file version stacking. Proposes an integration plan for the Agent Harness Deploy
> sensor fleet.
>
> Related canon: `distill/canon/REDLINES.md` #16 (no explanatory comments) + #17 (no
> in-file version stacking), `distill/canon/CORE_CANON.md` §3 (Comment/Version discipline),
> `distill/canon/VERIFICATION_PROTOCOL.md` AI slop sensor (Explanation bloat + Version
> stacking axes).
>
> Related skills: `distill/skills/comment_checker.md` (prompt-level), `slop-detector.md`
> (prose/naming), `harness-sensor.md` (Q3 computational sensor).

---

## 1. The problem

AI coding assistants produce two persistent forms of slop that survive in the repo:

1. **Explanation bloat** — comments that restate the code (`# loop through items` above
   `for x in items:`). Zero information, wastes tokens, rots when code changes. Research:
   arXiv 2605.02741 (Volume-Quality Inverse Law — comment bloat predicts structural
   decay); arXiv 2512.20334 (Comment Traps — commented-out/defective comments propagate
   defects at up to 58%).

2. **Version stacking** — in-file version markers accumulated across edits (`<!-- v2 -->`,
   `# v3 fixed X`, `<!-- updated 2026-07-15 -->`). Context rot (arXiv 2606.09090) and
   recursive-depth debt. Version truth should live in git + `CHANGELOG.md`, never in-file.

The harness already has **prompt-level** coverage (`comment_checker` skill, REDLINES #16/#17,
CORE_CANON Comment/Version discipline). This doc evaluates **computational (Q3) CLI tools**
that can run deterministically in CI / pre-commit / `verify.py` to catch what prompts miss.

---

## 2. Evaluated tools

| Tool | Repo | Approach | Languages | Accuracy | Auto-fix? | Pre-commit? |
|------|------|----------|-----------|----------|-----------|-------------|
| **uncomment** | [goldziher/uncomment](https://github.com/goldziher/uncomment) | tree-sitter AST | 306 | 100% (AST, no false positives in strings) | dry-run + write | yes |
| **nocmt** | [2mawi2/nocmt](https://github.com/2mawi2/nocmt) | regex, language-aware | Go, JS, TS, Python, Rust, etc. | high (regex-based, rare edge cases) | writes (staged-only mode) | yes (install hook) |
| **llmstrip** | [HugoLopes45/llmstrip](https://github.com/HugoLopes45/llmstrip) | 34 rules (regex + structural) | code + prose + commits | high (catches structural patterns regex misses) | `--report --fail` (CI mode) | yes |
| **llm-lint** | [JadenRazo/llm-lint](https://github.com/JadenRazo/llm-lint) | rule scanner (LLM001-015) | any (pattern-based) | medium (broad artifacts, not comment-specific) | auto-fix + `git rm --cached` | yes (CI) |
| **devibe** | [nHunter0/devibe](https://github.com/nHunter0/devibe) | Python lib, pattern rules | any (text-based) | medium (emoji, status prefix, placeholder) | library API | no (library) |
| **pystrip** | [pystrip/pystrip](https://github.com/pystrip/pystrip) | libcst (Python only) | Python | 100% (CST) | `--check` (CI) + write | yes |

### 2.1 Strengths/weaknesses summary

| Tool | Best for | Weakness |
|------|----------|----------|
| **uncomment** | AST-precise comment removal across 306 languages | No AI-specific pattern detection (catches *all* comments, not just slop) |
| **nocmt** | Cleaning AI comments from git-staged changes only | Regex-based → edge cases in strings/regex literals; no AST |
| **llmstrip** | Detecting LLM writing patterns (structural, not just regex) | Binary may need build; 34 rules are prose-oriented, less code-comment-focused |
| **llm-lint** | CI gate for LLM artifacts (CLAUDE.md, Co-authored-by, refusal text) | Not comment-quality focused; broader artifact scanning |
| **devibe** | Emoji/status-prefix/placeholder cleanup | Library only, no CLI; limited language coverage |
| **pystrip** | Python-only precise comment/docstring removal | Python only; removes *all* comments, not just slop |

### 2.2 Key gap across all tools

**None of these tools detect version stacking** (`<!-- v2 -->`, `# v3 fixed X`). This is a
gap the Agent Harness Deploy harness fills with its own `scripts/sync.py` guard
(`check_canon_version_stacking()`). The CLI tools complement but do not replace this.

---

## 3. Integration plan

### 3.1 Design principles (from canon)

- **Maker ≠ checker** (VERIFICATION_PROTOCOL.md): CLI sensors are Q3 computational — they
  report, they don't auto-fix by default. Auto-fix risks deleting intentional comments.
- **Report-first** (honest clause): sensors output findings + fix instructions. Human or
  agent decides whether to act.
- **Sensor output = fix instructions** (VERIFICATION_PROTOCOL.md): every finding must
  include a specific fix, not just "ERROR."
- **No gold-plating**: integrate the minimum that covers the gap. Don't vendor 6 tools
  when 2 cover 90% of cases.

### 3.2 Recommended stack

| Layer | Tool | Role | When |
|-------|------|------|------|
| **Primary detector** | `uncomment --dry-run` | AST-precise comment inventory (what exists, where) | `harness-sensor` SENSOR-4 in `code` mode |
| **AI-pattern detector** | `llmstrip --report --mode code` | Catch LLM structural patterns regex/AST miss | `harness-sensor` SENSOR-4 supplement |
| **Version stacking** | `scripts/sync.py` guard (already built) | Reject canon files with stacked version markers | pre-sync gate (already active) |
| **Prompt-level** | `comment_checker` skill (already exists) | Agent self-check before declaring done | after code edits |

### 3.3 What NOT to integrate (and why)

| Tool | Why not |
|------|---------|
| **nocmt** (auto-strip) | Auto-stripping staged comments risks deleting intentional ones. `uncomment --dry-run` covers detection; auto-fix should be agent-mediated, not silent. |
| **llm-lint** | Focuses on LLM *artifacts* (CLAUDE.md, Co-authored-by), not comment quality. Out of scope for this problem. |
| **devibe** | Library only, no CLI. Emoji/status-prefix cleanup is niche. `comment_checker` skill already covers this at prompt level. |
| **pystrip** | Python only, removes *all* comments. Too aggressive for a multi-language harness. |

### 3.4 Integration approach (phased)

#### Phase 1: Detection only (no auto-fix) — IMPLEMENTED

Added to `harness-sensor` skill (`distill/skills/harness-sensor.md`):

```
### SENSOR-4b: Comment slop (code mode, if uncomment available)
- Run: `uncomment --dry-run <changed_files>`
- Report: comment count per file, lines with comments
- Cross-reference with comment_checker skill output
- Flag: comments that restate code (explanation bloat)
- Fix instruction: "Delete comment at line N — it restates the code. See REDLINES.md #16."
```

```
### SENSOR-4c: LLM pattern (code mode, if llmstrip available)
- Run: `llmstrip --report --mode code <changed_files>`
- Report: LLM boilerplate patterns found
- Fix instruction: per-finding fix from llmstrip output
```

**Graceful degradation**: if `uncomment` or `llmstrip` are not installed, SENSOR-4b/4c
report "tool not installed — skipping (install uncomment/llmstrip for Q3 comment slop
detection)" and fall back to prompt-level `comment_checker` skill only. The harness never
*requires* external tools — it uses them when available.

#### Phase 2: CI gate (optional, project-specific)

For projects that want CI enforcement:

```yaml
# .github/workflows/comment-discipline.yml
- name: Comment slop check
  run: |
    uncomment --dry-run --check src/ || echo "Comment slop detected — see report"
    llmstrip --report --fail --mode code src/ || exit 1
```

This is opt-in per project, not part of the default harness deploy. The canon
(REDLINES #16/#17) is the default; CI gates are project-specific hardening.

#### Phase 3: Pre-commit hook (optional, user opt-in)

```bash
# .git/hooks/pre-commit (or via pre-commit framework)
uncomment --dry-run --check $(git diff --cached --name-only --diff-filter=ACM)
```

Only for users who explicitly request it. The deployer does not auto-install
pre-commit hooks for comment stripping — that's a project-level decision.

---

## 4. False-positive risk assessment

| Tool | False-positive risk | Mitigation |
|------|---------------------|------------|
| **uncomment** | Low — AST-precise, won't touch strings. But it flags *all* comments, not just slop. | Use `--dry-run` for reporting; agent/human decides what to delete. Never auto-strip. |
| **llmstrip** | Low-medium — 34 rules are well-tested but may flag legitimate prose in docstrings. | `--report` mode only; review before acting. |
| **sync.py guard** | Very low — code-span stripping prevents matching examples in rule descriptions. Tested: 0 false positives on current canon. | Already mitigated via `_strip_code_spans()`. |

---

## 5. Decision

| Question | Answer |
|----------|--------|
| Integrate CLI tools into default deploy? | **No.** Canon (REDLINES #16/#17) + `comment_checker` skill cover prompt-level. CLI tools are opt-in per project. |
| Which tools to recommend? | `uncomment` (AST detection) + `llmstrip` (LLM pattern detection). |
| Auto-fix by default? | **No.** Report-first. Agent or human decides. Maker ≠ checker. |
| Version stacking tool? | Already built: `scripts/sync.py` `check_canon_version_stacking()`. No external tool needed. |
| When to revisit? | When a tool adds version-stacking detection (currently none do). Or when `uncomment` adds AI-specific filtering (currently removes all comments, not just slop). |

---

## 6. Research references

| Paper | Key finding | Relevance |
|-------|-------------|-----------|
| arXiv 2605.02741 — AI-Generated Smells | Volume-Quality Inverse Law: code volume predicts structural decay | Comment bloat = volume bloat = decay |
| arXiv 2512.20334 — Comment Traps | Defective commented-out code propagates defects at 58% | Comments are not just noise — they're defect vectors |
| arXiv 2606.09090 — Context Rot | 23% of repos have stale AI config references | Version stacking = in-file context rot |
| IEEE SW 2026 — AI Slop | Reviewers develop pattern recognition for AI comments (emojis, hedging) | Validates slop sensor approach |
| arXiv 2505.09021 — AI-Mediated Comment Improvement | LLM can rewrite comments along quality axes | Future: comment *improvement*, not just deletion |
| arXiv 2506.14649 — IsComment | Issue-based RAG for comment generation, reduces hallucination | Future: context-aware comment generation |

---

*This doc is evaluation-only. The canon changes (REDLINES #16/#17, CORE_CANON Comment/Version
discipline, VERIFICATION slop axes) are the active enforcement. CLI integration is opt-in per
project via `harness-sensor` SENSOR-4b/4c with graceful degradation.*
