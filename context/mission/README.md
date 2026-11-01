# Mission và cách làm tự chủ — NNC BidOps Agent

Thiết lập 30/10/2026 theo chỉ dẫn của Dũng. Phương pháp vận hành kế thừa từ [nnc-claude-plugins](https://github.com/VOSYDUNG/nnc-claude-plugins) **main `94ddf8b`** (plugin `nnc` 5.1.0-alpha.2: `ai-oser` R2, `mission-formation`, `adaptive-delivery`) — đúng phần "NNC OSER" mà SOP P1/P2 trang 7 chỉ định dùng lại ("Formation làm rõ công việc, phương án và quyết định. Delivery chọn cách triển khai theo loại đầu ra"). Không dùng skill cục bộ NNC-AI-OSer v1 hay OSER v4 (xem mục Audit).

**Trạng thái:** plugin ghim tại `.claude/vendor/nnc-oser-94ddf8b/` (marketplace cục bộ `nnc-bidops-local`; chỉ kế thừa, không gửi ngược về repo). Formation [BIDOPS-F01](BIDOPS-F01.formation.json) ở REALITY_AUDIT, `formation-check` hợp lệ. Mission [nháp](BIDOPS-M01.contract.draft.json) **chưa duyệt; `oser init` chưa chạy.**

Chạy kernel trực tiếp: `python -I .claude/vendor/nnc-oser-94ddf8b/nnc/oser/oser.py <lệnh> --project .`. Lên bản phương pháp mới: thay thư mục vendor bằng commit mới, ghi commit vào tên thư mục.

## Hai nguồn phương pháp

| Nguồn | Trả lời | Ở đâu |
| --- | --- | --- |
| SOP P1/P2 của Dũng (v1 26/10/2026) | Sản phẩm **làm gì, đến đâu là đạt**: P1 yêu cầu → P2 xây/thử/bàn giao | `sources/method/SOP-P1-P2-VA-CA-KHO-2-v1.pdf` (không có trong repo plugin) |
| OSER R2 | Agent **vận hành thế nào**: Formation → Mission khóa authority + mẫu số nghiệm thu, Decision Contract, Clean Desk, checkpoint | plugin vendor; `.nnc-oser/` sau init |

## Lộ trình Formation (thay cho "đợt/lô")

| Giai đoạn | Việc của BidOps | Sản phẩm | Trạng thái |
| --- | --- | --- | --- |
| INTAKE | Bài toán bằng lời nghiệp vụ | `problem` trong F01 | Xong (nháp) |
| REALITY_AUDIT | As-is, người/vai, công cụ, ràng buộc, baseline | F01 `current_reality`; `context/HOP-VA-DUNG-CHUNG.md` | **Đang làm** — chờ người đang làm xác nhận as-is |
| RESEARCH | Chọn 2–3 ứng viên ca đầu; so 3 cách làm (quy trình/Excel · cấu hình/Skill · công cụ) có nguồn; fixture tổng hợp cho ca P2-VALIDATION | F01 `research`; `data-work/fixtures/`; `outputs/BIDOPS-P1-001/v0/` | Chưa |
| DECISION | Decision Card D07 đủ 9 mục, có lối "thử trước"; gói họp chốt D01/D02 | `requirements/DECISION-CARD-D07.md`; `outputs/BIDOPS-HOP/<yyyy-mm-dd>-chot-p1/` | Chưa |
| MISSION_READY | Hướng đã chọn, unresolved giải/hoãn rõ, Mission draft có authority + AC | F01 `mission_draft` | Chưa |
| Lock | Dũng duyệt → `oser init` | `.nnc-oser/` | Chưa (D09) |

Phần nào độc lập thì làm song song; nguồn lệch thì treo đúng phần đó và làm tiếp phần khác.

## Tự chủ (R2: không đội hình cố định)

Phiên chính tự chọn làm trực tiếp, giao subagent, hay song song nhiều subagent khi không đụng cùng file. Không có bảng model theo vai, không wave/packet bắt buộc.

**Chính sách của Dũng (30/10/2026):** phiên chính Opus giữ quyết định, viết brief, ghi STATE; việc song song giao subagent **Sonnet**. Subagent trả ≤40 dòng + đường dẫn; phiên chính không tự đọc file dài.

Subagent định nghĩa sẵn trong `.claude/agents/` (vì mang luật riêng của dự án): `nghien-cuu` (đối chiếu bằng chứng, chỉ đọc), `kiem-luat` (soi guardrail, chỉ đọc), `thu-ky-hop` (gói họp, không tự ghi quyết định). Việc soạn/kiểm khác: subagent chung, brief nêu file được ghi, thứ không được đụng, tiêu chí nhận; người kiểm khác người soạn.

## Mức quyết định (Decision Contract R2)

- **D0–D1** (phiên chính tự quyết): chia việc, giao ai, bố cục tài liệu/fixture, xử lý phát hiện của `kiem-luat`, treo phần nguồn lệch.
- **D2** (Decision Card): cách làm (D07 — chủ nghiệp vụ chọn).
- **D3** (chỉ người có quyền, không tự trả lời): danh mục/gói chào, tương đương kỹ thuật, giá, NCC, cam kết giao, master/quyền, người thử độc lập (D01–D06); gửi/upload/nộp thầu; push/remote GitHub (D08); duyệt/sửa Mission (D09).

**Gỡ kẹt:** subagent sai 2 lần → viết lại brief hoặc tự làm → vẫn kẹt: ghi mục chờ trong `PROJECT_STATE.md`, chuyển phần độc lập kế tiếp, gom câu hỏi báo một lần.

## Clean Desk

| Loại | File |
| --- | --- |
| CURRENT AUTHORITY | SOP P1/P2 gốc; `CLAUDE.md` / `AGENTS.md` (chỉ dẫn Dũng); luật graph `requirements/00-README-AUTHORITY.md`; node đã LOCKED trong `requirements/10-LOCK-REGISTER.md` (hiện chưa có) |
| CURRENT STATE | `context/PROJECT_STATE.md`; `requirements/DECISIONS.md`; `context/mission/BIDOPS-F01.formation.json` |
| WORKING DRAFT | node chưa khóa: `requirements/01-PRD-CORE.md`, `P1-REQUEST.md`, `08-SOURCE-MAP.md`, `11-ROLE-AUTHORITY-MAP.md`, `BACKLOG-ACCEPTANCE.md`, `P2-VALIDATION.md`; `discovery/`, `context/HOP-VA-DUNG-CHUNG.md`, contract nháp |
| EVIDENCE / ARTIFACT | `sources/` (chỉ đọc), `data-work/`, `outputs/` |
| HISTORY | `sources/history/v1..v3`, `discovery/research-snapshots/` |

Hệ tài liệu sản phẩm lock (authority graph, kế thừa mẫu Kho Bậc 1.5): file chủ từng node, điều kiện LOCKED, amendment và chính sách chống refactor ở [`requirements/00-README-AUTHORITY.md`](../../requirements/00-README-AUTHORITY.md). Formation/Mission dùng graph này: `research`/`decision` trong F01 trỏ ID node, không chép nội dung.

Phiên mới chỉ cần AUTHORITY + STATE. Chỉ phiên chính ghi STATE/DECISIONS. Draft không thành authority vì nằm gần authority.

## Đo chi phí

Chưa đo. Sau init dùng `oser usage`; thiếu nguồn ghi UNKNOWN, không quy ra % gói hay tiền.

## Audit nhiễu plugin cũ (30/10/2026)

Đã gỡ khỏi dự án: `cong-cu/doi-bac.py`, `.claude/BAC-DANG-DUNG.md`, `.claude/CO-CAU-NHAN-SU.md`, 4 subagent đội hình cố định, `context/GOAL-DOT-1.md` (mẫu GOAL/lô/sóng của NNC-AI-OSer v1), thuật ngữ quản đốc/R0–R3/ghế, ghim model theo vai, số quota "77%/56%/6,7×". Không bị nhiễm: `sources/` (chữ "packet" là gói discovery, "R02/R03/R10" là mã tham chiếu, "V4/R3" là ô Excel), `discovery/`, `requirements/P1-REQUEST.md`, `P2-VALIDATION.md`, `BACKLOG-ACCEPTANCE.md`.

## Khóa Mission (khi Dũng duyệt D09)

1. F01 đạt MISSION_READY.
2. Dũng duyệt goal + AC trong contract nháp; xoá `_status`, `_notes`.
3. `oser init --project . --contract <file>`; thêm một dòng trỏ `.nnc-oser/BOOTSTRAP.md` vào `CLAUDE.md`.
4. Checkpoint đầu: facts hiện có, next_action theo giai đoạn đang làm.
