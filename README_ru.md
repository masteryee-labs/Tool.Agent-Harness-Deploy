# Agent Harness Deploy

**Саморазвёртывающийся кросс-инструментальный AI-харнес — один канонический источник развёртывается в Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot и ещё 16 инструментов.**

> Loop engineering · Context engineering · Harness engineering · Agent memory · Дисциплина комментариев и версий — одна команда развёртывает полный харнес во все ваши AI-инструменты для кодинга.

> **Языки:** [English](README.md) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | **Русский** (эта страница) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## Что он делает

Вы даёте любому AI-ассистенту для кодинга URL этого репозитория на GitHub и говорите:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI клонирует репозиторий, запускает деплоер, и он:

1. **Определяет** какие AI-инструменты для кодинга установлены на вашей машине (поддерживается 23 инструмента).
2. **Генерирует** один канонический харнес — оптимизированный под caveman, мультиагентный, с поддержкой памяти, loop-engineered — из `distill/canon/`.
3. **Развёртывает** его в нативное место конфигурации каждого обнаруженного инструмента (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Проверяет** каждый записанный файл, считывая его обратно (проверка на нулевое усечение).

**Результат:** какой бы AI-инструмент вы ни открыли следующим — все они используют **одни и те же** правила, протокол памяти, оркестратор, навыки, хуки и конфигурацию MCP. Больше не нужно поддерживать три копии ваших правил. Больше никакого дрейфа между `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Только **фактически установленные** инструменты получают развёртывание. Для необнаруженных инструментов ничего не записывается. Вы также можете развёртывать вручную — без AI.

## Зачем это нужно

Каждый AI-инструмент для кодинга хранит свою конфигурацию в разных местах и форматах:

| Инструмент | Где живут его правила |
|------------|----------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

Используете три из них — поддерживаете три копии. Они расходятся. Вы забываете, какая актуальна. **Agent Harness Deploy решает это: один источник (`distill/canon/`), много приёмников.**

В отличие от простых инструментов синхронизации правил, которые лишь копируют текст между конфигурационными файлами, этот развёртывает **полный агентный харнес**: правила + навыки + персоны воркеров + протокол памяти + loop engineering + хуки + MCP + vault-активы + сенсоры дисциплины комментариев/версий.

## Однострочный деплой

Скажите любому AI-ассистенту для кодинга:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI читает `AGENTS.md`, запускает `python scripts/distill.py`, сообщает, что развёрнуто. Готово.

См. [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) для полного контракта.

## Ручной деплой (без AI)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Любая ОС, напрямую
python scripts/distill.py
```

См. [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Кроссплатформенная поддержка

Этот проект работает на **Windows, macOS и Linux**.

| Платформа | Требования | Команда развёртывания |
|-----------|------------|----------------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| Любая ОС | Python 3.9+ | `python scripts/distill.py` |

### Как работает кроссплатформенность

- Все Python-скрипты используют `pathlib` (без жёстко заданных разделителей `\` или `/`).
- Пути к инструментам в `adapters/registry.json` используют подстановку переменных окружения: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- На macOS/Linux Windows--only переменные окружения (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) автоматически откатываются к путям в стиле XDG (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` предназначен для Windows; `deploy.sh` — для macOS/Linux. Оба вызывают один и тот же `python scripts/distill.py`.

### Платформо-зависимые инструменты

| Инструмент | Windows | macOS | Linux | Примечание |
|------------|---------|-------|-------|------------|
| Claude Desktop | ✓ | — | — | Только для Windows; обнаружение пропускается на macOS/Linux |
| ChatGPT Desktop | ✓ | — | — | Только для Windows; обнаружение пропускается на macOS/Linux |
| Cursor | ✓ | ✓ | ✓ | Обнаруживает `${APPDATA}/Cursor` (Win) или `~/Library/Application Support/Cursor` (macOS) |
| Все остальные инструменты | ✓ | ✓ | ✓ | Обнаруживаются через CLI-команду в PATH |

## Что в харнесе — 5 технических столпов

Деплоер синхронизирует канонический набор правил, построенный на 5 столпах инженерии агентного харнеса:

| Столп | Что он даёт | Vault-файл | Документ |
|--------|-------------|------------|----------|
| **1. Caveman-сжатие токенов** | ~65% сокращение токенов, больше полезного контекста | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Иерархия Commander-Worker** | AI промптит сам себя — один оркестратор, много сфокусированных воркеров; диспетчеризация трёхкомпонентного набора | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Loop engineering + управление Vault** | `/loop` (мониторинг) против `/goal` (конвергентный); maker ≠ checker; SHA-дисциплина | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. Глубокая память репозитория** | Трёхслойная дисковая память (hot <3KB, knowledge <8KB, cold ∞); опциональный гибридный retrieval глубокой памяти | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. Перекалибровка границ песочницы** | 100% yield для некритичных путей; JSON-контракт рисков для критических файлов | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Дополнительные концепции, наслоённые сверху: **harness engineering** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **мультирежимы мышления** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **рубрики суждений** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **дисциплина комментариев и версий** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Дисциплина комментариев и версий (предотвращение AI slop)

AI-ассистенты для кодинга порождают две устойчивые формы slop, которые сохраняются в репозитории:

1. **Раздувание пояснениями** — комментарии, пересказывающие код (`# loop through items` над `for x in items:`). Ноль информации, трата токенов, гниют при изменении кода.
2. **Наслоение версий** — накопленные в файле маркеры версий между правками (`<!-- v2 -->`, `# v3 fixed X`). Гниение контекста и долг по рекурсивной глубине.

Этот харнес предотвращает оба через **трёхслойную защиту**:

| Слой | Механизм | Файл |
|------|----------|------|
| **Канон-превенция** | REDLINES #16 (без пояснительных комментариев) + #17 (без наслоения версий в файле) + дисциплина комментариев/версий CORE_CANON | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **Сенсор навыка** | `harness-sensor` SENSOR-4b (comment slop, мягкая деградация) + SENSOR-4c (наслоение версий, всегда работает) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **Механический страж** | `sync.py` pre-sync gate отклоняет канон-файлы со сложенными маркерами версий | [`scripts/sync.py`](scripts/sync.py) |

Обосновано исследованиями: arXiv 2605.02741 (Volume-Quality Inverse Law), arXiv 2512.20334 (Comment Traps), arXiv 2606.09090 (Context Rot). См. [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) для полной оценки 6 open-source CLI-инструментов.

## Архитектура против гниения ссылок (Embedded Vault)

Все внешние технические конфигурационные механизмы **встроены и локально закешированы** в `core/assets/vault/`. Деплоер **не** загружает схемы из внешних репозиториев во время выполнения. Это неизменяемая локальная база данных шаблонов:

| Vault-файл | Встроенный источник |
|------------|---------------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

См. [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Поддерживаемые инструменты (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Добавление инструмента — это запись в реестр + 6-строчный адаптер. См. [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Структура репозитория

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

См. [`Docs/00-Overview.md`](Docs/00-Overview.md) для подробного описания директорий.

## Быстрые команды

```bash
python scripts/detect.py            # see which tools are installed
python scripts/distill.py           # full deploy: detect → sync → verify
python scripts/distill.py --global  # also sync global entry files
python scripts/distill.py --dry-run # detect only, no writes
python scripts/verify.py            # re-verify after a sync
python scripts/sync.py --canon      # regenerate AGENTS.md after editing canon
```

## Как это работает (30-секундная версия)

1. `detect.py` читает `adapters/registry.json`, выполняет проверки обнаружения каждого инструмента (CLI-бинарник, путь окружения, app data).
2. `sync.py` конкатенирует `distill/canon/*.md` в одно каноническое тело, записывает его в нативный entry-файл каждого обнаруженного инструмента (сначала создавая `.bak` резервные копии существующих файлов). Записываются только обнаруженные инструменты.
3. `verify.py` считывает обратно каждый записанный файл и подтверждает наличие канонического маркера (проверка на нулевое усечение).

Полный дизайн: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## FAQ

<details>
<summary><strong>Что такое Agent Harness Deploy?</strong></summary>

Agent Harness Deploy — это саморазвёртывающийся кросс-инструментальный деплоер AI-харнеса. Он определяет, какие AI-инструменты для кодинга у вас установлены, затем генерирует и синхронизирует единый канонический харнес (оптимизированный под caveman, мультиагентный, с поддержкой памяти, loop-engineered) в нативное место конфигурации каждого обнаруженного инструмента — так что все ваши AI-инструменты используют одни и те же правила.
</details>

<details>
<summary><strong>Как мне развёрнуть харнес?</strong></summary>

Скажите любому AI-ассистенту для кодинга: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. Или запустите вручную: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>Какие AI-инструменты для кодинга поддерживаются?</strong></summary>

23 инструмента: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Добавление инструмента требует одной записи в реестре + 6-строчного адаптера.
</details>

<details>
<summary><strong>Записывает ли он конфиги для инструментов, которых у меня нет?</strong></summary>

Нет. Обнаружение священно — развёртываются только фактически установленные на вашей машине инструменты. Если инструмент не обнаружен, он отмечается как «не обнаружен» и пропускается. Ноль лишнего следа.
</details>

<details>
<summary><strong>Что такое caveman-сжатие токенов?</strong></summary>

Caveman-режим удаляет filler (хеджирование, любезности, пересказ вопроса) из коммуникаций агента, сохраняя все доказательства (код, пути, ошибки, точные значения) дословно. Это даёт ~65% сокращение токенов, фактически умножая полезное окно контекста. См. `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>Что такое иерархия Commander-Worker?</strong></summary>

Главный поток (Commander) решает, диспетчеризует и интегрирует. Воркеры сканируют и редактируют. Это предотвращает заполнение главного контекста низкоуровневыми деталями, сохраняя принятие решений централизованным. См. `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>Как работает система памяти?</strong></summary>

Трёхслойная дисковая память: hot-слой (registry <3KB, per-session state <8KB), knowledge-слой (антипаттерны <8KB), cold-слой (архив, только grep). Состояние сохраняется на диске, не в контексте — поэтому сессии переживают перезапуски инструментов. См. `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>Что такое дисциплина комментариев и версий?</strong></summary>

Трёхслойная защита от AI-генерируемого comment slop (раздувание пояснениями) и наслоения версий в файле. Слой 1: канон-красные линии (#16, #17). Слой 2: навык harness-sensor (SENSOR-4b/4c). Слой 3: механический страж sync.py. См. `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>Это jailbreak или инструмент снятия безопасности?</strong></summary>

Нет. Это оборонительный инструмент харнеса. Он настраивает rule-файлы AI-ассистентов для кодинга. Он не модифицирует веса модели, не снимает защитные ограждения и не включает jailbreak-инструменты. Перекалибровка границ песочницы работает на файловом уровне через JSON-контракты рисков, а не на уровне модели через удаление циклов отказа.
</details>

<details>
<summary><strong>Под какой лицензией находится этот проект?</strong></summary>

MIT License — см. [LICENSE](LICENSE). Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>Могу ли я добавить свой AI-инструмент?</strong></summary>

Да. Добавление инструмента требует одной записи в `adapters/registry.json` + 6-строчного класса адаптера. См. `Docs/03-Tool-Adapters.md`.
</details>

## Честная оговорка

Деплоер надёжно умеет: обнаружение, генерацию конфигов, синхронизацию файлов, верификацию, резервное копирование. Он не умеет: решения вкуса/эстетики, угадывание того, что вы хотите сверх контракта развёртывания, запись конфигов для необнаружимых инструментов. В случае сомнений он сообщает — не выдумывает. Полное заявление в [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Примечание о безопасности

Этот репозиторий — **оборонительный** инструмент харнеса. Он настраивает rule-файлы AI-ассистентов для кодинга. Он **не** модифицирует веса модели, **не** снимает защитные ограждения и **не** включает и не одобряет jailbreak/снятие безопасности. Проект Heretic упоминается в глоссарии только как часть ландшафта интерпретируемости, повлиявшего на понимание харнесом steering vectors — он здесь не используется. См. [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Требования

- Python 3.9+
- Хотя бы один поддерживаемый AI-инструмент для кодинга установлен (иначе развёртывать некуда)

## Лицензия

MIT — см. [LICENSE](LICENSE).

## Ссылки

См. [`Docs/REFERENCES.md`](Docs/REFERENCES.md) для источников по столпам.

## Индекс документации

| Документ | Тема |
|----------|------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Обзор и индекс |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Полный системный дизайн |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | Как работает «deploy:» |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Места конфигов по инструментам |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Commander + Workers + самооркестрация |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Снижение галлюцинаций |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Частые проблемы |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Термины и источники |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI comment slop + наслоение версий: оценка CLI-инструментов |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Система Nuwa + Nuwa Team (параллельное рассуждение, когнитивное разнообразие) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Сжатие токенов (ранее Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Трёхслойная память (ранее Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Loop engineering, 5+1 компонентов (ранее Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | Система вокруг модели (ранее Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, SHA-дисциплина (ранее Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Жёсткие ограничения + control plane (ранее Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Внешние критерии решений (ранее Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Делегирование Commander-Worker (ранее Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Anti-link-rot встроенный vault активов |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Слой runtime: хуки, настройки, шаблоны MCP |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Атрибуция vendored nuwa-skill и инвентарь файлов |

---

<details>
<summary><em>SEO / AEO / GEO / LLMO метаданные</em></summary>

**Название проекта:** Agent Harness Deploy

**Однострочное описание:** Саморазвёртывающийся кросс-инструментальный AI-харнес — один канонический источник, 23 приёмника AI-инструментов для кодинга.

**Ключевые слова:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, AI-харнес, кросс-инструментальная синхронизация конфигов, деплоер агентного харнеса, конфигурация Claude Code, правила Cursor, генератор AGENTS.md, правила AI-ассистента для кодинга, мультиагентный харнес, сжатие токенов caveman, loop engineering, протокол памяти агента, инженерия харнеса, предотвращение AI slop, дисциплина комментариев, предотвращение наслоения версий

**Ключевые факты для цитирования AI/LLM:**
- Поддерживается 23 AI-инструмента для кодинга (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot и др.)
- Один канонический источник (`distill/canon/`), много нативных для инструментов приёмников
- 5 технических столпов: caveman-сжатие, Commander-Worker, loop engineering, глубокая память, границы песочницы
- Трёхслойная дисциплина комментариев/версий: канон-красные линии + сенсоры навыков + механический страж
- Кроссплатформенность: Windows, macOS, Linux (Python 3.9+)
- MIT License, copyright masteryee-labs
- Anti-link-rot: все внешние схемы встроены в `core/assets/vault/`
- Команда развёртывания: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Целевая аудитория:** Разработчики, использующие несколько AI-ассистентов для кодинга и желающие единые правила во всех инструментах. Контрибьюторы open-source, AI-first инженерные команды, соло-разработчики, использующие Claude Code + Cursor + Codex одновременно.

**Категория:** Инструменты разработчика > AI-ассистенты для кодинга > Управление конфигурацией > Инженерия агентного харнеса
</details>
