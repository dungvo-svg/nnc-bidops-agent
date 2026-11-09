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
| `LCK-LAYERS` | D15 | Dũng | Dũng (xác nhận trực tiếp 02/11/2026) | `SRC-CHAT-DUNG-0211` (xác nhận ghi hồ sơ), `SRC-RELAY-DUNG-0211`, `SRC-OSER-VENDOR`, `SRC-LITE-V7` | DIRECT_REQUIREMENT | Lớp điều hành BidOps/CEO và lớp node có phương pháp làm việc của agent/tài liệu/bản thể riêng; cùng phương pháp ≠ cùng owner; node đủ thiết lập làm thật ngay, blocker theo node | 02/11/2026 (hồ sơ) | Dũng đổi chỉ đạo | **CONFIRMED_USER_DIRECTION** — Dũng xác nhận trực tiếp 02/11/2026 trong phiên cha (`SRC-CHAT-DUNG-0211`). Ghi hồ sơ, **không phải runtime lock**: không cấp thêm quyền runtime, không `oser init`. Giờ gốc của phần chuyển lại vẫn là metadata gap |
| `LCK-EXECUTION` | D14 | Dũng | Dũng (xác nhận trực tiếp 02/11/2026) | `SRC-CHAT-DUNG-0211`, `SRC-RELAY-DUNG-0211`, `SRC-LITE-V7` | DIRECT_REQUIREMENT | Chỉ đạo 02/11: Dũng/Shin giữ mục tiêu; Claude cha tự điều phối; DATA + A trước song song; HỌP sau, đóng băng; làm trong session | 02/11/2026 (hồ sơ) | Dũng đổi chỉ đạo; gate DATA/A đạt và mở HỌP; xung đột với khóa nghiệp vụ | **CONFIRMED_USER_DIRECTION** — Dũng xác nhận trực tiếp 02/11/2026 trong phiên cha (`SRC-CHAT-DUNG-0211`). Ghi hồ sơ, **không phải runtime lock**: không cấp thêm quyền runtime, không `oser init`. Giờ gốc của phần chuyển lại vẫn là metadata gap |
| `LCK-WORKSPACE` | D16 | Dũng | Dũng (chat 05/11) | `SRC-CHAT-DUNG-0511`, `SRC-DRIVE-THUOC-0911` | DIRECT_REQUIREMENT | Một file chung + hộp thư theo người; chia theo bảng nhóm; file chuẩn quyết định bố cục; vá đúng ô | 05/11/2026 (hồ sơ) | Dũng đổi chỉ đạo; nhóm đổi bảng chia; refactor file gọn lớn | **CONFIRMED_USER_DIRECTION** — ghi hồ sơ cách làm, không phải khóa nghiệp vụ |
| `LCK-SNAPSHOT-POLICY` | D17 | Dũng | Dũng (chat 05/11) | `SRC-CHAT-DUNG-0511`, `SRC-THUOC-LOCK-0511` | DIRECT_REQUIREMENT | Bản chụp dữ liệu local chỉ đọc + hash + bản đồ vị trí; khóa ghép là mã; không sửa bộ cũ | 05/11/2026 | Dũng đổi chỉ đạo | **CONFIRMED_USER_DIRECTION** |
| `LCK-IDENTITY-THUOC` | `11` § Identity node Thuốc | Dũng | (trống — từng người tự xác nhận dòng mình) | `SRC-KOM-AK-0511`, `SRC-HOP-0411-0911`, `SRC-DRIVE-THUOC-0911` | SOURCE_CONFIRMED | Gom kết quả theo node: người ↔ mã AK ↔ hộp thư ↔ cột giá; tránh ghi nhầm người | (trống) | Nhóm đổi bảng chia; thêm người | PROPOSED — thiếu xác nhận của từng người và email; không cấp quyền |
| `LCK-MATCH-KEY` | D11 | Phet + chủ master | (trống — chờ D02) | `SRC-WB-BGC`, `SRC-WB-KOM`, `SRC-STEVIMED` | DATA_MEASURED | MPSC duy nhất 2.126/2.126; STT KOM/Stevimed lặp/lệch → ghép nhầm | (trống) | Master đổi; có bảng nối mới | PROPOSED — thiếu Approved by, Effective |
| `LCK-VALUE-SEMANTICS` | D12, D18 | Người sở hữu quy tắc giá | (trống) | `SRC-PLAN-R10`, `SRC-WA-0913`, `SRC-WB-BGC`, `SRC-KOM-AK-0511` (công thức GV), `SRC-HOP-0411-0911` (05/11) | DATA_MEASURED + DIRECT_REQUIREMENT | Trống/0/chưa xác nhận đang bị lẫn; CNJ bị hiểu là KIP; giá 2027 thực là giá chào 2026 | (trống) | Quy tắc giá được duyệt khác | PROPOSED — thiếu Requirement owner cụ thể, Approved by, Effective |
| `LCK-STATUS` | D13 | Chủ nghiệp vụ | (trống) | `SRC-PLAN-R10`, `SRC-SOP-P1P2` | PRODUCT_DECISION | "đã giao/nhận/kiểm/nạp/được phép chào" là các trạng thái khác nhau | (trống) | Quy trình duyệt đổi | PROPOSED — thiếu Approved by, Effective |

## Bản chụp dữ liệu (không phải `LCK-*`)

Khóa dữ liệu theo chỉ đạo Dũng; **không** khóa quyết định nghiệp vụ, không nâng D* nào thành LOCKED.

| Snapshot | Chỉ đạo | Nguồn | Phạm vi | Mở lại khi |
| --- | --- | --- | --- | --- |
| `LOCK-20261105` | Dũng (chat 05/11): "LOCK dữ liệu chốt hôm nay… đặt bộ lock ở local" | `SRC-THUOC-LOCK-0511`, `SRC-KOM-AK-0511` | File chung Thuốc 6 đơn vị (1.721 dòng) + 5 file chia đợt 1 Komsenahak (1.110 dòng) + bản đồ vị trí; quy tắc tiền tệ trong `LOCK.md` §3 | Kom đủ nguồn + giá → refactor file gọn lớn và tạo `LOCK-YYYYMMDD` mới; không sửa bộ cũ |

`D01`–`D09`: chưa đủ điều kiện đề xuất khóa (thiếu người duyệt/bằng chứng). D02 và D01 cần chọn trong họp trước khi đề xuất `LCK-MASTER`, `LCK-CASE-1`.
