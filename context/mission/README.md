# Mission và cách làm tự chủ — NNC BidOps Agent

Thiết lập 30/10/2026 theo chỉ dẫn của Dũng. Phương pháp vận hành kế thừa từ [nnc-claude-plugins](https://github.com/VOSYDUNG/nnc-claude-plugins) **main `94ddf8b`** (plugin `nnc` 5.1.0-alpha.2: `ai-oser` R2, `mission-formation`, `adaptive-delivery`) — đúng phần "NNC OSER" mà SOP P1/P2 trang 7 chỉ định dùng lại ("Formation làm rõ công việc, phương án và quyết định. Delivery chọn cách triển khai theo loại đầu ra"). Không dùng skill cục bộ NNC-AI-OSer v1 hay OSER v4 (xem mục Audit).

**Trạng thái:** plugin ghim tại `.claude/vendor/nnc-oser-94ddf8b/` (marketplace cục bộ `nnc-bidops-local`; chỉ kế thừa, không gửi ngược về repo). Formation [BIDOPS-F01](BIDOPS-F01.formation.json) ở REALITY_AUDIT, `formation-check` hợp lệ. Mission [nháp](BIDOPS-M01.contract.draft.json) **chưa duyệt; `oser init` chưa chạy.**

Chạy kernel trực tiếp: `python -I .claude/vendor/nnc-oser-94ddf8b/nnc/oser/oser.py <lệnh> --project .`. Lên bản phương pháp mới: thay thư mục vendor bằng commit mới, ghi commit vào tên thư mục.

## Hai nguồn phương pháp

| Nguồn | Trả lời | Ở đâu |
| --- | --- | --- |
| SOP P1/P2 của Dũng (v1 26/10/2026) | Sản phẩm **làm gì, đến đâu là đạt**: P1 yêu cầu → P2 xây/thử/bàn giao | `sources/method/SOP-P1-P2-VA-CA-KHO-2-v1.pdf` (không có trong repo plugin) |
| OSER R2 | Agent **vận hành thế nào**: Formation → Mission khóa authority + mẫu số nghiệm thu, Decision Contract, Clean Desk, checkpoint | plugin vendor; `.nnc-oser/` sau init |

## Cách làm hiện hành từ 02/11/2026

Mục này áp dụng cho công việc đang chạy. Nó không thay hai nguồn phương pháp ở trên: OSER R2 vẫn là phần kế thừa, SOP P1/P2 vẫn là nguồn riêng. `LCK-METHOD` vẫn **PROPOSED**; không D*/LCK nào được đổi thành LOCKED. Chỉ dẫn mới nhất, rõ ràng của Dũng mới được đổi hướng; snapshot cũ không phủ quyết chỉ đạo mới.

**Nguồn:**
- **[T]** Dũng gõ trực tiếp trong phiên cha `a5ab430d` ngày 02/11: "Tôi giao Foundry/Shin phối hợp điều hành BidOps trong phạm vi đã chốt. Claude tự phân việc và thực thi; chỉ hỏi tôi khi đổi định hướng, thiếu quyết định nghiệp vụ hoặc gặp quyền chưa được cấp. Làm Data và Phương án trước, Họp sau khi đủ ngữ cảnh."
- **[R]** Lời Dũng do phiên điều phối (root) chuyển lại. Phiên cha chưa đọc được nguyên văn ở nguồn gốc. Gồm: bác view họp HTML ("xây cái gì vậy… tôi đã reject rồi"; "bật qua 1 host nữa thì chậm"; "quá nhiều chữ"), "ủa sao không làm cho xong đi", "phần họp nó đâu liên quan đến 2 phần kìa / nó là làm sau mà", "Ghi nhớ cho dự án luôn", "phương pháp chúng ta áp dụng cho dự án này đâu".
- **[L7]** Lite v7, sha256 `6f7a2442…956f`, §1–2, §11–12.

**Quy tắc:**
1. **Vai** [T][L7 §11]: Dũng và Shin giữ mục tiêu, phạm vi và các chốt. Phiên Claude cha giữ context, tự chia việc, điều phối, review độc lập rồi tích hợp. Nhánh là phiên Claude Desktop con chạy theo charter trong `context/branches/`. Mỗi artifact chỉ có một writer.
2. **Thứ tự** [T][R]: DATA và PHƯƠNG ÁN A chạy trước, song song. HỌP làm **sau**, khi nguồn và độ sẵn sàng đã đủ, và **không bao giờ chặn** hai phần đầu. Hiện HỌP **đóng băng**: không sửa, không thiết kế thêm, `outputs/hop/v1/` giữ làm lịch sử.
3. **Chỗ chưa rõ** [R]: tìm nguồn hiện hành → cùng thảo luận trước/sau kèm insight của Agent → phương án A/B và đề xuất. Chỉ hỏi Dũng khi có xung đột hoặc quyết định nghiệp vụ không tự giải được, và phải kèm lựa chọn đã nghiên cứu.
4. **Khóa từng chặng** [R]: theo authority và bằng chứng của `requirements/00-README-AUTHORITY.md`. Kết quả mỗi chặng ghi bền và chặng sau kế thừa. Không mở lại điều đã chốt. Không dừng ở việc giao task hay viết báo cáo: làm tới đầu ra dùng được, phần bị chặn thì nêu blocker chính xác và vẫn làm tiếp các phần độc lập.
5. **Phạm vi** [L7 §1–2][R]: năng lực toàn Company/CEO là tổng thể, thầu BV là ca hiện tại, không SPM. 19 người là bản đồ toàn Company, không phải ai cũng tham gia pilot. Mỗi cặp người–agent chỉ tính khi có quyền, kỹ năng, dữ liệu và cách liên lạc thật.
6. **Pilot hiện tại** [L7 §1]: nguồn hàng, phối hợp đưa hàng về, cơ sở giá hợp lý. Phần hậu kỳ vẫn thuộc tổng thể nhưng triển khai ở pha sau.
7. **Cách thảo luận** [R]: chưng cất trước/sau, không gắn AI vào kiểm tra quy trình cũ. Giao mục tiêu đủ lớn để Claude tự chia việc.
8. **Nơi làm và thứ để xem** [R]: làm ngay trong phiên Claude, dùng một nguồn dữ liệu hiện hành. Thứ để người xem là file dẫn xuất nằm trong project, không host hay UI ngoài. Excel đọc được cho toàn bộ dữ liệu là đầu ra nghiệp vụ của DATA, không phải dự án UI của HỌP. `outputs/ban-lam-viec/` chỉ là bảng nhìn nhanh cạnh session, không phải sản phẩm và không phải điều kiện hoàn thành.

**Lệch đã xảy ra (sai → sửa → bằng chứng):**

| Sai | Sửa | Bằng chứng |
| --- | --- | --- |
| Phiên cha tạo nhánh HỌP sau DATA v2 và giao dựng view HTML riêng. Nhánh có bật máy chủ cục bộ để kiểm render | Dũng bác [R]. HỌP đã dừng và đóng băng; view thay bằng file dẫn xuất cạnh session | `outputs/hop/v1/` (lịch sử); `context/branches/README.md`; việc tắt máy chủ là do nhánh tự báo, phiên cha chưa kiểm độc lập |
| Charter DATA đặt quy ước "dung dịch lọc máu → Hóa chất" không có nguồn | Chuyển thành khuyến nghị có nguồn (Thuốc, theo catalog chung), vẫn là đề xuất | `outputs/ban-lam-viec/BAN-LAM-VIEC.md` revision 3 |
| Phiên cha trả status rồi dừng | Giao DATA v4 và PHƯƠNG ÁN v3 tới đầu ra hoàn tất | `context/branches/README.md` |
| `CLAUDE.md` còn ghi "RESEARCH chờ Dũng cho chạy" và "subagent… không chạy nền" | **Chưa sửa** vì `CLAUDE.md` là file chỉ dẫn, cần Dũng đồng ý. Mục này ghi lại thực tế đã áp theo [T] | — |

### Cowork với phiên điều phối Shin/root (từ 03/11/2026)

**Nguồn:**
- **[T2]** Dũng gõ trực tiếp trong phiên cha ngày 03/11: "cowokring đi nhé → đó là đồng nghiệp của chúng ta trong quá trình xúc tiến dự án".
- **[R2]** Lời Dũng do điều phối chuyển nguyên văn: "giờ bạn và Phiên đó thiết lập cowork với nhau trong dự án này đi để việc chờ như vậy k diễn ra nữa và bạn gửi tin nó cũng biết".

Quy ước này là cách cộng tác. Nó không phải duyệt nghiệp vụ, giá hay production, và không gỡ hold nào khác.

**Vai:**
- **Shin/root (phiên điều phối, có Codex hỗ trợ)** chuyển các yêu cầu Dũng đã ủy quyền. Shin là **người vận chuyển**, không phải user và không phải người có thẩm quyền nghiệp vụ.
- **Phiên cha** nhận việc, tự chia việc và giao nhánh trong phạm vi.
- **Mỗi artifact một writer.** Phiên cha giữ tài liệu dự án. Nhánh giữ đúng artifact được giao.

**Một yêu cầu từ Shin nên có:**
- nguyên văn hoặc nguồn lời Dũng (message ID nếu có);
- requestID hoặc messageID;
- phạm vi; thay đổi hoặc lệnh dừng;
- đầu ra mong đợi.

Thiếu phần nào thì phiên cha vẫn làm phần rõ, rồi hỏi lại đúng phần thiếu.

**Phiên cha trả lời bằng một trong bốn trạng thái, kèm bằng chứng thật:**

| Trạng thái | Phải có |
| --- | --- |
| ĐÃ NHẬN | Nguồn đã đọc (hash); ai làm, ở đâu |
| ĐANG LÀM | Owner, bước hiện tại, artifact hoặc dispatch ID thật. Việc dài thì checkpoint theo mốc, không im lặng tới cuối |
| CẦN QUYẾT ĐỊNH / QUYỀN | Hành động, đích, lý do chính xác; trạng thái đã làm / bị từ chối / đang chờ / chưa rõ. Phần không bị chặn vẫn làm tiếp |
| XONG | Path, hash, readback/QA, phần còn mở và owner |

Không gọi "đã xếp hàng" là xong. Kết quả ghi bền trong dự án: receipt của nhánh, `context/branches/README.md`, `outputs/…`.

**Chống lặp và giao không chắc:**
- requestID trùng thì không làm lần hai.
- Gửi không rõ đã tới chưa thì đọc kết quả hoặc trạng thái phiên trước, rồi mới gửi lại.
- Danh tính đã thiết lập thì dùng lại; không xác minh lặp khi không có bằng chứng thay đổi:
  - phiên cha: Desktop `local_5e4b81c7-343c-47f7-a688-fe41f2921bfa`, Code `a5ab430d-1ab4-4c21-8a6a-2b597076de9f`, cwd dự án;
  - nhánh: xem `context/branches/README.md`.
- Tên ngắn của phiên gửi (`nnc-bidops-agent-*`) có thể đổi. Không đoán theo tiêu đề, không lưu pipe endpoint như credential.

**Thứ tự ưu tiên:**
1. Lệnh dừng, thu hồi hoặc thay đổi mới của Dũng, kể cả khi Dũng chỉ bấm từ chối một thao tác.
2. Chính sách của phiên nhận (quy tắc dự án, quyền).
3. Yêu cầu Shin chuyển.

Lệnh mới chỉ áp đúng phạm vi của nó. Khi chính sách cần Dũng xác nhận trực tiếp tại phiên nhận (đổi định hướng lớn, quyền chưa cấp, từ chối vừa xảy ra), phiên cha nói rõ yêu cầu đó và nguồn chính sách. Không tự vượt qua, không hạ chế độ quyền.

**Giới hạn thật (03/11):**
- Tin giữa các phiên chỉ vào hộp thư. Không đánh thức được phiên đang nghỉ hoặc đã tắt.
- Phiên gửi đã đóng thì không nhận được trả lời (đã gặp `No agent … reachable`, `ENOINBOX`). Khi đó kết quả nằm trong file dự án và Shin đọc lại từ file.
- Tin vào nhánh Desktop chỉ báo "delivered", không có ACK ngược; ACK chữ đến khi nhánh tự gửi.
- Quy ước này không thêm daemon, host, runtime mạng, thay đổi settings, quyền, ACL hay credential. Không thay thẩm quyền của CEO Quân hay chủ node nghiệp vụ.

**Phía Shin:**
- Giữ cửa sổ nhận tới khi có ACK hoặc checkpoint, sau đó theo receipt và artifact.
- Không gửi status liên tục. Không gửi lại một mục tiêu khi chưa rõ kết quả lần trước.

### Nền dự án và hai lớp (D15)

**Ghi chú thuật ngữ (02/11):**
- **Chỉ đạo:** Dũng chốt bỏ thuật ngữ "Foundry" khỏi BidOps. Chỉ đổi tên gọi, không đổi chức năng hay phương pháp.
- **Nguồn:** chuyển lại qua root, `Sentinel_cbf195f812b08191bb6155db3ccbab4c` — "Không đưa Foundry cá nhân của tôi nhé"; `Sentinel_7dceb5672c60819183eb6d409a6aa73d` — "Ở Bidops cũng gỡ thuật ngữ này đi". Chưa có giờ gốc.
- **Tên mới:**
  - Vị trí vận hành dự án → **điều hành BidOps/CEO**.
  - Phương pháp vận hành agent → **phương pháp làm việc của agent**.
  - Nền tảng cá nhân của Dũng không thuộc BidOps.
- **Giữ nguyên chữ "Foundry/Foudry"** ở những chỗ sau, để không hỏng evidence:
  - trích dẫn nguyên văn (chỉ đạo 02/11, lời chuyển lại về hai lớp);
  - đường dẫn `D:\DUNG\Foudry\…`;
  - locator phiên `foudry-*`;
  - hồ sơ bất biến (protocol `463a688c…`, receipt, bản v1–v3 cũ).
  Khi gặp "Foundry" trong các chỗ đó, hiểu là "điều hành BidOps/CEO".

**CONFIRMED_USER_DIRECTION** — Dũng xác nhận trực tiếp 02/11 ghi vào hồ sơ (lời gốc chuyển lại qua `SRC-RELAY-DUNG-0211`):
- "layer Foundry của chúng ta: phương pháp Claude plugin R2 alpha, R1 tự chủ OSER, tài liệu dự án và bản thể thống nhất → cũng có nhưng tầng lớp khác".
- "triển khai xong mỗi người cũng có … ở chính mình".
- "được triển khai ngay sau khi chúng ta thiết lập được".

Nền của toàn dự án là: node tự chủ đang thiết kế, R2 alpha, R1 tự chủ OSER, toàn bộ tài liệu và bản thể thống nhất. DATA, Phương án A và HỌP chỉ là cách tổ chức thực thi bên dưới nền đó.

| Lớp | Ai | Gồm | Trạng thái kiểm thật (runtime verified) |
| --- | --- | --- | --- |
| **Điều hành BidOps/CEO** | Dũng + Shin, cùng Claude cha `a5ab430d` tại thư mục này | R2/R1 để phát triển và điều phối BidOps; tài liệu dự án; bản thể thống nhất | Plugin ghim ở `.claude/vendor/nnc-oser-94ddf8b/` (`plugin.json` 5.1.0-alpha.2). **Chưa `oser init`** (không có `.nnc-oser/`; D09). Nhánh Desktop đang chạy. Nhắn tin giữa các phiên trên máy Dũng đã chạy. Drive đọc được bằng tài khoản Dũng |
| **Node** người–agent (CEO, Sơn, Phet, Linh, Hoa…) | từng người, trên máy và Agent của chính họ | R2/R1, tài liệu và bản thể **tại chính mình**, trong vai, dữ liệu và quyền riêng | Chỉ node Dũng có bằng chứng. Các node khác: **chưa có bằng chứng thiết lập**; blocker riêng từng node là chưa có endpoint/agent xác minh |

**Quy tắc lớp và kích hoạt** (`LCK-LAYERS`: chỉ đạo đã xác nhận, ghi hồ sơ 02/11; không phải runtime lock, chưa `oser init`):
- Cùng phương pháp **không** có nghĩa cùng owner hay cùng phạm vi.
- Lớp điều hành BidOps đã cài không chứng minh node nhân viên đã cài.
- CEO không ra lệnh trực tiếp cho agent của nhân viên; hai bên trao đổi việc và kết quả.
- Node nào thiết lập đủ thì **làm thật ngay** trong quyền hiện có, không đợi cả mạng; vừa làm vừa cải tiến.
- Blocker chỉ áp cho đúng node đang gặp nó. Không ghi READY khi chưa có bằng chứng. Không trì hoãn vô thời hạn.
- R2 Decision Card, test PASS hay MISSION_READY chưa phải là duyệt. `oser init` là khóa Mission bền, cần người có thẩm quyền xác nhận sau khi hiểu hệ quả. Sau khi đã chạy thật, muốn đổi hành vi thì dùng Delta Mission; đổi phạm vi, quyền hay chi phí thì phải chốt lại.

**Bản đồ tài liệu nền** (đọc trước khi ghi rộng):

| Tài liệu | Vai | Hiện hành / thay thế |
| --- | --- | --- |
| `CLAUDE.md`, `AGENTS.md` | chỉ dẫn dự án | hiện hành; hai câu cũ chờ Dũng (xem D14) |
| `requirements/00-README-AUTHORITY.md`, `DECISIONS.md`, `08`, `10`, `11` | authority graph, quyết định, nguồn, khóa, người–quyền | hiện hành. `11` (30/10) hẹp hơn A8/Lite v7 về vai, chưa sửa |
| `requirements/01-PRD-CORE.md`, `P1-REQUEST.md`, `P2-VALIDATION.md`, `BACKLOG-ACCEPTANCE.md` | bản nháp sản phẩm 30/10 | đang là bản nháp, hẹp hơn A8 (CEO đa nhánh, ba chế độ); chưa cập nhật |
| `context/mission/` (mục này, F01, M01 nháp) | phương pháp; Formation; Mission | mục này hiện hành. F01 ghi REALITY_AUDIT là đã cũ (thực tế đã làm research/thực thi); M01 chưa duyệt |
| `context/continuation-20261101/sources/PLAN-A-v8.md` — **A8 toàn văn** "A/P1: CEO toàn diện, mũi nhọn thầu BV và mạng người–agent", cập nhật 31/10 18:26, 98.525 byte, sha256 `7caf1d00…617f` | nền tổng thể: CEO + BidOps và node nhân viên hai tầng; CEO luôn cùng làm, ba chế độ, đại diện; node = người thật + agent + việc + quyền + hiện diện; agent của người giữ dữ liệu tự nhận, xử lý, trả, không bắt người làm trung gian; hàng–chứng từ–tiền; bus/onboarding §10 | **hiện hành về nguyên tắc** (Lite v7 là lát cắt, không thay A8). Số đếm và trạng thái 28–31/10 là lịch sử. Chưa xác minh byte trùng bản A8 trên Library (`BIDOPS-A-P1-CEO-HUMAN-NODES-20261031.md`). Phiên cha đọc trực tiếp dòng 1–45 và 501–555 ngày 02/11; Codex đọc dòng 24–153 và 300–499 (`continuation-20261101/SOURCE-MAP.md`); các dòng còn lại mới khớp hash |
| `context/continuation-20261101/` (còn lại, kèm `sources/PLAN-A-LITE-v1.md` sha256 `7a3a13fe…`) | continuity 01/11 | lịch sử / nguồn kế thừa |
| `outputs/company-continuation-20261102/` | v4 workbook (baseline nội bộ), Lite v7 (hiện hành), brief v5, working list | Lite v5/v6 và dictionary v0–v3 là lịch sử |
| `context/branches/`, `outputs/data-branch/`, `outputs/phuong-an/` | cách tổ chức thực thi và đầu ra | hiện hành; `outputs/hop/v1` là lịch sử, HỌP đóng băng |
| `data-work/pilots/bidops-b-next-20261101/` | code synthetic L1 | bằng chứng kỹ thuật, chưa runtime thật |
| Ngoài dự án, root đã kiểm, **cha chưa đọc**: bản A8 trên Library (có thể trùng `PLAN-A-v8.md` ở trên, chưa xác minh), phương án nghiệp vụ + mạng agent v2 30/10, HUMAN-NODE-EVIDENCE / AGENT-BUS-RESEARCH 31/10, MA-TRAN / DOI-CHIEU 28–29/10, blueprint-restored 01/11 | nền tổng thể (A8 là tổng thể; Lite v7 là lát cắt) | kế thừa nguyên tắc; số đếm cũ là lịch sử. Chưa có bản sao trong dự án |

**Quyết định và khóa:**
- `D15` trong `requirements/DECISIONS.md`; `LCK-LAYERS` trong `requirements/10-LOCK-REGISTER.md`: CONFIRMED_USER_DIRECTION (ghi hồ sơ 02/11, không phải runtime lock). Nguồn bổ sung: `SRC-OSER-VENDOR`.
- `D14` trong `requirements/DECISIONS.md`, kèm bằng chứng, gate, lựa chọn bị thay và điều kiện mở lại.
- `LCK-EXECUTION` trong `requirements/10-LOCK-REGISTER.md`: CONFIRMED_USER_DIRECTION (ghi hồ sơ 02/11, không phải runtime lock).
- Chốt mới 02/11 (chuyển lại, **chưa ghi khóa**, chờ Dũng xác nhận trực tiếp nếu cần ghi hồ sơ): quyết định giá/tương đương/nguồn/điều kiện mua–vận chuyển thuộc đúng subnode có thẩm quyền; vị trí điều hành BidOps/CEO dành CEO Quân tiếp nhận/ủy quyền; test mạng lưới bằng `dung.vo` (CTY) ↔ `dungvs11102002` (HOME) thay pilot Sơn; Opus quyết thị giác, Sonnet làm (`context/branches/VISUAL-DIRECTION-DANH-MUC.md`). Đang áp dụng cho việc trong quyền hiện có.
- Nguồn trong `requirements/08-SOURCE-MAP.md`: `SRC-CHAT-DUNG-0211`, `SRC-RELAY-DUNG-0211`, `SRC-LITE-V7`.

**Chưa chứng minh:**
- nguyên văn gốc của các lời [R];
- vai cụ thể của Shin;
- proposal chung với phía Cung ứng. Bản chữ QT-CU-04 v2.8 nháp 26/10 đã tìm thấy, nhưng chưa có insight chung.

## Lộ trình Formation (thay cho "đợt/lô")

| Giai đoạn | Việc của BidOps | Sản phẩm | Trạng thái |
| --- | --- | --- | --- |
| INTAKE | Bài toán bằng lời nghiệp vụ | `problem` trong F01 | Xong (nháp) |
| REALITY_AUDIT | As-is, người/vai, công cụ, ràng buộc, baseline | F01 `current_reality`; `context/HOP-VA-DUNG-CHUNG.md` | **Đang làm** — chờ người đang làm xác nhận as-is |
| RESEARCH | Chọn 2–3 ứng viên ca đầu; so 3 cách làm (quy trình/Excel · cấu hình/Skill · công cụ) có nguồn; fixture tổng hợp cho ca P2-VALIDATION | F01 `research`; `data-work/fixtures/`; `outputs/BIDOPS-P1-001/v0/` | Chưa |
| DECISION | Decision Card D07 đủ 9 mục, có lối "thử trước"; gói họp chốt D01/D02 | `requirements/DECISION-CARD-D07.md`; `outputs/BIDOPS-HOP/<yyyy-mm-dd>-chot-p1/` | Chưa |
| MISSION_READY | Hướng đã chọn, unresolved giải/hoãn rõ, Mission draft có authority + AC | F01 `mission_draft` | Chưa |
| Lock | Dũng duyệt → `oser init` | `.nnc-oser/` | Chưa (D09) |

Phần nào độc lập thì làm song song; nguồn lệch thì treo đúng phần đó và làm tiếp phần khác.

## Tự chủ (R2: không đội hình cố định)

Phiên chính tự chọn làm trực tiếp, giao subagent, hay song song nhiều subagent khi không đụng cùng file. Không có bảng model theo vai, không wave/packet bắt buộc.

**Chính sách của Dũng (30/10/2026):** phiên chính Opus giữ quyết định, viết brief, ghi STATE; việc song song giao subagent **Sonnet**. Subagent trả ≤40 dòng + đường dẫn; phiên chính không tự đọc file dài.

Subagent định nghĩa sẵn trong `.claude/agents/` (vì mang luật riêng của dự án): `nghien-cuu` (đối chiếu bằng chứng, chỉ đọc), `kiem-luat` (soi guardrail, chỉ đọc), `thu-ky-hop` (gói họp, không tự ghi quyết định). Việc soạn/kiểm khác: subagent chung, brief nêu file được ghi, thứ không được đụng, tiêu chí nhận; người kiểm khác người soạn.

## Mức quyết định (Decision Contract R2)

- **D0–D1** (phiên chính tự quyết): chia việc, giao ai, bố cục tài liệu/fixture, xử lý phát hiện của `kiem-luat`, treo phần nguồn lệch.
- **D2** (Decision Card): cách làm (D07 — chủ nghiệp vụ chọn).
- **D3** (chỉ người có quyền, không tự trả lời): danh mục/gói chào, tương đương kỹ thuật, giá, NCC, cam kết giao, master/quyền, người thử độc lập (D01–D06); gửi/upload/nộp thầu; push/remote GitHub (D08); duyệt/sửa Mission (D09).

**Gỡ kẹt:** subagent sai 2 lần → viết lại brief hoặc tự làm → vẫn kẹt: ghi mục chờ trong `PROJECT_STATE.md`, chuyển phần độc lập kế tiếp, gom câu hỏi báo một lần.

## Clean Desk

| Loại | File |
| --- | --- |
| CURRENT AUTHORITY | SOP P1/P2 gốc; `CLAUDE.md` / `AGENTS.md` (chỉ dẫn Dũng); luật graph `requirements/00-README-AUTHORITY.md`; node đã LOCKED trong `requirements/10-LOCK-REGISTER.md` (hiện chưa có) |
| CURRENT STATE | `context/PROJECT_STATE.md`; `requirements/DECISIONS.md`; `context/mission/BIDOPS-F01.formation.json` |
| WORKING DRAFT | node chưa khóa: `requirements/01-PRD-CORE.md`, `P1-REQUEST.md`, `08-SOURCE-MAP.md`, `11-ROLE-AUTHORITY-MAP.md`, `BACKLOG-ACCEPTANCE.md`, `P2-VALIDATION.md`; `discovery/`, `context/HOP-VA-DUNG-CHUNG.md`, contract nháp |
| EVIDENCE / ARTIFACT | `sources/` (chỉ đọc), `data-work/`, `outputs/` |
| HISTORY | `sources/history/v1..v3`, `discovery/research-snapshots/` |

Hệ tài liệu sản phẩm lock (authority graph, kế thừa mẫu Kho Bậc 1.5): file chủ từng node, điều kiện LOCKED, amendment và chính sách chống refactor ở [`requirements/00-README-AUTHORITY.md`](../../requirements/00-README-AUTHORITY.md). Formation/Mission dùng graph này: `research`/`decision` trong F01 trỏ ID node, không chép nội dung.

Phiên mới chỉ cần AUTHORITY + STATE. Chỉ phiên chính ghi STATE/DECISIONS. Draft không thành authority vì nằm gần authority.

## Đo chi phí

Chưa đo. Sau init dùng `oser usage`; thiếu nguồn ghi UNKNOWN, không quy ra % gói hay tiền.

## Audit nhiễu plugin cũ (30/10/2026)

Đã gỡ khỏi dự án: `cong-cu/doi-bac.py`, `.claude/BAC-DANG-DUNG.md`, `.claude/CO-CAU-NHAN-SU.md`, 4 subagent đội hình cố định, `context/GOAL-DOT-1.md` (mẫu GOAL/lô/sóng của NNC-AI-OSer v1), thuật ngữ quản đốc/R0–R3/ghế, ghim model theo vai, số quota "77%/56%/6,7×". Không bị nhiễm: `sources/` (chữ "packet" là gói discovery, "R02/R03/R10" là mã tham chiếu, "V4/R3" là ô Excel), `discovery/`, `requirements/P1-REQUEST.md`, `P2-VALIDATION.md`, `BACKLOG-ACCEPTANCE.md`.

## Khóa Mission (khi Dũng duyệt D09)

1. F01 đạt MISSION_READY.
2. Dũng duyệt goal + AC trong contract nháp; xoá `_status`, `_notes`.
3. `oser init --project . --contract <file>`; thêm một dòng trỏ `.nnc-oser/BOOTSTRAP.md` vào `CLAUDE.md`.
4. Checkpoint đầu: facts hiện có, next_action theo giai đoạn đang làm.
