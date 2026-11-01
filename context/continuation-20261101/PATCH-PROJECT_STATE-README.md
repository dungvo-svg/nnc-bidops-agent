# Ghi nhận việc áp patch PROJECT_STATE và README (đối chiếu ngày 01/11/2026)

> Bản audit/plan đã được Codex đối chiếu độc lập và lưu vào project ngày 01/11/2026. Claude Opus tổng hợp, Sonnet kiểm hai nhánh. Chưa thay runtime, chưa tích hợp code, chưa merge hay deploy. Chi tiết: SOURCES-READ.json và PUBLICATION-RECEIPT.json.

Tài liệu này ghi lại **những gì Codex đã thật sự áp** vào project owner, theo `PUBLICATION-RECEIPT.json` (03:27:32 UTC). Claude đối chiếu bằng Read/Grep thực tế lúc 01/11, sau lần publish. Phần nào **chưa áp** được ghi riêng và chỉ còn là đề xuất. Việc áp vào context theo đúng phạm vi Dũng giao cho audit, không cần thêm duyệt nghiệp vụ. Không có khóa D/LCK nào thay đổi.

## Đã áp

| File owner | Nội dung đã có (Claude đã đọc lại) |
| --- | --- |
| `context/PROJECT_STATE.md`, dòng 3–13 | Thêm mục mới "Continuity đã đối chiếu — 01/11/2026", gồm: pointer tới BRIEF → SOURCE-MAP → DECISION-LOG → PLAN-VS-IMPLEMENTATION → ROADMAP-STATUS; mô tả node CEO đa nhánh và vai Opus/Sonnet/Codex; code B cách ly ở `aac3e9428084…` với 100/100 test (receipt Codex) và smoke 1/1; trạng thái chưa tích hợp, chưa L4/L5; D11 vẫn PROPOSED; hai loại bằng chứng của D08; câu đánh dấu "các đoạn 30/10 phía dưới là snapshot lịch sử" |
| `README.md`, dòng 11 | Thêm pointer "Continuity BidOps 01/11" trỏ `context/continuation-20261101/BRIEF.md` |

Cách Codex áp khác đề xuất cũ ở một điểm: **không thay** câu "P2 chưa xây" ở dòng 26 mà chú thích lại ở dòng 13. Cách này giữ được lịch sử và vẫn đúng ý nghĩa.

## Chưa áp (vẫn là đề xuất, chưa phải lỗi)

- **Dòng 37 và dòng 40 vẫn giữ văn bản 30/10.** Dòng 37 ghi "Dũng chưa là thành viên org nào…". Dòng 40 ghi "Chờ Dũng: … tên org + lời mời (D08)". Chú thích ở dòng 13 đã đánh dấu chúng là lịch sử. Nếu muốn sửa trực tiếp dòng 40, đề xuất câu:
  > "Chờ Dũng: D02 → D01 → ai duyệt/nộp; xác nhận `LCK-METHOD`; đề xuất rút/thay D11 chờ chủ D11/D02; D08 chưa chốt (xem mục Continuity); Mission D09."
- **`discovery/DINH-HINH-SAN-PHAM.md` chưa áp bốn đính chính**: Mittaphab có trong danh mục; 2.736 và 2.126 khác grain; BV150 là Mittaphab; Kom là gói hiện hành. Chi tiết trong `C:\Users\Admin\Documents\Codex\2026-10-31\task\output\bidops-relock-20261101\OWNER-PROJECT-DOC-PATCH.md`.
- **Chưa đổi gì trong `requirements/DECISIONS.md` và `10-LOCK-REGISTER.md`.** Đây là chủ ý: các đề xuất D14/D15 và việc rút D11 phải chờ người có quyền.
