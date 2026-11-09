# Khung Agent dự án thầu: bản đồ, cách vận hành thực tế và nhật ký theo biên họp (09/11/2026)

Bản "as-built": ghi lại những gì **đang chạy thật** trên Drive và trên máy sau các buổi họp 04, 05 và 09/11. Phương án đề xuất ban đầu là [`AGENT-TEAMS-THUOC-v1.md`](../outputs/phuong-an/agent-teams-thuoc/v1/AGENT-TEAMS-THUOC-v1.md) (nhánh PHƯƠNG ÁN, chia thư mục theo nhóm A–E); thực tế đã chuyển sang **một file chung + Inbox theo người**. Tài liệu này không sửa bản v1, không nâng quyết định nghiệp vụ nào thành LOCKED.

Kinh nghiệm chưng cất: [`KINH-NGHIEM-THAU-THUOC-20261109.md`](KINH-NGHIEM-THAU-THUOC-20261109.md). Decision D16–D19 ở `requirements/DECISIONS.md`; identity node ở `requirements/11-ROLE-AUTHORITY-MAP.md`.

Nhãn: **[F]** có bằng chứng (file, hash, biên họp) · **[L]** lời nói trong họp, chữ ASR, chưa người có thẩm quyền xác nhận · **[M]** còn mở.

## 1. Bản đồ dữ liệu

### 1.1 Trên Drive (Shared drives › 004-Ban lam viec › 16-CNTT-Agent › Thau BV › THUOC-agent-teams-20261104)

| Vị trí | Nội dung | Ai ghi | Trạng thái |
|---|---|---|---|
| `10-DU-LIEU-CHUNG/THUOC-NGUON-HANG-6-DON-VI-v2.xlsx` (id `1ilOLCO-ecT_2NlyGi59Irr8tHqPwOI-y`) | **File chung**: sheet "Nguồn hàng" 1.721 dòng (679 hàng 5 BV + 1.042 hàng chỉ Kom; 74 mã Kom gộp vào 73 dòng BV), sheet "Chưa có giá" 1.222 dòng | Nhóm ghi ô vàng (Giá Sơn/Duy/Tar/Phét/Trang/Huyền, Kết quả trao đổi, Người / ngày); phiên Thầu chỉ vá đúng ô, giữ chế độ xem bộ lọc | [F] Đang dùng. Anh Sơn: "cần file này là được" (05/11) |
| `Inbox_thau/` (id `1pSE8nKwUdfB-aXow8OxjpgkRLj8S30a_`) | 5 thư mục người: `01_Trang` 979 dòng · `02_Tar` 36 · `03_Son` 23 · `04_Duy` 64 · `05_Huyen` 8; mỗi thư mục có file đợt 1, `BAO-GIA_dot-1_<tên>`, hướng dẫn riêng | Mỗi người ghi file của mình | [F] Tách theo cột "Người phụ trách" (AK) trong sheet "Giá NNC 2026" của file Kom: 0/#N/A → Trang, T/S/D/H → Tar/Sơn/Duy/Huyền |
| `Inbox_thau/AGENT_HUONG-DAN-CHO-CLAUDE (dùng chung · đợt 1 Komsenahak)` | Hướng dẫn cho Claude của từng người: nhận diện người dùng, cách khớp dòng, quy về VND/1 ĐVT, mẫu bảng đề xuất, điều cấm | Phiên Thầu | [F] |
| `20-NHOM-HANG/` (6 thư mục theo tình trạng nguồn) | File lọc theo tình trạng nguồn | — | [F] **Tạm gác** từ 05/11 (Dũng); không cập nhật theo các lần sửa sau |
| `90-LUU-TRU/` | Bộ Codex sáng 05/11, bản v2 nhóm chữ cái, đợt 1 hàng VN | — | Lưu trữ |

### 1.2 Trên máy

| Vị trí | Nội dung |
|---|---|
| `outputs/thuoc-bo-5bv-quan-y-20261105/LOCK-20261105/` | **Bộ khóa dữ liệu 05/11** (chỉ đọc): bản chụp file chung + 5 file chia + `VI-TRI-DONG.csv` (1.110 dòng, khóa ghép là cột Mã) + `MANIFEST.json` + `SHA256SUMS.txt` + script và dữ liệu chuẩn hóa. Đọc `LOCK.md` |
| `outputs/thuoc-bo-5bv-quan-y-20261105/v2/THUOC-NGUON-HANG-6-DON-VI-v2.xlsx` | File chung gốc trên máy = bản lock (bản dựng cũ để ở `_ban-dung-cu-truoc-chinh-tay/`) |
| `data-work/source-snapshots/kom-2027-gia-nnc-2026-nguoi-phu-trach-20261105/v1/` | File Kom có cột Người phụ trách (sha256 `20180e7d…`) |
| `outputs/hop/v3/` | Biên họp (RAW, tóm tắt, việc) 04, 05, 09/11 |

### 1.3 Nguồn và quy tắc tiền tệ

Theo `LOCK.md` §3: GM giá mua giữ tiền gốc **VND hoặc USD**; GV giá vốn **kíp** = (GM VND + vận chuyển) ÷ 1,22 hoặc GM USD × 22.000 + vận chuyển, kèm cột quy ra VND; Giá 1 chào thầu **kíp**; giá nhóm điền **VND / 1 ĐVT**. Giá Kom trong file là **giá 2026**, phải báo lại 2027 [F, họp 05/11 #3585–3587].

## 2. Khung Agent đang chạy

```
Người có thẩm quyền (CEO / người điều hành họp, chưa xác nhận danh tính trong biên)
        │ giao ưu tiên, hạn [L]
Phiên Thầu (Claude cha, Dũng) ── một đầu ghi file chung + Inbox + lock
   ├─ Phiên HỌP: nghe họp, RAW/tóm tắt/việc; chỉ đọc
   ├─ Subagent Sonnet: việc song song có kiểm (chuẩn hóa tên, audit)
   └─ Drive: file chung · Inbox_thau/<người>/ · hướng dẫn agent
Node người: Trang · Tar · Sơn · Duy · Huyền (+ Claude của từng người, theo hướng dẫn agent dùng chung)
```

| Vai | Làm | Không làm |
|---|---|---|
| **Dũng + phiên Thầu** | Tổng hợp, đánh giá dữ liệu; tách file theo bảng chia của nhóm; vá file chung đúng ô; gom ô vàng từ Inbox về file chung theo cột Mã; giữ bộ lock; soạn hướng dẫn | Giao việc ("dựa vào bảng chia của nhóm, tôi không phải người giao việc"); chốt giá, NCC, tương đương, Visa; chép đè file khi nhóm đã ghi; đưa dữ liệu ra ngoài công ty |
| **Node người (Trang/Tar/Sơn/Duy/Huyền)** | Hỏi NCC, điền 3 ô vàng (Giá <tên> VND/ĐVT, Kết quả trao đổi, Người / ngày), lưu báo giá gốc, cập nhật TRẠNG THÁI | Sửa cột ngoài ô vàng; tải về rồi tải lên lại; gửi số giá vào nhóm chat |
| **Claude của node người** | Đọc báo giá, khớp dòng (cùng hoạt chất + hàm lượng + dạng), quy về VND/1 ĐVT, trả bảng đề xuất | Ghi Drive; đổi tỷ giá; kết luận tương đương; đọc file người khác |
| **Phiên HỌP** | Ghi và tóm tắt họp khi Dũng yêu cầu bật; đánh dấu [L] và chỗ chưa nghe | Ghi điều gì là đã chốt khi chưa có người có thẩm quyền |

**Luồng một vòng:** bảng chia của nhóm (cột AK) → phiên Thầu tách file vào `Inbox_thau/<người>` → người + Claude của họ điền ô vàng, đổi TRẠNG THÁI → phiên Thầu kiểm file chưa bị đổi trong lúc ghép, gom theo Mã về file chung (chỉ đúng ô) → lock mới khi chốt mốc → refactor file gọn lớn khi đủ nguồn + giá.

## 3. Nhật ký hoạt động theo biên họp

| Ngày | Buổi | Điểm chính [L trừ khi ghi F] | Đã làm theo đó [F] |
|---|---|---|---|
| 04/11 15:44 | Họp nhóm Thuốc (74 phút) | Lọc hàng chưa có giá ra sheet riêng; thêm cột hoạt chất cạnh tên thương mại; lấy đủ hàng các BV; luật anh Sơn: có giá + đã thầu + Visa thì không tìm lại | Sheet "Chưa có giá"; cột Tên chuẩn (hoạt chất · hàm lượng · dạng); nhóm "Đã có, không tìm lại" theo luật Sơn (sau audit còn 5 dòng có Visa dùng được) |
| 05/11 09:03 | Họp thầu 4 BV + Quân y, tìm giá | **Đủ giá đến ngày 11, hồ sơ Kom 11–12, thầu Quân y 13**; làm chung một file, comment khi sai; thuốc: Tar, Sơn, Duy (Kom), Phét, Trang | Một file chung trên Drive; cách làm chung bằng chế độ xem bộ lọc riêng |
| 05/11 13:30 | Họp nhóm Thuốc (41 phút) | Giá Kom 2026 là giá cũ, phải báo lại; GM là giá mua chưa tính vận chuyển, giá mua cho chị Trang bằng VND, quy về đơn vị nhỏ nhất; tô hàng đã trúng; cấp quyền thêm giá cho Trang/Phét/Sơn; chia hàng VN cho Trang, còn lại Duy/Tar/Huyền; Dũng tổ chức nơi lưu báo giá; "không cần che gì" về giá (chưa phải quyết định quyền xem) | 3 cột giá Kom (GM VND/USD, GV kíp + VND, Giá 1); 46 ô "Trúng thầu"; cột Giá Sơn/Duy/Tar/Phét/Trang/Huyền; Inbox_thau 5 người + thư mục BAO-GIA; LOCK-20261105 |
| 09/11 09:06 | Họp tổng thầu (Zoom; thiếu chữ ~10 phút) | **Quân y trước, BV khác đến tuần sau**; tìm NCC và báo giá hàng chưa có giá "hôm nay, ngày mai"; 650/798 mã ghi tên thương mại → dịch ra hoạt chất; "113 mã báo năm ngoái, 14 mã trúng" (chưa kiểm dữ liệu); Linh lấy giá Misa; Sơn tìm NCC ngoài Hà Nội; Duy đưa giá thuốc đang bán vào folder | — |
| 09/11 09:34 | Họp nhóm Thuốc (27 phút) | **Làm tiếp trên file chị Trang đang làm (đợt 1)**; Dũng thêm **cột thành phần hoạt chất chính** vào file đó, Kom trước, gửi lại **chiều 09/11**; mã chưa có thành phần cho AI kiểm, chị Trang check; tách riêng file Kom để làm trước (chưa ai nhận); đơn vị tính FI/lọ/viên không thống nhất | **Chưa làm** (xem §4) |

## 4. Việc đang mở

| # | Việc | Nguồn | Ghi chú |
|---|---|---|---|
| 1 | ~~Thêm cột thành phần hoạt chất chính vào file đợt 1~~ **Xong** (Dũng báo 09/11; file "Final DOT-1_CHI-TRANG…dien-gia-261109" có cột Tên chuẩn + Tar check; 121 mã chưa rõ ở `01_Trang/Dung_inbox`) | Họp 09/11 [L] | Còn 7 mã chưa định danh (báo cáo nhóm 09/11) |
| 2 | Gom ô vàng từ 5 file Inbox về file chung | Luồng §2 | Theo `VI-TRI-DONG.csv`, khóa là Mã |
| 3 | Refactor file gọn lớn khi Kom đủ nguồn + giá | Dũng 05/11 | Dựng từ bộ lock + ô đã điền |
| 4 | Tách riêng file Kom để làm trước | Họp 09/11 #4504 [L] | Chưa ai nhận; cần Dũng quyết có làm không (file chia đã toàn Kom) |
| 5 | Danh sách thuốc không rõ để hỏi BV chính thức; phân tích 14/113 mã trúng 2026 (cần file đã chào 2026 "USB Gia thau Kom 2026") | Họp 09/11 [L] | Người làm chưa rõ |
| 6 | Huyền: định danh node | — | Đã có thư mục `05_Huyen`; vai và tài khoản chưa xác nhận [M] |

## 5. Câu hỏi cho người có thẩm quyền (vẫn mở)

1. Ai được xem giá mua, giá vốn, giá Misa, giá Duy đang bán; giá có nên ra khỏi thư mục chia sẻ cả công ty không.
2. Ai chốt hàng, giá, tương đương (thành phần do AI suy), NCC cho từng BV và Quân y.
3. Giá nộp Kom là Giá 1 hay Giá 2; 116 dòng Giá 1/GV ≈ 1,79 (có thể cộng VAT 5%).
4. Thống nhất ĐVT (FI/Fl/lọ/viên, vial/ampoule) theo nguồn nào.
5. File chính khi có "3 file Excel mới" (họp 09/11 #4540): quy ước hiện hành là file chung + file đợt 1 theo người.
