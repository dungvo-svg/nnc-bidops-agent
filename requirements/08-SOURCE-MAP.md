# 08 — SOURCE MAP (`SRC-*`)

Nguồn ở đâu và **chứng minh được tới đâu**. Danh mục tệp/hash chi tiết: `sources/inventory.json`, `sources/README.md` (không chép lại ở đây). Nguồn là bằng chứng để đọc, không tự cấp quyền.

| SRC | Ở đâu | Chứng minh được | Không chứng minh |
| --- | --- | --- | --- |
| `SRC-SOP-P1P2` | `sources/method/SOP-P1-P2-VA-CA-KHO-2-v1.pdf` (PDF chuẩn; bản trích `.txt`) | Phương pháp P1/P2 v1 26/10/2026, phạm vi do Dũng chốt; OSER R2 là phương pháp dùng lại | Người thử, baseline, kết quả thử thật |
| `SRC-CHAT-DUNG-3010` | Phiên Claude 30/10/2026 — nguyên văn ở `DECISIONS.md` mục "Bằng chứng D10" | Chỉ dẫn Dũng: áp OSER R2 main, Opus quyết/Sonnet song song, cài plugin chỉ để kế thừa, không push, dùng hệ tài liệu lock | Quyết định nghiệp vụ thầu |
| `SRC-WA-0918` | `sources/whatsapp/key-source-wording.json` (Oanh 30/10 09:18) | Đề nghị form/bảng gốc nhập một lần, lan sang BV | Đã được duyệt làm master |
| `SRC-WA-0922` | như trên (CEO 30/10 09:22) | Muốn trình bày cách làm cho gói mới, chia nguồn lực tháng 11 | Lịch/người trình bày cụ thể |
| `SRC-WA-0913` | như trên (Phet 30/10 09:13) | Sheet nhãn 2027 là giá đã chào năm 2026 | Quote hiện hành |
| `SRC-WA` | `sources/whatsapp/chronology.json`, `claims.json`, `historical-context.json` | 168 tin trong kỳ 29–30/10, 37 tin bối cảnh, 32 nhận định có nguồn | Tin sau 30/10 10:41; toàn lịch sử nhóm |
| `SRC-WB-BGC` | workbook bảng gốc HC (Oanh); phân tích `sources/analysis/workbooks/REPORT-WORKBOOKS.md` | 2.126 mã, 3.269 dòng, 5 BV; tham số lệch Settha/Meladek | Đồng bộ đa người; giá mới đã điền |
| `SRC-WB-KOM` | workbook Komsenahak (Phet); cùng báo cáo | Cấu trúc khác BGC; Com/Amp, 600 ml/500 ml lệch | Cầu nối với BGC |
| `SRC-STEVIMED` | phản hồi Stevimed (Trang 30/10); `discovery/research-snapshots/FOLLOWUP-V2.txt` | Có mã/ghi chú sai khác, không có trường giá; STT lệch giữa sheet | Giá chào |
| `SRC-IMG` | `sources/whatsapp/originals/`; `sources/analysis/images-pdf/` | Ảnh cột giá (Giá vốn ở M/J/K-GV tùy mẫu), packing list, gòn tẩm cồn | Công thức chung; lô đang chào |
| `SRC-PLAN-R10` | `sources/plans/plan-source-text.txt` (sửa 30/10 03:29:07 UTC) | Người/mốc dự kiến trong kế hoạch Cung ứng | Việc đã nộp/nạp thực tế |
| `SRC-THAU-BV-NNC` | `D:\WORK\Agent\Agent-first\personal-meeting-assistant\.local\projects\thau-bv-nnc\work` (ngoài workspace; đọc docstring/đầu file 30/10) | Pipeline thầu của Dũng: ghép trạng thái A–D, danh mục chung, `SCHEMA.md` không đoán loại giá; chứa `build_tender_sets.py` (KHÔNG chạy) | Logic đã kiểm; dữ liệu hiện hành |
| `SRC-CUNGUNG-TOOLS` | `D:\WORK\cung-ung-ban-do\tools` (`doc_bang_gia_misa.py`, `so_ip_voi_so.py`) | Có công cụ kiểm bảng giá mua (tiền lệch, giá cũ, thiếu NCC) | Đã chạy trên dữ liệu hiện hành |
| `SRC-KHO15-GRAPH` | `D:\WORK\nnc-kho-1-5\reference\piops\docs\du-an\kho-bac-1-5\` (ngoài workspace) | Mẫu authority graph/lock register được kế thừa | Nội dung nghiệp vụ BidOps |

`discovery/research-snapshots/` và `sources/` bị gitignore: chỉ có ở máy gốc, bản clone sẽ không có.

Khi hai `SRC` lệch: treo phần bị ảnh hưởng, ghi vào `PROJECT_STATE.md`, không ghi đè.
