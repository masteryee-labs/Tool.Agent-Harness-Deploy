# Agent Harness Deploy

**跨工具 AI harness 自动部署器 — 一份通用规则，同步到 Claude Code、Codex、Cursor、Devin、Antigravity 等 14 个工具。**

> 循环工程 · 上下文工程 · Harness 工程 · Agent 记忆 — 一行指令把完整 harness 部署到你所有的 AI 编程工具。

> 语言：**English**([README.md](README.md)) | [繁體中文](README_zh-TW.md) | **简体中文**（本页）

---

## 它做什么

你把这个 repo 的 GitHub 链接贴给任何 AI 编程助手，说：

> **帮我部署：https://github.com/\<you\>/agent-harness-deploy**
> （英文：deploy: https://github.com/\<you\>/agent-harness-deploy）

AI 会 clone 这个 repo、运行部署器，部署器会：

1. **检测**你电脑装了哪些 AI 编程工具（14 种）。
2. **生成**一份通用工作环境（穴居人优化、多代理、记忆体、循环工程化），来源是 `distill/canon/` + `core/assets/vault/`。
3. **同步**到每个检测到的工具的原生配置位置——只同步有装的工具，没装的不碰。
4. **验证**每个写入的文件（读回确认，零截断）。

**结果：**你下次打开任何一个 AI 工具——Claude Code、Antigravity、Codex、Devin、Cursor
等共 14 种——它们都共享**同一份**规则、记忆协议、指挥官、技能。不用再维护三份规则副本，
不用再担心 `.claude/`、`.codex/`、`.devin/`、`AGENTS.md` 之间的漂移。

只有**实际安装**的工具会被同步，没装的工具不会被写入（零多余足迹）。也可以手动部署，不需要 AI。

## 为什么需要

不同 AI 工具把配置存在不同地方、不同格式：

| 工具 | 规则存放位置 |
|------|-------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Claude Desktop | `claude_desktop_config.json` |

同时用三个就要维护三份，它们会漂移，你会忘了哪份是最新的。Agent Harness Deploy 解决这件事：
**一个来源（`distill/canon/`），多个目标。**

## 一行部署

跟任何 AI 编程助手说：

```
帮我部署：https://github.com/<you>/agent-harness-deploy
```

AI 会读 `AGENTS.md`（或 `CLAUDE.md`）、执行 `python scripts/distill.py`、回报同步了什么。完成。

完整流程见 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md)。

## 手动部署（不用 AI）

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# 任何系统，直接执行
python scripts/distill.py
```

详见 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy。

## 工作环境里有什么——5 大技术支柱

部署器同步的通用规则集建立在 2026 工作环境工程的 5 大支柱上：

| 支柱 | 带来什么 | Vault 文件 | 文档 |
|------|---------|----------|------|
| **1. 穴居人 Token 压缩** | 约 65% token 缩减，更多可用 context | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. 指挥官-执行者层级** | AI 自己 prompt 自己——一个指挥官，多个专注执行者；派工三件套 | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. 循环工程与 Vault 控制** | `/loop`（持续监控）vs `/goal`（收敛目标）；作者 ≠ 验收；SHA 纪律 | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. 深层 Repo 记忆** | 三层磁盘记忆（热 <3KB、知识 <8KB、冷 ∞）；可选深层记忆混合检索 | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. 沙箱边界重对齐** | 非关键路径 100% 产出率；关键文件 JSON 风险合约 | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

## 防链接腐朽架构（Embedded Vault）

所有外部技术配置机制都**内嵌并本地缓存**在 `core/assets/vault/`。部署器**不会**在运行时
从外部 repo 抓取 schema。这是不可变的本地模板数据库：

| Vault 文件 | 内嵌来源 |
|----------|---------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

详见 [`core/assets/vault/README.md`](core/assets/vault/README.md)。

## 支持工具（14 种）

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude
Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI

新增工具只需一个 registry 条目 + 6 行 adapter。见
[`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md)。

## Repo 结构

```
agent-harness-deploy/
├── AGENTS.md                  # 给读 AGENTS.md 的工具的入口文件
├── CLAUDE.md                  # 给读 CLAUDE.md 的工具的入口文件
├── README.md / README_zh-TW.md / README_zh-CN.md
├── core/assets/               # Vault、skills、runtime（hooks、settings、MCP）
├── Docs/                      # 文档
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # 工具 adapter + registry.json
├── scripts/                   # detect、distill、sync、verify、deploy、worktree、plan_dispatch
└── .agent/                    # 部署器自己的工作环境（自己用自己）
```

详见 [`Docs/00-Overview.md`](Docs/00-Overview.md) 的目录说明。

## 常用命令

```bash
python scripts/detect.py            # 看装了哪些工具
python scripts/distill.py           # 完整部署：检测 → 同步 → 验证
python scripts/distill.py --global  # 也同步全局入口文件
python scripts/distill.py --dry-run # 只检测，不写入
python scripts/verify.py            # 同步后重新验证
python scripts/sync.py --canon      # 改完 canon 后重新生成 AGENTS.md
```

## 运作原理（30 秒版）

1. `detect.py` 读 `adapters/registry.json`，对每个工具跑检测检查（全局二进制、环境路径、app data）。
2. `sync.py` 把 `distill/canon/*.md` 串成一份通用内容，写进每个检测到的工具的原生入口文件
   （覆盖前先备份成 `.bak`）。只有检测到的工具才被写入。
3. `verify.py` 读回每个写入的文件，确认通用标记存在（零截断检查）。

完整设计：[`Docs/01-Architecture.md`](Docs/01-Architecture.md)。

## 诚实条款

部署器能可靠做到：检测、配置生成、文件同步、验证、备份。做不到：品味/美感决策、
猜测部署合约以外的需求、帮没检测到的工具写配置。不确定时就回报，不编造。
较罕见工具的配置 schema 若因本地信息不足而省略，会标示为 `Dynamic Stub - Pending System Context`，
**不会**捏造不存在的 CLI 旗标。完整说明见 [`Docs/00-Overview.md`](Docs/00-Overview.md)。

## 安全说明

这个 repo 是**防御性**的工作环境工具，只配置 AI 编程助手的规则文件。它**不会**修改模型权重、
**不会**移除安全护栏、**不会**捆绑或背书越狱/移除安全的工具。Pillar 5 的"沙箱边界重对齐"
是在**文件层级**透过 JSON 风险合约强制安全，不是在模型层级移除拒绝循环。术语表里提到 Heretic 项目，
只是因为它属于可解释性景观的一部分、影响了工作环境对 steering vector 的理解——本 repo 并未使用。
见 [`Docs/13-Glossary.md`](Docs/13-Glossary.md)。

## 需求

- Python 3.9+
- 至少安装一个支持的 AI 编程工具（否则没有同步目标）

## 授权

MIT — 见 [LICENSE](LICENSE)。

## 文档索引

| 文档 | 主题 |
|------|------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | 总览与索引 |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | 完整系统设计 |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | 「帮我部署」怎么运作 |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | 各工具配置位置 |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | 指挥官 + 执行者 + 自我编排 |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | 降低幻觉 |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | 常见问题 |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | 术语与来源 |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | 女娲系统 + 女娲团队（平行推理、认知多样性） |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Token 压缩（原 Docs/05-Caveman-Optimization.md） |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | 三层记忆（原 Docs/06-Memory-System.md） |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | 循环工程、5+1 组件（原 Docs/07-Loop-Engineering.md） |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | 模型外围的系统（原 Docs/08-Harness-Engineering.md） |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | 作者 ≠ 验收、SHA 纪律（原 Docs/10-Verification-Protocol.md） |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | 指挥官-执行者委派架构 + 派工三件套（原 Docs/Agents/commander.md） |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | 8 步控制循环生命周期（原 Docs/harness_control_plane.md） |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | 工作区评分规则（正/负例）（原 Docs/harness_rubrics.md） |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | 防链接腐朽内嵌资产库 |

## 参考资料

各支柱的来源链接见 [`Docs/REFERENCES.md`](Docs/REFERENCES.md)。
