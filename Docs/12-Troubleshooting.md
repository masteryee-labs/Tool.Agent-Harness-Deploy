# 12 ??Troubleshooting

> Common issues and fixes. Check here before escalating.

## Detection issues

### "My tool is installed but not detected"

The registry's detection checks are best-effort. They check common install locations and
`<tool> --version`. If your install is unusual, detection may miss it.

**Fix:**
1. Run `python scripts/detect.py --json` to see what evidence each check produced.
2. Find your tool's actual config location (its docs, or `where <tool>` / `which <tool>`).
3. Edit `adapters/registry.json` ??update the `detect.checks` for your tool to match your
   system. Paths support `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`, `~`.
4. Re-run `python scripts/detect.py` to confirm detection.
5. Re-run `python scripts/distill.py` to sync.

### "A tool I don't want is being detected"

**Fix:** Use `--tools` to sync only what you want:
```bash
python scripts/distill.py --tools claude_code,codex
```

Or remove the tool's entry from `adapters/registry.json` if you never want it.

### "Detection says `rc=1` for a command I know works"

Some CLI tools return non-zero from `--version` on certain platforms, or write to stderr.
The check treats non-zero as "not detected."

**Fix:** Add a `dir` or `file` check for that tool's config directory as an alternative.
The `method: "any"` setting means any passing check counts.

## Sync issues

### "Old deploy polluted my global MCP config"

Old versions of Agent Harness Deploy (before the scope fix) wrote to global MCP files
even without `--global`, affecting Claude Desktop, Cline, Roo Code, and Windsurf.

**Fix:** The deployer now auto-cleans this on every run (Step 0). Just update the repo
and re-deploy:
```bash
git pull
python scripts/distill.py
```

If the auto-cleanup reports "unsafe skip" (you added MCP servers after the old deploy),
review manually:
```bash
python scripts/migrate.py --report    # see what needs attention
```

To force-restore from `.bak` (destructive — overwrites current with backup):
```bash
python scripts/migrate.py --restore
```

### "Sync wrote to the wrong path"

The registry's `config.project_entry` or `config.global_entry` is wrong for your setup.

**Fix:** Edit `adapters/registry.json` ??`config` for that tool. Re-run sync. The old
wrong file will have a `.bak`; clean it up manually if needed.

### "Sync failed with a permission error"

The target path is read-only or owned by another user.

**Fix:** Check permissions on the target directory. On Windows, make sure the file isn't
open in another program. On macOS/Linux, check ownership and `chmod`.

### "Sync overwrote my custom rules!"

It shouldn't have ??sync backs up to `.bak` first. But if you ran sync and your custom
rules are gone:

**Fix:** Restore from the `.bak`:
```bash
mv .claude/CLAUDE.md.bak .claude/CLAUDE.md   # example for Claude Code
```

Then, to keep your custom rules *and* the Agent Harness Deploy harness, merge them: put your custom
rules in a separate file that the tool reads, or append them to the canon-generated entry
(but note: re-running sync will overwrite the entry again ??better to add custom rules to
`distill/canon/` so they survive re-syncs).

### "Cursor .mdc file has wrong frontmatter"

Cursor's `.mdc` format requires specific frontmatter fields. The adapter generates:
```yaml
---
description: Agent Harness Deploy harness rules
globs: **/*
alwaysApply: true
---
```
If your Cursor version needs different fields, edit `adapters/base.py` `_wrap_mdc()`.

## Verification issues

### "Verify FAILS ??marker missing"

The canonical body should contain "Agent Harness Deploy." If verify says marker missing:
1. Check the file actually exists at the reported path.
2. Open it ??is it empty or truncated? (Sync may have been interrupted.)
3. Re-run `python scripts/sync.py --tools <that_tool>` and re-verify.

### "Verify passes but the tool doesn't follow the rules"

The tool may not auto-load its entry file, or may need a restart.

**Fix:**
- Claude Code: restart the session (it reads CLAUDE.md at session start).
- Codex: restart the CLI.
- Cursor: the `.mdc` with `alwaysApply: true` should load automatically; if not, check
  Cursor's rules settings.
- Devin: restart.

## Python issues

### "python: command not found"

Install Python 3.9+ from python.org, or use `py` (Windows launcher):
```bash
py scripts/distill.py
```

### "ModuleNotFoundError: No module named 'adapters'"

You're running from the wrong directory. The scripts expect to run from the repo root:
```bash
cd /path/to/Tool.Agent-Harness-Deploy
python scripts/distill.py
```

### "JSON parse error in registry.json"

You edited `registry.json` and broke the syntax. Validate it:
```bash
python -c "import json; json.load(open('adapters/registry.json', encoding='utf-8'))"
```
Fix the syntax error and re-run.

## Canon issues

### "I edited AGENTS.md directly and sync overwrote it"

AGENTS.md is generated from `distill/canon/`. Direct edits don't survive re-sync.

**Fix:** Move your changes into `distill/canon/` (probably `CORE_CANON.md` or a new canon
file), then run `python scripts/sync.py --canon` to regenerate AGENTS.md with your changes
baked in.

### "The canon body in AGENTS.md is stale after I edited canon"

You need to regenerate:
```bash
python scripts/sync.py --canon
```

## Still stuck

1. Run `python scripts/detect.py --json` and `python scripts/verify.py --json` ??save output.
2. Check `adapters/registry.json` for your tool's entry.
3. Read the relevant Doc (`03-Tool-Adapters.md`, `02-Deployment-Guide.md`).
4. If all else fails, open an issue with the JSON output and your tool/version/OS.
