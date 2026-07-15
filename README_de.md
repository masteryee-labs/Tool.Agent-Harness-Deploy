# Agent Harness Deploy

**Selbst-deployende plattformübergreifende AI-Harness — eine kanonische Quelle, deployed zu Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot & 16 weiteren.**

> Loop Engineering · Context Engineering · Harness Engineering · Agent Memory · Kommentar- und Versionsdisziplin — ein Befehl deployt das komplette Harness in alle deine AI-Coding-Tools.

> **Sprachen:** **English** | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) (diese Seite) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## Was es tut

Du gibst einem beliebigen AI-Coding-Assistent die GitHub-URL dieses Repos und sagst:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

Die AI klont das Repo, führt den Deployer aus und dieser:

1. **Erkennt** welche AI-Coding-Tools auf deiner Maschine installiert sind (23 Tools unterstützt).
2. **Generiert** ein kanonisches Harness — caveman-optimiert, multi-agent, memory-fähig, loop-engineered — aus `distill/canon/`.
3. **Deployt** es an den nativen Konfigurationsort jedes erkannten Tools (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Verifiziert** jede geschriebene Datei durch Zurücklesen (Zero-Truncation-Check).

**Ergebnis:** Welches AI-Tool du als nächstes öffnest — sie alle teilen sich **dieselben** Regeln, das Memory-Protokoll, den Orchestrator, die Skills, Hooks und die MCP-Konfiguration. Kein Pflegen von drei Kopien deiner Regeln mehr. Kein Drift mehr zwischen `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Nur Tools, die **tatsächlich installiert** sind, werden deployed. Für nicht erkannte Tools wird nichts geschrieben. Du kannst auch manuell deployen — keine AI erforderlich.

## Warum

Jedes AI-Coding-Tool speichert seine Konfiguration an einem anderen Ort und in einem anderen Format:

| Tool | Wo seine Regeln liegen |
|------|------------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

Benutzt du drei davon, pflegst du drei Kopien. Sie driften auseinander. Du vergisst, welche aktuell ist. **Agent Harness Deploy behebt das: eine Quelle (`distill/canon/`), viele Senken.**

Im Gegensatz zu einfachen Rules-Sync-Tools, die nur Text zwischen Konfigurationsdateien kopieren, deployt dies ein **vollständiges Agent-Harness**: Regeln + Skills + Worker-Personas + Memory-Protokoll + Loop Engineering + Hooks + MCP + Vault-Assets + Kommentar-/Versionsdisziplin-Sensoren.

## Das Einzeilen-Deploy

Sag einem beliebigen AI-Coding-Assistent:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

Die AI liest `AGENTS.md`, führt `python scripts/distill.py` aus, meldet was deployed wurde. Fertig.

Siehe [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) für den vollständigen Vertrag.

## Manuelles Deploy (ohne AI)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Jedes OS, direkt
python scripts/distill.py
```

Siehe [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Plattformübergreifende Unterstützung

Dieses Projekt funktioniert auf **Windows, macOS und Linux**.

| Plattform | Anforderungen | Deploy-Befehl |
|-----------|---------------|---------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| Jedes OS | Python 3.9+ | `python scripts/distill.py` |

### Wie plattformübergreifend funktioniert

- Alle Python-Skripte verwenden `pathlib` (keine fest codierten `\` oder `/` Separatoren).
- Tool-Pfade in `adapters/registry.json` verwenden Env-Expansion: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- Auf macOS/Linux fallen Windows-only Env-Variablen (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) automatisch auf XDG-artige Pfade zurück (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` ist für Windows; `deploy.sh` ist für macOS/Linux. Beide rufen dasselbe `python scripts/distill.py` auf.

### Plattformspezifische Tools

| Tool | Windows | macOS | Linux | Hinweis |
|------|---------|-------|-------|---------|
| Claude Desktop | ✓ | — | — | Windows-only-App; Erkennung überspringt auf macOS/Linux |
| ChatGPT Desktop | ✓ | — | — | Windows-only-App; Erkennung überspringt auf macOS/Linux |
| Cursor | ✓ | ✓ | ✓ | Erkennt `${APPDATA}/Cursor` (Win) oder `~/Library/Application Support/Cursor` (macOS) |
| Alle anderen Tools | ✓ | ✓ | ✓ | Erkannt via CLI-Befehl auf PATH |

## Was im Harness steckt — 5 technische Säulen

Der Deployer synchronisiert einen kanonischen Regelsatz, der auf 5 Säulen des Agent-Harness-Engineings aufbaut:

| Säule | Was es dir gibt | Vault-Datei | Doku |
|-------|-----------------|------------|------|
| **1. Caveman-Token-Kompression** | ~65% Token-Einsparung, mehr nutzbarer Kontext | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Commander-Worker-Hierarchie** | Die AI steuert sich selbst — ein Orchestrator, viele fokussierte Worker; Dispatch-Dreier-Set | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Loop Engineering + Vault-Kontrolle** | `/loop` (Monitoring) vs `/goal` (konvergent); Maker ≠ Checker; SHA-Disziplin | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. Deep Repo Memory** | Drei-Schichten-Festplatten-Memory (hot <3KB, knowledge <8KB, cold ∞); optionales Deep-Memory-Hybrid-Retrieval | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. Sandbox-Boundary-Realignment** | Nicht-kritischer Pfad 100% Yield; Critical-File-JSON-Risiko-Vertrag | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Zusätzliche Konzepte obendrauf: **Harness Engineering** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **Multi-Thinking-Modi** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **Judgment-Rubrics** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **Kommentar- und Versionsdisziplin** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Kommentar- und Versionsdisziplin (AI-Slop-Prävention)

AI-Coding-Assistenten produzieren zwei hartnäckige Formen von Slop, die im Repo überleben:

1. **Erklärungs-Bloat** — Kommentare, die den Code wiederholen (`# loop through items` über `for x in items:`). Null Information, verschwendet Tokens, verrottet bei Code-Änderungen.
2. **Versions-Stapelung** — In-File-Versionsmarker, die über Edits hinweg akkumulieren (`<!-- v2 -->`, `# v3 fixed X`). Context-Rot und Recursive-Depth-Schulden.

Dieses Harness verhindert beides durch eine **Drei-Schichten-Verteidigung**:

| Schicht | Mechanismus | Datei |
|---------|-------------|-------|
| **Canon-Prävention** | REDLINES #16 (keine erklärenden Kommentare) + #17 (keine In-File-Versions-Stapelung) + CORE_CANON Kommentar-/Versionsdisziplin | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **Skill-Erkennung** | `harness-sensor` SENSOR-4b (Kommentar-Slop, Graceful Degradation) + SENSOR-4c (Versions-Stapelung, läuft immer) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **Mechanischer Guard** | `sync.py` Pre-Sync-Gate lehnt Canon-Dateien mit gestapelten Versionsmarkern ab | [`scripts/sync.py`](scripts/sync.py) |

Forschungsbasiert: arXiv 2605.02741 (Volume-Quality Inverse Law), arXiv 2512.20334 (Comment Traps), arXiv 2606.09090 (Context Rot). Siehe [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) für die vollständige Evaluation von 6 Open-Source-CLI-Tools.

## Anti-Link-Rot-Architektur (Embedded Vault)

Alle externen technischen Konfigurationsmechanismen sind **eingebettet und lokal gecacht** in `core/assets/vault/`. Der Deployer holt **keine** Schemata zur Laufzeit aus externen Repos. Dies ist eine unveränderliche lokale Template-Datenbank:

| Vault-Datei | Eingebettete Quelle |
|-------------|---------------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

Siehe [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Unterstützte Tools (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Ein Tool hinzuzufügen ist ein Registry-Eintrag + ein 6-Zeilen-Adapter. Siehe [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Repo-Layout

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # Entry file for AGENTS.md-aware tools
├── CLAUDE.md                  # Entry file for CLAUDE.md-aware tools
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10 more languages
├── core/assets/               # Vault, skills, runtime (hooks, settings, MCP)
├── Docs/                      # Documentation
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # Tool adapters + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                    # The deployer's own harness (dogfooded)
```

Siehe [`Docs/00-Overview.md`](Docs/00-Overview.md) für detaillierte Verzeichnisbeschreibungen.

## Schnellbefehle

```bash
python scripts/detect.py            # see which tools are installed
python scripts/distill.py           # full deploy: detect → sync → verify
python scripts/distill.py --global  # also sync global entry files
python scripts/distill.py --dry-run # detect only, no writes
python scripts/verify.py            # re-verify after a sync
python scripts/sync.py --canon      # regenerate AGENTS.md after editing canon
```

## Wie es funktioniert (30-Sekunden-Version)

1. `detect.py` liest `adapters/registry.json`, führt die Erkennungs-Checks jedes Tools aus (CLI-Binary, Env-Pfad, App-Data).
2. `sync.py` verkettet `distill/canon/*.md` zu einem kanonischen Body, schreibt ihn in die native Entry-Datei jedes erkannten Tools (bestehende Dateien werden zuerst nach `.bak` gesichert). Nur erkannte Tools werden geschrieben.
3. `verify.py` liest jede geschriebene Datei zurück und bestätigt, dass der kanonische Marker vorhanden ist (Zero-Truncation-Check).

Vollständiges Design: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## FAQ

<details>
<summary><strong>Was ist Agent Harness Deploy?</strong></summary>

Agent Harness Deploy ist ein selbst-deployender, plattformübergreifender AI-Harness-Deployer. Es erkennt, welche AI-Coding-Tools du installiert hast, und generiert und synchronisiert dann ein einzelnes kanonisches Harness (caveman-optimiert, multi-agent, memory-fähig, loop-engineered) an den nativen Konfigurationsort jedes erkannten Tools — sodass alle deine AI-Tools sich dieselben Regeln teilen.
</details>

<details>
<summary><strong>Wie deploye ich das Harness?</strong></summary>

Sag einem beliebigen AI-Coding-Assistent: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. Oder führe manuell aus: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>Welche AI-Coding-Tools werden unterstützt?</strong></summary>

23 Tools: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Ein Tool hinzuzufügen erfordert einen Registry-Eintrag + einen 6-Zeilen-Adapter.
</details>

<details>
<summary><strong>Schreibt es Konfigurationen für Tools, die ich nicht installiert habe?</strong></summary>

Nein. Erkennung ist heilig — nur Tools, die tatsächlich auf deiner Maschine installiert sind, werden deployed. Wenn ein Tool nicht erkannt wird, wird es als „nicht erkannt" gemeldet und übersprungen. Null unnötiger Footprint.
</details>

<details>
<summary><strong>Was ist Caveman-Token-Kompression?</strong></summary>

Caveman-Modus entfernt Füllstoff (Hedging, Höflichkeiten, Wiederholen der Frage) aus Agent-Kommunikationen, während alle Beweise (Code, Pfade, Fehler, exakte Werte) unverändert erhalten bleiben. Dies erreicht ~65% Token-Reduktion und multipliziert effektiv das nutzbare Kontextfenster. Siehe `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>Was ist die Commander-Worker-Hierarchie?</strong></summary>

Der Haupt-Thread (Commander) entscheidet, dispatcht und integriert. Worker scannen und editieren. Das verhindert, dass der Haupt-Kontext sich mit Low-Level-Details füllt, während die Entscheidungsfindung zentralisiert bleibt. Siehe `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>Wie funktioniert das Memory-System?</strong></summary>

Drei-Schichten-Festplatten-Memory: Hot-Schicht (Registry <3KB, Per-Session-State <8KB), Knowledge-Schicht (Anti-Patterns <8KB), Cold-Schicht (Archiv, nur grep). State persistiert auf der Festplatte, nicht im Kontext — sodass Sessions Tool-Neustarts überleben. Siehe `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>Was ist Kommentar- und Versionsdisziplin?</strong></summary>

Eine Drei-Schichten-Verteidigung gegen AI-generierten Kommentar-Slop (Erklärungs-Bloat) und In-File-Versions-Stapelung. Schicht 1: Canon-Red-Lines (#16, #17). Schicht 2: harness-sensor-Skill (SENSOR-4b/4c). Schicht 3: sync.py mechanischer Guard. Siehe `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>Ist das ein Jailbreak- oder Safety-Removal-Tool?</strong></summary>

Nein. Dies ist ein defensives Harness-Tool. Es konfiguriert die Regel-Dateien von AI-Coding-Assistenten. Es modifiziert keine Modell-Gewichte, entfernt keine Safety-Guardrails und bündelt keine Jailbreak-Tools. Das Sandbox-Boundary-Realignment arbeitet auf Datei-Ebene via JSON-Risiko-Verträgen, nicht auf Modell-Ebene durch Entfernen von Refusal-Loops.
</details>

<details>
<summary><strong>Unter welcher Lizenz steht dieses Projekt?</strong></summary>

MIT-Lizenz — siehe [LICENSE](LICENSE). Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>Kann ich mein eigenes AI-Tool hinzufügen?</strong></summary>

Ja. Ein Tool hinzuzufügen erfordert einen Eintrag in `adapters/registry.json` + eine 6-Zeilen-Adapter-Klasse. Siehe `Docs/03-Tool-Adapters.md`.
</details>

## Ehrlichkeits-Klausel

Der Deployer kann zuverlässig: Erkennung, Konfigurations-Generierung, Datei-Sync, Verifikation, Backup. Er kann nicht: Geschmacks-/Ästhetik-Entscheidungen, erraten was du jenseits des Deploy-Vertrags willst, Konfigurationen für Tools schreiben die er nicht erkennen kann. Bei Unsicherheit meldet er — er erfindet nichts. Vollständige Aussage in [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Safety-Hinweis

Dieses Repo ist ein **defensives** Harness-Tool. Es konfiguriert die Regel-Dateien von AI-Coding-Assistenten. Es modifiziert **keine** Modell-Gewichte, entfernt **keine** Safety-Guardrails und bündelt oder befürwortet **keine** Jailbreak-/Safety-Removal-Tools. Das Heretic-Projekt wird im Glossar nur als Teil der Interpretability-Landschaft referenziert, die das Verständnis des Harness für Steering-Vektoren informierte — es wird hier nicht verwendet. Siehe [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Anforderungen

- Python 3.9+
- Mindestens ein unterstütztes AI-Coding-Tool installiert (sonst gibt es nichts, worauf deployed werden kann)

## Lizenz

MIT — siehe [LICENSE](LICENSE).

## Referenzen

Siehe [`Docs/REFERENCES.md`](Docs/REFERENCES.md) für Quell-Referenzen nach Säule.

## Dokumentations-Index

| Doku | Thema |
|------|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Überblick & Index |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Vollständiges System-Design |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | Wie „deploy:" funktioniert |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Per-Tool-Konfigurationsorte |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Commander + Workers + Selbst-Orchestrierung |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Halluzinations-Reduktion |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Häufige Probleme |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Begriffe & Quellen |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI-Kommentar-Slop + Versions-Stapelung: CLI-Tool-Evaluation |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Nuwa-System + Nuwa-Team (paralleles Reasoning, kognitive Diversität) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Token-Kompression (war Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Drei-Schichten-Memory (war Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Loop Engineering, 5+1 Komponenten (war Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | System um das Modell (war Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, SHA-Disziplin (war Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Hard Stops + Control Plane (war Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Externalisierte Entscheidungs-Kriterien (war Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Commander-Worker-Delegation (war Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Anti-Link-Rot eingebettete Asset-Vault |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Runtime-Schicht: Hooks, Settings, MCP-Templates |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Vendored nuwa-skill Attribution & Datei-Inventar |

---

<details>
<summary><em>SEO / AEO / GEO / LLMO Metadaten</em></summary>

**Projektname:** Agent Harness Deploy

**Einzeilen-Beschreibung:** Selbst-deployende plattformübergreifende AI-Harness — eine kanonische Quelle, 23 AI-Coding-Tool-Senken.

**Keywords:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, KI-Coding-Harness, plattformübergreifende KI-Konfigurationssynchronisation, Agent-Harness-Deployer, KI-Coding-Assistenten-Regeln, Mehrfach-Agenten-Harness, Token-Kompression, Schleifen-Engineering, Agenten-Memory-Protokoll, Harness-Engineering, KI-Slop-Prävention, Kommentardisziplin, Versionsstapelungs-Prävention

**Schlüsselfakten für AI/LLM-Zitation:**
- 23 AI-Coding-Tools unterstützt (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot, etc.)
- Eine kanonische Quelle (`distill/canon/`), viele tool-native Senken
- 5 technische Säulen: Caveman-Kompression, Commander-Worker, Loop Engineering, Deep Memory, Sandbox-Boundary
- Drei-Schichten-Kommentar-/Versionsdisziplin: Canon-Red-Lines + Skill-Sensoren + mechanischer Guard
- Plattformübergreifend: Windows, macOS, Linux (Python 3.9+)
- MIT-Lizenz, Copyright masteryee-labs
- Anti-Link-Rot: alle externen Schemata eingebettet in `core/assets/vault/`
- Deploy-Befehl: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Zielgruppe:** Entwickler, die mehrere AI-Coding-Assistenten nutzen und konsistente Regeln über alle Tools hinweg wünschen. Open-Source-Beitragende, AI-first-Engineering-Teams, Solo-Entwickler die Claude Code + Cursor + Codex gleichzeitig nutzen.

**Kategorie:** Entwickler-Tools > AI-Coding-Assistenten > Konfigurations-Management > Agent-Harness-Engineering
</details>
