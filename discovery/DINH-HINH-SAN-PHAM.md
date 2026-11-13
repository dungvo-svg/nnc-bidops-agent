# Định hình sản phẩm NNC BidOps — kết quả nghiên cứu (30/10/2026)

> Giai đoạn Formation: REALITY_AUDIT → RESEARCH. Evidence + đề xuất, **không phải authority**. Định nghĩa sản phẩm nằm ở file chủ [`requirements/01-PRD-CORE.md`](../requirements/01-PRD-CORE.md); quyết định ở [`DECISIONS.md`](../requirements/DECISIONS.md); khóa đề xuất ở [`10-LOCK-REGISTER.md`](../requirements/10-LOCK-REGISTER.md). Số liệu là của **Công ty NNC**, kênh HC. Nhãn: **F** = có nguồn · **GT** = giả thuyết/suy luận · **?** = chưa biết.
>
> Cách làm: 3 nhánh nghiên cứu chỉ đọc chạy song song (Sonnet) — hiện trạng & cách làm việc, dữ liệu & ngữ nghĩa giá, phương án & tài sản dùng lại; Opus tổng hợp và đề xuất. Không mở lại workbook gốc (số lấy từ phân tích đã có, đã cộng kiểm chéo); không chép giá vốn. Bản nháp ba nhánh lưu tại `discovery/research-snapshots/RESEARCH-{A-ASIS,B-DATA,C-OPTIONS}-20261030.md` (chỉ ở máy gốc, gitignore). Số chỉ có trong bản nháp (đọc ảnh/đếm của nhánh) mà chưa kiểm độc lập được ghi **GT**. Tài liệu nội bộ: có tham số giá, tên BV, thông tin nhân sự — không đưa ra ngoài công ty.

## 1. Tóm tắt một trang

- **Sản phẩm nên là gì (đề xuất):** một lớp *bằng chứng và quyết định theo từng gói thầu* — mỗi dòng yêu cầu BV (đúng version) được ghép với hàng NNC và chào NCC có ngày/đơn vị/hiệu lực, có trạng thái rõ, rồi trình người có quyền chọn chào. Chưa phải app. Xem `01-PRD-CORE` mục "Sản phẩm đề xuất".
- **Khuyến nghị cách làm (chỉ khuyến nghị, D07 do chủ nghiệp vụ chọn):** cách 1 làm nền (chốt chủ master + form trên Excel sẵn có) **cộng một lát mỏng cách 2** (bước đối chiếu có dấu vết, agent đề xuất ghép, người duyệt) trên **một** ca có sai khác thật. Hoãn công cụ mới đến khi có số đo.
- **Tài sản lớn nhất phát hiện được:** pipeline thầu của Dũng `personal-meeting-assistant/.local/projects/thau-bv-nnc/work` (theo docstring/đầu file, chưa đọc thân hàm: ghép trạng thái A–D, danh mục chung, `SCHEMA.md` cấm đoán loại giá). Đề xuất (GT): **ADAPT logic** sau khi đọc kỹ, không dựng song song. `build_tender_sets.py` ở đó vẫn **không chạy**.
- **Chặn lớn nhất:** chưa ai là chủ master (≥3 bảng bị coi là master); hướng dẫn trong BGC có phân vai "duyệt" nhưng tin nhắn không cho thấy ai duyệt thật, và không có bằng chứng ai nộp; quy tắc giá (hệ số, % vận chuyển, FX, thuế) lệch giữa các bảng.
- **Đề xuất (GT) khóa sớm nếu người có quyền xác nhận:** phương pháp (`LCK-METHOD`) và ba luật dữ liệu có bằng chứng đo (D11–D13). Chủ master và ca đầu cần họp.

## 2. Hiện trạng và cách làm việc thật (tái dựng, **chưa được người làm xác nhận**)

Luồng một gói (F trừ khi ghi khác; mã tin đầy đủ ở `sources/whatsapp/chronology.json`):

| # | Bước | Ai | Ghi chú |
| --- | --- | --- | --- |
| 1 | BV phát hành hồ sơ xlsx (Thuốc/Hóa chất/VTTH, tiếng Lào) | BV → Phet | Ngày phát hành, kênh nhận: ? |
| 2 | Báo hạn, nhờ hỗ trợ làm bảng giá; giữ phần chuẩn bị + in hồ sơ | Phet | 29/10 09:50, 09:58 |
| 3 | Nguồn tin gói; xem giá tỉnh | Siêng, Tình | 29/10 09:55, 09:58 |
| 4 | Tìm NCC Trung Quốc, xin giá/mẫu, tính giá vốn vào Google Sheet riêng; cập nhật nhiều lần (28/10, 29/10, 30/10 10:23) | Tình giao list → Sơn | Sơn nhờ Phet nhập (28/10 09:35); số lần chính xác: GT (nháp A) |
| 5 | Nhập giá vào bảng theo nhóm (giá vốn, giá 1 TW / giá 2 tỉnh, sau VAT) | Phet | 29/10 10:29–10:33 |
| 6 | Nguồn khác: Sharma, Stevimed, bảng giá mua gần nhất | Linh, Trang, An | 29–30/10 |
| 7 | Vòng kiểm hàng chưa có giá | Phet + Cung ứng | 29/10 16:57–17:06 |
| 8 | Tranh luận chất lượng/giá/MOQ/mẫu | Phet, Tình, Sơn | gạc, cottonoid |
| 9 | Tính giá/biên: công thức cũ + phân tích AI hai phương án | Phet, Oanh | 28/10 |
| 10 | **Duyệt giá/danh mục chào** | **?** | Hướng dẫn BGC (`Huong dan!B1:C28`, theo `REPORT-WORKBOOKS.md`) phân vai nhập–tính–duyệt–in; trong 168 tin không có tin nào về việc duyệt — thực tế ai duyệt: ? |
| 11 | In / **nộp** | Phet in; nộp: **?** | |

Song song: Dũng dựng danh mục chung + 4 bộ theo gói bằng script, gửi 29/10 15:14; Oanh gửi bảng gốc chung (BGC) 30/10 09:18.

**Cách làm việc quanh dự án:** họp Zoom do CEO triệu tập (29/10 09:00, 30/10 08:15) — chỉ có thẻ lịch, **không biên bản**; chỉ đạo qua WhatsApp; kế hoạch Cung ứng R10 (F1–F5, tracker 0/5, CEO + Claude kiểm thư mục) là **dự kiến**, chưa kiểm thực thi; Oanh đã dùng AI phân tích giá và CEO khuyến khích.

**Đau có số (F):** 5 gói có hạn 4/11 · 13/11 · 25/11 · 26/11 · 27/11 (+SVNK chưa có hạn); BGC 2.126 mã / 3.269 dòng (Mahosod 824, Settha 911, Meladek 205, SVNK 676, Mittaphap 653); Komsenahak 1.455 dòng / 27 BV; danh mục chung 29/10 19:08: Tìm nguồn 1.346 · Đã có giá 1.145 · Xem lại 210 · Tính giá 28 · Chốt NCC 7; giao việc mới 61/2.126 mã; Phet xin nghỉ 26/11–1/12 trùng 2 hạn nộp. **Chưa có số:** thời gian mỗi gói, số vòng làm lại, tỷ lệ quote hết hạn.

## 3. Dữ liệu — bảng nào dùng được

| Bảng | Khóa dùng được? | Trạng thái dữ liệu |
| --- | --- | --- |
| BGC (Oanh) | **Có** — mã MPSC duy nhất 2.126/2.126; 3.269 dòng BV khớp mã 100% | Vùng chào NCC V:AB **trống**; tỷ giá `Tham so!B5:B8` trống; 22.814 công thức chưa có kết quả lưu |
| Danh mục chung (Dũng) | ? — không có tệp trong workspace | 2.736 mặt hàng (cộng trạng thái) ≠ 2.126 mã BGC — chưa đối chiếu |
| Komsenahak (Phet) | **Không** — cột mã chứa STT, 15 lặp, 16 vắng; không có cột số lượng | 202 `#N/A`; hai họ công thức khác nhau; nhãn 2027 nhưng mốc 2024 |
| Bảng nhóm Phet, sheet Sơn, bảng mua gần nhất, Sharma | ? — chỉ có ảnh/link, không có tệp | chưa đo |
| Stevimed | STT lệch giữa 2 sheet | **không có trường giá** |

Ba hệ khóa chưa có bảng nối: MPSC (BGC) · mã AMIS/MISA · STT Komsenahak.

**Ngữ nghĩa giá (chỉ nêu vị trí):** "Giá vốn" có ≥4 cách hiểu (ảnh giá Viêng Chăn, BGC `AC`, KOM `I`, cột giá vốn của Phet chưa gồm vận chuyển tỉnh). Hệ số chia BGC 1,12 vs KOM 1,22. % vận chuyển tỉnh: Phet nói 5%/12% là vận chuyển tỉnh, chưa nằm trong giá vốn (C12); ảnh các mẫu có tham số khác nhau (claims: 5%, 12%, 28%, 25%); BGC dùng 5% chung (GT: lệch theo nhóm), và công thức BV!L không có bước này dù ghi chú nói có. Cột "Giá CHỐT" BGC không sheet BV nào đọc. Tỷ giá: BGC nhân, bảng mua gần nhất chia (GT, đo 2 dòng). Tiền tệ: BGC không chặn giá trị lạ; R10 chỉ cho VND/USD/THB/CNY/LAK (CNJ bị hiểu là KIP). Cơ sở thuế (trước/sau VAT) lệch giữa Phet, KOM và R10.

## 4. Điểm khóa đề xuất

Theo luật graph: chỉ người ở cột *Approved by* khóa; agent đề xuất. Chi tiết 8 trường ở `10-LOCK-REGISTER`.

Nội dung, bằng chứng và trường còn thiếu của từng khóa nằm ở file chủ (`DECISIONS.md` D10–D13, `10-LOCK-REGISTER.md`); ở đây chỉ tóm tắt:

- `LCK-METHOD` (D10) — phương pháp; chỉ thiếu Dũng xác nhận + ngày.
- `LCK-MATCH-KEY` (D11) — khóa ghép; thiếu người duyệt (chờ D02).
- `LCK-VALUE-SEMANTICS` (D12) — trống/0/chưa xác nhận, lịch sử ≠ quote, mã tiền; thiếu người sở hữu quy tắc giá.
- `LCK-STATUS` (D13) — bộ trạng thái; thiếu người duyệt quy trình.
- D02 (master; ứng viên GT: BGC) và D01 (ca đầu, xem §8) — **chọn trong họp**, sau đó mới đề xuất khóa.

**Chưa nên khóa:** cách làm (D07) trước khi có số đo lát thử; công thức/hệ số/thuế/% vận chuyển (D03) trước khi người sở hữu xác nhận; danh mục chào, tương đương kỹ thuật; giao diện/stack; baseline; hệ mã hàng cuối (App Cung ứng có bước đổi mã 02/11); tên org/repo (D08).

## 5. Mâu thuẫn giữa nguồn (treo đúng phần, không tự chọn)

1. **Master:** BGC của Oanh (5 BV) · danh mục chung của Dũng (4 gói, không Mittaphap) · Phet làm giá tại file Komsenahak.
2. **Số hàng:** danh mục chung 2.736 > BGC 2.126 dù BGC có thêm Mittaphap.
3. **Tập gói và tên BV:** Phet {Mittaphap, Komsenahak, Mahosod, Settha, MeDek} · Dũng {Mahosot, Settha, MeDek, SVNK}; Mahosod/Mahosot, Meladek/MeDek.
4. **"Giá 2027":** Phet nói là giá đã chào 2026; file gắn 2027; KOM còn mốc 2024.
5. **Sharma:** Linh "đã gửi" · Phet "đã up" rồi nhờ kiểm lại.
6. **Giá gạc TQ:** Phet thấy rẻ hơn · Sơn thấy đắt · Tình: số lượng nhiều giá chưa tốt.
7. **Quy tắc giá:** hệ số 1,12 vs 1,22; % vận chuyển 5% chung vs theo mẫu/nhóm; ghi chú nói chia (1−5%) nhưng công thức không có; tỷ lệ hoa hồng giữa BGC và KOM khác nhau (GT, nháp B); trước/sau VAT.
8. **Chiều tỷ giá:** BGC nhân · bảng mua gần nhất chia (GT, nháp B đo 2 dòng ảnh I09).
9. **Bảng mua gần nhất:** có dòng ghi "Mua từ n NCC" nhưng chỉ một mã NCC/ô (GT, nháp B đọc ảnh I09) — nếu đúng thì trái quy tắc "một dòng = mã × NCC" của R10.
10. **Báo cáo nội bộ lỗi thời:** báo cáo ảnh nói chưa tải ảnh Phet nhưng bản sau đã tải I14–I17; 169 vs 168 tin; 29 vs 32 nhận định (31 nhận định + 1 giả thuyết); 19 tiền tố mã tin 6 ký tự bị trùng (đã kiểm lại trên `chronology.json`: 42/168 tin) → phải dùng ID đầy đủ.
11. **"Sếp duyệt":** có trong hướng dẫn của BGC (`Huong dan`, theo `REPORT-WORKBOOKS.md`) như phân vai dự kiến; tin nhắn không có việc duyệt nào — chưa biết đã thực hiện hay ai là "sếp".

## 6. Chưa rõ (cần hỏi, không đoán)

- Ai duyệt giá / danh mục chào; ai nộp, nộp thế nào; BV được chào từng dòng hay cả lô.
- "BV 150" là BV nào; "thêm 1 gói nữa" (CEO 09:22) là gói nào; buổi thứ Hai là họp phân công hay trình bày cách làm, ai trình bày.
- Phạm vi App Trợ lý Cung ứng so với BidOps (trùng giá/NCC/mã?); mã nguồn App chưa tìm thấy.
- File nào **được phép** dùng làm ví dụ (Dũng hỏi Phet 30/10 10:28 về ảnh có giá vốn — chưa thấy trả lời).
- Nghĩa các cột KOM (GM/VC/GT/HH/BS D); số lượng BGC G:K là 0 hay trống; đồng nghĩa ĐVT (Com=Tab? Pcs=Ea?).
- Bản Sharma hiện hành; sheet Sơn sau 30/10 10:23; R10 diễn ra thế nào sau 10:41 30/10.
- Ai làm thay Phet 26/11–1/12.

## 7. Phần thiếu — thiếu gì, ai có thể cung cấp

**Phiếu P1 so với SOP (7 mục thiếu):**

| Mục SOP | Thiếu | Ai cung cấp |
| --- | --- | --- |
| Ca cụ thể | gói/lô đầu (D01) | Dũng + CEO/Phet |
| Hiện trạng được xác nhận | người đang làm xác nhận luồng mục 2, nhất là bước 10–11 | Phet, Tình, Oanh |
| Ví dụ được phép | xác nhận file/ảnh nào được dùng (có cột giá vốn) | Phet, CEO |
| Người dùng đầu ra, người duyệt | tên người cụ thể | CEO |
| Tiêu chí đúng/sai | ví dụ + kết quả mong đợi | chủ nghiệp vụ |
| Baseline | thời gian một ca, số lần sửa tay, mức hỗ trợ | đề xuất: người đang làm đo; ai ghi — chờ Dũng giao |
| Người thử độc lập | D06 | Dũng xác nhận (theo SOP) |

**Điều kiện vào P2 (SOP trang 3) còn thiếu:** phiếu P1 được nhận · master hiện hành (D02) · phạm vi thay đổi + cách quay lại · môi trường thử (`data-work/` mới có README) · người thử/kiểm nghiệp vụ. Làm được ngay: fixture tổng hợp + kịch bản (SOP P2 mục 6).

**Trường dữ liệu thiếu cho đối tượng tối thiểu:**

| Đối tượng | Thiếu | Ai |
| --- | --- | --- |
| Yêu cầu BV | mã gói; nguồn file + sheet + dòng; ngày bản BV; quy cách tách trường; số lượng (KOM) | Phet, Oanh |
| Hàng NNC | bảng nối MPSC ↔ MISA ↔ STT KOM; quy đổi ĐVT | Hoa, Oanh, Phet |
| Chào NCC | hiệu lực đến; MOQ; bội đóng gói; hệ số hộp→đơn vị; lead time; điều kiện giao; mã NCC chuẩn; tin nguồn; nhiều NCC/mã | Sơn, Linh, Trang, Tình, Yaeng |
| Bằng chứng kỹ thuật | hãng/nước/đăng ký + hạn; lô/hạn dùng; kết quả mẫu; người nhận tương đương | Phet, Tình, người kỹ thuật (D04) |
| Kịch bản giá | tham số có phiên bản/hiệu lực/chủ; basis giao/thuế; % tỉnh theo nhóm; bậc số lượng | Phet, Oanh, An, Linh, Hoa |
| Quyết định | log từng dòng; cờ chào/không chào; ảnh chụp lúc duyệt | người có quyền (chưa gán) |

## 8. Đề xuất bước tiếp

1. **Họp ngắn trước buổi thứ Hai** (CEO, Oanh, Phet; Dũng điều phối) chốt theo thứ tự: D02 master → D01 ca đầu → D11–D13 ba luật dữ liệu → ai duyệt/nộp (bổ sung `CAP-*`). Gói họp do subagent `thu-ky-hop` soạn từ file này.
2. **Ca đầu — ba ứng viên** (D01 quyết):
   - *Komsenahak, phần hàng chưa có giá + dòng sai khác* — có nhu cầu thật (CEO giao 30/10 09:15), hạn 13/11, sai khác có sẵn (Com/Amp, 600/500 ml); nhược: khóa yếu, không số lượng, Phet đang làm giá ở đó.
   - *Mahosot qua BGC* — khóa sạch, hạn 25/11 (thời gian đủ); nhược: vùng chào trống, Phet xin nghỉ gần hạn.
   - *Lô Stevimed/cottonoid* — nhỏ, nhiều bằng chứng sai khác; nhược: không có giá, khó đo giá trị.
   Khuyến nghị (GT): Komsenahak phần giới hạn nếu Phet đồng ý; nếu không, Mahosot. Tránh Mittaphab.
3. **Song song, không chờ họp:** fixture tổng hợp + expected cho 9 ca `P2-VALIDATION` dưới `data-work/fixtures/`; đọc thân hàm `match_build.py`/`build_master.py`/`SCHEMA.md` (chỉ đọc) để quyết `REUSE/ADAPT`.
4. **Sau khi có D01/D02:** người đang làm xác nhận as-is → cập nhật `P1-REQUEST` → Decision Card D07 → F01 sang DECISION.
