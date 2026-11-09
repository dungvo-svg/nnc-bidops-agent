# 11 — NGƯỜI / VAI (`ACT-*`) VÀ QUYỀN (`CAP-*`) — DRAFT

Chủ duy nhất cho người-vai-quyền. Vai lấy theo nguồn (tổng hợp 30/10/2026 từ `SRC-WA`, `SRC-PLAN-R10`, `SRC-SOP-P1P2`); **chưa được ai xác nhận**. Không gán việc người khác cho Dũng. Mã tham chiếu: chron = whatsapp/chronology.json, C## = claims.json, KSW = key-source-wording.json, R10 = kế hoạch Cung ứng.

## ACT — người và phần việc có nguồn

| ACT | Người | Phần việc có nguồn |
| --- | --- | --- |
| `ACT-DUNG` | Dũng | CEO nhờ rà hàng chưa có giá Komsenahak và BV khác trước họp thứ Hai (30/10 09:15, C04); thẻ họp 29/10 "Oanh, Dũng hỗ trợ xử lý dữ liệu… báo cáo"; soạn danh mục chung 29/10; chốt người thử độc lập (SOP) |
| `ACT-OANH` | Oanh | Gửi bảng gốc chung, đề xuất form/bảng gốc (KSW 09:18); 28/10 gửi phân tích giá Mittaphap, được nhờ hướng dẫn Phet. Vai duyệt trong SOP chỉ ở ca Kho |
| `ACT-CEO` | CEO (HoangQuan, "Sếp") | Triệu tập họp, chỉ đạo, duyệt; theo R10: nạp app, kiểm thư mục |
| `ACT-PHET` | Phet | Nhận file thầu từng BV, làm bảng giá, chuẩn bị/in hồ sơ (C16); tổng hợp hạn nộp; xin nghỉ 26/11–1/12 (chưa thấy duyệt) |
| `ACT-SON` | Sơn | Tìm NCC/giá hàng Trung Quốc, tính giá vốn, báo mẫu/MOQ/vận chuyển |
| `ACT-TINH` | Mrs Tình | Phet nhờ xem giá 2027 (29/10 10:07); trao đổi mẫu/số lượng với Sơn. Quyền duyệt: chưa biết |
| `ACT-SIENG` | Siêng | Nguồn tin gói Komsenahak (29/10 09:55); trong danh sách họp 30/10. Vai chưa biết |
| `ACT-TRANG` | Trang | Gửi Stevimed 30/10; R10: gửi giá Tuấn Việt cho Hoa, Lacco chuyển Linh, T2 |
| `ACT-LINH` | Linh | Gửi giá Sharma; R10 F4 giá Lacco; T2 |
| `ACT-YAENG` | Yaeng | R10 F1 danh mục NCC + 3 mã chung |
| `ACT-HOA` | Hoa | R10 F2 danh mục hàng; F5 giá ALC/Tuấn Việt; T1 sửa mã MISA (thay Namfon) |
| `ACT-AN` | Phạm An | R10 F3 sửa bảng giá; gửi bảng giá mua gần nhất |
| `ACT-KHAC` | Lý, Đức, Khem, malita, PE/TA | Lý: R10 T2. Khác: vai chưa biết |

## Identity node nhóm Thuốc (đề xuất khóa `LCK-IDENTITY-THUOC`, 09/11/2026)

Gắn một người với một node, một hộp thư, một mã chia việc và một cột giá, để gom kết quả không nhầm người. **Chỉ là định danh, không cấp quyền quyết định** (CAP vẫn như bảng dưới). Nguồn: `SRC-KOM-AK-0511` (cột AK), `SRC-HOP-0411-0911`, `SRC-DRIVE-THUOC-0911`, chat Dũng (`SRC-CHAT-DUNG-0511`).

| node_id | Người | Mã AK trong bảng chia Kom | Hộp thư Drive | Cột giá file chung | Vai có bằng chứng | Còn thiếu để khóa |
| --- | --- | --- | --- | --- | --- | --- |
| `THUOC-DUNG` | Dũng (`dung.vo@nnclaogroup.com`) | — | `Inbox_thau/06_Dung` (có từ 07/11), `01_Trang/Dung_inbox` | — | Tổng hợp, chia file theo bảng nhóm, vá file chung, giữ lock; tự nêu "không phải người giao việc" | — (người dùng phiên) |
| `THUOC-TRANG` | Trang | `0` / `#N/A` (chưa ai nhận, 979 dòng) | `01_Trang` | Giá Trang | Hàng NCC Việt Nam, hỏi giá, tính giá vốn (họp 05/11); file "Final DOT-1…dien-gia-261109", 8 báo giá NCC trong `BAO-GIA_dot-1_Trang` | Trang xác nhận nhận phần 0/#N/A; email |
| `THUOC-TAR` | Tar | `T` (36 dòng) | `02_Tar` | Giá Tar | Nhóm Thuốc; "Tar check" trong file Trang; "chờ Tar xác nhận sau tra cứu" (báo cáo 09/11) | Vai cụ thể; email |
| `THUOC-SON` | Sơn | `S` (23 dòng) | `03_Son` | Giá Sơn | Nguồn Trung Quốc; tìm NCC ngoài Hà Nội (họp 09/11); ảnh thuốc bổ sung | Email |
| `THUOC-DUY` | Duy | `D` (64 dòng) | `04_Duy` | Giá Duy | Thuốc Kom (họp 05/11 "kéo Duy vào"); file "Thau 2027 Duy"; giá thuốc đang bán (họp 09/11) | Email; ranh giới quyền giá OTC và giá thầu |
| `THUOC-HUYEN` | Huyền ("Hiền" trong ASR là Huyền theo Dũng 09/11) | `H` (8 dòng) | `05_Huyen` | Giá Huyền | Điểm danh họp 09/11; "Theo dõi giá" trong `BAO-GIA_dot-1_Huyen` | Vai; không có trong danh sách 19 người; email |
| `THUOC-TINH` | Mrs Tình | — | — | — (dấu kiểm giá trong sheet Giá NNC KOM) | "Chị Tình kiểm giá, không thay người phụ trách xác nhận hàng" (báo cáo 09/11) | Quyền duyệt giá chưa biết |
| `THUOC-PHET` | Phét | — | — | Giá Phét | Nguồn đã nộp MTP; hàng hiếm hỏi Phét; giữ công thức giá Kom | Quyền chốt giá nộp |

Quy ước: ghi kết quả của người nào thì chỉ vào cột giá của người đó và các ô "Kết quả trao đổi", "Người / ngày" trên dòng có mã đó. Đổi người phụ trách là đổi trong bảng chia của nhóm (cột AK), không sửa ở đây.

## CAP — quyền quyết định (ai giữ: chưa chốt)

| CAP | Quyền | Quyết định liên quan | Người giữ |
| --- | --- | --- | --- |
| `CAP-PICK-CASE` | Chọn ca/gói/lô đầu và người dùng đầu ra | D01 | Chưa chốt |
| `CAP-MASTER-WRITE` | Ghi/cập nhật master, lan thay đổi | D02 | Chưa chốt |
| `CAP-PRICE-RULE` | Quy tắc giá/FX/thuế/vận chuyển | D03 | Chưa chốt |
| `CAP-EQUIV` | Nhận/từ chối sai khác quy cách/chứng từ | D04 | Chưa chốt |
| `CAP-COMMIT` | Cam kết quote/MOQ/lô-hạn/tuyến/capacity/tiền | D05 | Chưa chốt |
| `CAP-PORTFOLIO` | Chọn danh mục chào từng gói | D01, D05 | Chưa chốt |
| `CAP-TESTER` | Chỉ định người thử P1/P2 độc lập | D06 | Dũng (theo SOP) |
| `CAP-METHOD` | Chọn cách làm (Excel/cấu hình/Skill/công cụ) | D07 | Chủ nghiệp vụ (chưa xác định người) |
| `CAP-REPO` | Nơi lưu/push repo | D08 | Dũng + Sếp Quân |
| `CAP-MISSION` | Duyệt Mission, `oser init`, ghi khóa `LCK-*` | D09, D10 | Dũng |

Agent không giữ CAP nào; chỉ đề xuất kèm bằng chứng.
