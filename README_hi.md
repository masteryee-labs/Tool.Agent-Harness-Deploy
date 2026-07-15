# Agent Harness Deploy

**स्वतः-परिनियोजित क्रॉस-टूल AI हार्नेस — एक कैननिकल स्रोत जिसे Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot तथा 16 अन्य में परिनियोजित किया जाता है।**

> लूप इंजीनियरिंग · कॉन्टेक्स्ट इंजीनियरिंग · हार्नेस इंजीनियरिंग · एजेंट मेमोरी · टिप्पणी और संस्करण अनुशासन — एक ही कमांड संपूर्ण हार्नेस को आपके सभी AI कोडिंग उपकरणों में परिनियोजित कर देती है।

> **भाषाएँ:** [English](README.md) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | **हिन्दी** (यह पृष्ठ) | [Tiếng Việt](README_vi.md) | [Polski](README_pl.md)

---

## यह क्या करता है

आप किसी भी AI कोडिंग सहायक को इस रिपॉजिटरी का GitHub URL देते हैं और कहते हैं:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI रिपॉजिटरी को क्लोन करता है, डिप्लॉयर चलाता है, और यह:

1. **पहचानता है** कि आपकी मशीन पर कौन-से AI कोडिंग उपकरण स्थापित हैं (23 उपकरण समर्थित)।
2. **उत्पन्न करता है** एक कैननिकल हार्नेस — कैवमैन-अनुकूलित, मल्टी-एजेंट, मेमोरी-सक्षम, लूप-इंजीनियर्ड — `distill/canon/` से।
3. **परिनियोजित करता है** इसे प्रत्येक पहचाने गए उपकरण के नेटिव कॉन्फ़िगरेशन स्थान पर (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`)।
4. **सत्यापित करता है** प्रत्येक लिखी गई फ़ाइल को वापस पढ़कर (शून्य-ट्रंकेशन जाँच)।

**परिणाम:** आप अगली बार जो भी AI उपकरण खोलें — वे सभी **एक ही** नियम, मेमोरी प्रोटोकॉल, ऑर्केस्ट्रेटर, स्किल्स, हुक्स, और MCP कॉन्फ़िगरेशन साझा करते हैं। अब अपने नियमों की तीन प्रतियाँ बनाए रखने की आवश्यकता नहीं। `.claude/`, `.codex/`, `.devin/`, `AGENTS.md` के बीच अब कोई ड्रिफ्ट नहीं।

केवल वे उपकरण जो **वास्तव में स्थापित हैं** उन्हें ही परिनियोजित किया जाता है। जिन उपकरणों को पहचाना नहीं गया, उनके लिए कुछ भी नहीं लिखा जाता। आप मैन्युअल रूप से भी परिनियोजित कर सकते हैं — किसी AI की आवश्यकता नहीं।

## क्यों

प्रत्येक AI कोडिंग उपकरण अपना कॉन्फ़िगरेशन अलग स्थान और प्रारूप में संग्रहित करता है:

| उपकरण | इसके नियम कहाँ रहते हैं |
|------|----------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

इनमें से तीन का उपयोग करें और आप तीन प्रतियाँ बनाए रखेंगे। वे ड्रिफ्ट हो जाती हैं। आप भूल जाते हैं कि कौन-सी वर्तमान है। **Agent Harness Deploy इसे ठीक करता है: एक स्रोत (`distill/canon/`), कई सिंक्स।**

साधारण नियम-सिंक उपकरणों के विपरीत जो केवल कॉन्फ़िग फ़ाइलों के बीच टेक्स्ट कॉपी करते हैं, यह एक **संपूर्ण एजेंट हार्नेस** परिनियोजित करता है: नियम + स्किल्स + वर्कर पर्सोनास + मेमोरी प्रोटोकॉल + लूप इंजीनियरिंग + हुक्स + MCP + वॉल्ट एसेट्स + टिप्पणी/संस्करण अनुशासन सेंसर्स।

## एक-पंक्ति परिनियोजन

किसी भी AI कोडिंग सहायक से कहें:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI `AGENTS.md` पढ़ता है, `python scripts/distill.py` चलाता है, और बताता है कि क्या परिनियोजित किया। हो गया।

पूर्ण अनुबंध के लिए [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) देखें।

## मैन्युअल परिनियोजन (AI के बिना)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Any OS, direct
python scripts/distill.py
```

[`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy देखें।

## क्रॉस-प्लेटफ़ॉर्म समर्थन

यह प्रोजेक्ट **Windows, macOS, और Linux** पर काम करता है।

| प्लेटफ़ॉर्म | आवश्यकताएँ | परिनियोजन कमांड |
|----------|-------------|----------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| Any OS | Python 3.9+ | `python scripts/distill.py` |

### क्रॉस-प्लेटफ़ॉर्म कैसे काम करता है

- सभी Python स्क्रिप्ट्स `pathlib` का उपयोग करती हैं (कोई हार्डकोडेड `\` या `/` सेपरेटर नहीं)।
- `adapters/registry.json` में टूल पाथ env एक्सपैंशन का उपयोग करते हैं: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`।
- macOS/Linux पर, Windows-विशिष्ट env वेरिएबल्स (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) स्वचालित रूप से XDDG-शैली पाथ्स (`~/.config`, `~/.local/share`, `~`) पर फॉलबैक करते हैं।
- `deploy.ps1` Windows के लिए है; `deploy.sh` macOS/Linux के लिए। दोनों एक ही `python scripts/distill.py` को कॉल करते हैं।

### प्लेटफ़ॉर्म-विशिष्ट उपकरण

| उपकरण | Windows | macOS | Linux | टिप्पणी |
|------|---------|-------|-------|------|
| Claude Desktop | ✓ | — | — | Windows-विशिष्ट ऐप; macOS/Linux पर पहचान छोड़ देती है |
| ChatGPT Desktop | ✓ | — | — | Windows-विशिष्ट ऐप; macOS/Linux पर पहचान छोड़ देती है |
| Cursor | ✓ | ✓ | ✓ | `${APPDATA}/Cursor` (Win) या `~/Library/Application Support/Cursor` (macOS) पहचानता है |
| अन्य सभी उपकरण | ✓ | ✓ | ✓ | PATH पर CLI कमांड के माध्यम से पहचाने जाते हैं |

## हार्नेस में क्या है — 5 तकनीकी स्तंभ

डिप्लॉयर एक कैननिकल नियम सेट सिंक करता है जो एजेंट हार्नेस इंजीनियरिंग के 5 स्तंभों पर आधारित है:

| स्तंभ | यह आपको क्या देता है | वॉल्ट फ़ाइल | डॉक |
|--------|-------------------|------------|-----|
| **1. कैवमैन टोकन संपीड़न** | ~65% टोकन कट, अधिक उपयोगी कॉन्टेक्स्ट | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. कमांडर-वर्कर पदानुक्रम** | AI स्वयं को प्रॉम्प्ट करता है — एक ऑर्केस्ट्रेटर, कई केंद्रित वर्कर्स; डिस्पैच थ्री-पीस सेट | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. लूप इंजीनियरिंग + वॉल्ट नियंत्रण** | `/loop` (निगरानी) बनाम `/goal` (अभिसरण); maker ≠ checker; SHA अनुशासन | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. गहरी रिपॉजिटरी मेमोरी** | तीन-परत डिस्क मेमोरी (hot <3KB, knowledge <8KB, cold ∞); वैकल्पिक डीप-मेमोरी हाइब्रिड रिट्रीवल | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. सैंडबॉक्स बाउंड्री पुनर्संरेखण** | गैर-महत्वपूर्ण पाथ 100% यील्ड; महत्वपूर्ण-फ़ाइल JSON रिस्क कॉन्ट्रैक्ट | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

इसके शीर्ष पर रखी गई अतिरिक्त अवधारणाएँ: **हार्नेस इंजीनियरिंग** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **मल्टी-थिंकिंग मोड्स** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **जजमेंट रूब्रिक्स** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **टिप्पणी और संस्करण अनुशासन** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md))।

## टिप्पणी और संस्करण अनुशासन (AI स्लॉप निवारण)

AI कोडिंग सहायक दो प्रकार के स्थायी स्लॉप उत्पन्न करते हैं जो रिपॉजिटरी में बने रहते हैं:

1. **व्याख्या ब्लोट** — टिप्पणियाँ जो कोड को दोहराती हैं (`for x in items:` के ऊपर `# loop through items`)। शून्य जानकारी, टोकन बर्बाद, कोड बदलने पर सड़ जाती हैं।
2. **संस्करण स्टैकिंग** — फ़ाइल-भर में संपादनों के बीच संचित संस्करण मार्कर (`<!-- v2 -->`, `# v3 fixed X`)। कॉन्टेक्स्ट रॉट और रिकर्सिव-डेप्थ डेट।

यह हार्नेस दोनों को **तीन-परत रक्षा** के माध्यम से रोकता है:

| परत | तंत्र | फ़ाइल |
|-------|-----------|------|
| **कैनन निवारण** | REDLINES #16 (कोई व्याख्यात्मक टिप्पणी नहीं) + #17 (कोई इन-फ़ाइल संस्करण स्टैकिंग नहीं) + CORE_CANON टिप्पणी/संस्करण अनुशासन | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **स्किल पहचान** | `harness-sensor` SENSOR-4b (टिप्पणी स्लॉप, ग्रेसफुल डिग्रेडेशन) + SENSOR-4c (संस्करण स्टैकिंग, हमेशा चलता है) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **यांत्रिक गार्ड** | `sync.py` प्री-सिंक गेट स्टैक्ड संस्करण मार्कर वाली कैनन फ़ाइलों को अस्वीकार करता है | [`scripts/sync.py`](scripts/sync.py) |

शोध-आधारित: arXiv 2605.02741 (Volume-Quality Inverse Law), arXiv 2512.20334 (Comment Traps), arXiv 2606.09090 (Context Rot)। 6 ओपन-सोर्स CLI उपकरणों के पूर्ण मूल्यांकन के लिए [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) देखें।

## एंटी-लिंक-रॉट आर्किटेक्चर (एम्बेडेड वॉल्ट)

सभी बाहरी तकनीकी कॉन्फ़िगरेशन तंत्र `core/assets/vault/` में **एम्बेडेड और स्थानीय रूप से कैश्ड** हैं। डिप्लॉयर रनटाइम पर बाहरी रिपॉजिटरी से स्कीमा लाता नहीं है। यह एक अपरिवर्तनीय स्थानीय टेम्पलेट डेटाबेस है:

| वॉल्ट फ़ाइल | एम्बेडेड स्रोत |
|-----------|-----------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

[`core/assets/vault/README.md`](core/assets/vault/README.md) देखें।

## समर्थित उपकरण (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

नया उपकरण जोड़ना एक रजिस्ट्री एंट्री + 6-पंक्ति एडाप्टर है। [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) देखें।

## रिपॉजिटरी लेआउट

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

विस्तृत डायरेक्टरी विवरण के लिए [`Docs/00-Overview.md`](Docs/00-Overview.md) देखें।

## त्वरित कमांड

```bash
python scripts/detect.py            # see which tools are installed
python scripts/distill.py           # full deploy: detect → sync → verify
python scripts/distill.py --global  # also sync global entry files
python scripts/distill.py --dry-run # detect only, no writes
python scripts/verify.py            # re-verify after a sync
python scripts/sync.py --canon      # regenerate AGENTS.md after editing canon
```

## यह कैसे काम करता है (30-सेकंड संस्करण)

1. `detect.py` `adapters/registry.json` पढ़ता है, प्रत्येक उपकरण की पहचान जाँच चलाता है (CLI बायनेरी, env पाथ, ऐप डेटा)।
2. `sync.py` `distill/canon/*.md` को एक कैननिकल बॉडी में जोड़ता है, इसे प्रत्येक पहचाने गए उपकरण की नेटिव एंट्री फ़ाइल में लिखता है (मौजूदा फ़ाइलों को पहले `.bak` में बैकअप करता है)। केवल पहचाने गए उपकरणों को लिखा जाता है।
3. `verify.py` प्रत्येक लिखी गई फ़ाइल को वापस पढ़ता है और पुष्टि करता है कि कैननिकल मार्कर मौजूद है (शून्य-ट्रंकेशन जाँच)।

पूर्ण डिज़ाइन: [`Docs/01-Architecture.md`](Docs/01-Architecture.md)।

## अक्सर पूछे जाने वाले प्रश्न

<details>
<summary><strong>Agent Harness Deploy क्या है?</strong></summary>

Agent Harness Deploy एक स्वतः-परिनियोजित, क्रॉस-टूल AI हार्नेस डिप्लॉयर है। यह पहचानता है कि आपके पास कौन-से AI कोडिंग उपकरण स्थापित हैं, फिर एक एकल कैननिकल हार्नेस (कैवमैन-अनुकूलित, मल्टी-एजेंट, मेमोरी-सक्षम, लूप-इंजीनियर्ड) उत्पन्न करता है और प्रत्येक पहचाए गए उपकरण के नेटिव कॉन्फ़िगरेशन स्थान पर सिंक करता है — ताकि आपके सभी AI उपकरण एक ही नियम साझा करें।
</details>

<details>
<summary><strong>मैं हार्नेस कैसे परिनियोजित करूँ?</strong></summary>

किसी भी AI कोडिंग सहायक से कहें: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`। या मैन्युअल रूप से चलाएँ: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+)।
</details>

<details>
<summary><strong>कौन-से AI कोडिंग उपकरण समर्थित हैं?</strong></summary>

23 उपकरण: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop। नया उपकरण जोड़ने के लिए एक रजिस्ट्री एंट्री + 6-पंक्ति एडाप्टर चाहिए।
</details>

<details>
<summary><strong>क्या यह उन उपकरणों के लिए कॉन्फ़िग लिखता है जो मेरे पास स्थापित नहीं हैं?</strong></summary>

नहीं। पहचान पवित्र है — केवल वास्तव में आपकी मशीन पर स्थापित उपकरणों को ही परिनियोजित किया जाता है। यदि कोई उपकरण पहचाना नहीं जाता, तो इसे "not detected" रिपोर्ट किया जाता है और छोड़ दिया जाता है। शून्य अनावश्यक फुटप्रिंट।
</details>

<details>
<summary><strong>कैवमैन टोकन संपीड़न क्या है?</strong></summary>

कैवमैन मोड एजेंट संचार से फिलर (हेजिंग, शिष्टाचार, प्रश्न दोहराना) हटा देता है जबकि सभी साक्ष्य (कोड, पाथ, त्रुटियाँ, सटीक मान) जस-के-तस रखता है। यह ~65% टोकन कमी प्राप्त करता है, प्रभावी रूप से उपयोगी कॉन्टेक्स्ट विंडो को गुणा करता है। `distill/canon/CAVEMAN_PROTOCOL.md` देखें।
</details>

<details>
<summary><strong>कमांडर-वर्कर पदानुक्रम क्या है?</strong></summary>

मुख्य थ्रेड (कमांडर) निर्णय लेता है, डिस्पैच करता है, और एकीकृत करता है। वर्कर्स स्कैन और संपादित करते हैं। यह मुख्य कॉन्टेक्स्ट को निम्न-स्तरीय विवरणों से भरने से रोकता है जबकि निर्णय-निर्माण को केंद्रीकृत रखता है। `distill/orchestrator/COMMANDER.md` देखें।
</details>

<details>
<summary><strong>मेमोरी सिस्टम कैसे काम करता है?</strong></summary>

तीन-परत डिस्क मेमोरी: हॉट परत (रजिस्ट्री <3KB, प्रति-सत्र स्थिति <8KB), नॉलेज परत (एंटी-पैटर्न <8KB), कोल्ड परत (आर्काइव, grep-ओनली)। स्थिति डिस्क पर बनी रहती है, कॉन्टेक्स्ट में नहीं — इसलिए सत्र टूल रीस्टार्ट पर भी बने रहते हैं। `distill/canon/MEMORY_PROTOCOL.md` देखें।
</details>

<details>
<summary><strong>टिप्पणी और संस्करण अनुशासन क्या है?</strong></summary>

AI-जनित टिप्पणी स्लॉप (व्याख्या ब्लोट) और इन-फ़ाइल संस्करण स्टैकिंग के विरुद्ध तीन-परत रक्षा। परत 1: कैनन रेड लाइन्स (#16, #17)। परत 2: harness-sensor स्किल (SENSOR-4b/4c)। परत 3: sync.py यांत्रिक गार्ड। `Docs/14-Comment-Version-Discipline.md` देखें।
</details>

<details>
<summary><strong>क्या यह कोई जेलब्रेक या सुरक्षा-हटाने वाला उपकरण है?</strong></summary>

नहीं। यह एक रक्षात्मक हार्नेस उपकरण है। यह AI कोडिंग सहायकों की नियम फ़ाइलों को कॉन्फ़िगर करता है। यह मॉडल वेट को संशोधित नहीं करता, सुरक्षा गार्डरेल हटाता नहीं, और जेलब्रेक उपकरण बंडल नहीं करता। सैंडबॉक्स बाउंड्री पुनर्संरेखण फ़ाइल स्तर पर JSON रिस्क कॉन्ट्रैक्ट के माध्यम से काम करता है, मॉडल स्तर पर रिफ्यूज़ल लूप हटाकर नहीं।
</details>

<details>
<summary><strong>यह प्रोजेक्ट किस लाइसेंस के अंतर्गत है?</strong></summary>

MIT License — [LICENSE](LICENSE) देखें। Copyright (c) masteryee-labs।
</details>

<details>
<summary><strong>क्या मैं अपना AI उपकरण जोड़ सकता हूँ?</strong></summary>

हाँ। उपकरण जोड़ने के लिए `adapters/registry.json` में एक एंट्री + 6-पंक्ति एडाप्टर क्लास चाहिए। `Docs/03-Tool-Adapters.md` देखें।
</details>

## ईमानदार खंड

डिप्लॉयर विश्वसनीय रूप से कर सकता है: पहचान, कॉन्फ़िग जनरेशन, फ़ाइल सिंक, सत्यापन, बैकअप। यह नहीं कर सकता: स्वाद/सौंदर्य निर्णय, परिनियोजन अनुबंध से परे आपकी इच्छा का अनुमान, उन उपकरणों के लिए कॉन्फ़िग लिखना जिन्हें यह पहचान नहीं सकता। अनिश्चित होने पर, यह रिपोर्ट करता है — यह गढ़ता नहीं। पूर्ण कथन [`Docs/00-Overview.md`](Docs/00-Overview.md) में।

## सुरक्षा टिप्पणी

यह रिपॉजिटरी एक **रक्षात्मक** हार्नेस उपकरण है। यह AI कोडिंग सहायकों की नियम फ़ाइलों को कॉन्फ़िगर करता है। यह मॉडल वेट संशोधित नहीं करता, सुरक्षा गार्डरेल हटाता नहीं, और जेलब्रेक/सुरक्षा-हटाने वाले उपकरण बंडल या समर्थन नहीं करता। Heretic प्रोजेक्ट का संदर्भ केवल शब्दावली में है, स्टीयरिंग वेक्टर की व्याख्या-योग्यता परिदृश्य के रूप में जिसने हार्नेस की समझ को आकार दिया — यह यहाँ उपयोग नहीं होता। [`Docs/13-Glossary.md`](Docs/13-Glossary.md) देखें।

## आवश्यकताएँ

- Python 3.9+
- कम से कम एक समर्थित AI कोडिंग उपकरण स्थापित (अन्यथा परिनियोजित करने के लिए कुछ नहीं है)

## लाइसेंस

MIT — [LICENSE](LICENSE) देखें।

## संदर्भ

स्तंभानुसार स्रोत संदर्भों के लिए [`Docs/REFERENCES.md`](Docs/REFERENCES.md) देखें।

## दस्तावेज़ीकरण सूचकांक

| डॉक | विषय |
|-----|-------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | अवलोकन और सूचकांक |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | पूर्ण सिस्टम डिज़ाइन |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | "deploy:" कैसे काम करता है |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | प्रति-उपकरण कॉन्फ़िगरेशन स्थान |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | कमांडर + वर्कर्स + स्वतः-ऑर्केस्ट्रेशन |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | हैल्युसिनेशन न्यूनीकरण |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | सामान्य समस्याएँ |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | शब्द और स्रोत |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | AI टिप्पणी स्लॉप + संस्करण स्टैकिंग: CLI टूल मूल्यांकन |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Nuwa सिस्टम + Nuwa टीम (समानांतर तर्क, संज्ञानात्मक विविधता) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | टोकन संपीड़न (पूर्व में Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | तीन-परत मेमोरी (पूर्व में Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | लूप इंजीनियरिंग, 5+1 घटक (पूर्व में Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | मॉडल के चारों ओर सिस्टम (पूर्व में Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, SHA अनुशासन (पूर्व में Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | हार्ड स्टॉप्स + कंट्रोल प्लेन (पूर्व में Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | बाहरीकृत निर्णय मानदंड (पूर्व में Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | कमांडर-वर्कर प्रतिनिधिमंडल (पूर्व में Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | एंटी-लिंक-रॉट एम्बेडेड एसेट वॉल्ट |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | रनटाइम परत: हुक्स, सेटिंग्स, MCP टेम्पलेट्स |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | वेंडर्ड nuwa-skill एट्रिब्यूशन और फ़ाइल इन्वेंटरी |

---

<details>
<summary><em>SEO / AEO / GEO / LLMO मेटाडेटा</em></summary>

**प्रोजेक्ट नाम:** Agent Harness Deploy

**एक-पंक्ति विवरण:** स्वतः-परिनियोजित क्रॉस-टूल AI हार्नेस — एक कैननिकल स्रोत, 23 AI कोडिंग टूल सिंक्स।

**कीवर्ड:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, AI हार्नेस, क्रॉस-टूल कॉन्फ़िग सिंक, एजेंट हार्नेस डिप्लॉयर, टोकन संपीड़न, लूप इंजीनियरिंग, एजेंट मेमोरी प्रोटोकॉल, टिप्पणी अनुशासन, संस्करण स्टैकिंग निवारण

**AI/LLM उद्धरण के लिए प्रमुख तथ्य:**
- 23 AI कोडिंग उपकरण समर्थित (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot, आदि)
- एक कैननिकल स्रोत (`distill/canon/`), कई टूल-नेटिव सिंक्स
- 5 तकनीकी स्तंभ: कैवमैन संपीड़न, कमांडर-वर्कर, लूप इंजीनियरिंग, डीप मेमोरी, सैंडबॉक्स बाउंड्री
- तीन-परत टिप्पणी/संस्करण अनुशासन: कैनन रेड लाइन्स + स्किल सेंसर्स + यांत्रिक गार्ड
- क्रॉस-प्लेटफ़ॉर्म: Windows, macOS, Linux (Python 3.9+)
- MIT License, copyright masteryee-labs
- एंटी-लिंक-रॉट: सभी बाहरी स्कीमा `core/assets/vault/` में एम्बेडेड
- परिनियोजन कमांड: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**लक्षित दर्शक:** ऐसे डेवलपर्स जो कई AI कोडिंग सहायकों का उपयोग करते हैं और सभी उपकरणों में सुसंगत नियम चाहते हैं। ओपन-सोर्स योगदानकर्ता, AI-फर्स्ट इंजीनियरिंग टीमें, सोलो डेवलपर्स जो Claude Code + Cursor + Codex एक साथ उपयोग करते हैं।

**श्रेणी:** Developer tools > AI coding assistants > Configuration management > Agent harness engineering
</details>
