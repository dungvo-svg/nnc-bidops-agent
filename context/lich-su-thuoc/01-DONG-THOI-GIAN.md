# 01. Dòng thời gian (26/10 → 13/11/2026)

## Trước khi có Agent thầu (thẻ lịch, chưa có biên bản)
- **26/10:** họp "Làm rõ những vấn đề về cung ứng".
- **29/10:** họp tình hình làm giá thầu (đưa file vào Claude phân tích; Oanh, Dũng hỗ trợ dữ liệu). Cùng ngày Phet báo hạn nộp; theo lời Phet, chưa đối chiếu hồ sơ gốc:

  | Gói | Hạn nộp |
  |---|---|
  | MTP | 04/11 |
  | Kom | 13/11 |
  | Mahosot | 25/11 |
  | Settha | 26/11 |
  | Mẹ&Bé/Dek | 27/11 |
  | SVNK | chưa có hạn |
- **30/10:** họp rà báo giá thầu BV "150" để Ms Phet làm; lưu ý vận chuyển hàng Trung Quốc của Sơn.

## 30/10 – 02/11: dựng dự án BidOps
- **30/10:**
  - Dũng yêu cầu áp phương pháp tự chủ OSER R2 (nnc-claude-plugins main `94ddf8b`) cho dự án.
  - Chia việc: Opus quyết, Sonnet chạy song song.
  - Thêm hệ thống tài liệu khóa (authority graph, DECISIONS, LOCK) để giảm việc sửa cấu trúc thiếu chủ đích.
- **31/10:** BidOps định hướng là node CEO đa nhánh, thầu BV là mũi nhọn. Mỗi người có máy, Claude và Agent riêng. Repo công ty chưa tạo được vì thiếu quyền.
- **01/11:** Claude soát code synthetic do Codex dựng, tìm 3 lỗi thật; Codex sửa, 100/100 test đạt. Dũng: "không xem Codex là mặc nhiên đúng".
- **02/11:**
  - Dũng giao Shin/Foundry phối hợp điều hành BidOps.
  - Agent tự phân việc; chỉ hỏi khi đổi định hướng, thiếu quyết định nghiệp vụ hoặc thiếu quyền.
  - Mở 3 nhánh DATA, PHƯƠNG ÁN, HỌP.

## 03/11 – 05/11: bắt đầu thầu thuốc
- **03/11 sáng:**
  - Sếp Quân chủ trì họp "Tổ chức làm 5 gói thầu bằng Claude": 3 folder thuốc, vật tư tiêu hao, hóa chất; bảng gốc và form báo giá cố định.
  - Chỉ đạo CEO trên WhatsApp lúc 10:47.
- **03/11:** nhánh DATA chuẩn hóa Kom vào lược đồ chung, dựng `TIM-GIA-DOT-1`. Nhánh PHƯƠNG ÁN dựng PHUONG-AN-A v1–v4.
- **04/11:**
  - Họp nhóm Thuốc (Dũng, Sơn, Tar): lọc hàng chưa có giá để chia tìm, map theo hoạt chất, giữ tên thương mại.
  - Sau họp, anh Sơn góp ý: dữ liệu tổng đã tốt, chỉ cần "băm" nhóm để mọi người tự chia.
  - Dũng: Kom coi như một bệnh viện, mã giữ nguyên.
- **05/11:**
  - Họp sáng: thầu 4 BV + Cục Quân y, hạn chung đủ giá ngày 11.
  - Họp nhóm Thuốc 13:30: bắt đầu từ sheet Kom, đơn vị nhỏ nhất, Dũng demo AI điền thẳng sheet Drive.
  - Dũng sửa file chung nhiều lượt: Kom bị chẻ, cần gộp; viết song ngữ Việt–Lào cho chị Trang; tiền tệ KIP hay VND.
  - Tạo cây Inbox theo người. Chốt cách làm: một file chung và Inbox theo người (D16), bộ khóa LOCK-20261105 lưu local (D17).

## 06/11 – 09/11
- **06–08/11:** không có tin Dũng trong phiên chính (Dũng hết token). Nhóm làm trên nhiều bản file; một bản tách 2026–2027 xuất hiện ngày 08/11.
- **09/11:**
  - Họp tổng thầu: ưu tiên Quân y; Kom phần lớn ghi tên thương mại, cần dịch ra hoạt chất.
  - Họp nhóm Thuốc: thêm cột thành phần, làm trên file chị Trang (đợt 1).
- **09/11 tối:**
  - Dũng yêu cầu chưng cất kinh nghiệm, hồ sơ Agent và quy trình gói thầu, tách Human/Agent.
  - Gom file 7 BV vào một bể chung: Mittaphab đi đầu, hàng không trùng với gói sau thì không tìm; chị Tình kiểm giá rồi mới đưa vào file thầu.
  - Tạo D18–D20 (PROPOSED). Dũng cho phép push.

## 10/11: gộp giá KOM
- Sáng có họp Zoom, hóa ra là họp sales kênh SPM, không phải họp thầu. Dũng giữ lại làm insight thị trường Lào.
- Gộp giá KOM trên Google Sheet "KOM-2027_Gia-hoi-tu" qua Chrome. Gỡ 134 ảnh AI khỏi sheet.
- Tối, chị Tar chốt quy tắc hội tụ (qua Dũng): chỉ so giá mua; ứng viên không tính VAT; log so giá để local. Kết quả 535 mã có giá.

## 11/11: ảnh, chuẩn bị chị Tình kiểm giá, mâu thuẫn Tar/Trang
- **Sáng:**
  - Ảnh chỉ cần link trên file làm việc; ảnh thật chỉ cần khi nộp.
  - Chị Tar nghỉ, nên ghi thẳng sheet chính kiểu "gộp khác biệt".
  - Tỷ giá chỉ giữ một chỗ (dòng 7 sheet chính).
- **Chiều:**
  - Thêm cột phục vụ chị Tình kiểm giá, cùng giá OTC Viêng Chăn (file chị Hoa).
  - 348 giá vốn đạt; chốt snapshot 17:35.
- **Tối:**
  - 20:43–20:45 gửi WhatsApp cho nhóm Thầu BV, chị Tình, chị Tar.
  - Chị Tar phản hồi "copy cái cũ c Trang đưa vô mã khác". Agent điều tra: 146 mã chị Tar thêm/đổi, 93 mã không ghi nguồn.
  - Agent tự quy đổi giá 13 mã → Dũng: "sao lại quy giá?" → trả về số cũ.
  - Quy tắc mới: mã chỉ 1 ứng viên thì gán luôn; 538 mã chưa có giá thì không tìm nữa.

## 12/11: form chị Oanh, bao bì, SVNK, thông tin hàng
- **Sáng:**
  - Chị Oanh nhắn (08:53–09:01): đưa thông tin và ảnh thuốc vào form báo giá Komsenahak, chừa 2 cột giá, "chỉ đưa thông tin vào, không đổi gì". Agent đầu tiên hiểu nhầm là tin chị Trang.
  - Dũng chốt Q1–Q6; Agent ghi form trên ổ H: (v1…).
  - Gói thiết kế bao bì cho 36 mã thiếu ảnh (nhà máy sẽ sản xuất theo mẫu).
- **11:09:** Phet báo KOM dời sang tuần sau; SVNK gửi 17/11, chị Tình duyệt giá sáng 16/11.
- **14:38 và 14:45:** họp với chị Tar về SVNK (2 video ghi hình). Kết quả: SVNK hội tụ v3 (297 mã) chép lên Drive, nhắn chị Tar 17:16.
- **19h–21h:**
  - Dũng hỏi còn hàng nào thiếu thông tin → lòi ra 19 mã chưa báo hôm qua.
  - Dũng: "nguồn là nguồn nhập chứ không phải xuất xứ", "sao ban đầu bạn ko hỏi luôn".
  - Xử lý từng mã: KOM-547, Aciclovir, Duy.
- **21:07–21:12:** chị Tar góp ý tên NSX/nước chưa đầy đủ, chưa thống nhất; tên hàng chào còn tiếng Việt.
  - Chuẩn hóa NSX/nước/quy cách 310 ô và tên hàng chào/thành phần 107 ô (bằng Tìm và thay thế, so toàn sheet trước/sau).
- **22h–23h45:**
  - Form chị Oanh v6 → v10.
  - Dũng làm rõ lời chị Oanh: không sửa thông tin của người khác.
  - KOM-547 → CARDIONID theo chị Tar.
  - Sửa NSX nhà phân phối cho 5 mã. Giữ KOM-798, 375.
  - Visa không bắt buộc.
  - Báo cáo hướng hoàn thành KOM để chuyển sang SVNK.

## 13/11
- **08:20:** form chị Oanh bị lưu lại qua Google Trang tính, không rõ ai lưu. Nội dung giống v10, cách lưu ảnh đổi.
- **08:35:** sheet KOM chỉ đổi 1 ô so với tối qua (KOM-1117, NSX → DK Pharma). Chị Tình chưa kiểm mã nào.
- **Sáng:** Dũng push git (commit `d636607`). Agent đã loại profile Chrome tạm (`_chrome-temp`) khỏi commit.
- **09:13–09:16:** chị Tar nhờ đưa % và công thức theo bảng giá Phét từng mã vào file SVNK; mã không có trong Phét thì dùng 25/8/10/5.
  - Agent so khác biệt file chị Tar trên Drive (chị đã sửa 365 ô).
  - Điền % và công thức cho 297 mã trên bản local. 83 mã có giá vốn trùng Phét ra giá chào khớp 100%.
  - 09:39 thay file trên Drive (file không đổi từ 09:26).
- **09:17:** Dũng yêu cầu ghi lịch sử này lên git.
