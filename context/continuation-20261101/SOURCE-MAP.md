# Bản đồ nguồn: version, hash, mức độ đọc

> Bản audit/plan đã được Codex đối chiếu độc lập và lưu vào project ngày 01/11/2026. Claude Opus tổng hợp, Sonnet kiểm hai nhánh. Các nhãn draft/đề xuất trong nội dung là trạng thái quyết định, không có nghĩa file còn ở ngoài project. Chưa thay runtime, tích hợp code, merge hay deploy. Chi tiết nguồn/giới hạn: SOURCES-READ.json và PUBLICATION-RECEIPT.json.


**Quy ước nhãn:**
- **FRESH-READ** — đọc bằng tool trong lượt audit 01/11.
- **HASH-MATCH** — nội dung đã nhận đủ chữ ở lượt trước trong cùng conversation; lượt 01/11 chỉ xác minh SHA256 khớp, không đọc lại.
- **INDEX** — chỉ biết đường dẫn và hash, chưa đọc nội dung.
- **CODEX-RECEIPT** — số liệu do Codex báo, Claude chưa tự kiểm.

**Ký hiệu đường dẫn:**
- `OWNER` = `D:\WORK\Agent\Agent-first\NNC BidOps Agent`
- `OUT` = `C:\Users\Admin\Documents\Codex\2026-10-31\task\output`

## Phương án và bàn giao

| Nguồn | Đường dẫn | SHA256 | Nhãn |
| --- | --- | --- | --- |
| A version 8 | `OWNER\context\continuation-20261101\sources\PLAN-A-v8.md` | `7caf1d009a6a5598748f6b22c8b4ee783526e21cce00fb1d4b382ba282db617f` (khớp `SOURCE-RECEIPT.json`) | **FRESH-READ dòng 24–153 và 300–499** (§1 mission, §2 năm phép kiểm, §3 CEO, §4 node người–agent, §7 hàng–chứng từ–tiền, §8–10 tín hiệu, runtime, cửa onboarding). Các dòng 1–23, 154–299 và 500–558 là HASH-MATCH |
| Lite version 1 | `OWNER\context\continuation-20261101\sources\PLAN-A-LITE-v1.md` | `7a3a13fe64ba6add909fed2f0cd09a08ed91c5dfbec56c894702302220bdcd9d` | **FRESH-READ toàn bộ (72 dòng)** |
| Sự thật trích từ workbook | `OWNER\context\continuation-20261101\sources\QUALITY-SOURCE-FACTS.json` | (Codex 03:58:29 UTC) | FRESH-READ. Đây là bản trích có cấu trúc, read-only, do Codex làm, không tính lại workbook |
| Readout B v4, 6.655 byte | `OWNER\context\continuation-20261101\sources\IMPLEMENTATION-READOUT-v4.md` | `290854053f39dfe82648599bf4f2a2d488facf330365485585062f480bd55b3a` | FRESH-READ. Chỉ dùng phần BidOps |
| Manifest bàn giao B; bundle 10 phụ lục | `OUT\bidops-parent-context-20261031\sources\` | `8f7b7fd2…`, `b877d67e…` (theo thẻ evidence 31/10) | Nhận đủ chữ 31/10. Lượt 01/11 không có quyền đọc thư mục này nên **chưa kiểm lại hash**. Kích thước bundle lệch 137.395 so với 135.602 byte: nghi lỗi metadata, chưa xác minh |

## Nguồn chat, kế hoạch và file gốc (đọc 01/11 bằng `source-audit-sonnet`, Opus đối chiếu)

### Chat WhatsApp

`OWNER\sources\whatsapp\chronology.json` đã được đọc đủ 168 tin; tin cuối là Sơn, 30/10 10:28. Dưới đây là các tin quyết định, theo thứ tự thời gian.

**29/10**
- 09:48 — `3EB080A33A52E10CAF6CFC`: Phét gửi file thầu Mahosod, hạn 25/11. Kèm 3 file xlsx, cả 3 **không có** trong 22 file gốc.
- 09:55 — `3A80D142E07EE83C9B44`: Kom hạn 13/11.
- 09:58 — `3EB0A915BEF866D46BD980`: bảng lịch hạn 5 gói, kèm Phét xin nghỉ 26/11–1/12.
- 10:24–10:33: quy tắc cột giá. Phét trả lời trong chat riêng: dùng cột giá vốn; 5% và 12% là vận chuyển tỉnh; giá 1 là trung ương, giá 2 là tỉnh. Đây là chỉ dẫn trong chat riêng, chưa phải quy tắc đã duyệt.
- 15:14: Dũng gửi 5 file ZIP (Mahosot, Settha, MeDek, SVNK, danh mục chung). Không thấy ZIP Mittaphab. Một ZIP bị cắt tên trên giao diện.
- 15:32 — `3EB01AF6E719058BE6DE13`: Dũng gửi link Drive. Phét ghi nhận lúc 15:34; không có bằng chứng ai đã dùng.
- 17:00–17:06: Linh gửi Sharma. Phét trả lời "Chị up rồi", sau đó nhờ kiểm tra lại. Không có tin nào cho thấy đã kiểm xong.

**30/10**
- 08:02 — `3EB0B384E12E312624D381`: Trang gửi Stevimed (F05).
- 08:16 — `3EB0CBFE7CE3AF62C6B261`: Sếp họp "rà soát báo giá thầu BV 150 để ms Phet làm". Khớp với nhận định BV150 = Mittaphab và Phét là owner.
- 09:13 — `3EB088C10765BFD7C8C2CC`: "giá trong sheet giá 2027 là giá mình đưa vào báo thầu năm 2026". Cũng lúc 09:13, `3EB0BFC8D9E35B6932F750`: gửi file Kom (F02).
- 09:15 — `3EB0F48F803EAD3A6A6264`: giao Dũng rà hàng chưa có giá trước họp thứ Hai.
- 09:18 — `3EB02667E93477F013B336`: Oanh gửi BGC.
- 09:22 — `3EB0443DA0D4D9D22B7574`: Sếp trả lời "thứ 2 trình bày cách làm này… tháng 11 chia nguồn lực". Đây là chỉ đạo, không phải phê duyệt.
- 10:23 — `3EB01D10495CECB4448236`: Sơn báo thêm 50 hàng Jundamed.

**Không có trong chat:** tin phê duyệt giá, NCC, danh mục hay cam kết; tin nộp thầu; xác nhận F02 đã được dùng.

### Kế hoạch R10

`OWNER\sources\plans\plan-source-text.txt` (FRESH-READ bởi worker): kế hoạch nộp dữ liệu cho **App Trợ lý Cung ứng**, không phải kế hoạch thầu. Mọi mục F1–F5 đều "Chưa"; đã nộp 0/5. Trong kế hoạch, Phét chỉ có việc T2 ngày 02/11.

### 22 file gốc

`OWNER\sources\inventory.json` và `source-files.json` liệt kê F01–F05, I01–I09, I11–I18 (I10 đã loại).
- **Chưa xác minh được** bộ HSMT, bìa chính thức hay addenda trong phần nội dung đã đọc. Inventory/tên file không chứng minh nội dung của các ảnh chưa đọc hoặc 424 ảnh nhúng.
- Worker xem 4 ảnh JPEG:
  - **I17:** cột O và Q được khoanh; có `#DIV/0!` ở cột P.
  - **I13:** S-cottonoid 1.5x3.0, 2.5x5, 2x4, đơn vị Pack, số lượng 100.
  - **I14:** bảng thuốc; cột M "Giá vốn" 5%, N "Lãi NNC" 28%.
  - **I12:** ảnh mẫu, không có nhãn đọc được, không đủ để xác định danh tính.
  - Không OCR chữ Lào nhỏ.

### Workbook (theo `QUALITY-SOURCE-FACTS.json`)

**F01 BGC** (`e8d755a2…`, 10 sheet; structured extraction này chọn 8 sheet liên quan):
- Sheet `Trung thau 2026`:
  - A1 tự ghi "DANH MỤC NNC TRÚNG THẦU 2026 (đọc từ bản scan quyết định/hợp đồng…)". Header nằm ở A3:K3.
  - 189 dòng trúng, 149 mã MPSC: Mahosod 65, Settha 87, Meladek 37; Thuốc 54, VTTH 122, Hóa chất 13.
  - Bản scan gốc chưa được đọc lại.
- `Huong dan!C25`: giá mua cũ lấy từ bảng Mittaphap 2027, **chưa xác nhận còn hiệu lực, phải hỏi lại NCC**. Các cột 2026 chỉ để gợi ý nơi hỏi giá.
- Các sheet BV có ô G4 và H4 tra `Bang goc` bằng `MATCH` theo cột B (mã). Công thức không chứng minh giá trị đã được tính lại.

**F05 Stevimed** (`ce67f4f5…`):
- `Price!A1` ghi "anh Nam gửi yêu cầu ngày 24/10/2026".
- E3 = SK.12.01-24, F3 version 1, G3 ghi lệch quy cách.
- E4 = MP.25.01-02, G4 ghi màng 37x37 trong khi yêu cầu là 40x42.
- **Không có giá số.** Đây là phản hồi kỹ thuật.

**F02 Kom** (`1b12de81…`, 6 sheet, gồm một sheet roster quân đội đã loại vì chứa liên hệ cá nhân):
- Ô I8 của hai sheet mẫu ghi ngày ký 13/11/2026. Đây là ngày trên mẫu thư, **không phải giờ đóng thầu**.
- Ảnh nhúng trong workbook chưa được OCR.

## Owner project

- **Authority graph:** `OWNER\requirements\00-README-AUTHORITY.md`, `01-PRD-CORE.md`, `08-SOURCE-MAP.md`, `10-LOCK-REGISTER.md`, `11-ROLE-AUTHORITY-MAP.md`, `DECISIONS.md`.
  - Claude soạn hoặc đọc ở các lượt 30–31/10.
  - Nội dung hiện hành của `10-LOCK-REGISTER.md` được thấy ngày 01/11: không có node nào LOCKED.
- **P1 và formation:** `OWNER\requirements\P1-REQUEST.md`; `OWNER\context\mission\BIDOPS-F01.formation.json` (giai đoạn RESEARCH, cũng soạn ở các lượt trước).
- **Trạng thái:** `OWNER\context\PROJECT_STATE.md` — FRESH-READ 01/11.
- **Bằng chứng gốc:** `OWNER\sources\` gồm 22 file trong inventory: 4 JPEG đã xem, 3 workbook có structured extraction có giới hạn; các phần còn lại giữ INDEX/chưa xác minh. Chronology 168 tin và kế hoạch R10 đã được đọc theo phạm vi ghi ở trên.

## Code và receipt của B

| Thành phần | Đường dẫn | Bằng chứng |
| --- | --- | --- |
| Workpack inbox | `OUT\bidops-B-pilot-20261031\project\src\workpacks.py` | `1c8e6192bc324b3f5e42d79ac83f2308f0965eef569ca6942aa9875b96c951d4`. FRESH-READ, có `sha256sum` 01/11 |
| Test workpacks | `OUT\bidops-B-pilot-20261031\project\tests\test_workpacks.py` | `cdcea9aa088d1c09bd6e40b2115731ccb8917acddf7c6d3dfd6ac3446a45de45`. FRESH-READ; SHA được assert trong smoke |
| Bộ test đầy đủ | `OUT\bidops-B-pilot-20261031\project\tests\` | 100 hàm `def test_` trong 8 file (đếm bằng grep). Lượt chạy 100/100 là CODEX-RECEIPT: `OUT\bidops-B-pilot-20261031\control\continuation-20261031\POSTPATCH-VERIFICATION.json` |
| Tái hiện trước khi vá | `…\control\continuation-20261031\PREPATCH-REPRO.json` | Chạy trên code `dc32dd61…`. CODEX-RECEIPT |
| Commit local | `…\control\continuation-20261031\POSTPATCH-LOCAL-COMMIT.json` | `aac3e9428084254ae21fba4eaf0ee7b85a014b70`, không có remote |
| Smoke của Claude | `OUT\bidops-relock-20261101\project\tests\test_relock_smoke.py` → `OUT\bidops-relock-20261101\project\sandbox\SMOKE-RESULT.json` | Ran 1 test, OK (01/11). Gọi `main(argv)` trong process, không phải CLI chạy ở process riêng |
| Ghim kỹ thuật | `OUT\bidops-relock-20261101\RELOCK.json` | Không phải khóa nghiệp vụ |
| Dữ liệu thật | ngoài Git, dưới `OUT\bidops-B-pilot-20261031\` (`catalog\`, `workpacks\`) | CODEX-RECEIPT: `common-catalog.sqlite` `e825a777…`, Kom DB `8ce69bd4…`, `draft-inbox.sqlite` `8f4fc701…`, XLSX `c4076734…`; journal mode `delete`; 3.523 DRAFT / 0 review. Claude **chưa mở** catalog/inbox thật |
| Các con số 2.068 / 1.455 / 3.523 / 4.577 | Pilot `README.md` (FRESH-READ), `docs\DATA-CONTRACT.md` §17 (đọc 31/10) | Codex viết tài liệu này. Claude chưa đối chiếu với catalog |
| 649 / 798 / 8 của Kom | `KOM-INTAKE-SUMMARY.json` `4bd04710…` (nhận 31/10) | Trường `legacy_price_states.priced` = 649. Nghĩa "giá đã chào năm 2026": tin Phét 30/10 09:13, mã `3EB088C10765BFD7C8C2CC` |

## Mốc thời gian nguồn

- **Discovery:** WhatsApp đọc tới 30/10 10:28, kiểm cuối 10:41 UTC+7. Bổ sung hai tin 30/10 16:09 (Sơn) và 16:37 (Tình).
- **Catalog production:** tạo 29/10 15:22, share link 15:32. Nguồn Sơn: bản 30/10 16:52.
- **Supply map v18:** cutoff 26/10. Kế hoạch và hướng dẫn 28/10 thay giả định cũ hơn.
- **Ngày 31/10:** không có tin nghiệp vụ nào trong tập đã thu. Không suy ra công ty không làm việc hôm đó.

## Nguồn còn thiếu

- HSMT/addenda chính thức của cả 5 case.
- PDF MOF (lỗi 503).
- Visa gia hạn hiện hành.
- Quote hiện hành đã chấp nhận (con số 0 chỉ là của pilot; không suy ra toàn công ty không có quote).
- Tồn kho, lô, giao hàng, thanh toán, vốn.
- Danh tính/ACL nhân viên.
- Phạm vi App Trợ lý Cung ứng.
- Artifact lab L3 (chưa kiểm lại trong audit này).
