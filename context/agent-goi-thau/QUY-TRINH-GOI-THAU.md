# Quy trình một gói thầu (Human + Agent) — BẢN NHÁP (09/11/2026)

Đúc kết từ ca Thuốc 30/10–09/11 ([kinh nghiệm](../KINH-NGHIEM-THAU-THUOC-20261109.md)); vai Agent ở [hồ sơ Agent](HO-SO-AGENT-GOI-THAU.md). Trạng thái: **đề xuất** (D20 PROPOSED). Chưa thay SOP P1/P2; khi được duyệt sẽ thành phiếu P1 cho cách làm gói thầu.

Nhãn: **QUY TẮC** = giữ ở mọi gói · **CÁCH THỨC** = mặc định theo ca Thuốc, đổi được.

## 1. Năm lớp dữ liệu (sửa sự cố "dữ liệu tràn lan")

| Lớp | Là gì | Ai ghi | Định dạng | Quy tắc |
|---|---|---|---|---|
| **L0 Nguồn thô** | Hồ sơ BV/Kom, danh sách trúng, báo giá gốc, file năm trước | Không ai (chỉ đọc) | Giữ nguyên định dạng gốc | Chụp **một lần** vào `00-NGUON/` + hash. Hai bản khác nhau của cùng nguồn → treo, hỏi người giữ nguồn |
| **L1 Bản thể gói** | Một file duy nhất cho gói: mỗi mã một dòng; nguyên văn + chuẩn hóa + giá đã nhận + trạng thái | **Chỉ AG-GOI** | Một file (xem §3), cố định tên | Không ai sửa trực tiếp; mọi thay đổi qua intake; mỗi lần đổi nâng lock |
| **L2 Runtime** | File làm việc theo người (`Inbox/<người>/`), file tra cứu, file nháp, file của Agent cá nhân | Chủ của file | Tách từ L1, cùng bố cục | Không chép runtime vào L1 bằng tay; không gộp việc của người khác vào file của mình |
| **L3 Quyết định** | Giá chào, NCC chọn, tương đương, Visa, danh mục chào | Người có thẩm quyền (ô duyệt hoặc chữ ký) | Cột duyệt trong L1, do người ghi qua ô của mình hoặc qua bảng duyệt | AI không điền; có người + ngày + căn cứ |
| **L4 Xuất bản** | Soft copy theo mẫu BV, bộ ảnh, bảng trình bày, báo cáo | AG-GOI sinh ra | Theo mẫu BV | Luôn sinh lại từ L1 + L3; không sửa tay bản xuất |

**Sổ lock:** `LOCK-<GÓI>-<YYYYMMDD-HHMM>/` gồm bản chụp L1, bảng chia, bản đồ vị trí, danh sách ô đổi so với lock trước và hash. **QUY TẮC:** lock cũ không sửa; bản thể hiện hành = lock mới nhất.

## 1b. Bể chung nhiều gói (chỉ đạo Dũng 09/11)

Khi nhiều gói chạy cùng mùa, không tìm hàng theo từng gói riêng. Agent gom yêu cầu mọi gói vào **một bể chung**, trải lên timeline, rồi mới chia việc.

| QUY TẮC | Nội dung |
|---|---|
| Gói nộp trước phủ gói nộp sau | Mỗi cụm hàng (cùng mã BV, hoặc cùng tên chuẩn có nhãn AI) chỉ tìm **một lần**, ở gói nộp sớm nhất còn chưa nộp; các gói sau nhận lại kết quả |
| Gói đã nộp đi đầu | Mittaphab đã nộp: cụm có giá MTP → gói sau dùng lại hàng/NCC, chỉ kiểm giá và yêu cầu 2027 của BV đó. Cụm **chỉ** có ở gói đã nộp, không gói sau nào cần → **không tìm** |
| Lặp lại mỗi lần có gói mới | Khi có file thầu mới hoặc một gói vừa nộp: Agent dựng lại bể chung, nâng lock, báo số "tìm mới lần đầu" của từng gói |
| Gói đang làm vẫn phủ gói sau | Kom đang làm: cụm trùng gói sau được đánh dấu; khi Kom chốt, gói sau nhận "có nguồn Kom". Vẫn kiểm ĐVT, hàm lượng theo yêu cầu từng BV |
| Không chứa giá | Bể chung chỉ có cụm, gói, hạn, trạng thái; giá nằm ở bản thể từng gói (tránh thêm bản sao giá) |
| Đủ điều kiện mới hỏi NCC | Cụm phải có hoạt chất · hàm lượng · dạng · ĐVT rõ; cụm thiếu thì làm rõ hoạt chất trước (Tar xác nhận thành phần) |

Bản đầu: `outputs/thuoc-be-chung-7-goi-20261109/BE-CHUNG-THUOC-7-GOI_20261109.xlsx` (7 gói, 1.521 cụm). Hạn tìm mặc định = hạn nộp − 3 ngày cho tính giá, chị Tình kiểm và làm hồ sơ (CÁCH THỨC).

## 2. Các bước

| Bước | Người [H] | Agent [A] | Ra | Cổng qua bước |
|---|---|---|---|---|
| **0. Nhận gói** | Người điều hành nêu gói, hạn, ưu tiên | AG-GOI tạo khung gói: `00-NGUON/`, `10-BAN-THE/`, `20-RUNTIME/`, `30-DUYET/`, `40-XUAT-BAN/`, `LOCK/`; chụp L0 + hash | Khung gói + LOCK-0 | Có hồ sơ yêu cầu chính thức và hạn (hoặc ghi "hạn chưa rõ") |
| **1. Dựng bản thể** | — | AG-GOI + AG-CHUAN: mỗi mã một dòng, giữ nguyên văn, chuẩn hóa tên/hoạt chất/nhóm (có nhãn độ chắc), ghép trùng giữa BV theo mã | L1 + LOCK-1 | Đủ 100% mã; không trùng; phần AI suy ra có màu |
| **2. Đối chiếu lịch sử** | Phét xác nhận nguồn đã nộp và công thức giá | AG-CHUAN: trúng/chào năm trước, nguồn đã nộp, giá Kom/BV khác, Visa đã có; tính "tìm một lần, dùng nhiều gói" | Cột lịch sử trong L1 + danh sách "đã có, không tìm lại" | Người giữ quy tắc giá xác nhận cách đọc giá (tiền tệ, công thức) |
| **3. Chia việc** | Nhóm điền **bảng chia** từ **bể chung** (người phụ trách từng cụm); người điều hành duyệt. Mỗi người nhận **một hàng đợi đã xếp sẵn** và làm **tuần tự** từ trên xuống | AG-GOI lập kế hoạch song song kiểu Agent (xem §2b): xếp hàng đợi theo hạn, gom lô theo NCC/nước, giới hạn việc đang làm; chụp bảng chia vào lock; tách runtime theo người | `20-RUNTIME/<người>/` + hàng đợi theo người | Bảng chia có trong lock; tổng cụm chia = tổng cụm "tìm mới" |
| **4. Tìm nguồn & báo giá** | Từng người hỏi NCC, điền ô của mình, lưu báo giá gốc, đổi trạng thái. Ca Thuốc: chị Trang nhận khung ≈ 900 mã; **chị Lý cùng tìm thuốc phía sau** (phần chia lấy theo bảng chia của nhóm) | AG-CANHAN đọc báo giá, đề xuất bảng giá cho chủ; AG-GOI trả lời câu hỏi dữ liệu, không ghi runtime | Runtime đã điền + báo giá gốc | Cụm chỉ được hỏi NCC khi đủ điều kiện (§1b) |
| **5. Nhận về** | — | AG-NHAN kiểm và đưa ô hợp lệ vào L1 theo mã; báo ô bị từ chối cho đúng người; AG-GOI nâng lock | L1 mới + LOCK-n + danh sách thay đổi | Không ô nào đi vào L1 mà chưa qua kiểm |
| **6. Tính giá** | Theo quy trình cung ứng liên kết Kế toán: **giá vốn kế hoạch = giá mua + cước theo điểm nhận** (QT-CU-04 khúc 2; cước theo QT-CU-05), so NCC bằng giá vốn chứ không bằng giá mua; giá bán/lãi theo QT-CU-07. Người giữ quy tắc giá xác nhận công thức (tiền tệ, vận chuyển, hệ số, VAT) | AG-GOI tính giá vốn và giá chào **đề xuất** theo công thức đã xác nhận; so giá cùng loại (GM/GV/chào, ĐVT, tiền tệ, VAT, thời điểm) | Cột giá đề xuất trong L1 | Công thức có người xác nhận |
| **7. Kiểm giá & duyệt** | **Chị Tình kiểm giá** (cân đo, quyết định) **trước khi giá vào file nộp**; duyệt giá hai cấp có lưu vết theo QT-CU-04 khúc 3 và QT-KT-01 điều 22 (quản lý hàng kênh → CEO); dược hoặc người có quyền xác nhận tương đương; CEO chốt danh mục và giá chào | AG-GOI soạn bảng kiểm giá cho chị Tình và bảng duyệt gọn, có phương án và hệ quả (R2 decision contract) | L3 có người + ngày | Mọi dòng chào có chị Tình kiểm + duyệt; dòng không chào có lý do. Chưa qua kiểm thì không vào file nộp |
| **8. Hồ sơ nộp** | Phét/người nộp kiểm bản in và nộp | AG-GOI sinh soft copy theo mẫu BV, bộ ảnh có nguồn, Visa; kiểm thiếu | L4 + LOCK-NOP | Người nộp xác nhận đã nộp |
| **9. Sau thầu** | Nhận kết quả trúng/trật | AG-GOI ghi trúng/trật/giá trúng vào lịch sử; rút kinh nghiệm | Lịch sử + bài học | — |

## 2b. Chia việc kiểu Agent, người làm tuần tự (CÁCH THỨC)

Agent chạy song song được; người thì làm từng việc một. Vì vậy AG-GOI lập kế hoạch song song **ở cấp nhóm**, còn mỗi người chỉ nhận **một hàng đợi tuần tự**:

1. **Xếp theo hạn (EDD):** cụm của gói nộp sớm nhất lên trước; trong cùng hạn, cụm phủ nhiều gói lên trước (tìm một lần, dùng nhiều chỗ).
2. **Gom lô theo NCC/nước (batching):** các cụm hỏi cùng một NCC hoặc cùng nước (Việt Nam, Trung Quốc…) xếp liền nhau để một lần hỏi được nhiều mã.
3. **Giới hạn việc đang làm (WIP, kiểu Kanban):** mỗi người tối đa một lô đang hỏi NCC + một lô đang chờ trả lời; xong mới kéo lô kế tiếp. Chờ NCC thì kéo lô khác, không mở thêm.
4. **Cân tải theo năng lực thật:** số cụm chia theo tốc độ đã đo được ở ca trước, không chia đều; hàng khó (hiếm, dạng đặc biệt) đi riêng cho người quen nguồn.
5. **Nhịp ngắn:** sáng nhận hàng đợi, chiều Agent nhận về và báo phần trễ so với hạn tìm; trễ thì Agent đề xuất chuyển lô, người điều hành quyết.

Agent **không giao việc**: hàng đợi là đề xuất dựa trên bảng chia của nhóm; người điều hành duyệt.

## 3. Chọn file hay sheet (QUY TẮC: chọn một lần ở bước 0, ghi vào lock)

| Lớp | Mặc định đề xuất | Vì sao |
|---|---|---|
| L0 | Giữ nguyên file gốc (xlsx/pdf) | Không biến đổi nguồn |
| L1 | **Một file xlsx do Agent giữ**, kèm bản xem Google Sheets chỉ đọc | Agent ghi được có kiểm, có hash; người xem qua bản chỉ đọc. Tránh chuyển đổi qua lại sinh bản trùng |
| L2 | **Google Sheets theo người** (một file, một sheet chính) | Người làm trực tiếp trên Drive, có lịch sử phiên bản; không cần tải về |
| L3 | Ô duyệt trong bảng duyệt Google Sheets (một file cho gói) | Có người, ngày và lịch sử sửa |
| L4 | Theo mẫu BV (thường xlsx) | Nộp đúng mẫu |

**CÁCH THỨC:** nếu nhóm quen làm trực tiếp trên một Google Sheet chung, vẫn được, với điều kiện: chỉ một file được gọi là L1, các ô người ghi được khóa vùng (protected range) theo người, và Agent vẫn nhận về qua bước kiểm trước khi nâng lock.

## 4. Đặt tên và vị trí (CÁCH THỨC, mặc định)

```
<Gói>/                       ví dụ KOM-2027/
  00-NGUON/                  L0, chỉ đọc
  10-BAN-THE/BAN-THE_<GOI>.xlsx    L1 (một file, tên cố định)
  20-RUNTIME/<NN>_<Người>/   L2 + BAO-GIA/
  30-DUYET/DUYET_<GOI>        L3
  40-XUAT-BAN/               L4
  LOCK/LOCK-<GOI>-<ngày-giờ>/
  00-DOC-TRUOC.md            trạng thái + đường dẫn (một trang)
```

Tên file không chứa "final", "v2", "(1)", "moi". Phiên bản nằm trong LOCK, không nằm trong tên file.

## 5. Nhịp vận hành

- **Đầu phiên Agent:** đọc Drive thật, so với lock mới nhất, liệt kê thay đổi ngoài quy trình (file mới, bản trùng) và báo trước khi làm.
- **Mỗi mốc (sáng/chiều hoặc khi có người đổi trạng thái):** nhận về → nâng lock → báo cáo ngắn theo đúng loại đếm.
- **Trước họp:** báo cáo 1 trang + câu hỏi D3 có phương án.
- **Sau họp:** việc là lời nói [L] chỉ thành việc khi người có thẩm quyền xác nhận.

## 6. Áp vào Kom 2027 ngay (đề xuất, cần Dũng xác nhận)

Hiện có ≥ 7 bản chứa giá Kom (xem kinh nghiệm §1). Để có một bản thể trước hạn 13/11:

1. Dũng chỉ định **một** bản làm L1 (đề xuất: sheet "Giá NNC KOM — Làm việc chung", vì báo cáo nhóm 09/11 đang đếm theo bản này).
2. Các bản còn lại chuyển vào `_archive`, ghi rõ "không làm trên bản này".
3. AG-GOI chụp LOCK-KOM mới từ L1 + bảng chia hiện hành, rồi nhận về từ các file runtime (Trang Final, Duy, Tar, Sơn, Huyền) theo mã.
