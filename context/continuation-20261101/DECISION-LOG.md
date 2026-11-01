# Nhật ký quyết định: chỉ dẫn người dùng, khóa nghiệp vụ, đề xuất của model

> Bản audit/plan đã được Codex đối chiếu độc lập và lưu vào project ngày 01/11/2026. Claude Opus tổng hợp, Sonnet kiểm hai nhánh. Các nhãn draft/đề xuất trong nội dung là trạng thái quyết định, không có nghĩa file còn ở ngoài project. Chưa thay runtime, tích hợp code, merge hay deploy. Chi tiết nguồn/giới hạn: SOURCES-READ.json và PUBLICATION-RECEIPT.json.


## Chỉ dẫn hiện hành của Dũng (phạm vi công việc, không phải khóa nghiệp vụ)

Các chỉ dẫn dưới đây được chuyển tới qua task/parent. Hiệu lực của chúng dựa trên chỉ dẫn trực tiếp của Dũng. Bản gốc nguyên văn của U-30A nằm trong `requirements/DECISIONS.md`, mục "Bằng chứng D10". Các mục khác chưa có bản gốc lưu trong owner project.

| Mã | Nội dung | Nguồn |
| --- | --- | --- |
| U-30A | Áp dụng OSER R2 main `94ddf8b`, SOP P1/P2 và authority graph; Opus quyết, Sonnet làm song song | Chat 30/10 |
| U-31A | BidOps là node CEO đa nhánh, thầu BV là mũi nhọn; CEO trực tiếp chào hàng; nhân viên sở hữu máy và Agent | Chỉ dẫn 31/10; task 01/11 |
| U-31B | Được làm B synthetic local trong workspace cách ly (AUTH-20261031-LOCAL-B) | Manifest B |
| U-31C | Thử tạo repo private trong `nnc-lao`; không được thì giữ local, không fallback | Manifest B. Kết quả xem BRIEF, mục repo |
| U-31D | Đưa Kom vào phạm vi; SQLite là nguồn chuẩn của pilot, Excel chỉ là bản xuất; thêm demand lifecycle | Manifest B, cập nhật 11:53 UTC |
| U-01A | Báo riêng phần BidOps và lưu bền trong project | Sentinel `ecaae41e…`, task 01/11 |

## Khóa nghiệp vụ trong owner (`requirements/10-LOCK-REGISTER.md`): không có node nào LOCKED

| Mã | Trạng thái thực | Đề xuất của model (chờ người có quyền) |
| --- | --- | --- |
| D01, D02 | Chưa chốt | Chọn trong họp |
| D10 / `LCK-METHOD` | PROPOSED: còn thiếu xác nhận của Dũng và ngày hiệu lực (Effective from) | — |
| D11 / `LCK-MATCH-KEY` (theo MPSC) | PROPOSED | **Đề xuất rút hoặc thay, chờ chủ D11/D02 duyệt.** Phản ví dụ: MPSC02MD00102 tách thành 40mm và 30mm/EP3 (A8 §6 vòng 2) |
| D12, D13 | PROPOSED | Giữ nguyên. Pilot có test L1 cho hành vi (unknown ≠ 0; tách trạng thái), chưa có người duyệt |
| "D14", "D15" | **Chưa có trong `DECISIONS.md`**, chỉ là mã đề xuất | D14: pilot B cách ly là nơi chạy code. D15: khóa ghép theo dòng nguồn + biến thể có version. Xem `C:\Users\Admin\Documents\Codex\2026-10-31\task\output\bidops-relock-20261101\OWNER-PROJECT-DOC-PATCH.md` |
| D08 | Chưa chốt | Chỉ ghi lại hai loại bằng chứng repo trong BRIEF; không sửa D08 |

## Hiểu sai trước đây đã được nguồn mới thay thế

| Hiểu sai trước đây | Đúng theo nguồn | Nguồn |
| --- | --- | --- |
| Đội hình ghế, GOAL-DOT, toggle model của NNC-AI-OSer v1 | Đã gỡ | Audit 30/10 |
| "Danh mục chung không có Mittaphab" | Có cột Mittaphab; 223/269/653 dòng | `RESEARCH-A-LOCAL-31-10.md` §2.1 |
| 2.736 với 2.126 là chênh lệch hoặc mất hàng | Hai số khác grain | A8 §1 |
| "Kom là gói lịch sử" | Gói hiện hành 2027; chỉ phần giá là của năm trước | A8 §1; báo cáo Kom 31/10 |
| Năm phạm vi phê duyệt là năm phép kiểm nghiệp vụ | Hai trục khác nhau | A8 §2; pilot BRIEF 31/10 |

## Bằng chứng nguồn mới (01/11, vòng 2) — không phải quyết định

- **Không có phê duyệt hay nộp thầu trong chat.** Đã đọc đủ 168 tin trong chat 28–30/10: không có tin nào phê duyệt giá, NCC hay danh mục, cũng không có tin nộp thầu.
- **Sếp 30/10 09:22 chỉ là chỉ đạo** (`3EB0443DA0D4D9D22B7574`): "trình bày cách làm cho gói mới, tháng 11 chia nguồn lực". Tin này không phê duyệt kiến trúc, giá hay NCC.
- **Phân vai Mittaphab có thêm bằng chứng.** Sếp 30/10 08:16 (`3EB0CBFE7CE3AF62C6B261`) giao rà báo giá BV150 cho Phét. Điều này khớp với BV150 = Mittaphab và Phét làm owner, củng cố quyết định không tiếp quản gói này.
- **Có lịch sử trúng thầu 2026** trong BGC (189 dòng, 149 MPSC). Đây là bằng chứng lịch sử cho căn cứ cạnh tranh. Bản scan gốc chưa đọc lại, nên không coi là quote hiện hành.
- **Đề xuất rút/thay D11 có thêm lý do.** Các sheet BV trong workbook BGC tra theo MPSC (`MATCH` cột B), nên cùng một mã nhưng khác quy cách sẽ bị gộp. D11 vẫn PROPOSED, chờ chủ D11/D02.
- **Hạn Kom 13/11 chỉ có một nguồn.** Mốc kế hoạch 13/11 dựa duy nhất trên tin Phét. Ô `I8` trong Kom là ngày trên mẫu thư, không phải căn cứ hạn nộp.
- **Không đặt policy mới.** Không có quy định chung "CEO không làm việc staff" hay "apply/use phải khác người". CEO vẫn trực tiếp chào hàng; ranh giới chỉ là không điều khiển Agent hay máy của người khác. Tách người theo phạm vi phải dựa trên thẩm quyền thật.

## Câu hỏi mở

| Câu hỏi | Người nên hỏi |
| --- | --- |
| Ai duyệt giá, ai nộp | CEO, chủ nghiệp vụ |
| Chủ master (D02) | CEO, Oanh, Phét |
| Ca đầu tiên (D01) | — |
| Người thử độc lập (D06) | Dũng |
| Hạn chính thức từng gói | HSMT; đề nghị hỏi Phét, chờ CEO xác nhận người phụ trách |
| App Cung ứng giao với BidOps ở đâu | CEO |
