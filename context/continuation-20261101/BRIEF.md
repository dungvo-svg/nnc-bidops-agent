# BidOps: bản tóm tắt để phiên mới làm tiếp (01/11/2026, đã lưu trong project)

> Bản audit/plan đã được Codex đối chiếu độc lập và lưu vào project ngày 01/11/2026. Claude Opus tổng hợp, Sonnet kiểm hai nhánh. Các nhãn draft/đề xuất trong nội dung là trạng thái quyết định, không có nghĩa file còn ở ngoài project. Chưa thay runtime, tích hợp code, merge hay deploy. Chi tiết nguồn/giới hạn: SOURCES-READ.json và PUBLICATION-RECEIPT.json.


Claude Opus soạn và tổng hợp; hai Sonnet kiểm nguồn/phạm vi; Codex đã đối chiếu độc lập và lưu bộ tài liệu này trong project owner ngày 01/11/2026. Đây là continuity và đề xuất đã review, chưa phải khóa nghiệp vụ hay code tích hợp. Chỉ nói về BidOps, không gộp Kho/PMA.

## Mission

**Mục tiêu.** BidOps là node của CEO, phục vụ nhiều nhánh kinh doanh; thầu bệnh viện là mũi nhọn.
- CEO **trực tiếp** chào hàng và điều phối nhiều nhánh, kể cả khi có nhân viên.
- Mỗi node gồm: người + Agent của chính người đó + phần việc nằm trong năng lực, quyền và quan hệ thật của họ.
- Mỗi người tự giữ máy và Agent của mình. CEO trao đổi mission và nhận kết quả, không điều khiển máy hay Agent của người khác.

**Đích sản phẩm** (A8 §1–2): cùng một case giữ trọn chuỗi hàng–chứng từ–tiền.
- **Năm phép kiểm nghiệp vụ, tách riêng nhau:** đáp ứng hồ sơ, khả năng cung ứng, kinh tế/vốn, căn cứ cạnh tranh, kết quả thực hiện. Không gộp thành một điểm sẵn sàng hay xác suất thắng.
- **Các phạm vi phê duyệt** là một trục khác: tương đương kỹ thuật, giá, cam kết NCC, danh mục, ghi master/nộp.
- **Ba trục bằng chứng** hàng–chứng từ–tiền (`ledger.qualify`) lại là một trục thứ ba.

## Không làm lúc này

- Không thu hẹp thành trợ lý thầu riêng của Dũng.
- Không xây master thứ hai, broker, web hay VM.
- Không gửi chào hàng, nộp thầu hay ghi master.
- Không tiếp quản gói Mittaphab.

Vòng hiện tại chỉ làm audit và tài liệu, không build tính năng.

## Vai thực thi (theo chỉ dẫn Dũng, U-30A)

- **Opus** (phiên chính): giữ quyết định và đề bài.
- **Sonnet:** kiểm song song; ở vòng sau, khi đã chốt phạm vi, có thể được giao cài đặt.
- **Codex:** bên thực thi ngang hàng và người review độc lập.

## Tài nguyên

| Thứ | Ở đâu | Trạng thái |
| --- | --- | --- |
| Discovery, authority graph, P1 | `D:\WORK\Agent\Agent-first\NNC BidOps Agent` | Tại 01/11: `git rev-parse HEAD` báo fatal (chưa có commit), toàn bộ file untracked; không node nào LOCKED |
| Phương án A | `…\context\continuation-20261101\sources\PLAN-A-v8.md`, `PLAN-A-LITE-v1.md` | Snapshot 31/10, không phải trạng thái mọi gói hôm nay |
| Code B synthetic | `C:\Users\Admin\Documents\Codex\2026-10-31\task\output\bidops-B-pilot-20261031\project` | Commit local `aac3e9428084…`, không có remote, **chưa tích hợp vào owner** |
| Ghim kỹ thuật | `C:\Users\Admin\Documents\Codex\2026-10-31\task\output\bidops-relock-20261101\RELOCK.json` | Chỉ ghim kỹ thuật, không phải khóa nghiệp vụ |

## Quyền nghiệp vụ và repo

- Mọi node D/LCK ở owner đều **chưa LOCKED**.
- Dũng đã cho phép B synthetic chạy local (AUTH-20261031-LOCAL-B).
- **Repo công ty, tách hai loại bằng chứng:**
  1. *Lịch sử:* một lần thử tạo private `nnc-lao/nnc-bidops` bị từ chối vì thiếu CreateRepository.
  2. *Chẩn đoán auth hiện tại:* `gh` chỉ lưu tài khoản `VOSYDUNG`. Đọc membership trong org trả 404 và yêu cầu scope `admin:org`.
  - Kết quả này **không** chứng minh Dũng không phải thành viên, cũng không chứng minh có quyền tạo repo. Không kết luận nguyên nhân chỉ là thiếu lời mời.
  - Không dùng repo cá nhân hay public thay thế.
- **Chưa cấp:** ghi master, chấp nhận quote, liên hệ, nộp, ACL, VM.

## Trạng thái một dòng

**Đã có (L1 local):**
- Pilot có 3.523 source intake (2.068 bốn BV + 1.455 Kom) và 4.577 nghĩa vụ theo case. Đây **không phải** số biến thể duy nhất.
- 3.523 DRAFT, 0 review. Theo receipt Codex ngày 31/10; Claude chưa mở catalog.
- 100/100 test, theo receipt Codex.
- Smoke 1/1 do Claude chạy.

**Chưa có:**
- Người hoặc Agent thật.
- Variant có danh tính đầy đủ: 0. Quote được chấp nhận trong pilot: 0. Hai con số này chỉ là của pilot, không suy ra toàn công ty không có quote.
- HSMT chính thức. Trong phạm vi nội dung đã đọc, chưa xác minh được bộ HSMT/bìa/addenda chính thức; các ảnh chưa đọc và ảnh nhúng không được dùng để kết luận có hay không có tài liệu đó. Ba workbook Mahosot Phét gửi lúc 29/10 09:48 cũng không có trong 22 file đó. Đây là thiếu trong phạm vi project, không có nghĩa công ty không có.
- Dữ liệu hàng–chứng từ–tiền.
- Chat 28–30/10 không có tin nào phê duyệt giá/NCC/danh mục hay nộp thầu (đọc đủ 168 tin, 01/11).

**Khoảng trống ở mức code** (Sonnet đọc thân hàm; Opus kiểm tại chỗ `ledger.py` 534–591 và 703–761). Chi tiết: `PLAN-VS-IMPLEMENTATION.md`.
- Actor và reviewer chỉ là nhãn tự khai trên máy local, chưa phải principal đã xác thực. Đây là ranh giới kỹ thuật trước production, không phải policy công ty. Tách người theo từng phạm vi phải dựa trên thẩm quyền thật, không tự tạo thêm người duyệt.
- Ba trục hàng–chứng từ–tiền mới chỉ kiểm "có ref hay không".
- `certificate_check` và `portfolio_check` là hàm thuần, chưa nối vào ledger.
- WIP1 chỉ chặn ở bước accept, không chặn ở bước receive.
- `link_demand` nhận `fulfillment` mà không đòi case `won`.
- Ledger và `catalog_lifecycle` là hai nơi giữ trạng thái case, chưa nối với nhau. Quy tắc deadline lệch nhau.
- Năm phép kiểm nghiệp vụ chưa thành đối tượng riêng.
- Test chỉ là L1, chưa chạy với người dùng thật.

**Sự thật nguồn bổ sung 01/11** (`context/continuation-20261101/sources/QUALITY-SOURCE-FACTS.json`, Codex trích read-only):
- BGC F01, sheet `Trung thau 2026`:
  - Tự ghi là danh mục NNC trúng thầu 2026, lấy từ scan quyết định/hợp đồng.
  - 189 dòng trúng, 149 mã MPSC (Mahosod 65, Settha 87, Meladek 37).
  - Đây là bằng chứng lịch sử cho căn cứ cạnh tranh. Bản scan gốc chưa được đọc lại. Không coi là quote hiện hành.
- Các sheet BV trong BGC tra `Bang goc` bằng `MATCH` theo **mã ở cột B (MPSC)**. Workbook đang dùng tự ghép theo mã, nên biến thể khác quy cách cùng một MPSC có thể bị gộp. Đây là thêm một lý do để đề xuất thay D11.

**Đọc tiếp** (các file hiện có cùng thư mục): `SOURCE-MAP.md` → `DECISION-LOG.md` → `PLAN-VS-IMPLEMENTATION.md` → `ROADMAP-STATUS.md`.
