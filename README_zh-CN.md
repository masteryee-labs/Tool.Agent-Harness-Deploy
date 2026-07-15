# Agent Harness Deploy

**自部署的跨工具 AI 线束——一套规范源码，部署到 Claude Code、Codex、Cursor、Devin、Antigravity、Windsurf、GitHub Copilot 等 16+ 工具。**

> 循环工程 · 上下文工程 · 线束工程 · 智能体记忆 · 注释与版本纪律——一条命令即可将完整线束部署到你所有的 AI 编程工具。

> **语言：** [English](README.md) | [繁體中文](README_zh-TW.md) | **简体中文（本页）** | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## 它做什么

你给任意 AI 编程助手这个仓库的 GitHub 链接，然后说：

> **帮我部署：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI 会克隆仓库、运行部署器，然后它会：

1. **检测**你的机器上安装了哪些 AI 编程工具（支持 23 个工具）。
2. **生成**一套规范线束——经过穴居人优化、多智能体、记忆增强、循环工程化——源自 `distill/canon/`。
3. **部署**到每个已检测工具的原生配置位置（`.claude/`、`.codex/`、`.devin/`、`AGENTS.md`、`.cursor/rules/`）。
4. **验证**每个写入的文件，通过回读确认（零截断检查）。

**结果：**无论你接下来打开哪个 AI 工具——它们都共享**同一套**规则、记忆协议、编排器、技能、钩子和 MCP 配置。再也不用维护三份规则副本。`.claude/`、`.codex/`、`.devin/`、`AGENTS.md` 之间再也不漂移。

只有**实际安装**的工具才会被部署。未检测到的工具不会写入任何内容。你也可以手动部署——无需 AI。

## 为什么

每个 AI 编程工具都把配置存放在不同的位置和格式：

| 工具 | 规则存放位置 |
|------|-------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

用了三个工具，你就得维护三份副本。它们会漂移。你会忘记哪份是最新的。**Agent Harness Deploy 解决了这个问题：一个源（`distill/canon/`），多个汇。**

与仅在配置文件之间复制文本的简单规则同步工具不同，本工具部署的是一套**完整的智能体线束**：规则 + 技能 + 工作者角色 + 记忆协议 + 循环工程 + 钩子 + MCP + 保险库资产 + 注释/版本纪律传感器。

## 一行部署

告诉任意 AI 编程助手：

```
帮我部署：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI 会读取 `AGENTS.md`，运行 `python scripts/distill.py`，报告部署了什么。完成。

完整契约请见 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md)。

## 手动部署（无需 AI）

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# 任意操作系统，直接运行
python scripts/distill.py
```

请见 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy。

## 跨平台支持

本项目可在 **Windows、macOS 和 Linux** 上运行。

| 平台 | 要求 | 部署命令 |
|------|------|---------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| 任意操作系统 | Python 3.9+ | `python scripts/distill.py` |

### 跨平台如何工作

- 所有 Python 脚本使用 `pathlib`（不硬编码 `\` 或 `/` 分隔符）。
- `adapters/registry.json` 中的工具路径使用环境变量展开：`${HOME}`、`${APPDATA}`、`${LOCALAPPDATA}`、`~`。
- 在 macOS/Linux 上，Windows 专属的环境变量（`${APPDATA}`、`${LOCALAPPDATA}`、`${USERPROFILE}`）会自动回退到 XDG 风格路径（`~/.config`、`~/.local/share`、`~`）。
- `deploy.ps1` 用于 Windows；`deploy.sh` 用于 macOS/Linux。两者都调用相同的 `python scripts/distill.py`。

### 平台专属工具

| 工具 | Windows | macOS | Linux | 说明 |
|------|---------|-------|-------|------|
| Claude Desktop | ✓ | — | — | Windows 专属应用；macOS/Linux 上检测会跳过 |
| ChatGPT Desktop | ✓ | — | — | Windows 专属应用；macOS/Linux 上检测会跳过 |
| Cursor | ✓ | ✓ | ✓ | 检测 `${APPDATA}/Cursor`（Windows）或 `~/Library/Application Support/Cursor`（macOS） |
| 其他所有工具 | ✓ | ✓ | ✓ | 通过 PATH 上的 CLI 命令检测 |

## 线束内容——5 大技术支柱

部署器同步一套基于智能体线束工程 5 大支柱构建的规范规则集：

| 支柱 | 给你带来什么 | 保险库文件 | 文档 |
|------|------------|-----------|------|
| **1. 穴居人 token 压缩** | 约 65% token 削减，更多可用上下文 | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. 指挥官-工作者层级** | AI 自我提示——一个编排器，多个专注工作者；派发三件套 | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. 循环工程 + 保险库控制** | `/loop`（监控）vs `/goal`（收敛）；制造者 ≠ 检查者；SHA 纪律 | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. 深度仓库记忆** | 三层磁盘记忆（热层 <3KB，知识层 <8KB，冷层 ∞）；可选深度记忆混合检索 | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. 沙箱边界重对齐** | 非关键路径 100% 产出；关键文件 JSON 风险契约 | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

在此之上叠加的额外概念：**线束工程**（[`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)）、**多思维模式**（[`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)）、**判断准则**（[`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)）、**注释与版本纪律**（[`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)）。

## 注释与版本纪律（防止 AI 垃圾）

AI 编程助手会产生两种持久存在于仓库中的垃圾：

1. **解释膨胀**——复述代码的注释（`for x in items:` 上面的 `# loop through items`）。零信息量，浪费 token，代码变更后即腐烂。
2. **版本堆叠**——跨编辑累积的文件内版本标记（`<!-- v2 -->`、`# v3 fixed X`）。上下文腐烂和递归深度债务。

本线束通过**三层防御**来防止这两种问题：

| 层 | 机制 | 文件 |
|----|------|------|
| **规范预防** | REDLINES #16（禁止解释性注释）+ #17（禁止文件内版本堆叠）+ CORE_CANON 注释/版本纪律 | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **技能检测** | `harness-sensor` SENSOR-4b（注释垃圾，优雅降级）+ SENSOR-4c（版本堆叠，始终运行） | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **机械守卫** | `sync.py` 同步前门控，拒绝含有堆叠版本标记的规范文件 | [`scripts/sync.py`](scripts/sync.py) |

研究支撑：arXiv 2605.02741（质量-数量逆定律）、arXiv 2512.20334（注释陷阱）、arXiv 2606.09090（上下文腐烂）。对 6 款开源 CLI 工具的完整评估请见 [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)。

## 防链接腐烂架构（嵌入式保险库）

所有外部技术配置机制都**内嵌并本地缓存**在 `core/assets/vault/` 中。部署器在运行时**不会**从外部仓库获取 schema。这是一个不可变的本地模板数据库：

| 保险库文件 | 嵌入来源 |
|----------|---------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

请见 [`core/assets/vault/README.md`](core/assets/vault/README.md)。

## 支持的工具（23 个）

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

添加一个工具只需一条 registry 条目 + 一个 6 行适配器。请见 [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md)。

## 仓库布局

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

详细目录说明请见 [`Docs/00-Overview.md`](Docs/00-Overview.md)。

## 快速命令

```bash
python scripts/detect.py            # see which tools are installed
python scripts/distill.py           # full deploy: detect → sync → verify
python scripts/distill.py --global  # also sync global entry files
python scripts/distill.py --dry-run # detect only, no writes
python scripts/verify.py            # re-verify after a sync
python scripts/sync.py --canon      # regenerate AGENTS.md after editing canon
```

## 工作原理（30 秒版）

1. `detect.py` 读取 `adapters/registry.json`，运行每个工具的检测检查（CLI 二进制、环境路径、应用数据）。
2. `sync.py` 将 `distill/canon/*.md` 拼接为一个规范主体，写入每个已检测工具的原生入口文件（先将现有文件备份为 `.bak`）。只有已检测的工具才会被写入。
3. `verify.py` 回读每个写入的文件，确认规范标记存在（零截断检查）。

完整设计：[`Docs/01-Architecture.md`](Docs/01-Architecture.md)。

## 常见问题

<details>
<summary><strong>什么是 Agent Harness Deploy？</strong></summary>

Agent Harness Deploy 是一个自部署的跨工具 AI 线束部署器。它会检测你安装了哪些 AI 编程工具，然后生成并同步一套规范线束（穴居人优化、多智能体、记忆增强、循环工程化）到每个已检测工具的原生配置位置——这样你所有的 AI 工具都共享同一套规则。
</details>

<details>
<summary><strong>如何部署线束？</strong></summary>

告诉任意 AI 编程助手：`帮我部署：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`。或手动运行：`python scripts/distill.py`（Windows/macOS/Linux，Python 3.9+）。
</details>

<details>
<summary><strong>支持哪些 AI 编程工具？</strong></summary>

23 个工具：Claude Code、Antigravity (AGY)、Codex / Codex CLI、Devin / Devin CLI、Cursor、Claude Desktop、OpenCode、OpenClaw、Hermes、ZCode、Kimi Code、AGY CLI、Codex CLI、Devin CLI、Claude Code for VS Code、Codex IDE Extension、GitHub Copilot、Gemini Code Assist、Cline、Roo Code、Continue、Windsurf、ChatGPT Desktop。添加一个工具只需一条 registry 条目 + 一个 6 行适配器。
</details>

<details>
<summary><strong>它会为我没有安装的工具写入配置吗？</strong></summary>

不会。检测是神圣的——只有实际安装在你机器上的工具才会被部署。如果某个工具未被检测到，它会报告为"未检测到"并跳过。零不必要的足迹。
</details>

<details>
<summary><strong>什么是穴居人 token 压缩？</strong></summary>

穴居人模式会剥离智能体通信中的填充内容（对冲、客套、复述问题），同时保留所有证据（代码、路径、错误、精确值）原样不变。这实现了约 65% 的 token 削减，有效倍增了可用上下文窗口。请见 `distill/canon/CAVEMAN_PROTOCOL.md`。
</details>

<details>
<summary><strong>什么是指挥官-工作者层级？</strong></summary>

主线程（指挥官）负责决策、派发和整合。工作者负责扫描和编辑。这能防止主上下文被低级细节填满，同时保持决策集中。请见 `distill/orchestrator/COMMANDER.md`。
</details>

<details>
<summary><strong>记忆系统如何工作？</strong></summary>

三层磁盘记忆：热层（注册表 <3KB，每会话状态 <8KB）、知识层（反模式 <8KB）、冷层（归档，仅 grep）。状态持久化在磁盘上而非上下文中——因此会话可在工具重启后存活。请见 `distill/canon/MEMORY_PROTOCOL.md`。
</details>

<details>
<summary><strong>什么是注释与版本纪律？</strong></summary>

针对 AI 生成的注释垃圾（解释膨胀）和文件内版本堆叠的三层防御。第一层：规范红线（#16、#17）。第二层：harness-sensor 技能（SENSOR-4b/4c）。第三层：sync.py 机械守卫。请见 `Docs/14-Comment-Version-Discipline.md`。
</details>

<details>
<summary><strong>这是一个越狱或移除安全工具吗？</strong></summary>

不是。这是一个防御性线束工具。它配置 AI 编程助手的规则文件。它不会修改模型权重，不会移除安全护栏，也不会捆绑越狱工具。沙箱边界重对齐通过 JSON 风险契约在文件层面工作，而非在模型层面通过移除拒绝循环来工作。
</details>

<details>
<summary><strong>本项目使用什么许可证？</strong></summary>

MIT License——请见 [LICENSE](LICENSE)。Copyright (c) masteryee-labs。
</details>

<details>
<summary><strong>我可以添加自己的 AI 工具吗？</strong></summary>

可以。添加一个工具需要在 `adapters/registry.json` 中添加一条条目 + 一个 6 行适配器类。请见 `Docs/03-Tool-Adapters.md`。
</details>

## 诚实条款

部署器能可靠完成：检测、配置生成、文件同步、验证、备份。它不能完成：品味/审美决策、猜测你在部署契约之外的意图、为它无法检测的工具写配置。不确定时，它会报告——不会编造。完整声明请见 [`Docs/00-Overview.md`](Docs/00-Overview.md)。

## 安全声明

本仓库是一个**防御性**线束工具。它配置 AI 编程助手的规则文件。它**不会**修改模型权重，**不会**移除安全护栏，也**不会**捆绑或背书越狱/移除安全工具。Heretic 项目仅在术语表中作为启发本线束对引导向量理解的解释性景观的一部分被引用——此处不使用。请见 [`Docs/13-Glossary.md`](Docs/13-Glossary.md)。

## 环境要求

- Python 3.9+
- 至少安装一个受支持的 AI 编程工具（否则没有部署目标）

## 许可证

MIT——请见 [LICENSE](LICENSE)。

## 参考文献

按支柱分类的来源引用请见 [`Docs/REFERENCES.md`](Docs/REFERENCES.md)。

## 文档索引

| 文档 | 主题 |
|------|------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | 概览与索引 |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | 完整系统设计 |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | "帮我部署：" 如何工作 |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | 各工具配置位置 |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | 指挥官 + 工作者 + 自编排 |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | 幻觉减少 |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | 常见问题 |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | 术语与来源 |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI 注释垃圾 + 版本堆叠：CLI 工具评估 |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Nuwa 系统 + Nuwa 团队（并行推理，认知多样性） |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Token 压缩（原 Docs/05） |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | 三层记忆（原 Docs/06） |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | 循环工程，5+1 组件（原 Docs/07） |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | 模型周围的系统（原 Docs/08） |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | 制造者 ≠ 检查者，SHA 纪律（原 Docs/10） |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | 硬停止 + 控制平面（原 Docs/harness_control_plane） |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | 外部化决策准则（原 Docs/harness_rubrics） |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | 指挥官-工作者委派（原 Docs/Agents/commander） |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | 防链接腐烂嵌入式资产保险库 |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | 运行时层：钩子、设置、MCP 模板 |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | 内嵌 nuwa-skill 归属与文件清单 |

---

<details>
<summary><em>SEO / AEO / GEO / LLMO 元数据</em></summary>

**项目名称：** Agent Harness Deploy

**一句话描述：** 自部署的跨工具 AI 线束——一套规范源码，23 个 AI 编程工具汇。

**关键词：** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, AI 编程线束, 跨工具 AI 配置同步, 智能体线束部署器, 多智能体线束, 穴居人 token 压缩, 循环工程, 智能体记忆协议, 线束工程, AI 垃圾防治, 注释纪律, 版本堆叠防治

**供 AI/LLM 引用的关键事实：**
- 支持 23 个 AI 编程工具（Claude Code、Codex、Cursor、Devin、Antigravity、Windsurf、GitHub Copilot 等）
- 一套规范源码（`distill/canon/`），多个工具原生汇
- 5 大技术支柱：穴居人压缩、指挥官-工作者、循环工程、深度记忆、沙箱边界
- 三层注释/版本纪律：规范红线 + 技能传感器 + 机械守卫
- 跨平台：Windows、macOS、Linux（Python 3.9+）
- MIT License，版权 masteryee-labs
- 防链接腐烂：所有外部 schema 内嵌于 `core/assets/vault/`
- 部署命令：`帮我部署：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**目标受众：** 同时使用多个 AI 编程助手、希望在所有工具间保持规则一致的开发者。开源贡献者、AI 优先工程团队、同时使用 Claude Code + Cursor + Codex 的独立开发者。

**分类：** 开发者工具 > AI 编程助手 > 配置管理 > 智能体线束工程
</details>
