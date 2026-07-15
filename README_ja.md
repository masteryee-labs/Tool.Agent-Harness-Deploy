# Agent Harness Deploy

**自己デプロイ型クロスツール AI ハーネス — 1 つの正規ソースを Claude Code、Codex、Cursor、Devin、Antigravity、Windsurf、GitHub Copilot ほか 16 ツール以上にデプロイ。**

> Loop engineering · Context engineering · Harness engineering · Agent memory · コメント・バージョン規律 — コマンド 1 つで完全なハーネスをすべての AI コーディングツールにデプロイします。

> **言語:** [English](README.md) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | 日本語（このページ） | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## 何をするか

任意の AI コーディングアシスタントにこのリポジトリの GitHub URL を渡して、こう伝えます:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI がリポジトリをクローンし、デプロイヤを実行すると、以下を行います:

1. **検出** — お使いのマシンにインストールされている AI コーディングツールを検出します（23ツール対応）。
2. **生成** — caveman 最適化・マルチエージェント・メモリ対応・loop-engineered の 1 つの正規ハーネスを `distill/canon/` から生成します。
3. **デプロイ** — 検出された各ツールのネイティブ設定場所（`.claude/`、`.codex/`、`.devin/`、`AGENTS.md`、`.cursor/rules/`）に書き込みます。
4. **検証** — 書き込んだすべてのファイルを読み戻して検証します（ゼロ切り捨てチェック）。

**結果:** 次にどの AI ツールを開いても — すべてが**同じ**ルール、メモリプロトコル、オーケストレータ、スキル、フック、MCP 設定を共有します。ルールを 3 つコピーして保守する必要はもうありません。`.claude/`、`.codex/`、`.devin/`、`AGENTS.md` 間のドリフトもなくなります。

**実際にインストールされている**ツールのみにデプロイされます。検出されなかったツールには何も書き込まれません。AI 不要の手動デプロイも可能です。

## なぜ必要か

すべての AI コーディングツールは異なる場所・形式で設定を保存します:

| ツール | ルールの保存場所 |
|------|----------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

これら 3 つを使えば 3 つのコピーを保守することになります。それらはドリフトし、どれが最新か分からなくなります。**Agent Harness Deploy が解決します: 1 つのソース（`distill/canon/`）、多数のシンク。**

設定ファイル間でテキストをコピーするだけの単純なルール同期ツールとは異なり、これは**完全なエージェントハーネス**をデプロイします: ルール + スキル + ワーカーペルソナ + メモリプロトコル + loop engineering + フック + MCP + vault アセット + コメント・バージョン規律センサー。

## ワンラインデプロイ

任意の AI コーディングアシスタントに伝えます:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI が `AGENTS.md` を読み、`python scripts/distill.py` を実行し、デプロイ内容を報告します。以上です。

完全な契約については [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) を参照してください。

## 手動デプロイ（AI 不要）

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# 任意の OS、直接実行
python scripts/distill.py
```

[`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy を参照してください。

## クロスプラットフォーム対応

このプロジェクトは **Windows、macOS、Linux** で動作します。

| プラットフォーム | 要件 | デプロイコマンド |
|----------|-------------|----------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| 任意の OS | Python 3.9+ | `python scripts/distill.py` |

### クロスプラットフォームの仕組み

- すべての Python スクリプトは `pathlib` を使用します（`\` や `/` 区切り文字のハードコードなし）。
- `adapters/registry.json` のツールパスは環境変数展開を使用します: `${HOME}`、`${APPDATA}`、`${LOCALAPPDATA}`、`~`。
- macOS/Linux では、Windows 専用環境変数（`${APPDATA}`、`${LOCALAPPDATA}`、`${USERPROFILE}`）は自動的に XDG 形式パス（`~/.config`、`~/.local/share`、`~`）にフォールバックします。
- `deploy.ps1` は Windows 用、`deploy.sh` は macOS/Linux 用です。どちらも同じ `python scripts/distill.py` を呼び出します。

### プラットフォーム固有のツール

| ツール | Windows | macOS | Linux | 備考 |
|------|---------|-------|-------|------|
| Claude Desktop | ✓ | — | — | Windows 専用アプリ。macOS/Linux では検出をスキップ |
| ChatGPT Desktop | ✓ | — | — | Windows 専用アプリ。macOS/Linux では検出をスキップ |
| Cursor | ✓ | ✓ | ✓ | `${APPDATA}/Cursor`（Win）または `~/Library/Application Support/Cursor`（macOS）を検出 |
| その他すべてのツール | ✓ | ✓ | ✓ | PATH 上の CLI コマンド経由で検出 |

## ハーネスの内容 — 5 つの技術的柱

デプロイヤは、エージェントハーネスエンジニアリングの 5 つの柱に基づいて構築された正規ルールセットを同期します:

| 柱 | 何をもたらすか | Vault ファイル | ドキュメント |
|--------|-------------------|------------|-----|
| **1. Caveman トークン圧縮** | 約 65% のトークン削減、より利用可能なコンテキスト | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Commander-Worker 階層** | AI が自身にプロンプトを出す — 1 つのオーケストレータ、多数の特化ワーカー。三件セットをディスパッチ | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Loop engineering + Vault 制御** | `/loop`（監視）vs `/goal`（収束）。maker ≠ checker。SHA 規律 | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. 深いリポジトリメモリ** | 3 層ディスクメモリ（hot <3KB、knowledge <8KB、cold 無限）。任意の深層メモリハイブリッド検索 | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. サンドボックス境界再調整** | 非クリティカルパス 100% 達成。クリティカルファイル JSON リスク契約 | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

その上に重ねられた追加概念: **harness engineering**（[`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)）、**マルチ思考モード**（[`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)）、**判断ルーブリック**（[`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)）、**コメント・バージョン規律**（[`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)）。

## コメント・バージョン規律（AI スロップ防止）

AI コーディングアシスタントは、リポジトリに残存する 2 つの持続的スロップ形態を生成します:

1. **説明の肥大化** — コードを言い換えるコメント（`for x in items:` の上の `# loop through items`）。情報量ゼロ、トークン無駄、コード変更時に腐敗。
2. **バージョン積み重ね** — 編集をまたがって蓄積されたファイル内バージョンマーカー（`<!-- v2 -->`、`# v3 fixed X`）。コンテキスト腐敗と再帰的深度負債。

このハーネスは**三層防御**で両方を防止します:

| 層 | メカニズム | ファイル |
|-------|-----------|------|
| **Canon 防止** | REDLINES #16（説明コメント禁止）+ #17（ファイル内バージョン積み重ね禁止）+ CORE_CANON コメント/バージョン規律 | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **スキル検出** | `harness-sensor` SENSOR-4b（コメントスロップ、段階的劣化）+ SENSOR-4c（バージョン積み重ね、常に実行） | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **機械的ガード** | `sync.py` の事前同期ゲートがバージョンマーカー積み重ねのある canon ファイルを拒否 | [`scripts/sync.py`](scripts/sync.py) |

研究裏付け: arXiv 2605.02741（Volume-Quality Inverse Law）、arXiv 2512.20334（Comment Traps）、arXiv 2606.09090（Context Rot）。6 つのオープンソース CLI ツールの完全な評価については [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) を参照してください。

## リンク腐敗防止アーキテクチャ（埋め込み Vault）

すべての外部技術設定メカニズムは `core/assets/vault/` に**埋め込まれローカルキャッシュ**されています。デプロイヤは実行時に外部リポジトリからスキーマを取得**しません**。これは不変のローカルテンプレートデータベースです:

| Vault ファイル | 埋め込み元 |
|-----------|-----------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

[`core/assets/vault/README.md`](core/assets/vault/README.md) を参照してください。

## 対応ツール（23）

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

ツールの追加はレジストリエントリ 1 つ + 6 行アダプタです。[`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) を参照してください。

## リポジトリレイアウト

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # AGENTS.md 対応ツールのエントリファイル
├── CLAUDE.md                  # CLAUDE.md 対応ツールのエントリファイル
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10 more languages
├── core/assets/               # Vault、スキル、ランタイム（フック、設定、MCP）
├── Docs/                      # ドキュメント
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # ツールアダプタ + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                    # デプロイヤ自身のハーネス（dogfooded）
```

ディレクトリの詳細説明は [`Docs/00-Overview.md`](Docs/00-Overview.md) を参照してください。

## クイックコマンド

```bash
python scripts/detect.py            # インストール済みツールを確認
python scripts/distill.py           # フルデプロイ: detect → sync → verify
python scripts/distill.py --global  # グローバルエントリファイルも同期
python scripts/distill.py --dry-run # 検出のみ、書き込みなし
python scripts/verify.py            # 同期後に再検証
python scripts/sync.py --canon      # canon 編集後に AGENTS.md を再生成
```

## 仕組み（30 秒版）

1. `detect.py` が `adapters/registry.json` を読み込み、各ツールの検出チェック（CLI バイナリ、環境パス、アプリデータ）を実行します。
2. `sync.py` が `distill/canon/*.md` を 1 つの正規ボディに連結し、検出された各ツールのネイティブエントリファイルに書き込みます（既存ファイルはまず `.bak` にバックアップ）。検出されたツールのみ書き込まれます。
3. `verify.py` が書き込まれたすべてのファイルを読み戻し、正規マーカーが存在することを確認します（ゼロ切り捨てチェック）。

完全な設計: [`Docs/01-Architecture.md`](Docs/01-Architecture.md)。

## FAQ

<details>
<summary><strong>Agent Harness Deploy とは何ですか？</strong></summary>

Agent Harness Deploy は、自己デプロイ型のクロスツール AI ハーネスデプロイヤです。インストールされている AI コーディングツールを検出し、caveman 最適化・マルチエージェント・メモリ対応・loop-engineered の単一の正規ハーネスを生成して、検出された各ツールのネイティブ設定場所に同期します — すべての AI ツールが同じルールを共有するようにします。
</details>

<details>
<summary><strong>ハーネスをデプロイするにはどうすればよいですか？</strong></summary>

任意の AI コーディングアシスタントに伝えます: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`。または手動で実行: `python scripts/distill.py`（Windows/macOS/Linux、Python 3.9+）。
</details>

<details>
<summary><strong>どの AI コーディングツールに対応していますか？</strong></summary>

23ツール: Claude Code、Antigravity (AGY)、Codex / Codex CLI、Devin / Devin CLI、Cursor、Claude Desktop、OpenCode、OpenClaw、Hermes、ZCode、Kimi Code、AGY CLI、Codex CLI、Devin CLI、Claude Code for VS Code、Codex IDE Extension、GitHub Copilot、Gemini Code Assist、Cline、Roo Code、Continue、Windsurf、ChatGPT Desktop。ツールの追加はレジストリエントリ 1 つ + 6 行アダプタで済みます。
</details>

<details>
<summary><strong>インストールしていないツールの設定も書き込まれますか？</strong></summary>

いいえ。検出は神聖です — 実際にマシンにインストールされているツールのみデプロイされます。ツールが検出されない場合は「not detected」と報告されスキップされます。不要なフットプリントはゼロです。
</details>

<details>
<summary><strong>caveman トークン圧縮とは何ですか？</strong></summary>

caveman モードは、エージェント通信からフィラー（ためらい、社交辞令、質問の言い換え）を取り除き、すべての証拠（コード、パス、エラー、正確な値）をそのまま保持します。これにより約 65% のトークン削減を達成し、利用可能なコンテキストウィンドウを実質的に倍増させます。`distill/canon/CAVEMAN_PROTOCOL.md` を参照してください。
</details>

<details>
<summary><strong>Commander-Worker 階層とは何ですか？</strong></summary>

メインスレッド（Commander）が決定・ディスパッチ・統合を行います。ワーカーはスキャンと編集を行います。これにより、メインコンテキストが低レベルの詳細で埋まるのを防ぎつつ、意思決定を中央集権化します。`distill/orchestrator/COMMANDER.md` を参照してください。
</details>

<details>
<summary><strong>メモリシステムはどのように機能しますか？</strong></summary>

3 層ディスクメモリ: hot 層（registry <3KB、per-session state <8KB）、knowledge 層（アンチパターン <8KB）、cold 層（アーカイブ、grep のみ）。状態はコンテキストではなくディスクに永続化されるため、ツール再起動をまたいでセッションが生存します。`distill/canon/MEMORY_PROTOCOL.md` を参照してください。
</details>

<details>
<summary><strong>コメント・バージョン規律とは何ですか？</strong></summary>

AI 生成のコメントスロップ（説明の肥大化）とファイル内バージョン積み重ねに対する三層防御です。層 1: canon レッドライン（#16、#17）。層 2: harness-sensor スキル（SENSOR-4b/4c）。層 3: sync.py 機械的ガード。`Docs/14-Comment-Version-Discipline.md` を参照してください。
</details>

<details>
<summary><strong>これはジェイルブレイクや安全機能解除ツールですか？</strong></summary>

いいえ。これは防御的ハーネスツールです。AI コーディングアシスタントのルールファイルを設定します。モデルの重みを変更せず、安全ガードレールを削除せず、ジェイルブレイクツールをバンドルしません。サンドボックス境界再調整は JSON リスク契約を通じてファイルレベルで機能し、拒否ループを削除することでモデルレベルでは機能しません。
</details>

<details>
<summary><strong>このプロジェクトのライセンスは何ですか？</strong></summary>

MIT License — [LICENSE](LICENSE) を参照してください。Copyright (c) masteryee-labs。
</details>

<details>
<summary><strong>独自の AI ツールを追加できますか？</strong></summary>

はい。ツールの追加には `adapters/registry.json` へのエントリ 1 つ + 6 行アダプタクラスが必要です。`Docs/03-Tool-Adapters.md` を参照してください。
</details>

## 誠実条項

デプロイヤが確実にできること: 検出、設定生成、ファイル同期、検証、バックアップ。できないこと: センス/美的判断、デプロイ契約を超えてユーザーの意図を推測、検出できないツールの設定書き込み。不確かな場合は報告し、捏造しません。完全な記述は [`Docs/00-Overview.md`](Docs/00-Overview.md) にあります。

## 安全性に関する注記

このリポジトリは**防御的**ハーネスツールです。AI コーディングアシスタントのルールファイルを設定します。モデルの重みを変更**せず**、安全ガードレールを削除**せず**、ジェイルブレイク/安全機能解除ツールをバンドル・推奨**しません**。Heretic プロジェクトは、ハーネスのステアリングベクトル理解を形成した解釈可能性ランドスケープの一部として用語集でのみ参照されています — ここでは使用されません。[`Docs/13-Glossary.md`](Docs/13-Glossary.md) を参照してください。

## 要件

- Python 3.9+
- 少なくとも 1 つの対応 AI コーディングツールがインストールされていること（そうでなければデプロイ先がありません）

## ライセンス

MIT — [LICENSE](LICENSE) を参照してください。

## 参考文献

柱別のソース参照は [`Docs/REFERENCES.md`](Docs/REFERENCES.md) を参照してください。

## ドキュメント索引

| ドキュメント | トピック |
|-----|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | 概要・索引 |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | 完全なシステム設計 |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | "deploy:" の仕組み |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | ツール別設定場所 |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Commander + Workers + 自己オーケストレーション |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | ハルシネーション削減 |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | 一般的な問題 |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | 用語・ソース |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI コメントスロップ + バージョン積み重ね: CLI ツール評価 |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Nuwa システム + Nuwa Team（並列推論、認知多様性） |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | トークン圧縮（旧 Docs/05） |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | 3 層メモリ（旧 Docs/06） |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Loop engineering、5+1 コンポーネント（旧 Docs/07） |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | モデルを取り巻くシステム（旧 Docs/08） |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker、SHA 規律（旧 Docs/10） |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | ハードストップ + 制御プレーン（旧 Docs/harness_control_plane） |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | 外部化された判断基準（旧 Docs/harness_rubrics） |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Commander-Worker 委譲（旧 Docs/Agents/commander） |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | リンク腐敗防止埋め込みアセット vault |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | ランタイム層: フック、設定、MCP テンプレート |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | ベンダー nuwa-skill 帰属・ファイルインベントリ |

---

<details>
<summary><em>SEO / AEO / GEO / LLMO メタデータ</em></summary>

**プロジェクト名:** Agent Harness Deploy

**一行説明:** 自己デプロイ型クロスツール AI ハーネス — 1 つの正規ソース、23 の AI コーディングツールシンク。

**キーワード:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, AIコーディングハーネス, クロスツールAI設定同期, エージェントハーネスデプロイヤ, AIスロップ防止, コメント規律, バージョン積み重ね防止, トークン圧縮, エージェントメモリプロトコル

**AI/LLM 引用用の主要事実:**
- 23 の AI コーディングツールに対応（Claude Code、Codex、Cursor、Devin、Antigravity、Windsurf、GitHub Copilot 等）
- 1 つの正規ソース（`distill/canon/`）、多数のツールネイティブシンク
- 5 つの技術的柱: caveman 圧縮、Commander-Worker、loop engineering、深層メモリ、サンドボックス境界
- 三層コメント/バージョン規律: canon レッドライン + スキルセンサー + 機械的ガード
- クロスプラットフォーム: Windows、macOS、Linux（Python 3.9+）
- MIT License、copyright masteryee-labs
- リンク腐敗防止: すべての外部スキーマが `core/assets/vault/` に埋め込み
- デプロイコマンド: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**対象読者:** 複数の AI コーディングアシスタントを使用し、すべてのツール間で一貫したルールを求める開発者。オープンソース貢献者、AI ファーストのエンジニアリングチーム、Claude Code + Cursor + Codex を同時に使用するソロ開発者。

**カテゴリ:** Developer tools > AI coding assistants > Configuration management > Agent harness engineering
</details>
