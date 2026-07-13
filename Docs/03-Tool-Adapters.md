# 03 ??Tool Adapters

> How the deployer talks to each tool. How to add or fix a tool's config location.

## The registry

`adapters/registry.json` is the single source of tool-specific data. Each entry has:

```json
{
  "id": "claude_code",
  "name": "Claude Code",
  "detect": {
    "method": "any",
    "checks": [
      { "type": "command", "value": "claude --version" },
      { "type": "dir", "value": "${HOME}/.claude" }
    ]
  },
  "config": {
    "project_entry": ".claude/CLAUDE.md",
    "global_entry": "${HOME}/.claude/CLAUDE.md",
    "format": "markdown",
    "entry_filename": "CLAUDE.md"
  }
}
```

- **detect.method**: `"any"` (pass if any check passes) or `"all"` (pass if all pass).
- **detect.checks**: list of `command` / `dir` / `file` checks. Paths support `${HOME}`,
  `${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`, `~`.
- **config.project_entry**: where to write the entry file in the project (relative).
- **config.global_entry**: where to write the global entry file (used with `--global`).
- **config.format**: `markdown` (default), `mdc` (Cursor, wraps in YAML frontmatter),
  `json` (Claude Desktop, injects a pointer into existing JSON).

## Supported tools (23)

| Tool | id | Entry file | Format |
|------|----|-----------|--------|
| Claude Code | `claude_code` | `.claude/CLAUDE.md` | markdown |
| Antigravity (AGY) | `antigravity` | `AGENTS.md` | markdown |
| Codex / Codex CLI | `codex` | `.codex/instructions.md` | markdown |
| Devin / Devin CLI | `devin` | `.devin/AGENTS.md` | markdown |
| Cursor | `cursor` | `.cursor/rules/Agent Harness Deploy.mdc` | mdc |
| Claude Desktop | `claude_desktop` | `claude_desktop_config.json` | json |
| OpenCode | `opencode` | `.opencode/AGENTS.md` | markdown |
| OpenClaw | `openclaw` | `.openclaw/AGENTS.md` | markdown |
| Hermes | `hermes` | `.hermes/AGENTS.md` | markdown |
| ZCode | `zcode` | `.zcode/AGENTS.md` | markdown |
| Kimi Code | `kimi_code` | `.kimi-code/AGENTS.md` | markdown |
| AGY CLI | `agy_cli` | `AGENTS.md` (shared) | markdown |
| Codex CLI | `codex_cli` | `.codex/instructions.md` (shared) | markdown |
| Devin CLI | `devin_cli` | `.devin/AGENTS.md` (shared) | markdown |
| Claude Code for VS Code | `claude_code_vscode` | `.claude/CLAUDE.md` (shared) | markdown |
| Codex IDE Extension | `codex_vscode` | `.codex/instructions.md` (shared) | markdown |
| GitHub Copilot | `github_copilot` | `.github/copilot-instructions.md` | markdown |
| Gemini Code Assist | `gemini_code_assist` | `GEMINI.md` | markdown |
| Cline | `cline` | `.clinerules/agent-harness-deploy.md` | markdown |
| Roo Code | `roo_code` | `.roo/rules/agent-harness-deploy.md` | markdown |
| Continue | `continue_dev` | `.continue/rules/agent-harness-deploy.md` | markdown |
| Windsurf | `windsurf` | `.windsurf/rules/agent-harness-deploy.md` | markdown |
| ChatGPT Desktop | `chatgpt_desktop` | `.codex/instructions.md` (shared) | markdown |

> CLI/extension/desktop variants share entry files with their parent tools.
> Sync dedupes by target path, so the file is written once.
>
> **VS Code extension detection**: uses `glob` check type to match extension
> directories (e.g. `anthropic.claude-code-*`) in `~/.vscode/extensions/`.
> **Desktop app detection**: uses `dir` checks on install locations.

## How an adapter works

Each adapter is a thin Python class:

```python
# adapters/claude_code.py
from .base import BaseAdapter

class ClaudeCodeAdapter(BaseAdapter):
    tool_id = "claude_code"

ADAPTER = ClaudeCodeAdapter
```

`BaseAdapter` (`adapters/base.py`) does the real work:
- `detect()` ??runs the registry checks.
- `sync(body, global_too=False)` ??writes the canonical body to the tool's entry file(s).
  - Creates parent dirs.
  - Backs up existing file to `.bak`.
  - Wraps body in frontmatter for `.mdc`, or injects into JSON for Claude Desktop.
- `verify()` ??reads back written files, checks the canonical marker is present.

## Adding a new tool

1. Add an entry to `adapters/registry.json` with the tool's id, name, detect checks, and
   config paths.
2. Create `adapters/<id>.py`:
   ```python
   from .base import BaseAdapter
   class <Name>Adapter(BaseAdapter):
       tool_id = "<id>"
   ADAPTER = <Name>Adapter
   ```
3. Add `"<id>": "<id>"` to `_TOOL_ID_TO_MODULE` in `adapters/__init__.py`.
4. Run `python scripts/detect.py` to confirm detection works.
5. Run `python scripts/distill.py` to sync.

## Fixing a wrong path

If a tool is installed but not detected, the registry path is probably wrong for your
system. Check the tool's actual config location (its docs, or `where <tool>`), update the
`detect.checks` or `config.*_entry` in `registry.json`, and re-run. See `12-Troubleshooting.md`.

## Format handling

| Format | What the adapter does |
|--------|----------------------|
| `markdown` | Write the canonical body as-is. |
| `mdc` (Cursor) | Prepend YAML frontmatter (`description`, `globs`, `alwaysApply: true`), then body. |
| `json` (Claude Desktop) | Read existing JSON (or `{}`), inject a `_Agent Harness Deploy` pointer key. Does NOT dump the full canon body into JSON (it would break the config). |

## Why Claude Desktop is different

Claude Desktop's config is a single JSON file for MCP servers and settings ??not a rules
file. Dumping markdown into it would corrupt it. The adapter injects a small `_Agent Harness Deploy`
pointer instead. The full canon lives in the repo's `distill/canon/` for Claude Desktop
users to reference.
