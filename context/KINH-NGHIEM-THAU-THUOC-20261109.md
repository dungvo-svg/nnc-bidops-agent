# Case BidOps Thuốc: kinh nghiệm chưng cất (30/10 → 09/11/2026), bản tách Human / Agent

Theo khuôn "case lessons" của OSER R2: bài học có bằng chứng, dùng làm tham khảo. Đây **không phải quyết định**: quyết định ở `requirements/DECISIONS.md`, khóa ở `10-LOCK-REGISTER.md`, người/vai ở `11-ROLE-AUTHORITY-MAP.md`. Hồ sơ Agent và quy trình được đúc kết từ đây: [`agent-goi-thau/HO-SO-AGENT-GOI-THAU.md`](agent-goi-thau/HO-SO-AGENT-GOI-THAU.md), [`agent-goi-thau/QUY-TRINH-GOI-THAU.md`](agent-goi-thau/QUY-TRINH-GOI-THAU.md).

**Mục tiêu (Dũng 09/11):** Agent tự chủ chạy một gói thầu. Bài học được tách theo người dùng nó: **[H]** cho người, **[A]** cho Agent.

**Cách đọc nhãn:**
- **QUY TẮC** = phải giữ ở mọi gói, vì vi phạm sẽ hỏng dữ liệu hoặc vượt quyền.
- **CÁCH THỨC** = cách đã làm theo chủ đích của người điều phối trong ca này. Dùng làm mặc định, nhưng đổi được theo nhóm và gói, **không phải 100% như vậy**.

Nguồn:
- Chat Dũng 04–09/11 (phiên cha `a5ab430d`).
- Biên họp `outputs/hop/v3/` (04, 05, 09/11; chữ ASR, chưa duyệt).
- Drive `Thau BV/THUOC-agent-teams-20261104`, đọc 09/11 18:40.
- Bộ `LOCK-20261105`.

## 1. Sự cố phối hợp lớn nhất: dữ liệu tràn lan, không có một bản thể

Bằng chứng trên Drive ngày 09/11:

| Hiện tượng | Bằng chứng |
|---|---|
| **Một dữ liệu (giá Kom) nằm ở ≥ 7 nơi**, không nơi nào được tuyên bố là bản chuẩn | `THUOC-NGUON-HANG-6-DON-VI-v2.xlsx` (có người sửa 09/11 10:46); `…v3-TACH-2026-2027-20261108` (gsheet, và một bản xlsx trong `_archive`); `KOM-2027_Gia-hoi-tu` (cả xlsx lẫn gsheet); "KOM 2027 — Giá NNC KOM — Làm việc chung" (gsheet); `KOM_2027_HOI_TU_TINH_CHECK_DANG_LAM_V5_DL02.xlsx`; file "Final DOT-1…" của chị Trang (xlsx + gsheet); `Thau 2027 Duy.xlsx` (17 MB) |
| **Nguồn thô bị nhân bản, khác phiên bản** | File Kom 2027 có 2 bản khác cỡ (85 MB ở `00-Yeucaubandau`, 99 MB ở `Goi 2027`); danh sách trúng Kom 2026 có 2 bản (một bản "(1)") |
| **Chuyển xlsx ↔ Google Sheets sinh thêm bản** | Cùng tên vừa `.xlsx` vừa `.gsheet` ("Final DOT-1…", "Gia-hoi-tu", "v3-TACH") |
| **Runtime lẫn vào file hợp nhất** | File của chị Trang có thêm sheet "Tar Bổ sung" và "Komsenahak - không có thông tin": việc của người khác, kết quả tra cứu và dữ liệu gốc nằm chung một file làm việc |
| **Số liệu chia việc trôi giữa các bản** | Bảng chia lúc tách file ngày 05/11: Trang 979, Tar 36, Duy 64. Báo cáo nhóm 09/11: Trang 981, Tar 39, Duy 65. Cột AK là công thức tra từ một sheet khác, nên đổi theo bản |
| **Người không biết làm trên file nào** | Họp 09/11: "hiện có thêm 3 file Excel mới, mình làm tiếp trên file nào?"; "file sáng nay mới thấy" |
| **Một bản lock có, nhưng không ai cập nhật lên nó** | `LOCK-20261105` chỉ ở máy Dũng; từ 06/11 nhóm làm trên các bản khác, không bản nào được nâng thành lock mới |

**Nguyên nhân gốc (QUY TẮC rút ra):**
1. Không tuyên bố **một bản thể** (canonical) cho mỗi gói, kèm **một đầu ghi**.
2. **Runtime** (file làm việc của từng người, file tra cứu, file nháp) không tách khỏi bản thể, và không có bước **nhận về** (intake) có kiểm.
3. **Không chọn trước định dạng** (file Excel hay Google Sheet, một file nhiều sheet hay nhiều file), nên mỗi người chọn một kiểu.
4. **Nguồn thô không được chụp một lần rồi khóa**, nên mỗi người kéo một bản.

Cách sửa nằm trong quy trình: 5 lớp dữ liệu, một bản thể mỗi gói, Agent là đầu ghi duy nhất của bản thể, runtime chỉ vào qua intake.

## 2. Bài học cho NGƯỜI [H]

| # | Bài học | Loại |
|---|---|---|
| H1 | Chỉ ghi vào **file runtime của mình** (hộp thư cá nhân); không sửa bản thể, không tạo bản sao của bản thể | QUY TẮC |
| H2 | Mỗi giá ghi kèm **tiền tệ, ĐVT nhỏ nhất, NCC, ngày báo giá** và lưu **báo giá gốc** | QUY TẮC |
| H3 | Quyết định giá chào, NCC, tương đương, Visa, quyền xem giá vốn là việc của **người có thẩm quyền**, không giao cho AI | QUY TẮC |
| H4 | Lời nói trong họp chưa phải quyết định; muốn chốt thì người có thẩm quyền xác nhận bằng chữ (chat, comment, ô duyệt) | QUY TẮC |
| H5 | Không tải xlsx về sửa rồi tải lên lại; không đổi định dạng file của người khác | QUY TẮC |
| H6 | Cập nhật **trạng thái** (Chưa bắt đầu / Đang làm / Đã xong) để Agent biết khi nào nhận về | QUY TẮC |
| H7 | Chia việc theo **bảng chia của nhóm** (người phụ trách từng mã), không theo người điều phối | CÁCH THỨC (Dũng: "tôi không phải người giao việc") |
| H8 | Chia nguồn theo sở trường: NCC Việt Nam → Trang; Trung Quốc, ngoài Hà Nội → Sơn; hàng hiếm, nguồn đã nộp → Phét; kiểm giá → Tình; Kom thuốc → Duy; xác nhận thành phần → Tar | CÁCH THỨC (theo ca này) |
| H9 | Lọc bằng **chế độ xem bộ lọc** riêng | CÁCH THỨC |
| H10 | Báo cáo đúng loại đếm: "có nội dung tra cứu" ≠ "đã xác nhận hoạt chất"; "có ảnh nhận diện" ≠ "đủ ảnh nộp"; "trùng việc tìm" ≠ "đã xong" | QUY TẮC |
| H11 | Hỏi giá theo **hoạt chất + hàm lượng + dạng**, không theo tên thương mại; tên chưa rõ thì xin nhãn hoặc hãng | QUY TẮC |
| H12 | Giá năm trước, giá đã nộp và giá AI tìm chỉ là **đầu mối**, không phải giá hiện hành | QUY TẮC |

## 3. Bài học cho AGENT [A]

| # | Bài học | Loại |
|---|---|---|
| A1 | **Một gói, một bản thể, một đầu ghi (Agent).** Người không sửa bản thể; mọi thay đổi vào qua intake | QUY TẮC |
| A2 | **Nguồn thô chụp một lần, có hash, chỉ đọc.** Thấy hai bản khác nhau của cùng nguồn thì treo, không tự chọn | QUY TẮC |
| A3 | **Khóa ghép là mã** (KOM-…, MPSC, TH-…), không bao giờ là số dòng hay STT | QUY TẮC |
| A4 | **Runtime tách khỏi bản thể**: file theo người, file tra cứu, file nháp là runtime; Agent chỉ nhận về những ô được phép, có kiểm | QUY TẮC |
| A5 | **Mỗi lần nhận về là một lần nâng phiên bản bản thể** (lock mới, có hash, có danh sách ô đổi). Không sửa lock cũ | QUY TẮC |
| A6 | Trước khi ghi lên Drive: **chép về, so với lần trước, vá đúng ô, kiểm không đổi trong lúc vá rồi mới ghi**; không chép đè cả file | QUY TẮC |
| A7 | **Đơn vị tiền lấy theo công thức trong chính file nguồn**, không đoán theo độ lớn số (đã từng gắn nhầm giá mua VND thành kíp) | QUY TẮC |
| A8 | **Không sửa chữ nguyên văn** (tên thầu, spec, tên Kom); hoạt chất và tên chuẩn để ở cột riêng | QUY TẮC |
| A9 | **Trống ≠ 0 ≠ chưa xác nhận** (ô "0" trong file Kom từng làm 142 dòng bị xếp nhầm) | QUY TẮC |
| A10 | Phần AI suy ra phải **tô màu và ghi nhãn**; không bao giờ đưa vào ô "đã xác nhận" | QUY TẮC |
| A11 | **Ghép hàng chỉ khi cùng hoạt chất + hàm lượng + dạng + họ ĐVT**; còn lại để người chọn | QUY TẮC |
| A12 | Tự làm D0–D2 (bố cục, chuẩn hóa, đối chiếu, tách file, báo cáo); **D3 (giá chào, NCC, tương đương, quyền, nộp, gửi ra ngoài) dừng và hỏi** | QUY TẮC |
| A13 | Phiên mới **đọc Drive thật trước** (nhóm làm nhiều giữa các phiên); không tin trạng thái nhớ được | QUY TẮC |
| A14 | File chia **tách từ bản thể, cùng bố cục**; file nguồn khác chỉ dùng để chọn dòng | CÁCH THỨC (Dũng: "file nguồn làm chuẩn") |
| A15 | Viết cho người đọc: song ngữ Việt–Lào khi người dùng là người Lào; không ký hiệu cột; liệt kê đủ, đánh số; chú giải 1–2 dòng đầu sheet | CÁCH THỨC |
| A16 | Đếm phải nói rõ đơn vị đếm (dòng hay mã; ví dụ 1.115 dòng có ✓ khác 1.116 mã Kom) | QUY TẮC |

## 4. Khó của Komsenahak (Quân y)

| # | Khó | Hướng xử lý (ai) |
|---|---|---|
| 1 | Không có số lượng | Ưu tiên theo hàng đã trúng 2026 và hàng có đầu mối [A đề xuất, H chọn] |
| 2 | Phần lớn là tên thương mại hoặc tên Lào phiên âm; 363 mã thiếu hoạt chất → 356 có tra cứu, còn 7 chưa định danh | A tra cứu + gắn nhãn độ chắc; H (Tar, dược) xác nhận; xin nhãn hoặc hãng cho 7 mã |
| 3 | Một hoạt chất có nhiều mã thương hiệu (Amlodipine 10mg: KOM-92, 100, 102, 104, 461) | A xếp cạnh nhau theo tên chuẩn; chỉ gộp khi tên Kom có hoạt chất |
| 4 | Danh mục trộn thuốc với hóa chất, vật tư | A lọc theo mục (X = Thuoc → 1.116 mã) |
| 5 | Sheet giá là giá 2026; GM VND/USD, GV kíp (có dòng tra file ngoài), Giá 1/2 kíp; 116 dòng Giá 1/GV ≈ 1,79 | A giữ tiền gốc + ghi công thức; H (người giữ quy tắc giá) xác nhận |
| 6 | Dòng List 2027 và sheet giá lệch nhau | A ghép theo tên + ĐVT theo thứ tự, kiểm chéo (1.104/1.104) |
| 7 | Cột người phụ trách là công thức, đổi theo bản (0/#N/A = chưa nhận) | A chụp bảng chia vào lock; H đổi người thì đổi ở bảng chia |
| 8 | ĐVT không thống nhất (FI/Fl/lọ/viên, vial/ampoule) | A so theo họ ĐVT; H chốt chuẩn ĐVT [còn mở] |
| 9 | Danh sách trúng 2026 không có hàng trật | A ghép thêm file đã chào 2026 khi được giao |
| 10 | Hạn sát (13/11) với giá + ảnh + soft copy cùng lúc | A gom việc theo mã, theo dõi trạng thái; H quyết thứ tự và người |

## 5. Vai đã rõ dần (chi tiết ở `11` và hồ sơ Agent)

- **Người:**
  - Người điều hành / CEO: ưu tiên, hạn, quyết D3.
  - Phét: nguồn đã nộp, công thức giá Kom, hàng hiếm, hồ sơ.
  - Tình: kiểm giá.
  - Trang: NCC Việt Nam, giá mua, giá vốn.
  - Tar: xác nhận thành phần sau tra cứu.
  - Sơn: Trung Quốc, ngoài Hà Nội.
  - Duy: Kom thuốc, giá thuốc đang bán.
  - Huyền: phần được chia.
  - Linh: giá Misa.
  - Dũng: dữ liệu, tổng hợp, vận hành Agent. Không giao việc.
- **Agent:**
  - Agent Gói thầu: điều phối, giữ bản thể, đầu ghi duy nhất.
  - Agent Chuẩn hóa / Đối chiếu.
  - Agent Nhận về (intake).
  - Agent Họp.
  - Agent cá nhân của từng người (chỉ đề xuất cho chủ của nó).
