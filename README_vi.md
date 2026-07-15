# Agent Harness Deploy

**Bộ harness AI đa công cụ tự triển khai — một nguồn chuẩn duy nhất được triển khai đến Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot & 16 công cụ khác.**

> Kỹ thuật vòng lặp · Kỹ thuật ngữ cảnh · Kỹ thuật harness · Bộ nhớ agent · Kỷ luật bình luận và phiên bản — một lệnh triển khai toàn bộ harness đến mọi công cụ AI lập trình của bạn.

> **Ngôn ngữ:** [English](README.md) | [繁體中文](README_zh-TW.md) | [简体中文](README_zh-CN.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [Deutsch](README_de.md) | [Français](README_fr.md) | [Español](README_es.md) | [Português (BR)](README_pt-BR.md) | [Русский](README_ru.md) | [हिन्दी](README_hi.md) | **Tiếng Việt** (trang này) | [Polski](README_pl.md)

---

## Tính năng

Bạn đưa URL GitHub của repo này cho bất kỳ trợ lý AI lập trình nào và nói:

> **deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy**

AI sẽ clone repo, chạy trình triển khai, và nó sẽ:

1. **Phát hiện** những công cụ AI lập trình nào đang được cài đặt trên máy của bạn (hỗ trợ 23 công cụ).
2. **Tạo** một harness chuẩn duy nhất — được tối ưu theo phong cách caveman, đa agent, có bộ nhớ, kỹ thuật vòng lặp — từ `distill/canon/`.
3. **Triển khai** vào vị trí cấu hình gốc của mỗi công cụ được phát hiện (`.claude/`, `.codex/`, `.devin/`, `AGENTS.md`, `.cursor/rules/`).
4. **Xác minh** mọi tệp đã ghi bằng cách đọc lại (kiểm tra cắt xén bằng không).

**Kết quả:** bất kỳ công cụ AI nào bạn mở tiếp theo — tất cả đều dùng chung **cùng** quy tắc, giao thức bộ nhớ, orchestrator, kỹ năng, hooks, và cấu hình MCP. Không còn phải duy trì ba bản sao quy tắc. Không còn lệch pha giữa `.claude/`, `.codex/`, `.devin/`, `AGENTS.md`.

Chỉ những công cụ **thực sự được cài đặt** mới được triển khai. Không ghi gì cho các công cụ không được phát hiện. Bạn cũng có thể triển khai thủ công — không cần AI.

## Lý do

Mỗi công cụ AI lập trình lưu cấu hình ở một vị trí và định dạng khác nhau:

| Công cụ | Nơi lưu quy tắc |
|---------|------------------|
| Claude Code | `.claude/CLAUDE.md` |
| Antigravity / Gemini CLI | `AGENTS.md` |
| Codex / Codex CLI | `.codex/instructions.md` |
| Devin / Devin CLI | `.devin/AGENTS.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Windsurf | `.codeium/windsurf/memories/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Claude Desktop | `claude_desktop_config.json` |

Dùng ba công cụ trong số này thì bạn phải duy trì ba bản sao. Chúng bị lệch pha. Bạn quên bản nào là mới nhất. **Agent Harness Deploy giải quyết vấn đề: một nguồn (`distill/canon/`), nhiều điểm đến.**

Khác với các công cụ đồng bộ quy tắc đơn giản chỉ sao chép văn bản giữa các tệp cấu hình, cái này triển khai một **harness agent hoàn chỉnh**: quy tắc + kỹ năng + nhân vật worker + giao thức bộ nhớ + kỹ thuật vòng lặp + hooks + MCP + tài nguyên vault + cảm biến kỷ luật bình luận/phiên bản.

## Triển khai một dòng

Hãy nói với bất kỳ trợ lý AI lập trình nào:

```
deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy
```

AI đọc `AGENTS.md`, chạy `python scripts/distill.py`, báo cáo những gì đã triển khai. Xong.

Xem [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) để biết toàn bộ hợp đồng triển khai.

## Triển khai thủ công (không cần AI)

```bash
# Windows
powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1

# Linux / macOS
bash scripts/deploy.sh

# Bất kỳ hệ điều hành nào, trực tiếp
python scripts/distill.py
```

Xem [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) §Manual deploy.

## Hỗ trợ đa nền tảng

Dự án này hoạt động trên **Windows, macOS, và Linux**.

| Nền tảng | Yêu cầu | Lệnh triển khai |
|----------|---------|-----------------|
| Windows | Python 3.9+ | `powershell -ExecutionPolicy Bypass -File scripts\deploy.ps1` |
| macOS | Python 3.9+ | `bash scripts/deploy.sh` |
| Linux | Python 3.9+ | `bash scripts/deploy.sh` |
| Bất kỳ hệ điều hành | Python 3.9+ | `python scripts/distill.py` |

### Cách hoạt động đa nền tảng

- Tất cả script Python dùng `pathlib` (không hardcode dấu phân tách `\` hay `/`).
- Đường dẫn công cụ trong `adapters/registry.json` dùng mở rộng biến môi trường: `${HOME}`, `${APPDATA}`, `${LOCALAPPDATA}`, `~`.
- Trên macOS/Linux, các biến môi trường chỉ Windows (`${APPDATA}`, `${LOCALAPPDATA}`, `${USERPROFILE}`) tự động dự phòng về đường dẫn kiểu XDG (`~/.config`, `~/.local/share`, `~`).
- `deploy.ps1` dành cho Windows; `deploy.sh` dành cho macOS/Linux. Cả hai đều gọi cùng `python scripts/distill.py`.

### Công cụ theo nền tảng

| Công cụ | Windows | macOS | Linux | Ghi chú |
|---------|---------|-------|-------|---------|
| Claude Desktop | ✓ | — | — | Ứng dụng chỉ Windows; bỏ qua phát hiện trên macOS/Linux |
| ChatGPT Desktop | ✓ | — | — | Ứng dụng chỉ Windows; bỏ qua phát hiện trên macOS/Linux |
| Cursor | ✓ | ✓ | ✓ | Phát hiện `${APPDATA}/Cursor` (Win) hoặc `~/Library/Application Support/Cursor` (macOS) |
| Các công cụ khác | ✓ | ✓ | ✓ | Phát hiện qua lệnh CLI trên PATH |

## Thành phần harness — 5 trụ cột kỹ thuật

Trình triển khai đồng bộ một bộ quy tắc chuẩn được xây dựng trên 5 trụ cột của kỹ thuật harness agent:

| Trụ cột | Lợi ích mang lại | Tệp vault | Tài liệu |
|---------|------------------|-----------|----------|
| **1. Nén token caveman** | Giảm ~65% token, nhiều ngữ cảnh khả dụng hơn | `core/assets/vault/caveman_template.json` | [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) |
| **2. Phân cấp Commander-Worker** | AI tự phân công — một orchestrator, nhiều worker tập trung; triển khai bộ ba | `core/assets/vault/agency_framework.toml` | [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) |
| **3. Kỹ thuật vòng lặp + Kiểm soát Vault** | `/loop` (giám sát) so với `/goal` (hội tụ); maker ≠ checker; kỷ luật SHA | `agency_framework.toml` + `memory_mcp_schema.json` | [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) |
| **4. Bộ nhớ repo sâu** | Bộ nhớ đĩa ba lớp (hot <3KB, knowledge <8KB, cold ∞); tùy chọn truy xuất hybrid bộ nhớ sâu | `core/assets/vault/memory_mcp_schema.json` | [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) |
| **5. Tái căn chỉnh ranh giới sandbox** | Tỷ lệ hoàn thành 100% cho đường dẫn không quan trọng; hợp đồng rủi ro JSON cho tệp quan trọng | `core/assets/vault/strix_security_rules.json` | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |

Các khái niệm bổ sung được lớp phủ lên trên: **kỹ thuật harness** ([`HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md)), **chế độ đa tư duy** ([`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md)), **rubric đánh giá** ([`JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md)), **kỷ luật bình luận và phiên bản** ([`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md)).

## Kỷ luật bình luận và phiên bản (phòng chống AI slop)

Trợ lý AI lập trình tạo ra hai dạng slop tồn tại dai dẳng trong repo:

1. **Bình luận giải thích thừa** — bình luận nhắc lại code (`# loop through items` phía trên `for x in items:`). Không có thông tin, lãng phí token, mục nát khi code thay đổi.
2. **Xếp chồng phiên bản** — đánh dấu phiên bản tích lũy trong tệp qua các lần chỉnh sửa (`<!-- v2 -->`, `# v3 fixed X`). Mục nát ngữ cảnh và nợ độ sâu đệ quy.

Harness này ngăn chặn cả hai qua **phòng thủ ba lớp**:

| Lớp | Cơ chế | Tệp |
|-----|--------|-----|
| **Phòng ngừa canon** | REDLINES #16 (không bình luận giải thích) + #17 (không xếp chồng phiên bản trong tệp) + kỷ luật Bình luận/Phiên bản CORE_CANON | [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) |
| **Phát hiện kỹ năng** | `harness-sensor` SENSOR-4b (bình luận slop, suy giảm nhẹ nhàng) + SENSOR-4c (xếp chồng phiên bản, luôn chạy) | [`distill/skills/harness-sensor.md`](distill/skills/harness-sensor.md) |
| **Bảo vệ cơ học** | Cổng pre-sync của `sync.py` từ chối tệp canon có dấu phiên bản xếp chồng | [`scripts/sync.py`](scripts/sync.py) |

Có cơ sở nghiên cứu: arXiv 2605.02741 (Định luật nghịch đảo Thể tích-Chất lượng), arXiv 2512.20334 (Bẫy bình luận), arXiv 2606.09090 (Mục nát ngữ cảnh). Xem [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) để biết đánh giá đầy đủ 6 công cụ CLI mã nguồn mở.

## Kiến trúc chống link-rot (Vault nhúng)

Tất cả cơ chế cấu hình kỹ thuật bên ngoài được **nhúng và lưu đệm cục bộ** trong `core/assets/vault/`. Trình triển khai **không** lấy schema từ repo bên ngoài lúc chạy. Đây là cơ sở dữ liệu mẫu cục bộ bất biến:

| Tệp vault | Nguồn nhúng |
|-----------|-------------|
| `caveman_template.json` | JuliusBrussee/caveman, cheeseonamonkey/Lean-Caveman |
| `agency_framework.toml` | msitarzewski/agency-agents, obra/superpowers |
| `memory_mcp_schema.json` | DeusData/codebase-memory-mcp, kevintsai1202/deep-memory |
| `strix_security_rules.json` | usestrix/strix |
| `graphify_knowledge_spec.json` | safishamsi/graphify |

Xem [`core/assets/vault/README.md`](core/assets/vault/README.md).

## Công cụ được hỗ trợ (23)

Claude Code · Antigravity (AGY) · Codex / Codex CLI · Devin / Devin CLI · Cursor · Claude Desktop · OpenCode · OpenClaw · Hermes · ZCode · Kimi Code · AGY CLI · Codex CLI · Devin CLI · Claude Code for VS Code · Codex IDE Extension · GitHub Copilot · Gemini Code Assist · Cline · Roo Code · Continue · Windsurf · ChatGPT Desktop

Thêm một công cụ chỉ cần một mục registry + một adapter 6 dòng. Xem [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md).

## Bố cục repo

```
Tool.Agent-Harness-Deploy/
├── AGENTS.md                  # Tệp vào cho công cụ nhận biết AGENTS.md
├── CLAUDE.md                  # Tệp vào cho công cụ nhận biết CLAUDE.md
├── README.md / README_zh-TW.md / README_zh-CN.md / + 10 ngôn ngữ nữa
├── core/assets/               # Vault, kỹ năng, runtime (hooks, settings, MCP)
├── Docs/                      # Tài liệu
├── distill/                   # canon/ · orchestrator/ · skills/
├── adapters/                  # Adapter công cụ + registry.json
├── scripts/                   # detect, distill, sync, verify, deploy, worktree, plan_dispatch
└── .agents/                    # Harness riêng của trình triển khai (dogfooded)
```

Xem [`Docs/00-Overview.md`](Docs/00-Overview.md) để biết mô tả thư mục chi tiết.

## Lệnh nhanh

```bash
python scripts/detect.py            # xem công cụ nào đã cài đặt
python scripts/distill.py           # triển khai đầy đủ: detect → sync → verify
python scripts/distill.py --global  # đồng bộ thêm tệp vào toàn cục
python scripts/distill.py --dry-run # chỉ phát hiện, không ghi
python scripts/verify.py            # xác minh lại sau sync
python scripts/sync.py --canon      # tạo lại AGENTS.md sau khi sửa canon
```

## Cách hoạt động (phiên bản 30 giây)

1. `detect.py` đọc `adapters/registry.json`, chạy kiểm tra phát hiện của từng công cụ (binary CLI, đường dẫn env, app data).
2. `sync.py` nối `distill/canon/*.md` thành một thân chuẩn, ghi vào tệp vào gốc của từng công cụ được phát hiện (sao lưu tệp hiện có sang `.bak` trước). Chỉ công cụ được phát hiện mới được ghi.
3. `verify.py` đọc lại mọi tệp đã ghi và xác nhận marker chuẩn tồn tại (kiểm tra cắt xén bằng không).

Thiết kế đầy đủ: [`Docs/01-Architecture.md`](Docs/01-Architecture.md).

## Câu hỏi thường gặp

<details>
<summary><strong>Agent Harness Deploy là gì?</strong></summary>

Agent Harness Deploy là trình triển khai harness AI đa công cụ, tự triển khai. Nó phát hiện các công cụ AI lập trình bạn đã cài đặt, sau đó tạo và đồng bộ một harness chuẩn duy nhất (tối ưu caveman, đa agent, có bộ nhớ, kỹ thuật vòng lặp) vào vị trí cấu hình gốc của mỗi công cụ được phát hiện — để tất cả công cụ AI của bạn dùng chung quy tắc.
</details>

<details>
<summary><strong>Làm thế nào để triển khai harness?</strong></summary>

Hãy nói với bất kỳ trợ lý AI lập trình nào: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`. Hoặc chạy thủ công: `python scripts/distill.py` (Windows/macOS/Linux, Python 3.9+).
</details>

<details>
<summary><strong>Những công cụ AI lập trình nào được hỗ trợ?</strong></summary>

23 công cụ: Claude Code, Antigravity (AGY), Codex / Codex CLI, Devin / Devin CLI, Cursor, Claude Desktop, OpenCode, OpenClaw, Hermes, ZCode, Kimi Code, AGY CLI, Codex CLI, Devin CLI, Claude Code for VS Code, Codex IDE Extension, GitHub Copilot, Gemini Code Assist, Cline, Roo Code, Continue, Windsurf, ChatGPT Desktop. Thêm một công cụ chỉ cần một mục registry + một adapter 6 dòng.
</details>

<details>
<summary><strong>Nó có ghi cấu hình cho công cụ tôi chưa cài đặt không?</strong></summary>

Không. Phát hiện là tối thượng — chỉ những công cụ thực sự được cài đặt trên máy của bạn mới được triển khai. Nếu một công cụ không được phát hiện, nó được báo cáo là "không phát hiện" và bỏ qua. Không để lại dấu chân không cần thiết.
</details>

<details>
<summary><strong>Nén token caveman là gì?</strong></summary>

Chế độ caveman loại bỏ văn bản thừa (nhún nhường, xã giao, nhắc lại câu hỏi) khỏi giao tiếp agent trong khi giữ nguyên mọi bằng chứng (code, đường dẫn, lỗi, giá trị chính xác). Điều này đạt được giảm ~65% token, hiệu quả nhân cửa sổ ngữ cảnh khả dụng. Xem `distill/canon/CAVEMAN_PROTOCOL.md`.
</details>

<details>
<summary><strong>Phân cấp Commander-Worker là gì?</strong></summary>

Luồng chính (Commander) quyết định, phân công, và tích hợp. Worker quét và chỉnh sửa. Điều này ngăn ngữ cảnh chính bị lấp đầy bởi chi tiết cấp thấp trong khi giữ việc ra quyết định tập trung. Xem `distill/orchestrator/COMMANDER.md`.
</details>

<details>
<summary><strong>Hệ thống bộ nhớ hoạt động thế nào?</strong></summary>

Bộ nhớ đĩa ba lớp: lớp hot (registry <3KB, trạng thái mỗi phiên <8KB), lớp knowledge (anti-pattern <8KB), lớp cold (lưu trữ, chỉ grep). Trạng thái tồn tại trên đĩa, không trong ngữ cảnh — nên các phiên tồn tại qua các lần khởi động lại công cụ. Xem `distill/canon/MEMORY_PROTOCOL.md`.
</details>

<details>
<summary><strong>Kỷ luật bình luận và phiên bản là gì?</strong></summary>

Phòng thủ ba lớp chống slop bình luận do AI tạo (bình luận giải thích thừa) và xếp chồng phiên bản trong tệp. Lớp 1: red line canon (#16, #17). Lớp 2: kỹ năng harness-sensor (SENSOR-4b/4c). Lớp 3: bảo vệ cơ học sync.py. Xem `Docs/14-Comment-Version-Discipline.md`.
</details>

<details>
<summary><strong>Đây có phải công cụ jailbreak hay gỡ bỏ an toàn không?</strong></summary>

Không. Đây là công cụ harness phòng thủ. Nó cấu hình tệp quy tắc của trợ lý AI lập trình. Nó không sửa trọng số mô hình, không gỡ bỏ rào cản an toàn, và không đóng gói công cụ jailbreak. Tái căn chỉnh ranh giới sandbox hoạt động ở cấp tệp qua hợp đồng rủi ro JSON, không ở cấp mô hình bằng cách gỡ bỏ vòng lặp từ chối.
</details>

<details>
<summary><strong>Dự án này dùng giấy phép gì?</strong></summary>

Giấy phép MIT — xem [LICENSE](LICENSE). Bản quyền (c) masteryee-labs.
</details>

<details>
<summary><strong>Tôi có thể thêm công cụ AI của riêng mình không?</strong></summary>

Có. Thêm một công cụ cần một mục trong `adapters/registry.json` + một lớp adapter 6 dòng. Xem `Docs/03-Tool-Adapters.md`.
</details>

## Điều khoản trung thực

Trình triển khai có thể làm đáng tin cậy: phát hiện, tạo cấu hình, đồng bộ tệp, xác minh, sao lưu. Nó không thể làm: quyết định thẩm mỹ/khẩu vị, đoán điều bạn muốn ngoài hợp đồng triển khai, ghi cấu hình cho công cụ nó không thể phát hiện. Khi không chắc, nó báo cáo — không bịa đặt. Tuyên bố đầy đủ trong [`Docs/00-Overview.md`](Docs/00-Overview.md).

## Lưu ý an toàn

Repo này là công cụ harness **phòng thủ**. Nó cấu hình tệp quy tắc của trợ lý AI lập trình. Nó **không** sửa trọng số mô hình, **không** gỡ bỏ rào cản an toàn, và **không** đóng gói hay tán thành công cụ jailbreak/gỡ bỏ an toàn. Dự án Heretic chỉ được tham chiếu trong bảng thuật ngữ như một phần của bối cảnh khả diễn giải đã định hình hiểu biết của harness về vector điều hướng — nó không được dùng ở đây. Xem [`Docs/13-Glossary.md`](Docs/13-Glossary.md).

## Yêu cầu

- Python 3.9+
- Ít nhất một công cụ AI lập trình được hỗ trợ đã cài đặt (nếu không sẽ không có gì để triển khai)

## Giấy phép

MIT — xem [LICENSE](LICENSE).

## Tham chiếu

Xem [`Docs/REFERENCES.md`](Docs/REFERENCES.md) để biết tham chiếu nguồn theo từng trụ cột.

## Mục lục tài liệu

| Tài liệu | Chủ đề |
|----------|--------|
| [`Docs/00-Overview.md`](Docs/00-Overview.md) | Tổng quan & mục lục |
| [`Docs/01-Architecture.md`](Docs/01-Architecture.md) | Thiết kế hệ thống đầy đủ |
| [`Docs/02-Deployment-Guide.md`](Docs/02-Deployment-Guide.md) | Cách "deploy:" hoạt động |
| [`Docs/03-Tool-Adapters.md`](Docs/03-Tool-Adapters.md) | Vị trí cấu hình theo công cụ |
| [`Docs/04-Orchestrator-Design.md`](Docs/04-Orchestrator-Design.md) | Commander + Workers + tự orchestrate |
| [`Docs/09-Multi-Thinking-Modes.md`](Docs/09-Multi-Thinking-Modes.md) | Giảm ảo giác |
| [`Docs/12-Troubleshooting.md`](Docs/12-Troubleshooting.md) | Vấn đề thường gặp |
| [`Docs/13-Glossary.md`](Docs/13-Glossary.md) | Thuật ngữ & nguồn |
| [`Docs/14-Comment-Version-Discipline.md`](Docs/14-Comment-Version-Discipline.md) | Slop bình luận AI + xếp chồng phiên bản: đánh giá công cụ CLI |
| [`Docs/Agents/nuwa.md`](Docs/Agents/nuwa.md) | Hệ thống Nuwa + Nuwa Team (suy luận song song, đa dạng nhận thức) |
| [`distill/canon/CAVEMAN_PROTOCOL.md`](distill/canon/CAVEMAN_PROTOCOL.md) | Nén token (trước là Docs/05) |
| [`distill/canon/MEMORY_PROTOCOL.md`](distill/canon/MEMORY_PROTOCOL.md) | Bộ nhớ ba lớp (trước là Docs/06) |
| [`distill/canon/LOOP_PROTOCOL.md`](distill/canon/LOOP_PROTOCOL.md) | Kỹ thuật vòng lặp, 5+1 thành phần (trước là Docs/07) |
| [`distill/canon/HARNESS_ENGINEERING.md`](distill/canon/HARNESS_ENGINEERING.md) | Hệ thống quanh mô hình (trước là Docs/08) |
| [`distill/canon/VERIFICATION_PROTOCOL.md`](distill/canon/VERIFICATION_PROTOCOL.md) | Maker ≠ Checker, kỷ luật SHA (trước là Docs/10) |
| [`distill/canon/REDLINES.md`](distill/canon/REDLINES.md) | Hard stop + control plane (trước là Docs/harness_control_plane) |
| [`distill/canon/JUDGMENT_RUBRICS.md`](distill/canon/JUDGMENT_RUBRICS.md) | Tiêu chí quyết định ngoại hóa (trước là Docs/harness_rubrics) |
| [`distill/orchestrator/COMMANDER.md`](distill/orchestrator/COMMANDER.md) | Ủy quyền Commander-Worker (trước là Docs/Agents/commander) |
| [`core/assets/vault/README.md`](core/assets/vault/README.md) | Vault tài sản nhúng chống link-rot |
| [`core/assets/runtime/README.md`](core/assets/runtime/README.md) | Lớp runtime: hooks, settings, mẫu MCP |
| [`core/assets/skills/nuwa-skill/ATTRIBUTION.md`](core/assets/skills/nuwa-skill/ATTRIBUTION.md) | Ghi công nuwa-skill vendored & danh mục tệp |

---

<details>
<summary><em>Siêu dữ liệu SEO / AEO / GEO / LLMO</em></summary>

**Tên dự án:** Agent Harness Deploy

**Mô tả một dòng:** Bộ harness AI đa công cụ tự triển khai — một nguồn chuẩn duy nhất, 23 điểm đến công cụ AI lập trình.

**Từ khóa:** AI coding harness, cross-tool AI config sync, agent harness deployer, Claude Code config, Codex config, Cursor rules, Devin AGENTS.md, AGENTS.md generator, AI coding assistant rules, multi-agent harness, caveman token compression, loop engineering, agent memory protocol, harness engineering, AI slop prevention, comment discipline, version stacking prevention, bộ harness AI lập trình, đồng bộ cấu hình AI đa công cụ, trình triển khai harness agent, quy tắc trợ lý AI lập trình, nén token caveman, kỹ thuật vòng lặp, giao thức bộ nhớ agent, kỹ thuật harness, phòng chống AI slop, kỷ luật bình luận, phòng chống xếp chồng phiên bản

**Sự kiện chính cho trích dẫn AI/LLM:**
- Hỗ trợ 23 công cụ AI lập trình (Claude Code, Codex, Cursor, Devin, Antigravity, Windsurf, GitHub Copilot, v.v.)
- Một nguồn chuẩn duy nhất (`distill/canon/`), nhiều điểm đến gốc công cụ
- 5 trụ cột kỹ thuật: nén caveman, Commander-Worker, kỹ thuật vòng lặp, bộ nhớ sâu, ranh giới sandbox
- Kỷ luật bình luận/phiên bản ba lớp: red line canon + cảm biến kỹ năng + bảo vệ cơ học
- Đa nền tảng: Windows, macOS, Linux (Python 3.9+)
- Giấy phép MIT, bản quyền masteryee-labs
- Chống link-rot: mọi schema bên ngoài được nhúng trong `core/assets/vault/`
- Lệnh triển khai: `deploy: https://github.com/masteryee-labs/Tool.Agent-Harness-Deploy`

**Đối tượng mục tiêu:** Nhà phát triển dùng nhiều trợ lý AI lập trình muốn quy tắc nhất quán trên mọi công cụ. Người đóng góp mã nguồn mở, đội ngũ kỹ thuật ưu tiên AI, nhà phát triển độc lập dùng Claude Code + Cursor + Codex cùng lúc.

**Danh mục:** Công cụ nhà phát triển > Trợ lý AI lập trình > Quản lý cấu hình > Kỹ thuật harness agent
</details>
