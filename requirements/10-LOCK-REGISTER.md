# 10 — LOCK REGISTER (WHO / WHY / SOURCE / REOPEN)

Sổ duy nhất cho `LCK-*`. Không lặp nội dung quyết định (ở `DECISIONS.md`), người-quyền (ở `11`) hay nguồn (ở `08`).

## Lược đồ khóa

Mỗi `LCK-*` phải đủ 8 trường: `Covers D*` · `Requirement owner` · `Approved by` · `SRC-*` · `Evidence type` · `Lock reason` · `Effective from` · `Reopen if`. Thiếu một trường → quyết định liên quan **không** được gọi LOCKED.

Evidence type: `DIRECT_REQUIREMENT · DATA_MEASURED · PRODUCT_DECISION · SOURCE_CONFIRMED · IMPLEMENTATION_EVIDENCE`.

Khóa quyết định không tự duyệt P1, không tự mở P2, không tự phát hành. Agent chỉ đề xuất dòng `PROPOSED`; người ở cột Approved by mới đổi sang `LOCKED` (ghi ngày + bằng chứng duyệt).

## Khóa hiện hành

Chưa có.

## Đề xuất chờ duyệt

| Lock ID | Covers | Requirement owner | Approved by | Sources | Type | Lock reason | Effective | Reopen if | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `LCK-METHOD` | D10 | Dũng | Dũng (chờ xác nhận ghi khóa) | `SRC-SOP-P1P2`, `SRC-CHAT-DUNG-3010` | DIRECT_REQUIREMENT | SOP ghi "Phạm vi P1/P2 đã được Dũng chốt"; chỉ dẫn 30/10 áp OSER R2 main `94ddf8b` + graph này | (điền khi Dũng xác nhận) | SOP có version mới; Dũng đổi chỉ dẫn; plugin lên commit khác | PROPOSED |
| `LCK-MATCH-KEY` | D11 | Phet + chủ master | (trống — chờ D02) | `SRC-WB-BGC`, `SRC-WB-KOM`, `SRC-STEVIMED` | DATA_MEASURED | MPSC duy nhất 2.126/2.126; STT KOM/Stevimed lặp/lệch → ghép nhầm | (trống) | Master đổi; có bảng nối mới | PROPOSED — thiếu Approved by, Effective |
| `LCK-VALUE-SEMANTICS` | D12 | Người sở hữu quy tắc giá | (trống) | `SRC-PLAN-R10`, `SRC-WA-0913`, `SRC-WB-BGC` | DATA_MEASURED + DIRECT_REQUIREMENT | Trống/0/chưa xác nhận đang bị lẫn; CNJ bị hiểu là KIP; giá 2027 thực là giá chào 2026 | (trống) | Quy tắc giá được duyệt khác | PROPOSED — thiếu Requirement owner cụ thể, Approved by, Effective |
| `LCK-STATUS` | D13 | Chủ nghiệp vụ | (trống) | `SRC-PLAN-R10`, `SRC-SOP-P1P2` | PRODUCT_DECISION | "đã giao/nhận/kiểm/nạp/được phép chào" là các trạng thái khác nhau | (trống) | Quy trình duyệt đổi | PROPOSED — thiếu Approved by, Effective |

`D01`–`D09`: chưa đủ điều kiện đề xuất khóa (thiếu người duyệt/bằng chứng). D02 và D01 cần chọn trong họp trước khi đề xuất `LCK-MASTER`, `LCK-CASE-1`.
