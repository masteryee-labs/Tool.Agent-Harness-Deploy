# Agent Harness Deploy

**自我部署的跨工具 AI 線束——一份標準來源，部署到 Claude Code、Codex、Cursor、Devin、Antigravity、Windsurf、GitHub Copilot 等 16 種以上工具。**

> 迴圈工程 · 上下文工程 · 線束工程 · 智能體記憶 · 註解與版本紀律——一個指令即可將完整線束部署到你所有的 AI 程式工具。

> **語言：** [English](README.md) | **繁體中文（本頁）** | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## 功能簡介

你只需給任何 AI 程式助手這個 repo 的 GitHub URL，然後說：

> **幫我部屬：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI 會複製 repo、執行部署器，然後它會：

1. **偵測**你的機器上安裝了哪些 AI 程式工具（支援 23 種工具）。
2. **生成**一份標準線束——原始人最佳化、多智能體、記憶啟用、迴圈工程化——源自 `distill/canon/`。
3. **部署**到每個偵測到的工具的原生設定位置（`.claude/`、`.codex/`、`.devin/`、`AGENTS.md`、`.cursor/rules/`）。
4. **驗證**每個寫入的檔案，讀回確認（零截斷檢查）。

**結果：**無論你接下來開啟哪個 AI 工具——它們全部共享**相同**的規則、記憶協定、指揮官、技能、hooks 和 MCP 設定。不再維護三份規則副本。不再有 `.claude/`、`.codex/`、`.devin/`、`AGENTS.md` 之間的漂移。

只有**實際安裝**的工具才會被部署。未偵測到的工具不會寫入任何內容。你也可以手動部署——不需要 AI。

## 為什麼需要

每個 AI 程式工具都把設定存在不同的位置和格式：

| 工具 | 規則存放位置 |
|------|----------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

同時使用三個工具，你就得維護三份副本。它們會漂移。你會忘記哪份是最新的。**Agent Harness Deploy 解決了這個問題：一份來源（`distill/canon/`），多個接收端。**

不同於只在設定檔之間複製文字的簡單規則同步工具，這裡部署的是一套**完整的智能體線束**：規則 + 技能 + worker 人格 + 記憶協定 + 迴圈工程 + hooks + MCP + vault 資產 + 註解/版本紀律感測器。

## 一行部署

告訴任何 AI 程式助手：

```
幫我部屬：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI 會讀取 `AGENTS.md`、執行 `python scripts/distill.py`、回報部署了什麼。完成。

完整部署合約請見 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md)。

## 手動部署（不需 AI）

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# 任何作業系統，直接執行
python scripts/distill.py
```

請見 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy。

## 跨平台支援

本專案可在 **Windows、macOS 和 Linux** 上運作。

| 平台 | 需求 | 部署指令 |
|----------|-------------|----------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| 任何作業系統 | Python 3.9+ | `python scripts/distill.py` |

### 跨平台如何運作

- 所有 Python 腳本使用 `pathlib`（不硬編碼 `\` 或 `/` 分隔符）。
- `adapters/registry.json` 中的工具路徑使用環境變數展開：`${HOME}`、`${APPDATA}`、`${LOCALAPPDATA}`、`~`。
- 在 macOS/Linux 上，Windows 專屬環境變數（`${APPDATA}`、`${LOCALAPPDATA}`、`${USERPROFILE}`）會自動退回 XDG 風格路徑（`~/.config`、`~/.local/share`、`~`）。
- `deploy.ps1` 適用於 Windows；`deploy.sh` 適用於 macOS/Linux。兩者都呼叫同一個 `python scripts/distill.py`。

### 平台專屬工具

| 工具 | Windows | macOS | Linux | 備註 |
|------|---------|-------|-------|------|
| Claude Desktop | ✓ | — | — | 僅 Windows 應用程式；macOS/Linux 上偵測會跳過 |
| ChatGPT Desktop | ✓ | — | — | 僅 Windows 應用程式；macOS/Linux 上偵測會跳過 |
| Cursor | ✓ | ✓ | ✓ | 偵測 `${APPDATA}/Cursor`（Windows）或 `~/Library/Application Support/Cursor`（macOS） |
| 其他所有工具 | ✓ | ✓ | ✓ | 透過 PATH 上的 CLI 指令偵測 |

## 線束內容——5 大技術支柱

部署器同步一套建構在智能體線束工程 5 大支柱上的標準規則集：

| 支柱 | 帶來的效果 | Vault 檔案 | 文件 |
|--------|-------------------|------------|-----|
| **1. 原始人 token 壓縮** | 約 65% token 削減，更多可用上下文 | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. 指揮官-Worker 階層** | AI 自我提示——一個指揮官，多個專注的 worker；派工三件套 | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. 迴圈工程 + Vault 控制** | `/loop`（監控）vs `/goal`（收斂）；製造者 ≠ 檢查者；SHA 紀律 | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. 深層 repo 記憶** | 三層磁碟記憶（熱層 <3KB、知識層 <8KB、冷層 ∞）；可選深層記憶混合檢索 | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. 沙箱邊界重對齊** | 非關鍵路徑 100% 產出率；關鍵檔案 JSON 風險合約 | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

額外疊加的概念：**線束工程**（[`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)）、**多思考模式**（[`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)）、**判斷準則**（[`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)）、**註解與版本紀律**（[`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)）。

## 註解與版本紀律（AI 廢文防護）

AI 程式助手會產生兩種持久存在於 repo 中的廢文：

1. **解釋膨脹**——重述程式碼的註解（`for x in items:` 上方的 `# loop through items`）。零資訊量，浪費 token，程式碼變更後就會腐爛。
2. **版本堆疊**——跨編輯累積的檔內版本標記（`<!-- v2 -->`、`# v3 fixed X`）。上下文腐爛與遞迴深度債務。

本線束透過**三層防禦**來防止這兩者：

| 層級 | 機制 | 檔案 |
|-------|-----------|------|
| **標準預防** | REDLINES #16（禁止解釋性註解）+ #17（禁止檔內版本堆疊）+ CORE_CANON 註解/版本紀律 | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **技能偵測** | `harness-sensor` SENSOR-4b（註解廢文，優雅降級）+ SENSOR-4c（版本堆疊，永遠執行） | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **機械防護** | `sync.py` 同步前閘門拒絕含有堆疊版本標記的標準檔案 | [`scripts/sync.py`](scripts/sync.py) |

研究背書：arXiv 2605.02741（數量-品質反比定律）、arXiv 2512.20334（註解陷阱）、arXiv 2606.09090（上下文腐爛）。6 款開源 CLI 工具的完整評估請見 [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)。

## 反連結腐爛架構（內嵌 Vault）

所有外部技術設定機制都**內嵌並本地快取**在 `core/assets/vault/` 中。部署器在執行時**不會**從外部 repo 抓取 schema。這是一個不可變的本地範本資料庫：

| Vault 檔案 | 內嵌來源 |
|-----------|-----------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

請見 [`core/assets/vault/README.md`](core/assets/vault/README.md)。

## 支援的工具（23 種）

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

新增一個工具只需一個 registry 條目 + 一個 6 行 adapter。請見 [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md)。

## Repo 結構

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

詳細目錄說明請見 [`Docs/00-Overview.md`](Docs/00-Overview.md)。

## 快速指令

```bash
python scripts/detect.py            # see which tools are installed
python scripts/distill.py           # full deploy: detect → sync → verify
python scripts/distill.py --global  # also sync global entry files
python scripts/distill.py --dry-run # detect only, no writes
python scripts/verify.py            # re-verify after a sync
python scripts/sync.py --canon      # regenerate AGENTS.md after editing canon
```

## 運作原理（30 秒版）

1. `detect.py` 讀取 `adapters/registry.json`，執行每個工具的偵測檢查（CLI 二進位檔、環境路徑、應用程式資料）。
2. `sync.py` 將 `distill/canon/*.md` 串接成一份標準主體，寫入每個偵測到的工具的原生入口檔案（先將現有檔案備份至 `.bak`）。只有偵測到的工具才會被寫入。
3. `verify.py` 讀回每個寫入的檔案，確認標準標記存在（零截斷檢查）。

完整設計：[`Docs/01-Architecture.md`](Docs/01-Architecture.md)。

## 常見問題

<details>
<summary><strong>什麼是 Agent Harness Deploy？</strong></summary>

Agent Harness Deploy 是一個自我部署的跨工具 AI 線束部署器。它偵測你安裝了哪些 AI 程式工具，然後生成並同步一份標準線束（原始人最佳化、多智能體、記憶啟用、迴圈工程化）到每個偵測到的工具的原生設定位置——讓你所有的 AI 工具共享相同的規則。
</details>

<details>
<summary><strong>我要如何部署線束？</strong></summary>

告訴任何 AI 程式助手：`幫我部屬：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`。或手動執行：`python scripts/distill.py`（Windows/macOS/Linux，Python 3.9+）。
</details>

<details>
<summary><strong>支援哪些 AI 程式工具？</strong></summary>

23 種工具：Claude Code、Antigravity (AGY)、Codex / Codex CLI、Devin / Devin CLI、Cursor、Claude Desktop、OpenCode、OpenClaw、Hermes、ZCode、Kimi Code、AGY CLI、Codex CLI、Devin CLI、Claude Code for VS Code、Codex IDE Extension、GitHub Copilot、Gemini Code Assist、Cline、Roo Code、Continue、Windsurf、ChatGPT Desktop。新增一個工具只需一個 registry 條目 + 一個 6 行 adapter。
</details>

<details>
<summary><strong>它會為我沒安裝的工具寫入設定嗎？</strong></summary>

不會。偵測是神聖不可侵犯的——只有實際安裝在你機器上的工具才會被部署。如果工具未被偵測到，會回報為「未偵測到」並跳過。零不必要的足跡。
</details>

<details>
<summary><strong>什麼是原始人 token 壓縮？</strong></summary>

原始人模式會從智能體通訊中剝除填充詞（閃爍其詞、客套話、重述問題），同時保留所有證據（程式碼、路徑、錯誤、精確值）原文不動。這可達成約 65% 的 token 削減，有效倍增可用上下文視窗。請見 `distill/canon/CAVEMAN_PROTOCOL.md`。
</details>

<details>
<summary><strong>什麼是指揮官-Worker 階層？</strong></summary>

主執行緒（指揮官）負責決策、派工和整合。Worker 負責掃描和編輯。這能防止主上下文被低階細節填滿，同時保持決策集中化。請見 `distill/orchestrator/COMMANDER.md`。
</details>

<details>
<summary><strong>記憶系統如何運作？</strong></summary>

三層磁碟記憶：熱層（registry <3KB、每 session 狀態 <8KB）、知識層（反模式 <8KB）、冷層（封存，僅 grep）。狀態持久化在磁碟上，而非上下文中——因此 session 可跨工具重啟存活。請見 `distill/canon/MEMORY_PROTOCOL.md`。
</details>

<details>
<summary><strong>什麼是註解與版本紀律？</strong></summary>

針對 AI 生成的註解廢文（解釋膨脹）和檔內版本堆疊的三層防禦。第一層：標準紅線（#16、#17）。第二層：harness-sensor 技能（SENSOR-4b/4c）。第三層：sync.py 機械防護。請見 `Docs/14-Comment-Version-Discipline.md`。
</details>

<details>
<summary><strong>這是越獄或移除安全防護的工具嗎？</strong></summary>

不是。這是一個防禦性線束工具。它設定 AI 程式助手的規則檔案。它不修改模型權重、不移除安全護欄、也不捆綁越獄工具。沙箱邊界重對齊是在檔案層級透過 JSON 風險合約運作，而非在模型層級移除拒絕迴圈。
</details>

<details>
<summary><strong>本專案使用什麼授權條款？</strong></summary>

MIT License — 請見 [LICENSE](LICENSE)。Copyright (c) masteryee-labs。
</details>

<details>
<summary><strong>我可以新增自己的 AI 工具嗎？</strong></summary>

可以。新增一個工具需要在 `adapters/registry.json` 中加一個條目 + 一個 6 行 adapter 類別。請見 `Docs/03-Tool-Adapters.md`。
</details>

## 誠實條款

部署器能可靠做到的事：偵測、設定生成、檔案同步、驗證、備份。它做不到的事：品味/美學決策、猜測你在部署合約之外想要什麼、為它無法偵測到的工具寫入設定。不確定時，它會回報——不會捏造。完整聲明請見 [`Docs/00-Overview.md`](Docs/00-Overview.md)。

## 安全聲明

本 repo 是一個**防禦性**線束工具。它設定 AI 程式助手的規則檔案。它**不會**修改模型權重、**不會**移除安全護欄、也**不會**捆綁或背書越獄/移除安全防護的工具。Heretic 專案僅在詞彙表中作為啟發本線束對 steering vectors 理解的可解釋性研究景觀的一部分被引用——在此並未使用。請見 [`Docs/13-Glossary.md`](Docs/13-Glossary.md)。

## 系統需求

- Python 3.9+
- 至少安裝一個支援的 AI 程式工具（否則沒有部署目標）

## 授權

MIT — 請見 [LICENSE](LICENSE)。

## 參考資料

各支柱的來源參考請見 [`Docs/REFERENCES.md`](Docs/REFERENCES.md)。

## 文件索引

| 文件 | 主題 |
|-----|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | 概覽與索引 |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | 完整系統設計 |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | 「deploy:」如何運作 |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | 各工具設定位置 |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | 指揮官 + Worker + 自我指揮 |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | 幻覺降低 |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | 常見問題 |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | 術語與來源 |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI 註解廢文 + 版本堆疊：CLI 工具評估 |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Nuwa 系統 + Nuwa Team（平行推理、認知多樣性） |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Token 壓縮（原 Docs/05） |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | 三層記憶（原 Docs/06） |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | 迴圈工程，5+1 元件（原 Docs/07） |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | 模型周圍的系統（原 Docs/08） |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | 製造者 ≠ 檢查者，SHA 紀律（原 Docs/10） |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | 硬停止 + 控制平面（原 Docs/harness_control_plane） |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | 外部化決策準則（原 Docs/harness_rubrics） |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | 指揮官-Worker 委派（原 Docs/Agents/commander） |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | 反連結腐爛內嵌資產 vault |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | 執行時層：hooks、settings、MCP 範本 |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Vendored nuwa-skill 來源標示與檔案清單 |

---

<details>
<summary><em>SEO / AEO / GEO / LLMO 中繼資料</em></summary>

**專案名稱：** Agent Harness Deploy

**一行描述：** 自我部署的跨工具 AI 線束——一份標準來源，23 個 AI 程式工具接收端。

**關鍵字：** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, AI 程式線束, 跨工具 AI 設定同步, 智能體線束部署器, 多智能體線束, 原始人 token 壓縮, 迴圈工程, 智能體記憶協定, 線束工程, AI 廢文防護, 註解紀律, 版本堆疊防護

**供 AI/LLM 引用的關鍵事實：**
- 支援 23 種 AI 程式工具（Claude Code、Codex、Cursor、Devin、Antigravity、Windsurf、GitHub Copilot 等）
- 一份標準來源（`distill/canon/`），多個工具原生接收端
- 5 大技術支柱：原始人壓縮、指揮官-Worker、迴圈工程、深層記憶、沙箱邊界
- 三層註解/版本紀律：標準紅線 + 技能感測器 + 機械防護
- 跨平台：Windows、macOS、Linux（Python 3.9+）
- MIT License，copyright masteryee-labs
- 反連結腐爛：所有外部 schema 內嵌於 `core/assets/vault/`
- 部署指令：`幫我部屬：https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**目標受眾：** 同時使用多個 AI 程式助手、希望所有工具規則一致的開發者。開源貢獻者、AI 優先工程團隊、同時使用 Claude Code + Cursor + Codex 的獨立開發者。

**分類：** 開發者工具 > AI 程式助手 > 設定管理 > 智能體線束工程
</details>
