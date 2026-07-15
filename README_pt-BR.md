# Agent Harness Deploy

**Harness de IA multi-ferramenta com autoimplantação — uma fonte canônica implantada no Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot e mais 16.**

> Engenharia de loops · Engenharia de contexto · Engenharia de harness · Memória de agente · Disciplina de comentários e versões — um comando implanta o harness completo em todas as suas ferramentas de IA para programação.

> **Idiomas:** [English](README.md) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) (esta página) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## O que faz

Você fornece a qualquer assistente de IA para programação a URL deste repositório no GitHub e diz:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

A IA clona o repositório, executa o implantador, e ele:

1. **Detecta** quais ferramentas de IA para programação estão instaladas na sua máquina (23 ferramentas suportadas).
2. **Gera** um harness canônico único — otimizado em modo caveman, multiagente, com memória, com engenharia de loops — a partir de `distill/canon/`.
3. **Implanta** no local de configuração nativo de cada ferramenta detectada (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Verifica** cada arquivo gravado lendo-o de volta (verificação de truncamento zero).

**Resultado:** independente de qual ferramenta de IA você abrir em seguida — todas compartilham as **mesmas** regras, protocolo de memória, orquestrador, habilidades, hooks e configuração de MCP. Chega de manter três cópias das suas regras. Chega de divergência entre `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Apenas ferramentas **realmente instaladas** recebem a implantação. Nada é gravado para ferramentas que não são detectadas. Você também pode implantar manualmente — sem necessidade de IA.

## Por quê

Cada ferramenta de IA para programação armazena sua configuração em um local e formato diferentes:

| Ferramenta | Onde ficam suas regras |
|------------|------------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

Use três delas e você mantém três cópias. Elas divergem. Você esquece qual é a atual. **O Agent Harness Deploy resolve isso: uma fonte (`distill/canon/`), muitos destinos.**

Diferente de ferramentas simples de sincronização de regras que apenas copiam texto entre arquivos de configuração, isto implanta um **harness de agente completo**: regras + habilidades + personas de worker + protocolo de memória + engenharia de loops + hooks + MCP + recursos do vault + sensores de disciplina de comentários/versão.

## A implantação em uma linha

Diga a qualquer assistente de IA para programação:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

A IA lê o `AGENTS.md`, executa `python scripts/distill.py`, relata o que implantou. Pronto.

Consulte [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) para o contrato completo.

## Implantação manual (sem IA)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Qualquer SO, direto
python scripts/distill.py
```

Consulte [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Suporte multiplataforma

Este projeto funciona em **Windows, macOS e Linux**.

| Plataforma | Requisitos | Comando de implantação |
|------------|------------|------------------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| Qualquer SO | Python 3.9+ | `python scripts/distill.py` |

### Como funciona o suporte multiplataforma

- Todos os scripts Python usam `pathlib` (sem separadores `\` ou `/` fixos no código).
- Os caminhos das ferramentas em `adapters/registry.json` usam expansão de variáveis de ambiente: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- No macOS/Linux, variáveis de ambiente exclusivas do Windows (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) automaticamente fazem fallback para caminhos no estilo XDG (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` é para Windows; `deploy.sh` é para macOS/Linux. Ambos chamam o mesmo `python scripts/distill.py`.

### Ferramentas específicas por plataforma

| Ferramenta | Windows | macOS | Linux | Observação |
|------------|---------|-------|-------|------------|
| Claude Desktop | ✓ | — | — | Aplicativo exclusivo do Windows; detecção é ignorada no macOS/Linux |
| ChatGPT Desktop | ✓ | — | — | Aplicativo exclusivo do Windows; detecção é ignorada no macOS/Linux |
| Cursor | ✓ | ✓ | ✓ | Detecta `${APPDATA}/Cursor` (Win) ou `~/Library/Application Support/Cursor` (macOS) |
| Todas as outras | ✓ | ✓ | ✓ | Detectadas via comando CLI no PATH |

## O que há no harness — 5 pilares técnicos

O implantador sincroniza um conjunto de regras canônicas construído sobre 5 pilares da engenharia de harness de agentes:

| Pilar | O que oferece a você | Arquivo do vault | Doc |
|-------|----------------------|------------------|-----|
| **1. Compressão de tokens em modo caveman** | ~65% de redução de tokens, mais contexto utilizável | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Hierarquia Comandante-Worker** | A IA se auto-prompteia — um orquestrador, muitos workers focados; conjunto de despacho em três partes | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Engenharia de loops + Controle de Vault** | `/loop` (monitoramento) vs `/goal` (convergente); maker ≠ checker; disciplina de SHA | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. Memória profunda do repositório** | Memória em disco em três camadas (quente <3KB, conhecimento <8KB, fria ∞); recuperação híbrida de memória profunda opcional | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. Realinhamento de limite de sandbox** | Rendimento de 100% em caminhos não críticos; contrato de risco JSON para arquivos críticos | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Conceitos adicionais em camadas superiores: **engenharia de harness** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **modos de pensamento múltiplo** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **rubricas de julgamento** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **disciplina de comentários e versões** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Disciplina de comentários e versões (prevenção de slop de IA)

Assistentes de IA para programação produzem duas formas persistentes de slop que sobrevivem no repositório:

1. **Inflação de explicação** — comentários que apenas reafirmam o código (`# percorre os itens` acima de `for x in items:`). Zero informação, desperdiça tokens, apodrece quando o código muda.
2. **Acúmulo de versões** — marcadores de versão dentro do arquivo acumulados entre edições (`<!-- v2 -->`, `# v3 corrigiu X`). Apodrecimento de contexto e dívida de profundidade recursiva.

Este harness previne ambos por meio de uma **defesa em três camadas**:

| Camada | Mecanismo | Arquivo |
|--------|-----------|---------|
| **Prevenção no cânon** | REDLINES #16 (sem comentários explicativos) + #17 (sem acúmulo de versões dentro do arquivo) + disciplina de Comentário/Versão do CORE_CANON | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **Detecção por habilidade** | `harness-sensor` SENSOR-4b (slop de comentário, degradação tolerante) + SENSOR-4c (acúmulo de versões, sempre executado) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **Guarda mecânico** | `sync.py` pré-sincronização rejeita arquivos canônicos com marcadores de versão empilhados | [`scripts/sync.py`](scripts/sync.py) |

Baseado em pesquisa: arXiv 2605.02741 (Lei Inversa Volume-Qualidade), arXiv 2512.20334 (Armadilhas de Comentários), arXiv 2606.09090 (Apodrecimento de Contexto). Consulte [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) para a avaliação completa de 6 ferramentas CLI de código aberto.

## Arquitetura anti-link-rot (Vault embutido)

Todos os mecanismos externos de configuração técnica são **embutidos e armazenados em cache localmente** em `core/assets/vault/`. O implantador **não** busca esquemas de repositórios externos em tempo de execução. Este é um banco de dados local imutável de modelos:

| Arquivo do vault | Fonte embutida |
|------------------|----------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

Consulte [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Ferramentas suportadas (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Adicionar uma ferramenta é uma entrada no registry + um adapter de 6 linhas. Consulte [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Estrutura do repositório

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # Arquivo de entrada para ferramentas que reconhecem AGENTS.md
├── CLAUDE.md                  # Arquivo de entrada para ferramentas que reconhecem CLAUDE.md
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10 idiomas adicionais
├── core/assets/               # Vault, skills, runtime (hooks, settings, MCP)
├── Docs/                      # Documentação
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # Adapters de ferramentas + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                    # O próprio harness do implantador (dogfooded)
```

Consulte [`Docs/00-Overview.md`](Docs/00-Overview.md) para descrições detalhadas dos diretórios.

## Comandos rápidos

```bash
python scripts/detect.py            # ver quais ferramentas estão instaladas
python scripts/distill.py           # implantação completa: detect → sync → verify
python scripts/distill.py --global  # também sincroniza arquivos de entrada globais
python scripts/distill.py --dry-run # apenas detecção, sem gravações
python scripts/verify.py            # reverificar após uma sincronização
python scripts/sync.py --canon      # regenerar AGENTS.md após editar o cânon
```

## Como funciona (versão de 30 segundos)

1. `detect.py` lê `adapters/registry.json`, executa as verificações de detecção de cada ferramenta (binário CLI, caminho de env, dados de aplicativo).
2. `sync.py` concatena `distill/canon/*.md` em um corpo canônico único, grava no arquivo de entrada nativo de cada ferramenta detectada (fazendo backup dos arquivos existentes para `.bak` primeiro). Apenas ferramentas detectadas são gravadas.
3. `verify.py` lê de volta cada arquivo gravado e confirma se o marcador canônico está presente (verificação de truncamento zero).

Design completo: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## Perguntas frequentes

<details>
<summary><strong>O que é o Agent Harness Deploy?</strong></summary>

O Agent Harness Deploy é um implantador de harness de IA multi-ferramenta com autoimplantação. Ele detecta quais ferramentas de IA para programação você tem instaladas, então gera e sincroniza um único harness canônico (otimizado em modo caveman, multiagente, com memória, com engenharia de loops) no local de configuração nativo de cada ferramenta detectada — para que todas as suas ferramentas de IA compartilhem as mesmas regras.
</details>

<details>
<summary><strong>Como faço para implantar o harness?</strong></summary>

Diga a qualquer assistente de IA para programação: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. Ou execute manualmente: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>Quais ferramentas de IA para programação são suportadas?</strong></summary>

23 ferramentas: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Adicionar uma ferramenta exige uma entrada no registry + um adapter de 6 linhas.
</details>

<details>
<summary><strong>Ele grava configurações para ferramentas que não tenho instaladas?</strong></summary>

Não. A detecção é sagrada — apenas ferramentas realmente instaladas na sua máquina recebem a implantação. Se uma ferramenta não é detectada, ela é relatada como "não detectada" e ignorada. Pegada desnecessária zero.
</details>

<details>
<summary><strong>O que é compressão de tokens em modo caveman?</strong></summary>

O modo caveman remove enfeites (hesitação, cortesias, reafirmação da pergunta) das comunicações do agente, mantendo toda a evidência (código, caminhos, erros, valores exatos) intacta. Isso alcança ~65% de redução de tokens, efetivamente multiplicando a janela de contexto utilizável. Consulte `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>O que é a hierarquia Comandante-Worker?</strong></summary>

A thread principal (Comandante) decide, despacha e integra. Os Workers escaneiam e editam. Isso evita que o contexto principal se encha de detalhes de baixo nível, mantendo a tomada de decisão centralizada. Consulte `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>Como funciona o sistema de memória?</strong></summary>

Memória em disco em três camadas: camada quente (registry <3KB, estado por sessão <8KB), camada de conhecimento (antipadrões <8KB), camada fria (arquivo, apenas grep). O estado persiste no disco, não no contexto — então as sessões sobrevivem entre reinícios de ferramentas. Consulte `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>O que é disciplina de comentários e versões?</strong></summary>

Uma defesa em três camadas contra slop de comentários gerado por IA (inflação de explicação) e acúmulo de versões dentro do arquivo. Camada 1: red lines do cânon (#16, #17). Camada 2: habilidade harness-sensor (SENSOR-4b/4c). Camada 3: guarda mecânico do sync.py. Consulte `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>Isto é uma ferramenta de jailbreak ou remoção de segurança?</strong></summary>

Não. Esta é uma ferramenta de harness defensiva. Ela configura os arquivos de regras dos assistentes de IA para programação. Não modifica pesos do modelo, não remove guardrails de segurança e não empacota ferramentas de jailbreak. O realinhamento de limite de sandbox atua no nível de arquivo via contratos de risco JSON, não no nível do modelo removendo loops de recusa.
</details>

<details>
<summary><strong>Sob qual licença está este projeto?</strong></summary>

Licença MIT — consulte [LICENSE](LICENSE). Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>Posso adicionar minha própria ferramenta de IA?</strong></summary>

Sim. Adicionar uma ferramenta exige uma entrada em `adapters/registry.json` + uma classe de adapter de 6 linhas. Consulte `Docs/03-Tool-Adapters.md`.
</details>

## Cláusula de honestidade

O implantador faz de forma confiável: detecção, geração de configuração, sincronização de arquivos, verificação, backup. Ele não consegue fazer: decisões de gosto/estética, adivinhar o que você quer além do contrato de implantação, gravar configurações para ferramentas que não consegue detectar. Quando incerto, ele relata — não fabrica. Declaração completa em [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Nota de segurança

Este repositório é uma ferramenta de harness **defensiva**. Ele configura os arquivos de regras dos assistentes de IA para programação. Ele **não** modifica pesos do modelo, **não** remove guardrails de segurança e **não** empacota ou endossa ferramentas de jailbreak/remoção de segurança. O projeto Heretic é referenciado no glossário apenas como parte do cenário de interpretabilidade que informou a compreensão do harness sobre vetores de direcionamento — ele não é usado aqui. Consulte [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Requisitos

- Python 3.9+
- Pelo menos uma ferramenta de IA para programação suportada instalada (caso contrário, não há para onde implantar)

## Licença

MIT — consulte [LICENSE](LICENSE).

## Referências

Consulte [`Docs/REFERENCES.md`](Docs/REFERENCES.md) para referências de fontes por pilar.

## Índice de documentação

| Doc | Tópico |
|-----|--------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Visão geral & índice |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Design completo do sistema |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | Como o "deploy:" funciona |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Locais de configuração por ferramenta |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Comandante + Workers + auto-orquestração |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Redução de alucinação |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Problemas comuns |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Termos & fontes |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | Slop de comentário de IA + acúmulo de versões: avaliação de ferramentas CLI |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Sistema Nuwa + Nuwa Team (raciocínio paralelo, diversidade cognitiva) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Compressão de tokens (antigo Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Memória em três camadas (antigo Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Engenharia de loops, componentes 5+1 (antigo Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | Sistema em torno do modelo (antigo Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, disciplina de SHA (antigo Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Hard stops + control plane (antigo Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Critérios de decisão externalizados (antigo Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Delegação Comandante-Worker (antigo Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Vault de recursos embutidos anti-link-rot |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Camada de runtime: hooks, settings, modelos de MCP |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Atribuição do nuwa-skill vendored & inventário de arquivos |

---

<details>
<summary><em>Metadados SEO / AEO / GEO / LLMO</em></summary>

**Nome do projeto:** Agent Harness Deploy

**Descrição em uma linha:** Harness de IA multi-ferramenta com autoimplantação — uma fonte canônica, 23 destinos de ferramentas de IA para programação.

**Palavras-chave:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, harness de IA para programação, sincronização de configuração multi-ferramenta, implantador de harness de agente, regras de assistente de IA, compressão de tokens caveman, engenharia de loops, protocolo de memória de agente, engenharia de harness, prevenção de slop de IA, disciplina de comentários, prevenção de acúmulo de versões

**Fatos-chave para citação por IA/LLM:**
- 23 ferramentas de IA para programação suportadas (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot, etc.)
- Uma fonte canônica (`distill/canon/`), muitos destinos nativos por ferramenta
- 5 pilares técnicos: compressão caveman, Comandante-Worker, engenharia de loops, memória profunda, limite de sandbox
- Disciplina de comentários/versões em três camadas: red lines do cânon + sensores de habilidade + guarda mecânico
- Multiplataforma: Windows, macOS, Linux (Python 3.9+)
- Licença MIT, copyright masteryee-labs
- Anti-link-rot: todos os esquemas externos embutidos em `core/assets/vault/`
- Comando de implantação: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Público-alvo:** Desenvolvedores que usam múltiplos assistentes de IA para programação e desejam regras consistentes em todas as ferramentas. Contribuidores de código aberto, equipes de engenharia AI-first, desenvolvedores solo usando Claude Code + Cursor + Codex simultaneamente.

**Categoria:** Ferramentas de desenvolvedor > Assistentes de IA para programação > Gerenciamento de configuração > Engenharia de harness de agente
</details>
