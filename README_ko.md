# Agent Harness Deploy

**자가 배포형 크로스툴 AI 하니스 — 하나의 정규 소스를 Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot 및 16개 이상 도구에 배포.**

> 루프 엔지니어링 · 컨텍스트 엔지니어링 · 하니스 엔지니어링 · 에이전트 메모리 · 주석 및 버전 규율 — 하나의 명령으로 모든 AI 코딩 도구에 완전한 하니스를 배포합니다.

> **언어:** [English](README.md) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | **한국어**（이 페이지） | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## 이 도구가 하는 일

이 저장소의 GitHub URL을 아무 AI 코딩 어시스턴트에게 주고 말합니다:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI가 저장소를 클론하고, 배포기를 실행하면 다음을 수행합니다:

1. **감지** — 머신에 설치된 AI 코딩 도구를 감지합니다 (23개 도구 지원).
2. **생성** — `distill/canon/`에서 캐브맨 최적화, 멀티 에이전트, 메모리 지원, 루프 엔지니어링 기반의 하나의 정규 하니스를 생성합니다.
3. **배포** — 감지된 모든 도구의 네이티브 설정 위치(`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`)에 배포합니다.
4. **검증** — 작성된 모든 파일을 다시 읽어 검증합니다 (잘림 제로 검사).

**결과:** 다음에 어떤 AI 도구를 열든 — 모두 **동일한** 규칙, 메모리 프로토콜, 오케스트레이터, 스킬, 훅, MCP 설정을 공유합니다. 더 이상 세 개의 규칙 사본을 유지할 필요가 없습니다. `.claude/`, `.codex/`, `.devin/`, `AGENTS.md` 간의 드리프트도 사라집니다.

**실제로 설치된 도구에만** 배포됩니다. 감지되지 않은 도구에는 아무것도 작성되지 않습니다. AI 없이도 수동으로 배포할 수 있습니다.

## 왜 필요한가

모든 AI 코딩 도구는 설정을 서로 다른 위치와 형식으로 저장합니다:

| 도구 | 규칙이 위치하는 곳 |
|------|----------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

이 중 세 개를 사용하면 세 개의 사본을 유지해야 합니다. 사본들은 서로 달라집니다. 어느 것이 최신인지 잊게 됩니다. **Agent Harness Deploy가 해결합니다: 하나의 소스(`distill/canon/`), 여러 개의 싱크.**

단순히 설정 파일 간에 텍스트만 복사하는 규칙 동기화 도구와 달리, 이 도구는 **완전한 에이전트 하니스**를 배포합니다: 규칙 + 스킬 + 워커 페르소나 + 메모리 프로토콜 + 루프 엔지니어링 + 훅 + MCP + 볼트 자산 + 주석/버전 규율 센서.

## 한 줄 배포

아무 AI 코딩 어시스턴트에게 말합니다:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI가 `AGENTS.md`를 읽고, `python scripts/distill.py`를 실행한 뒤 배포한 내용을 보고합니다. 끝입니다.

전체 계약은 [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md)를 참조하세요.

## 수동 배포 (AI 없이)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# 모든 OS, 직접 실행
python scripts/distill.py
```

[`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy를 참조하세요.

## 크로스 플랫폼 지원

이 프로젝트는 **Windows, macOS, Linux**에서 작동합니다.

| 플랫폼 | 요구사항 | 배포 명령 |
|----------|-------------|----------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| 모든 OS | Python 3.9+ | `python scripts/distill.py` |

### 크로스 플랫폼 작동 방식

- 모든 Python 스크립트는 `pathlib`를 사용합니다 (하드코딩된 `\` 또는 `/` 구분자 없음).
- `adapters/registry.json`의 도구 경로는 환경 변수 확장을 사용합니다: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- macOS/Linux에서 Windows 전용 환경 변수(`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`)는 자동으로 XDG 스타일 경로(`~/.config`, `~/.local/share`, `~`)로 대체됩니다.
- `deploy.ps1`은 Windows용; `deploy.sh`는 macOS/Linux용입니다. 둘 다 동일한 `python scripts/distill.py`를 호출합니다.

### 플랫폼별 도구

| 도구 | Windows | macOS | Linux | 비고 |
|------|---------|-------|-------|------|
| Claude Desktop | ✓ | — | — | Windows 전용 앱; macOS/Linux에서는 감지 시 건너뜀 |
| ChatGPT Desktop | ✓ | — | — | Windows 전용 앱; macOS/Linux에서는 감지 시 건너뜀 |
| Cursor | ✓ | ✓ | ✓ | `${APPDATA}/Cursor`(Win) 또는 `~/Library/Application Support/Cursor`(macOS) 감지 |
| 그 외 모든 도구 | ✓ | ✓ | ✓ | PATH의 CLI 명령으로 감지 |

## 하니스에 포함된 것 — 5개 기술 기둥

배포기는 에이전트 하니스 엔지니어링의 5개 기둥으로 구축된 정규 규칙 세트를 동기화합니다:

| 기둥 | 제공하는 것 | 볼트 파일 | 문서 |
|--------|-------------------|------------|-----|
| **1. 캐브맨 토큰 압축** | ~65% 토큰 절감, 더 많은 사용 가능 컨텍스트 | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. 커맨더-워커 계층** | AI가 스스로에게 프롬프트 — 하나의 오케스트레이터, 여러 집중 워커; 3피스 세트 디스패치 | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. 루프 엔지니어링 + 볼트 제어** | `/loop`(모니터링) vs `/goal`(수렴); 메이커 ≠ 체커; SHA 규율 | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. 심층 저장소 메모리** | 3계층 디스크 메모리(핫 <3KB, 지식 <8KB, 콜드 ∞); 선택적 심층 메모리 하이브리드 검색 | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. 샌드박스 경계 재정렬** | 비중요 경로 100% 수율; 중요 파일 JSON 리스크 계약 | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

그 위에 추가된 개념: **하니스 엔지니어링**([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **멀티 사고 모드**([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **판단 루브릭**([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **주석 및 버전 규율**([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## 주석 및 버전 규율 (AI 슬롭 방지)

AI 코딩 어시스턴트는 저장소에 남는 두 가지 지속적 슬롭 형태를 생성합니다:

1. **설명 잉여** — 코드를 반복하는 주석(`for x in items:` 위의 `# loop through items`). 정보가 없고, 토큰을 낭비하며, 코드가 변경되면 썩습니다.
2. **버전 적층** — 편집마다 누적되는 파일 내 버전 마커(`<!-- v2 -->`, `# v3 fixed X`). 컨텍스트 부패와 재귀적 깊이 부채를 초래합니다.

이 하니스는 **3계층 방어**를 통해 둘 다 방지합니다:

| 계층 | 메커니즘 | 파일 |
|-------|-----------|------|
| **캐논 방지** | REDLINES #16(설명 주석 금지) + #17(파일 내 버전 적층 금지) + CORE_CANON 주석/버전 규율 | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **스킬 감지** | `harness-sensor` SENSOR-4b(주석 슬롭, 우아한 저하) + SENSOR-4c(버전 적층, 항상 실행) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **기계적 가드** | `sync.py` 사전 동기화 게이트가 적층된 버전 마커가 있는 캐논 파일 거부 | [`scripts/sync.py`](scripts/sync.py) |

연구 기반: arXiv 2605.02741(볼륨-품질 반비례 법칙), arXiv 2512.20334(주석 함정), arXiv 2606.09090(컨텍스트 부패). 6개 오픈소스 CLI 도구 평가는 [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)를 참조하세요.

## 링크 부패 방지 아키텍처 (내장 볼트)

모든 외부 기술 설정 메커니즘은 `core/assets/vault/`에 **내장되어 로컬 캐시**됩니다. 배포기는 런타임에 외부 저장소에서 스키마를 가져오지 **않습니다**. 이것은 불변 로컬 템플릿 데이터베이스입니다:

| 볼트 파일 | 내장 소스 |
|-----------|-----------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

[`core/assets/vault/README.md`](core/assets/vault/README.md)를 참조하세요.

## 지원 도구 (23개)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

도구 추가는 레지스트리 항목 하나 + 6줄 어댑터입니다. [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md)를 참조하세요.

## 저장소 구조

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # AGENTS.md 인식 도구용 진입 파일
├── CLAUDE.md                  # CLAUDE.md 인식 도구용 진입 파일
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10개 언어 더
├── core/assets/               # 볼트, 스킬, 런타임(훅, 설정, MCP)
├── Docs/                      # 문서
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # 도구 어댑터 + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                    # 배포기 자체 하니스(도그푸딩)
```

상세 디렉터리 설명은 [`Docs/00-Overview.md`](Docs/00-Overview.md)를 참조하세요.

## 빠른 명령

```bash
python scripts/detect.py            # 설치된 도구 확인
python scripts/distill.py           # 전체 배포: 감지 → 동기화 → 검증
python scripts/distill.py --global  # 전역 진입 파일도 동기화
python scripts/distill.py --dry-run # 감지만, 쓰기 없음
python scripts/verify.py            # 동기화 후 재검증
python scripts/sync.py --canon      # 캐논 편집 후 AGENTS.md 재생성
```

## 작동 방식 (30초 버전)

1. `detect.py`가 `adapters/registry.json`을 읽고 각 도구의 감지 검사(CLI 바이너리, 환경 경로, 앱 데이터)를 실행합니다.
2. `sync.py`가 `distill/canon/*.md`를 하나의 정규 본문으로 연결하여 감지된 각 도구의 네이티브 진입 파일에 작성합니다(기존 파일은 먼저 `.bak`으로 백업). 감지된 도구에만 작성됩니다.
3. `verify.py`가 작성된 모든 파일을 다시 읽고 정규 마커가 존재하는지 확인합니다(잘림 제로 검사).

전체 설계: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## FAQ

<details>
<summary><strong>Agent Harness Deploy란 무엇인가요?</strong></summary>

Agent Harness Deploy는 자가 배포형 크로스툴 AI 하니스 배포기입니다. 설치된 AI 코딩 도구를 감지한 뒤, 하나의 정규 하니스(캐브맨 최적화, 멀티 에이전트, 메모리 지원, 루프 엔지니어링)를 감지된 모든 도구의 네이티브 설정 위치에 생성 및 동기화합니다 — 모든 AI 도구가 동일한 규칙을 공유하게 합니다.
</details>

<details>
<summary><strong>하니스를 어떻게 배포하나요?</strong></summary>

아무 AI 코딩 어시스턴트에게 말합니다: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. 또는 수동으로 실행: `python scripts/distill.py`(Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>어떤 AI 코딩 도구가 지원되나요?</strong></summary>

23개 도구: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. 도구 추가는 레지스트리 항목 하나 + 6줄 어댑터면 됩니다.
</details>

<details>
<summary><strong>설치하지 않은 도구의 설정도 작성하나요?</strong></summary>

아니요. 감지가 최우선입니다 — 실제로 머신에 설치된 도구에만 배포됩니다. 도구가 감지되지 않으면 "감지되지 않음"으로 보고되고 건너뜁니다. 불필요한 흔적은 제로입니다.
</details>

<details>
<summary><strong>캐브맨 토큰 압축이란 무엇인가요?</strong></summary>

캐브맨 모드는 에이전트 통신에서 필러(주저, 인사, 질문 재진술)를 제거하면서 모든 증거(코드, 경로, 오류, 정확한 값)는 그대로 유지합니다. 이를 통해 ~65% 토큰 절감을 달성하여 사용 가능한 컨텍스트 창을 효과적으로 배가합니다. `distill/canon/CAVEMAN_PROTOCOL.md`를 참조하세요.
</details>

<details>
<summary><strong>커맨더-워커 계층이란 무엇인가요?</strong></summary>

메인 스레드(커맨더)가 결정하고, 디스패치하고, 통합합니다. 워커는 스캔하고 편집합니다. 이를 통해 메인 컨텍스트가 저수준 디테일로 채워지는 것을 방지하면서 의사결정은 중앙 집중화됩니다. `distill/orchestrator/COMMANDER.md`를 참조하세요.
</details>

<details>
<summary><strong>메모리 시스템은 어떻게 작동하나요?</strong></summary>

3계층 디스크 메모리: 핫 계층(레지스트리 <3KB, 세션별 상태 <8KB), 지식 계층(안티 패턴 <8KB), 콜드 계층(아카이브, grep 전용). 상태는 컨텍스트가 아닌 디스크에 저장됩니다 — 세션이 도구 재시작 후에도 유지됩니다. `distill/canon/MEMORY_PROTOCOL.md`를 참조하세요.
</details>

<details>
<summary><strong>주석 및 버전 규율이란 무엇인가요?</strong></summary>

AI 생성 주석 슬롭(설명 잉여)과 파일 내 버전 적층에 대한 3계층 방어입니다. 계층 1: 캐논 레드라인(#16, #17). 계층 2: harness-sensor 스킬(SENSOR-4b/4c). 계층 3: sync.py 기계적 가드. `Docs/14-Comment-Version-Discipline.md`를 참조하세요.
</details>

<details>
<summary><strong>이것은 탈옥 또는 안전 제거 도구인가요?</strong></summary>

아니요. 이것은 방어적 하니스 도구입니다. AI 코딩 어시스턴트의 규칙 파일을 설정합니다. 모델 가중치를 수정하지 않고, 안전 가드레일을 제거하지 않으며, 탈옥 도구를 번들하지 않습니다. 샌드박스 경계 재정렬은 거부 루프를 제거하는 모델 수준이 아닌, JSON 리스크 계약을 통한 파일 수준에서 작동합니다.
</details>

<details>
<summary><strong>이 프로젝트는 어떤 라이선스인가요?</strong></summary>

MIT License — [LICENSE](LICENSE)를 참조하세요. Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>나만의 AI 도구를 추가할 수 있나요?</strong></summary>

네. 도구 추가는 `adapters/registry.json`에 항목 하나 + 6줄 어댑터 클래스가 필요합니다. `Docs/03-Tool-Adapters.md`를 참조하세요.
</details>

## 정직 조항

배포기가 안정적으로 수행할 수 있는 것: 감지, 설정 생성, 파일 동기화, 검증, 백업. 수행할 수 없는 것: 취향/미적 결정, 배포 계약을 넘어 사용자가 원하는 것 추측, 감지할 수 없는 도구의 설정 작성. 불확실할 때는 보고합니다 — 날조하지 않습니다. 전체 성명은 [`Docs/00-Overview.md`](Docs/00-Overview.md)에 있습니다.

## 안전 노트

이 저장소는 **방어적** 하니스 도구입니다. AI 코딩 어시스턴트의 규칙 파일을 설정합니다. 모델 가중치를 수정하지 **않고**, 안전 가드레일을 제거하지 **않으며**, 탈옥/안전 제거 도구를 번들하거나 추천하지 **않습니다**. Heretic 프로젝트는 하니스의 스티어링 벡터 이해에 영향을 준 해석 가능성 환경의 일부로 용어집에서만 참조됩니다 — 여기서는 사용되지 않습니다. [`Docs/13-Glossary.md`](Docs/13-Glossary.md)를 참조하세요.

## 요구사항

- Python 3.9+
- 지원되는 AI 코딩 도구 최소 하나 설치 (그렇지 않으면 배포할 곳이 없음)

## 라이선스

MIT — [LICENSE](LICENSE)를 참조하세요.

## 참고문헌

기둥별 소스 참조는 [`Docs/REFERENCES.md`](Docs/REFERENCES.md)를 참조하세요.

## 문서 인덱스

| 문서 | 주제 |
|-----|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | 개요 및 인덱스 |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | 전체 시스템 설계 |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | "deploy:" 작동 방식 |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | 도구별 설정 위치 |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | 커맨더 + 워커 + 자가 오케스트레이션 |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | 환각 감소 |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | 일반적인 문제 |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | 용어 및 소스 |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI 주석 슬롭 + 버전 적층: CLI 도구 평가 |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Nuwa 시스템 + Nuwa 팀(병렬 추론, 인지 다양성) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | 토큰 압축 (구 Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | 3계층 메모리 (구 Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | 루프 엔지니어링, 5+1 컴포넌트 (구 Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | 모델 주변의 시스템 (구 Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | 메이커 ≠ 체커, SHA 규율 (구 Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | 하드 스톱 + 제어 평면 (구 Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | 외재화된 결정 기준 (구 Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | 커맨더-워커 위임 (구 Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | 링크 부패 방지 내장 자산 볼트 |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | 런타임 계층: 훅, 설정, MCP 템플릿 |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | 벤더된 nuwa-skill 저작권 및 파일 인벤토리 |

---

<details>
<summary><em>SEO / AEO / GEO / LLMO 메타데이터</em></summary>

**프로젝트 이름:** Agent Harness Deploy

**한 줄 설명:** 자가 배포형 크로스툴 AI 하니스 — 하나의 정규 소스, 23개 AI 코딩 도구 싱크.

**키워드:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, AI 코딩 하니스, 크로스툴 AI 설정 동기화, 에이전트 하니스 배포기, 멀티 에이전트 하니스, 캐브맨 토큰 압축, 루프 엔지니어링, 에이전트 메모리 프로토콜, 하니스 엔지니어링, AI 슬롭 방지, 주석 규율, 버전 적층 방지

**AI/LLM 인용을 위한 핵심 사실:**
- 23개 AI 코딩 도구 지원 (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot 등)
- 하나의 정규 소스(`distill/canon/`), 여러 도구 네이티브 싱크
- 5개 기술 기둥: 캐브맨 압축, 커맨더-워커, 루프 엔지니어링, 심층 메모리, 샌드박스 경계
- 3계층 주석/버전 규율: 캐논 레드라인 + 스킬 센서 + 기계적 가드
- 크로스 플랫폼: Windows, macOS, Linux (Python 3.9+)
- MIT License, copyright masteryee-labs
- 링크 부패 방지: 모든 외부 스키마가 `core/assets/vault/`에 내장
- 배포 명령: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**대상 독자:** 여러 AI 코딩 어시스턴트를 사용하며 모든 도구에서 일관된 규칙을 원하는 개발자. 오픈소스 기여자, AI 우선 엔지니어링 팀, Claude Code + Cursor + Codex를 동시에 사용하는 솔로 개발자.

**카테고리:** 개발자 도구 > AI 코딩 어시스턴트 > 설정 관리 > 에이전트 하니스 엔지니어링
</details>
