# Agent Harness Deploy

**跨工具 AI harness 自動部署器 — 一份共通規則，同步到 Claude Code、Codex、Cursor、Devin、Antigravity 等 14 個工具。**

> 迴圈工程 · 上下文工程 · Harness 工程 · Agent 記憶 — 一行指令把完整 harness 部署到你所有的 AI 程式工具。

> 語言：**English**([README.md](README.md)) | **繁體中文**（本頁） | [简体中文](README_zh-CN.md)

---

## 它做什麼

你把這個 repo 的 GitHub 連結貼給任何 AI 程式助手，說：

> **幫我部屬：https://github.com/\<you\>/agent-harness-deploy**
> （英文：deploy: https://github.com/\<you\>/agent-harness-deploy）

AI 會 clone 這個 repo、執行部署器，部署器會：

1. **偵測**你電腦裝了哪些 AI 程式工具（14 種）。
2. **產生**一份共通工作環境（穴居人優化、多代理人、記憶體、迴圈工程化），來源是 `distill/canon/` + `core/assets/vault/`。
3. **同步**到每個偵測到的工具的原生設定位置——只同步有裝的工具，沒裝的不碰。
4. **驗證**每個寫入的檔案（讀回確認，零截斷）。

**結果：**你下次打開任何一個 AI 工具——Claude Code、Antigravity、Codex、Devin、Cursor
等共 14 種——它們都共用**同一份**規則、記憶協定、指揮官、技能。不用再維護三份規則副本，
不用再擔心 `.claude/`、`.codex/`、`.devin/`、`AGENTS.md` 之間的漂移。

只有**實際安裝**的工具會被同步，沒裝的工具不會被寫入（零多餘足跡）。也可以手動部屬，不需要 AI。

## 為什麼需要

不同 AI 工具把設定存在不同地方、不同格式：

| 工具 | 規則存放位置 |
|------|-------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Claude Desktop | `claude_desktop_config.json` |

同時用三個就要維護三份，它們會漂移，你會忘了哪份是最新的。Agent Harness Deploy 解決了這件事：
**一個來源（`distill/canon/`），多個目標。**

## 一行部屬

跟任何 AI 程式助手說：

```
幫我部屬：https://github.com/<you>/agent-harness-deploy
```

AI 會讀 `AGENTS.md`（或 `CLAUDE.md`）、執行 `python scripts/distill.py`、回報同步了什麼。完成。

完整流程見 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md)。

## 手動部屬（不用 AI）

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# 任何系統，直接執行
python scripts/distill.py
```

詳見 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy。

## 工作環境裡有什麼——5 大技術支柱

部署器同步的共通規則集建立在 2026 工作環境工程的 5 大支柱上：

| 支柱 | 帶來什麼 | Vault 檔 | 文件 |
|------|---------|---------|------|
| **1. 穴居人 Token 壓縮** | 約 65% token 縮減，更多可用 context | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. 指揮官-做事者階層** | AI 自己 prompt 自己——一個指揮官，多個專注執行者；派工三件套 | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. 迴圈工程與 Vault 控制** | `/loop`（持續監控）vs `/goal`（收斂目標）；作者 ≠ 驗收；SHA 紀律 | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. 深層 Repo 記憶** | 三層磁碟記憶（熱 <3KB、知識 <8KB、冷 ∞）；可選深層記憶混合檢索 | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. 沙箱邊界重對齊** | 非關鍵路徑 100% 產出率；關鍵檔案 JSON 風險合約 | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

## 防連結腐朽架構（Embedded Vault）

所有外部技術設定機制都**內嵌並本地快取**在 `core/assets/vault/`。部署器**不會**在執行時
從外部 repo 抓取 schema。這是不可變的本地範本資料庫：

| Vault 檔 | 內嵌來源 |
|----------|---------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

詳見 [`core/assets/vault/README.md`](core/assets/vault/README.md)。

## 支援工具（14 種）

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude
Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI

新增工具只需一個 registry 條目 + 6 行 adapter。見
[`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md)。

## Repo 結構

```
agent-harness-deploy/
├── AGENTS.md                  # 給讀 AGENTS.md 的工具的入口檔
├── CLAUDE.md                  # 給讀 CLAUDE.md 的工具的入口檔
├── README.md / README_zh-TW.md / README_zh-CN.md
├── core/assets/               # Vault、skills、runtime（hooks、settings、MCP）
├── Docs/                      # 文件
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # 工具 adapter + registry.json
├── scripts/                   # detect、distill、sync、verify、deploy、worktree、plan_dispatch
└── .agent/                    # 部署器自己的工作環境（自己用自己）
```

詳見 [`Docs/00-Overview.md`](Docs/00-Overview.md) 的目錄說明。

## 常用指令

```bash
python scripts/detect.py            # 看裝了哪些工具
python scripts/distill.py           # 完整部屬：偵測 → 同步 → 驗證
python scripts/distill.py --global  # 也同步全域入口檔
python scripts/distill.py --dry-run # 只偵測，不寫入
python scripts/verify.py            # 同步後重新驗證
python scripts/sync.py --canon      # 改完 canon 後重新產生 AGENTS.md
```

## 運作原理（30 秒版）

1. `detect.py` 讀 `adapters/registry.json`，對每個工具跑偵測檢查（全域二進位檔、環境路徑、app data）。
2. `sync.py` 把 `distill/canon/*.md` 串成一份共通內容，寫進每個偵測到的工具的原生入口檔
   （覆寫前先備份成 `.bak`）。只有偵測到的工具才被寫入。
3. `verify.py` 讀回每個寫入的檔案，確認共通標記存在（零截斷檢查）。

完整設計：[`Docs/01-Architecture.md`](Docs/01-Architecture.md)。

## 誠實條款

部署器能可靠做到：偵測、設定產生、檔案同步、驗證、備份。做不到：品味/美感決策、
猜測部屬合約以外的需求、幫沒偵測到的工具寫設定。不確定時就回報，不編造。
較罕見工具的設定 schema 若因本地資訊不足而省略，會標示為 `Dynamic Stub - Pending System Context`，
**不會**捏造不存在的 CLI 旗標。完整說明見 [`Docs/00-Overview.md`](Docs/00-Overview.md)。

## 安全說明

這個 repo 是**防禦性**的工作環境工具，只設定 AI 程式助手的規則檔。它**不會**修改模型權重、
**不會**移除安全護欄、**不會**捆綁或背書越獄/移除安全的工具。Pillar 5 的「沙箱邊界重對齊」
是在**檔案層級**透過 JSON 風險合約強制安全，不是在模型層級移除拒絕迴圈。名詞表裡提到 Heretic 專案，
只是因為它屬於可解釋性景觀的一部分、影響了工作環境對 steering vector 的理解——本 repo 並未使用。
見 [`Docs/13-Glossary.md`](Docs/13-Glossary.md)。

## 需求

- Python 3.9+
- 至少安裝一個支援的 AI 程式工具（否則沒有同步目標）

## 授權

MIT — 見 [LICENSE](LICENSE)。

## 文件索引

| 文件 | 主題 |
|------|------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | 總覽與索引 |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | 完整系統設計 |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | 「幫我部屬」怎麼運作 |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | 各工具設定位置 |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | 指揮官 + 做事者 + 自我編排 |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | 降低幻覺 |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | 常見問題 |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | 名詞與來源 |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | 女媧系統 + 女媧團隊（平行推理、認知多樣性） |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Token 壓縮（原 Docs/05） |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | 三層記憶（原 Docs/06） |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | 迴圈工程、5+1 組件（原 Docs/07） |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | 模型外圍的系統（原 Docs/08） |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | 作者 ≠ 驗收、SHA 紀律（原 Docs/10） |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | 紅線 + 控制迴圈（原 Docs/harness_control_plane） |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | 評分規則（原 Docs/harness_rubrics） |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | 指揮官委派（原 Docs/Agents/commander） |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | 防連結腐朽內嵌資產庫 |

## 參考資料

各支柱的來源連結見 [`Docs/REFERENCES.md`](Docs/REFERENCES.md)。
