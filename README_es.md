# Agent Harness Deploy

**Harness de IA multi-herramienta con autodespliegue — una fuente canónica desplegada en Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot y 16 más.**

> Ingeniería de bucles · Ingeniería de contexto · Ingeniería de harness · Memoria de agentes · Disciplina de comentarios y versiones — un comando despliega el harness completo a todas tus herramientas de codificación con IA.

> **Idiomas:** **English** (this file) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) (esta página) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## Qué hace

Le das a cualquier asistente de codificación con IA la URL de GitHub de este repositorio y le dices:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

La IA clona el repositorio, ejecuta el desplegador, y este:

1. **Detecta** qué herramientas de codificación con IA están instaladas en tu máquina (23 herramientas soportadas).
2. **Genera** un harness canónico — optimizado en modo caveman, multi-agente, con memoria habilitada, con ingeniería de bucles — desde `distill/canon/`.
3. **Despliega** el harness en la ubicación de configuración nativa de cada herramienta detectada (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Verifica** cada archivo escrito releyéndolo (comprobación de cero truncamiento).

**Resultado:** independientemente de la herramienta de IA que abras a continuación, todas comparten las **mismas** reglas, protocolo de memoria, orquestador, habilidades, hooks y configuración MCP. Se acabó el mantener tres copias de tus reglas. Se acabó la divergencia entre `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Solo las herramientas que están **realmente instaladas** reciben el despliegue. No se escribe nada para herramientas no detectadas. También puedes desplegar manualmente — no se requiere IA.

## Por qué

Cada herramienta de codificación con IA almacena su configuración en un lugar y formato diferentes:

|| Herramienta | Donde viven sus reglas |
||------|----------------------|
|| Claude Code | `.claude/CLAUDE.md` |
|| Antigravity / Gemini CLI | `AGENTS.md` |
|| Codex / Codex CLI | `.codex/instructions.md` |
|| Devin / Devin CLI | `.devin/AGENTS.md` |
|| Cursor | `.cursor/rules/*.mdc` |
|| Windsurf | `.codeium/windsurf/memories/` |
|| GitHub Copilot | `.github/copilot-instructions.md` |
|| Claude Desktop | `claude_desktop_config.json` |

Usa tres de estas y mantienes tres copias. Divergen. Olvidas cuál es la actual. **Agent Harness Deploy lo soluciona: una fuente (`distill/canon/`), muchos destinos.**

A diferencia de las simples herramientas de sincronización de reglas que solo copian texto entre archivos de configuración, este despliega un **harness de agente completo**: reglas + habilidades + personas de worker + protocolo de memoria + ingeniería de bucles + hooks + MCP + recursos del vault + sensores de disciplina de comentarios/versión.

## El despliegue en una línea

Dile a cualquier asistente de codificación con IA:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

La IA lee `AGENTS.md`, ejecuta `python scripts/distill.py`, reporta lo que desplegó. Listo.

Consulta [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) para el contrato completo.

## Despliegue manual (sin IA)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Cualquier SO, directo
python scripts/distill.py
```

Consulta [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Soporte multiplataforma

Este proyecto funciona en **Windows, macOS y Linux**.

|| Plataforma | Requisitos | Comando de despliegue |
||----------|-------------|----------------|
|| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
|| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
|| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
|| Cualquier SO | Python 3.9+ | `python scripts/distill.py` |

### Cómo funciona el soporte multiplataforma

- Todos los scripts de Python usan `pathlib` (sin separadores `\` o `/` codificados de forma fija).
- Las rutas de herramientas en `adapters/registry.json` usan expansión de variables de entorno: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- En macOS/Linux, las variables de entorno exclusivas de Windows (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) automáticamente hacen fallback a rutas estilo XDG (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` es para Windows; `deploy.sh` es para macOS/Linux. Ambos invocan el mismo `python scripts/distill.py`.

### Herramientas específicas por plataforma

|| Herramienta | Windows | macOS | Linux | Nota |
||------|---------|-------|-------|------|
|| Claude Desktop | ✓ | — | — | Aplicación exclusiva de Windows; la detección se omite en macOS/Linux |
|| ChatGPT Desktop | ✓ | — | — | Aplicación exclusiva de Windows; la detección se omite en macOS/Linux |
|| Cursor | ✓ | ✓ | ✓ | Detecta `${APPDATA}/Cursor` (Win) o `~/Library/Application Support/Cursor` (macOS) |
|| Todas las demás herramientas | ✓ | ✓ | ✓ | Detectadas vía comando CLI en el PATH |

## Qué hay en el harness — 5 pilares técnicos

El desplegador sincroniza un conjunto canónico de reglas construido sobre 5 pilares de la ingeniería de harness de agentes:

|| Pilar | Qué te aporta | Archivo del vault | Doc |
||--------|-------------------|------------|-----|
|| **1. Compresión de tokens en modo caveman** | ~65% de reducción de tokens, más contexto utilizable | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
|| **2. Jerarquía Comandante-Worker** | La IA se auto-promptea — un orquestador, muchos workers enfocados; despacho de conjunto de tres piezas | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
|| **3. Ingeniería de bucles + Control del vault** | `/loop` (monitorización) vs `/goal` (convergente); maker ≠ checker; disciplina SHA | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
|| **4. Memoria profunda del repositorio** | Memoria de disco de tres capas (hot <3KB, knowledge <8KB, cold ∞); recuperación híbrida de memoria profunda opcional | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
|| **5. Realineación de límites del sandbox** | Rendimiento del 100% en rutas no críticas; contrato de riesgo JSON para archivos críticos | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Conceptos adicionales superpuestos: **ingeniería de harness** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **modos multi-pensamiento** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **rúbricas de juicio** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **disciplina de comentarios y versiones** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Disciplina de comentarios y versiones (prevención de slop de IA)

Los asistentes de codificación con IA producen dos formas persistentes de slop que sobreviven en el repositorio:

1. **Hinchazón explicativa** — comentarios que reformulan el código (`# recorrer los items` encima de `for x in items:`). Cero información, desperdicia tokens, se pudre cuando cambia el código.
2. **Acumulación de versiones** — marcadores de versión dentro del archivo acumulados a lo largo de las ediciones (`<!-- v2 -->`, `# v3 arregló X`). Putrefacción de contexto y deuda de profundidad recursiva.

Este harness previene ambos mediante una **defensa de tres capas**:

|| Capa | Mecanismo | Archivo |
||-------|-----------|------|
|| **Prevención del canon** | REDLINES #16 (sin comentarios explicativos) + #17 (sin acumulación de versiones en archivo) + disciplina de comentarios/versión de CORE_CANON | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
|| **Detección por habilidad** | `harness-sensor` SENSOR-4b (slop de comentarios, degradación elegante) + SENSOR-4c (acumulación de versiones, siempre se ejecuta) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
|| **Guardia mecánica** | `sync.py` puerta pre-sincronización rechaza archivos del canon con marcadores de versión apilados | [`scripts/sync.py`](scripts/sync.py) |

Respaldado por investigación: arXiv 2605.02741 (Ley Inversa Volumen-Calidad), arXiv 2512.20334 (Trampas de Comentarios), arXiv 2606.09090 (Putrefacción de Contexto). Consulta [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) para la evaluación completa de 6 herramientas CLI de código abierto.

## Arquitectura anti-link-rot (Vault embebido)

Todos los mecanismos de configuración técnica externos están **embebidos y cacheados localmente** en `core/assets/vault/`. El desplegador **no** obtiene esquemas de repositorios externos en tiempo de ejecución. Esta es una base de datos de plantillas local inmutable:

|| Archivo del vault | Fuente embebida |
||-----------|-----------------|
|| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
|| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
|| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
|| `strix_security_rules.json` | usestrix/strix |
|| `graphify_knowledge_spec.json` | safishamsi/graphify |

Consulta [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Herramientas soportadas (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Añadir una herramienta es una entrada en el registro + un adaptador de 6 líneas. Consulta [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Estructura del repositorio

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

Consulta [`Docs/00-Overview.md`](Docs/00-Overview.md) para descripciones detalladas de los directorios.

## Comandos rápidos

```bash
python scripts/detect.py            # see which tools are installed
python scripts/distill.py           # full deploy: detect → sync → verify
python scripts/distill.py --global  # also sync global entry files
python scripts/distill.py --dry-run # detect only, no writes
python scripts/verify.py            # re-verify after a sync
python scripts/sync.py --canon      # regenerate AGENTS.md after editing canon
```

## Cómo funciona (versión de 30 segundos)

1. `detect.py` lee `adapters/registry.json`, ejecuta las comprobaciones de detección de cada herramienta (binario CLI, ruta de entorno, datos de la aplicación).
2. `sync.py` concatena `distill/canon/*.md` en un cuerpo canónico único, lo escribe en el archivo de entrada nativo de cada herramienta detectada (haciendo copia de seguridad de los archivos existentes a `.bak` primero). Solo las herramientas detectadas reciben escritura.
3. `verify.py` relee cada archivo escrito y confirma que el marcador canónico está presente (comprobación de cero truncamiento).

Diseño completo: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## Preguntas frecuentes

<details>
<summary><strong>¿Qué es Agent Harness Deploy?</strong></summary>

Agent Harness Deploy es un desplegador de harness de IA multi-herramienta con autodespliegue. Detecta qué herramientas de codificación con IA tienes instaladas, luego genera y sincroniza un único harness canónico (optimizado en modo caveman, multi-agente, con memoria habilitada, con ingeniería de bucles) en la ubicación de configuración nativa de cada herramienta detectada — para que todas tus herramientas de IA compartan las mismas reglas.
</details>

<details>
<summary><strong>¿Cómo despliego el harness?</strong></summary>

Dile a cualquier asistente de codificación con IA: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. O ejecútalo manualmente: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>¿Qué herramientas de codificación con IA están soportadas?</strong></summary>

23 herramientas: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Añadir una herramienta requiere una entrada en el registro + un adaptador de 6 líneas.
</details>

<details>
<summary><strong>¿Escribe configuraciones para herramientas que no tengo instaladas?</strong></summary>

No. La detección es sagrada — solo las herramientas realmente instaladas en tu máquina reciben el despliegue. Si una herramienta no se detecta, se reporta como "no detectada" y se omite. Cero huella innecesaria.
</details>

<details>
<summary><strong>¿Qué es la compresión de tokens en modo caveman?</strong></summary>

El modo caveman elimina el relleno (titubeos, cortesías, reformular la pregunta) de las comunicaciones del agente mientras mantiene toda la evidencia (código, rutas, errores, valores exactos) de forma verbatim. Esto logra ~65% de reducción de tokens, multiplicando efectivamente la ventana de contexto utilizable. Consulta `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>¿Qué es la jerarquía Comandante-Worker?</strong></summary>

El hilo principal (Comandante) decide, despacha e integra. Los workers escanean y editan. Esto evita que el contexto principal se llene de detalles de bajo nivel mientras mantiene la toma de decisiones centralizada. Consulta `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>¿Cómo funciona el sistema de memoria?</strong></summary>

Memoria de disco de tres capas: capa hot (registro <3KB, estado por-sesión <8KB), capa knowledge (anti-patrones <8KB), capa cold (archivo, solo grep). El estado persiste en disco, no en contexto — así las sesiones sobreviven a reinicios de herramientas. Consulta `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>¿Qué es la disciplina de comentarios y versiones?</strong></summary>

Una defensa de tres capas contra el slop de comentarios generado por IA (hinchazón explicativa) y la acumulación de versiones dentro del archivo. Capa 1: líneas rojas del canon (#16, #17). Capa 2: habilidad harness-sensor (SENSOR-4b/4c). Capa 3: guardia mecánica de sync.py. Consulta `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>¿Es esto una herramienta de jailbreak o de eliminación de seguridad?</strong></summary>

No. Esta es una herramienta de harness defensiva. Configura los archivos de reglas de los asistentes de codificación con IA. No modifica los pesos del modelo, no elimina las barreras de seguridad y no incluye herramientas de jailbreak. La realineación de límites del sandbox funciona a nivel de archivo mediante contratos de riesgo JSON, no a nivel de modelo eliminando bucles de rechazo.
</details>

<details>
<summary><strong>¿Bajo qué licencia está este proyecto?</strong></summary>

Licencia MIT — consulta [LICENSE](LICENSE). Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>¿Puedo añadir mi propia herramienta de IA?</strong></summary>

Sí. Añadir una herramienta requiere una entrada en `adapters/registry.json` + una clase adaptadora de 6 líneas. Consulta `Docs/03-Tool-Adapters.md`.
</details>

## Cláusula de honestidad

El desplegador puede hacer de forma fiable: detección, generación de configuración, sincronización de archivos, verificación, copia de seguridad. No puede hacer: decisiones de gusto/estética, adivinar lo que quieres más allá del contrato de despliegue, escribir configuraciones para herramientas que no puede detectar. Cuando hay incertidumbre, reporta — no fabrica. Declaración completa en [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Nota de seguridad

Este repositorio es una herramienta de harness **defensiva**. Configura los archivos de reglas de los asistentes de codificación con IA. **No** modifica los pesos del modelo, **no** elimina las barreras de seguridad, y **no** incluye ni respalda herramientas de jailbreak/eliminación de seguridad. El proyecto Heretic se referencia en el glosario únicamente como parte del panorama de interpretabilidad que informó la comprensión del harness sobre los vectores de steering — no se utiliza aquí. Consulta [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Requisitos

- Python 3.9+
- Al menos una herramienta de codificación con IA soportada instalada (de lo contrario no hay nada a lo que desplegar)

## Licencia

MIT — consulta [LICENSE](LICENSE).

## Referencias

Consulta [`Docs/REFERENCES.md`](Docs/REFERENCES.md) para las referencias de fuentes por pilar.

## Índice de documentación

|| Doc | Tema |
||-----|-------|
|| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Visión general e índice |
|| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Diseño completo del sistema |
|| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | Cómo funciona "deploy:" |
|| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Ubicaciones de configuración por herramienta |
|| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Comandante + Workers + auto-orquestación |
|| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Reducción de alucinaciones |
|| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Problemas comunes |
|| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Términos y fuentes |
|| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | Slop de comentarios de IA + acumulación de versiones: evaluación de herramientas CLI |
|| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Sistema Nuwa + Equipo Nuwa (razonamiento paralelo, diversidad cognitiva) |
|| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Compresión de tokens (antes Docs/05) |
|| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Memoria de tres capas (antes Docs/06) |
|| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Ingeniería de bucles, 5+1 componentes (antes Docs/07) |
|| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | Sistema alrededor del modelo (antes Docs/08) |
|| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, disciplina SHA (antes Docs/10) |
|| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Paradas obligatorias + plano de control (antes Docs/harness_control_plane) |
|| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Criterios de decisión externalizados (antes Docs/harness_rubrics) |
|| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Delegación Comandante-Worker (antes Docs/Agents/commander) |
|| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Vault de recursos embebidos anti-link-rot |
|| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Capa de runtime: hooks, settings, plantillas MCP |
|| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Atribución de nuwa-skill vendored e inventario de archivos |

---

<details>
<summary><em>Metadatos SEO / AEO / GEO / LLMO</em></summary>

**Nombre del proyecto:** Agent Harness Deploy

**Descripción de una línea:** Harness de IA multi-herramienta con autodespliegue — una fuente canónica, 23 destinos de herramientas de codificación con IA.

**Palabras clave:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, harness de IA para programación, sincronización de configuración multi-herramienta, desplegador de harness de agentes, reglas de asistente de IA, compresión de tokens caveman, ingeniería de bucles, protocolo de memoria de agentes, prevención de slop de IA, disciplina de comentarios, prevención de acumulación de versiones

**Hechos clave para citación por IA/LLM:**
- 23 herramientas de codificación con IA soportadas (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot, etc.)
- Una fuente canónica (`distill/canon/`), muchos destinos nativos por herramienta
- 5 pilares técnicos: compresión caveman, Comandante-Worker, ingeniería de bucles, memoria profunda, límites del sandbox
- Disciplina de comentarios/versión de tres capas: líneas rojas del canon + sensores de habilidad + guardia mecánica
- Multiplataforma: Windows, macOS, Linux (Python 3.9+)
- Licencia MIT, copyright masteryee-labs
- Anti-link-rot: todos los esquemas externos embebidos en `core/assets/vault/`
- Comando de despliegue: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Audiencia objetivo:** Desarrolladores que usan múltiples asistentes de codificación con IA y desean reglas consistentes en todas las herramientas. Contribuyentes de código abierto, equipos de ingeniería AI-first, desarrolladores individuales que usan Claude Code + Cursor + Codex simultáneamente.

**Categoría:** Herramientas de desarrollador > Asistentes de codificación con IA > Gestión de configuración > Ingeniería de harness de agentes
</details>
