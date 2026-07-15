# Agent Harness Deploy

**Samorozpakowujący się, wielonarzędziowy harness AI — jedno kanoniczne źródło wdrażane do Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot i 16 kolejnych.**

> Loop engineering · Context engineering · Harness engineering · Pamięć agenta · Dyscyplina komentarzy i wersji — jedno polecenie wdraża kompletny harness do wszystkich Twoich narzędzi AI do kodowania.

> **Języki:** [English](README.md) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | [Tiếng Việt](README_vi.md) | **Polski** (ta strona)

---

## Co to robi

Dajesz dowolnemu asystentowi AI do kodowania URL tego repozytorium i mówisz:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI klonuje repozytorium, uruchamia deployer, a on:

1. **Wykrywa** które narzędzia AI do kodowania są zainstalowane na Twojej maszynie (obsługa 23 narzędzi).
2. **Generuje** jeden kanoniczny harness — zoptymalizowany w stylu caveman, wieloagentowy, z obsługą pamięci, oparty na loop engineering — z `distill/canon/`.
3. **Wdraża** go do natywnego miejsca konfiguracji każdego wykrytego narzędzia (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Weryfikuje** każdy zapisany plik, odczytując go ponownie (sprawdzenie braku obcięcia).

**Wynik:** niezależnie od tego, które narzędzie AI otworzysz jako następne — wszystkie współdzielą **te same** reguły, protokół pamięci, orkiestrator, umiejętności, hooki i konfigurację MCP. Koniec z utrzymywaniem trzech kopii reguł. Koniec z rozjeżdżaniem się `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Tylko narzędzia **faktycznie zainstalowane** otrzymują wdrożenie. Nic nie jest zapisywane dla narzędzi, które nie zostały wykryte. Możesz również wdrożyć ręcznie — bez użycia AI.

## Dlaczego

Każde narzędzie AI do kodowania przechowuje swoją konfigurację w innym miejscu i formacie:

| Narzędzie | Gdzie żyją jego reguły |
|-----------|------------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

Używasz trzech z nich i utrzymujesz trzy kopie. One się rozjeżdżają. Zapominasz, która jest aktualna. **Agent Harness Deploy naprawia to: jedno źródło (`distill/canon/`), wiele odbiorników.**

W przeciwieństwie do prostych narzędzi do synchronizacji reguł, które tylko kopiują tekst między plikami konfiguracyjnymi, to wdraża **kompletny harness agenta**: reguły + umiejętności + persony workerów + protokół pamięci + loop engineering + hooki + MCP + zasoby vault + czujniki dyscypliny komentarzy/wersji.

## Wdrożenie jedno linią

Powiedz dowolnemu asystentowi AI do kodowania:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI czyta `AGENTS.md`, uruchamia `python scripts/distill.py`, raportuje co wdrożyło. Gotowe.

Zobacz [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) dla pełnej umowy.

## Wdrożenie ręczne (bez AI)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Dowolny OS, bezpośrednio
python scripts/distill.py
```

Zobacz [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Obsługa wieloplatformowa

Ten projekt działa na **Windows, macOS i Linux**.

| Platforma | Wymagania | Polecenie wdrożenia |
|-----------|-----------|---------------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| Dowolny OS | Python 3.9+ | `python scripts/distill.py` |

### Jak działa wieloplatformowość

- Wszystkie skrypty Python używają `pathlib` (bez zakodowanych na sztywno separatorów `\` ani `/`).
- Ścieżki narzędzi w `adapters/registry.json` używają rozwijania zmiennych środowiskowych: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- Na macOS/Linux zmienne środowiskowe specyficzne dla Windows (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) automatycznie fallbackują do ścieżek w stylu XDG (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` jest dla Windows; `deploy.sh` jest dla macOS/Linux. Oba wywołują ten sam `python scripts/distill.py`.

### Narzędzia specyficzne dla platformy

| Narzędzie | Windows | macOS | Linux | Uwaga |
|-----------|---------|-------|-------|-------|
| Claude Desktop | ✓ | — | — | Aplikacja tylko na Windows; wykrywanie pomija na macOS/Linux |
| ChatGPT Desktop | ✓ | — | — | Aplikacja tylko na Windows; wykrywanie pomija na macOS/Linux |
| Cursor | ✓ | ✓ | ✓ | Wykrywa `${APPDATA}/Cursor` (Win) lub `~/Library/Application Support/Cursor` (macOS) |
| Wszystkie inne narzędzia | ✓ | ✓ | ✓ | Wykrywane przez komendę CLI na PATH |

## Co zawiera harness — 5 filarów technicznych

Deployer synchronizuje kanoniczny zestaw reguł zbudowany na 5 filarach inżynierii harnessu agenta:

| Filar | Co Ci daje | Plik vault | Dokumentacja |
|-------|------------|------------|--------------|
| **1. Kompresja tokenów caveman** | ~65% redukcji tokenów, więcej użytecznego kontekstu | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Hierarchia Commander-Worker** | AI promptuje samo siebie — jeden orkiestrator, wielu wyspecjalizowanych workerów; dispatch zestawu trójelementowego | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Loop engineering + kontrola Vault** | `/loop` (monitorowanie) vs `/goal` (zbieżne); maker ≠ checker; dyscyplina SHA | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. Głęboka pamięć repo** | Trójwarstwowa pamięć dyskowa (hot <3KB, knowledge <8KB, cold ∞); opcjonalne hybrydowe wyszukiwanie deep-memory | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. Realignacja granicy sandbox** | 100% wydajności dla ścieżek niekrytycznych; kontrakt ryzyka JSON dla plików krytycznych | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Dodatkowe koncepcje nałożone na wierzch: **harness engineering** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **tryby wielomyślenia** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **rubryki ocen** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **dyscyplina komentarzy i wersji** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Dyscyplina komentarzy i wersji (zapobieganie AI slop)

Asystenty AI do kodowania produkują dwie trwałe formy slop, które przetrwają w repozytorium:

1. **Nadużycie wyjaśnień** — komentarze, które przepowiadają kod (`# przejdź przez elementy` nad `for x in items:`). Zero informacji, marnuje tokeny, gnije gdy kod się zmienia.
2. **Nakładanie wersji** — znaczniki wersji w pliku akumulujące się przez edycje (`<!-- v2 -->`, `# v3 naprawiono X`). Rot kontekstu i dług głębokości rekurencyjnej.

Ten harness zapobiega obu przez **trójwarstwową obronę**:

| Warstwa | Mechanizm | Plik |
|---------|-----------|------|
| **Prewencja w canon** | REDLINES #16 (bez komentarzy wyjaśniających) + #17 (bez nakładania wersji w pliku) + CORE_CANON dyscyplina komentarzy/wersji | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **Wykrywanie przez skill** | `harness-sensor` SENSOR-4b (slop komentarzy, graceful degradation) + SENSOR-4c (nakładanie wersji, zawsze uruchomiony) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **Zabezpieczenie mechaniczne** | `sync.py` bramka pre-sync odrzuca pliki canon z nałożonymi znacznikami wersji | [`scripts/sync.py`](scripts/sync.py) |

Poparte badaniami: arXiv 2605.02741 (Prawo odwrotne objętość-jakość), arXiv 2512.20334 (Pułapki komentarzy), arXiv 2606.09090 (Rot kontekstu). Zobacz [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) dla pełnej ewaluacji 6 narzędzi CLI open-source.

## Architektura anty-link-rot (wbudowany Vault)

Wszystkie zewnętrzne mechanizmy konfiguracji technicznej są **wbudowane i lokalnie buforowane** w `core/assets/vault/`. Deployer **nie** pobiera schematów z zewnętrznych repozytoriów w czasie działania. To niezmienna lokalna baza danych szablonów:

| Plik vault | Wbudowane źródło |
|------------|------------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

Zobacz [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Obsługiwane narzędzia (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Dodanie narzędzia to wpis w rejestrze + 6-linijkowy adapter. Zobacz [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Układ repozytorium

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # Plik wejściowy dla narzędzi obsługujących AGENTS.md
├── CLAUDE.md                  # Plik wejściowy dla narzędzi obsługujących CLAUDE.md
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10 kolejnych języków
├── core/assets/               # Vault, skills, runtime (hooks, settings, MCP)
├── Docs/                      # Dokumentacja
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # Adaptery narzędzi + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                   # Własny harness deployera (dogfooded)
```

Zobacz [`Docs/00-Overview.md`](Docs/00-Overview.md) dla szczegółowych opisów katalogów.

## Szybkie polecenia

```bash
python scripts/detect.py            # zobacz które narzędzia są zainstalowane
python scripts/distill.py           # pełne wdrożenie: detect → sync → verify
python scripts/distill.py --global  # także synchronizacja globalnych plików wejściowych
python scripts/distill.py --dry-run # tylko wykrywanie, bez zapisów
python scripts/verify.py            # ponowna weryfikacja po sync
python scripts/sync.py --canon      # regeneruj AGENTS.md po edycji canon
```

## Jak to działa (wersja 30-sekundowa)

1. `detect.py` czyta `adapters/registry.json`, uruchamia sprawdzenia wykrywania każdego narzędzia (binarka CLI, ścieżka env, dane aplikacji).
2. `sync.py` łączy `distill/canon/*.md` w jedno kanoniczne ciało, zapisuje je do natywnego pliku wejściowego każdego wykrytego narzędzia (najpierw robiąc kopię zapasową istniejących plików do `.bak`). Tylko wykryte narzędzia otrzymują zapis.
3. `verify.py` odczytuje ponownie każdy zapisany plik i potwierdza obecność znacznika kanonicznego (sprawdzenie braku obcięcia).

Pełny projekt: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## FAQ

<details>
<summary><strong>Czym jest Agent Harness Deploy?</strong></summary>

Agent Harness Deploy to samorozpakowujący się, wielonarzędziowy deployer harnessu AI. Wykrywa które narzędzia AI do kodowania masz zainstalowane, a następnie generuje i synchronizuje jeden kanoniczny harness (zoptymalizowany w stylu caveman, wieloagentowy, z obsługą pamięci, oparty na loop engineering) do natywnego miejsca konfiguracji każdego wykrytego narzędzia — tak aby wszystkie Twoje narzędzia AI współdzieliły te same reguły.
</details>

<details>
<summary><strong>Jak wdrożyć harness?</strong></summary>

Powiedz dowolnemu asystentowi AI do kodowania: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. Albo uruchom ręcznie: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>Które narzędzia AI do kodowania są obsługiwane?</strong></summary>

23 narzędzia: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Dodanie narzędzia wymaga jednego wpisu w rejestrze + 6-linijkowego adaptera.
</details>

<details>
<summary><strong>Czy zapisuje konfiguracje dla narzędzi, których nie mam zainstalowanych?</strong></summary>

Nie. Wykrywanie jest święte — tylko narzędzia faktycznie zainstalowane na Twojej maszynie otrzymują wdrożenie. Jeśli narzędzie nie jest wykryte, jest raportowane jako "nie wykryto" i pomijane. Zero niepotrzebnego śladu.
</details>

<details>
<summary><strong>Czym jest kompresja tokenów caveman?</strong></summary>

Tryb caveman usuwa wypełniacz (owijanie w bawełnę, uprzejmości, przepowiadanie pytania) z komunikacji agenta, zachowując przy tym całą evidencję (kod, ścieżki, błędy, dokładne wartości) dosłownie. To osiąga ~65% redukcji tokenów, efektywnie mnożąc użyteczne okno kontekstu. Zobacz `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>Czym jest hierarchia Commander-Worker?</strong></summary>

Główny wątek (Commander) decyduje, deleguje i integruje. Workery skanują i edytują. To zapobiega wypełnianiu głównego kontekstu szczegółami niskopoziomowymi, zachowując centralizację podejmowania decyzji. Zobacz `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>Jak działa system pamięci?</strong></summary>

Trójwarstwowa pamięć dyskowa: warstwa hot (rejestr <3KB, stan per-sesja <8KB), warstwa knowledge (antywzorce <8KB), warstwa cold (archiwum, tylko grep). Stan utrzymuje się na dysku, nie w kontekście — więc sesje przetrwają restarty narzędzi. Zobacz `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>Czym jest dyscyplina komentarzy i wersji?</strong></summary>

Trójwarstwowa obrona przed generowanym przez AI slop komentarzy (nadużycie wyjaśnień) i nakładaniem wersji w pliku. Warstwa 1: czerwone linie canon (#16, #17). Warstwa 2: skill harness-sensor (SENSOR-4b/4c). Warstwa 3: zabezpieczenie mechaniczne sync.py. Zobacz `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>Czy to jest narzędzie jailbreak lub usuwania zabezpieczeń?</strong></summary>

Nie. To jest defensywne narzędzie harness. Konfiguruje pliki reguł asystentów AI do kodowania. Nie modyfikuje wag modelu, nie usuwa zabezpieczeń bezpieczeństwa i nie dołącza narzędzi jailbreak. Realignacja granicy sandbox działa na poziomie pliku przez kontrakty ryzyka JSON, nie na poziomie modelu przez usuwanie pętli odmowy.
</details>

<details>
<summary><strong>Jakiej licencji podlega ten projekt?</strong></summary>

Licencja MIT — zobacz [LICENSE](LICENSE). Copyright (c) masteryee-labs.
</details>

<details>
<summary><strong>Czy mogę dodać własne narzędzie AI?</strong></summary>

Tak. Dodanie narzędzia wymaga jednego wpisu w `adapters/registry.json` + 6-linijkowej klasy adaptera. Zobacz `Docs/03-Tool-Adapters.md`.
</details>

## Klauzula szczerości

Deployer potrafi niezawodnie: wykrywać, generować konfigurację, synchronizować pliki, weryfikować, robić kopie zapasowe. Nie potrafi: decyzji estetycznych, zgadywania czego chcesz poza umową wdrożenia, pisania konfiguracji dla narzędzi których nie może wykryć. Gdy nie jest pewien, raportuje — nie zmyśla. Pełne oświadczenie w [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Uwaga o bezpieczeństwie

To repozytorium jest **defensywnym** narzędziem harness. Konfiguruje pliki reguł asystentów AI do kodowania. **Nie** modyfikuje wag modelu, **nie** usuwa zabezpieczeń bezpieczeństwa i **nie** dołącza ani nie popiera narzędzi jailbreak/usuwania zabezpieczeń. Projekt Heretic jest przywoływany w glosariuszu tylko jako część krajobrazu interpretowalności, który ukształtował zrozumienie harnessu wektorów sterujących — nie jest tu używany. Zobacz [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Wymagania

- Python 3.9+
- Co najmniej jedno obsługiwane narzędzie AI do kodowania zainstalowane (inaczej nie ma dokąd wdrożyć)

## Licencja

MIT — zobacz [LICENSE](LICENSE).

## Referencje

Zobacz [`Docs/REFERENCES.md`](Docs/REFERENCES.md) dla referencji źródłowych według filaru.

## Indeks dokumentacji

| Dokument | Temat |
|----------|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Przegląd i indeks |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Pełny projekt systemu |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | Jak działa "deploy:" |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Lokalizacje konfiguracji per narzędzie |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Commander + Workery + samoorkiestracja |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Redukcja halucynacji |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Częste problemy |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Terminy i źródła |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI slop komentarzy + nakładanie wersji: ewaluacja narzędzi CLI |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | System Nuwa + Zespół Nuwa (równoległe rozumowanie, różnorodność poznawcza) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Kompresja tokenów (dawniej Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Trójwarstwowa pamięć (dawniej Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Loop engineering, 5+1 komponentów (dawniej Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | System wokół modelu (dawniej Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, dyscyplina SHA (dawniej Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Twarde zatrzymania + płaszczyzna sterowania (dawniej Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Externalizowane kryteria decyzyjne (dawniej Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Delegacja Commander-Worker (dawniej Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Vault wbudowanych zasobów anty-link-rot |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Warstwa runtime: hooki, ustawienia, szablony MCP |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Atrybucja vendored nuwa-skill i inwentarz plików |

---

<details>
<summary><em>Metadane SEO / AEO / GEO / LLMO</em></summary>

**Nazwa projektu:** Agent Harness Deploy

**Opis jedno linią:** Samorozpakowujący się, wielonarzędziowy harness AI — jedno kanoniczne źródło, 23 odbiorniki narzędzi AI do kodowania.

**Słowa kluczowe:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, harness AI, synchronizacja konfiguracji AI, narzędzia AI do kodowania, harness agenta, kompresja tokenów caveman, inżynieria pętli, protokół pamięci agenta, dyscyplina komentarzy, zapobieganie nakładaniu wersji, wieloagentowy harness, wdrażanie harness AI

**Kluczowe fakty do cytowania przez AI/LLM:**
- 23 narzędzia AI do kodowania obsługiwane (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot itd.)
- Jedno kanoniczne źródło (`distill/canon/`), wiele natywnych dla narzędzi odbiorników
- 5 filarów technicznych: kompresja caveman, Commander-Worker, loop engineering, głęboka pamięć, granica sandbox
- Trójwarstwowa dyscyplina komentarzy/wersji: czerwone linie canon + czujniki skill + zabezpieczenie mechaniczne
- Wieloplatformowość: Windows, macOS, Linux (Python 3.9+)
- Licencja MIT, copyright masteryee-labs
- Anty-link-rot: wszystkie zewnętrzne schematy wbudowane w `core/assets/vault/`
- Polecenie wdrożenia: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Grupa docelowa:** Programiści używający wielu asystentów AI do kodowania, którzy chcą spójnych reguł we wszystkich narzędziach. Współtwórcy open-source, zespoły inżynieryjne AI-first, samodzielni programiści używający Claude Code + Cursor + Codex jednocześnie.

**Kategoria:** Narzędzia deweloperskie > Asystenci AI do kodowania > Zarządzanie konfiguracją > Inżynieria harnessu agenta
</details>
