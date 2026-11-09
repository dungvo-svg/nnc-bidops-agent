# Quyết định và câu hỏi còn mở (file chủ `D*`)

Luật graph: [`00-README-AUTHORITY.md`](00-README-AUTHORITY.md). Khóa ở [`10-LOCK-REGISTER.md`](10-LOCK-REGISTER.md); người giữ quyền ở [`11`](11-ROLE-AUTHORITY-MAP.md); nguồn ở [`08`](08-SOURCE-MAP.md).

Đã có chỉ dẫn của Dũng: dùng tên thư mục NNC BidOps Agent, setup để tiếp tục với Claude, thu hội tụ nguồn để định hình sản phẩm. 30/10/2026 (chat với Claude): áp phương pháp tự chủ từ nnc-claude-plugins; Opus giữ quyết định, Sonnet làm song song; kiểm GitHub org nhưng chưa push — đã áp vào `.claude/` và `context/mission/`. Chưa có bằng chứng phê duyệt yêu cầu/portfolio/kiến trúc. Setup được phép không thay quyết định nghiệp vụ.

| Mã | Cần chốt | Người xác nhận | Trạng thái |
| --- | --- | --- | --- |
| D01 | Một ca/gói/lô đầu tiên, đầu ra ai dùng và điều kiện chào từng phần | Dũng + chủ nghiệp vụ phù hợp | Chưa chốt |
| D02 | Master/version và quyền cập nhật/lan thay đổi | Chủ master/nhóm được chỉ định | Chưa chốt |
| D03 | Trường giá/công thức/thuế/vận chuyển và tham số theo từng mẫu | Người sở hữu quy tắc giá | Chưa chốt |
| D04 | Sai khác quy cách/chứng từ: ai có quyền nhận/từ chối | Người nghiệp vụ/kỹ thuật có quyền | Chưa chốt |
| D05 | Quote hiện hành, MOQ, lô/hạn, route/carrier và capacity/cash | Cung ứng + người duyệt cam kết | Chưa xác minh đủ |
| D06 | Người thử P1/P2 độc lập, dữ liệu/môi trường được phép | Dũng | Chưa chốt |
| D07 | Cách làm phù hợp: quy trình/Excel/cấu hình/Skill/công cụ | Chủ nghiệp vụ sau so sánh P1 | Chưa chọn |
| D08 | Nơi lưu repo: GitHub org công ty (theo Dũng: Sếp Quân đã lập; org cụ thể chưa xác định), tên repo, private, phạm vi được push (chỉ tài liệu; `sources/`/data/output vẫn ignore; chỉ org nội bộ, private — tài liệu có tên BV khách hàng, hạn nộp, thông tin nhân sự) | Dũng + Sếp Quân | Org công ty: chưa chốt (kiểm 30/10: chưa xác định org). **Đối chiếu 02/11:** theo yêu cầu Dũng 01/11 13:08:50 UTC (`context/clone-handoff/README.md`), repo bàn giao `VOSYDUNG/nnc-bidops-agent` PRIVATE đã được cho phép cho bản bàn giao; không cấp quyền push tự động các vòng sau — mỗi lần push cần chỉ dẫn riêng |
| D09 | Duyệt Mission BIDOPS-M01 và chạy `oser init` (plugin `nnc` đã ghim theo chỉ dẫn Dũng 30/10) | Dũng | Chưa duyệt — có contract nháp ở `context/mission/` |
| D10 | Phương pháp dự án: SOP P1/P2 v1 + OSER R2 (main `94ddf8b`, plugin ghim) + authority graph/lock (`00-README-AUTHORITY.md`) | Dũng | Chỉ dẫn Dũng 30/10 (chat); đề xuất khóa `LCK-METHOD` — PROPOSED, chờ Dũng xác nhận. 02/11: cách áp dụng hiện hành ở `context/mission/README.md` § "Cách làm hiện hành từ 02/11/2026" (không thay D10) |
| D11 | Luật ghép: yêu cầu và chào giữ riêng; không ghép bằng STT; phạm vi BGC dùng mã MPSC; nguồn khác cần bảng nối trước khi ghép | Người sở hữu master (D02) + Phet | Chưa chốt — đề xuất `LCK-MATCH-KEY` (PROPOSED), bằng chứng đo ở `discovery/DINH-HINH-SAN-PHAM.md` §3 |
| D12 | Ngữ nghĩa giá trị: trống ≠ 0 ≠ chưa xác nhận; giá năm trước/mua gần nhất là lịch sử; mã tiền chỉ VND/USD/THB/CNY/LAK | Người sở hữu quy tắc giá | Chưa chốt — đề xuất `LCK-VALUE-SEMANTICS` (PROPOSED) |
| D13 | Bộ trạng thái dòng/gói: đã giao · đã nhận · đã kiểm · đã nạp · đủ điều kiện trình · đã quyết chào/không chào | Chủ nghiệp vụ | Chưa chốt — đề xuất `LCK-STATUS` (PROPOSED) |
| D15 | Nền dự án và hai lớp: lớp điều hành BidOps/CEO (Dũng + Shin + Claude cha) và lớp node người–agent, mỗi lớp có R2 alpha/R1 OSER, tài liệu và bản thể tại chính mình; cùng phương pháp ≠ cùng owner/phạm vi; node thiết lập đủ thì làm thật ngay trong quyền hiện có, blocker áp đúng node | Dũng | **CONFIRMED_USER_DIRECTION** — Dũng xác nhận trực tiếp 02/11 ghi vào hồ sơ; đang áp dụng. `LCK-LAYERS` ghi hồ sơ, không phải runtime lock; runtime chưa instantiation (chưa `oser init`) |
| D14 | Tổ chức thực thi từ 02/11: Dũng + Shin giữ mục tiêu/phạm vi/chốt; Claude cha giữ context, tự chia việc, review, tích hợp; DATA và Phương án A trước, song song; HỌP sau, không chặn hai phần đầu, hiện đóng băng; làm trong session Claude với file dẫn xuất trong project, không host/UI ngoài; ca hiện tại thầu BV không SPM, pilot = nguồn hàng + phối hợp đưa hàng về + giá có căn cứ | Dũng | **CONFIRMED_USER_DIRECTION** — Dũng xác nhận trực tiếp 02/11 ghi vào hồ sơ; đang áp dụng. `LCK-EXECUTION` ghi hồ sơ, không phải runtime lock |
| D16 | Không gian làm việc Thuốc (mức R2: D2): **một file chung** trên Drive (`Thau BV/THUOC-agent-teams-20261104/10-DU-LIEU-CHUNG`, id `1ilOLCO…`) + **hộp thư theo người** `Inbox_thau/0x_<tên>`; chia dòng theo bảng chia của nhóm (cột AK bảng giá Kom), Dũng không giao việc; file chia tách từ file chung (file chuẩn); vá đúng ô, không chép đè; tạm gác cây thư mục theo nhóm | Dũng | **CONFIRMED_USER_DIRECTION** — chat 05/11 (xem "Bằng chứng D16–D17"). Ghi hồ sơ cách làm, không phải quyết định nghiệp vụ. `LCK-WORKSPACE` |
| D17 | Chính sách bản chụp dữ liệu (D2): chốt mốc bằng bộ `LOCK-YYYYMMDD` local, chỉ đọc, có hash và bản đồ vị trí; khóa ghép là mã; đổi thì tạo bộ mới, không sửa bộ cũ; bản chụp không khóa quyết định nghiệp vụ | Dũng | **CONFIRMED_USER_DIRECTION** — chat 05/11 "LOCK dữ liệu chốt hôm nay… đặt bộ lock ở local". Đang áp dụng: `LOCK-20261105` |
| D18 | Ngữ nghĩa tiền tệ giá Kom (D2, con của D12): GM giá mua giữ tiền gốc VND hoặc USD; GV giá vốn kíp = (GM VND + vận chuyển) ÷ 1,22 hoặc GM USD × 22.000 + vận chuyển; Giá 1/Giá 2 chào thầu kíp; giá nhóm điền = VND / 1 ĐVT nhỏ nhất | Người sở hữu quy tắc giá (Phét? chưa xác nhận) | **PROPOSED** — bằng chứng: công thức trong sheet giá file Kom (DATA_MEASURED) + lời họp 05/11 "giá mua là VND cho chị Trang", "quy về đơn vị nhỏ nhất" (chưa gán người nói). Chưa có người có thẩm quyền xác nhận; mở: Giá 1 hay Giá 2 là giá nộp; 116 dòng Giá 1/GV ≈ 1,79 |
| D20 | Kiến trúc dữ liệu gói thầu (D2): 5 lớp L0 nguồn thô · L1 **một bản thể mỗi gói, Agent là đầu ghi duy nhất** · L2 runtime theo người · L3 quyết định của người có thẩm quyền · L4 xuất bản sinh từ L1+L3; runtime chỉ vào L1 qua intake có kiểm; mỗi lần đổi nâng lock; chọn định dạng (file/sheet) một lần ở đầu gói. Chi tiết: `context/agent-goi-thau/QUY-TRINH-GOI-THAU.md`, hồ sơ Agent ở `context/agent-goi-thau/HO-SO-AGENT-GOI-THAU.md` | Dũng | **PROPOSED** — rút từ sự cố dữ liệu tràn lan ca Thuốc (≥ 7 bản chứa giá Kom, nguồn thô 2 phiên bản, runtime lẫn file hợp nhất; `SRC-DRIVE-THUOC-0911`). Chờ Dũng xác nhận; áp vào Kom 2027 cần Dũng chỉ định một bản L1 |
| D19 | Thứ tự gói và hạn: Kom nộp 13/11 (đủ giá 11/11, hồ sơ 11–12), Mahosot 25/11, Settha 26/11, Mẹ & Bé 27/11; SVNK, Dek/Nhi chưa rõ; "Quân y trước, BV khác tuần sau" | CEO / người điều hành họp | **Chưa chốt** — lời nói trong họp 05/11 và 09/11 (ASR, chưa gán người nói) + mốc kế hoạch trong báo cáo nhóm 09/11; chưa đối chiếu thông báo đóng thầu. Đang dùng làm thứ tự làm việc, không phải cam kết |

## Bằng chứng D16–D17 — chỉ đạo của Dũng 05/11/2026 (phiên cha `a5ab430d`, `SRC-CHAT-DUNG-0511`)

- "giờ các anh chị làm việc ntn tạm gác các cây thư mục phức tạp nhé … file này tập trung hoàn thành vì a sơn nói cần nó là đc rồi"
- "promt ngắn cho Team nhé -> viết là dựa vào file chia của nhóm nhé tôi không phải người giao việc"
- "sao không dùng thị giác này vậy đừng follow theo file mới gửi vừa rồi quá mức nhé file nguồn làm chuẩn"
- "LOCK dữ liệu chốt hôm nay nhé (KOM chốt đợi nguồn + giá -> dữ liệu có gì sẽ refactor file gọn lớn và file chia đã có đủ cần lock vị trí … đặt bộ lock ở local nhé"
- **Phạm vi:** cách tổ chức dữ liệu và làm việc nhóm Thuốc; không gồm giá, NCC, tương đương, quyền xem giá vốn.
- **Mở lại khi:** Dũng đổi chỉ đạo; nhóm đổi bảng chia; refactor file gọn lớn sau khi Kom đủ nguồn + giá.

## Bằng chứng D10 — nguyên văn chỉ dẫn của Dũng (phiên Claude 30/10/2026)

- "áp dụng phương pháp thiết lập tự chủ cho dự án này nhé … kiểm tra github công ty có chưa … đặt kiểm tra chưa push gì nhé. Thiết lập dự án này trước théo P1/P2 đã có và định hình tự chủ"
- "chia việc song song , quyết định giữ opus còn sonnet làm song song" — **chính sách của Dũng**, không phải bảng ghim model theo vai của phương pháp.
- "main 94ddf8b … OSER R2 … này nhé"
- "ta cài để kế thừa phương án cho dự án lấy từ Repo để thiết lập chứ không cần gửi ngược về đó"
- "thiếu rồi ta ngoài P1 P2 còn có các Hệ thống tài liệu sản phẩm lock để giảm việc refactor thiếu chủ đích"
- "audit lại nhé vì có một số dữ liệu đang bị nhiễu theo tài liệu plugin cũ"

## Bằng chứng D14 — chỉ đạo của Dũng ngày 02/11/2026

- **Trực tiếp** (`SRC-CHAT-DUNG-0211`, phiên cha `a5ab430d`): "Tôi giao Foundry/Shin phối hợp điều hành BidOps trong phạm vi đã chốt. Claude tự phân việc và thực thi; chỉ hỏi tôi khi đổi định hướng, thiếu quyết định nghiệp vụ hoặc gặp quyền chưa được cấp. Làm Data và Phương án trước, Họp sau khi đủ ngữ cảnh."
- **Xác nhận ghi hồ sơ** (trực tiếp, phiên cha 02/11): "Ghi nhận các chỉ đạo tôi đã chốt vào hồ sơ dự án; việc này không cấp thêm quyền runtime và không chạy oser init".
- **Chuyển lại** (`SRC-RELAY-DUNG-0211`, chưa đọc nguyên văn gốc): "xây cái gì vậy -> phương án này rõ tôi đã reject rồi mà nhỉ -> nên tập trung vào session claude…"; "ủa sao không làm cho xong đi ? có cái gì mâu thuẫn hả"; "ý là phần họp nó đâu liên quan đến 2 phần kìa ?", "nó là làm sau mà ?"; "Ghi nhớ cho dự án luôn"; "phương pháp chúng ta áp dụng cho dự án này đâu"; "Rồi Decesion lock hoặc bản Lock cũng chưa có luôn ?".
- **Phạm vi:** cách tổ chức và thứ tự thực thi BidOps; không gồm quyết định nghiệp vụ thầu (D01–D05, D11–D13 giữ nguyên trạng thái).
- **Gate hoàn thành từng chặng:** DATA — Excel/export đọc được toàn sáu BV gồm Kom từ một nguồn chung, giá có niên độ/loại/điều kiện, tách raw/derived/approved. Phương án A — một tài liệu với pha thầu BV, vai từ tập con 19 người có trạng thái xác minh, nguồn Cung ứng mới nhất (hoặc pending có nơi đã tìm), vận hành Drive/Claude Team, checklist pilot thật có bằng chứng/blocker. HỌP chỉ mở lại khi hai gate trên đạt và Dũng/Shin muốn mở.
- **Lựa chọn cũ bị thay:** `CLAUDE.md` "Giai đoạn kế tiếp (RESEARCH) chờ Dũng cho chạy" và "Subagent chỉ gọi theo lượt… không chạy nền" (thực tế đã chạy nhánh Desktop theo chỉ đạo trực tiếp; `CLAUDE.md` chưa sửa, chờ Dũng); hướng view họp HTML `outputs/hop/v1/` (bị bác, giữ lịch sử); câu tạm thời của root về bỏ gate/chạy Họp ngay (đã rút lại, không áp dụng).
- **Mở lại khi:** Dũng có chỉ đạo mới rõ ràng; hoặc gate DATA/Phương án đạt và cần mở HỌP; hoặc phát hiện xung đột với quyết định nghiệp vụ đã khóa.

## Bằng chứng D15 — nền và các lớp (02/11/2026)

- **Xác nhận ghi hồ sơ** (trực tiếp, phiên cha 02/11): "Ghi nhận các chỉ đạo tôi đã chốt vào hồ sơ dự án; việc này không cấp thêm quyền runtime và không chạy oser init".
- **Evidence ID hội thoại root:** `Sentinel_be52a801cdb88191a02f6add7e87a043` (hai lớp), `Sentinel_09dcc3c254108191b54be11e215bb202` (triển khai ngay khi thiết lập), `Sentinel_ad7bddb85e9881919e52c908076ebd1b` (ghi vào dự án) — do phiên root cung cấp, phiên cha chưa tự kiểm. Giờ gốc chưa lấy được — metadata gap, không đoán giờ.
- **Chuyển lại** (`SRC-RELAY-DUNG-0211`, chưa đọc nguyên văn gốc): "tức tôi với bạn đang dựng khung cho dự án này : layer Foundry của chúng ta : phương pháp Claude plugin R2 alpha, R1 tự chủ OSER, tài liệu dự án và bản thể thống nhất. -> cũng có nhưng tầng lớp khác / triển khai xong mỗi người cũng cso phương pháp Claude plugin R2 alpha, R1 tự chủ OSER, tài liệu dự án và bản thể thống nhất. -> ở chính mình / vậy nên đừng hiểu nhầm cần có cái nhìn cho đúng nhé tuy hơn lộn xộn nhwung đó là thực tế"; "được triển khai ngay sau khi chúng ta thiết lập được".
- **Phạm vi:** cách hiểu lớp và quy tắc kích hoạt node; không cấp quyền mới, không thay quyết định nghiệp vụ.
- **Kiểm thật tại 02/11 (runtime verified):** `SRC-OSER-VENDOR` có trong dự án; chưa `oser init`; chỉ node Dũng có bằng chứng hoạt động. Không suy R1/R2 đã cài ở node khác.
- **Mở lại khi:** Dũng đổi chỉ đạo; có node khác thiết lập xong (cập nhật trạng thái node, không đổi quy tắc).
- Chi tiết bảng lớp và bản đồ tài liệu: `context/mission/README.md` § "Nền dự án và hai lớp (D15)".

Khi có quyết định thật, thêm ngày, người, phạm vi, nguồn dẫn và tác động. Không tự đổi Chưa chốt thành Đạt. Không yêu cầu chốt mọi câu trước khi làm các phần phân tích/fixture độc lập.
