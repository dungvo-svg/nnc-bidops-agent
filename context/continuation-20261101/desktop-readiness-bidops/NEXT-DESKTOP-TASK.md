# NEXT DESKTOP TASK — BidOps: tiếp tục hiện thực B synthetic có nối mạch

**Đích nhận duy nhất:** Claude Desktop BidOps conversation `a5ab430d-1ab4-4c21-8a6a-2b597076de9f`, Desktop local ID `local_5e4b81c7-343c-47f7-a688-fe41f2921bfa`, project `D:\WORK\Agent\Agent-first\NNC BidOps Agent`. Đây là nhiệm vụ chuẩn bị cho đúng phiên đó; việc file có trên đĩa không chứng minh phiên đã đọc hoặc bắt đầu. Không tạo phiên khác, không dùng inbound relay đang lệch đích, không đổi quyền để gửi.

## Mục tiêu thực thi

Tiếp tục **viết và kiểm code synthetic local**, từ pilot B đã có, để chứng minh một vòng nối mạch có trạng thái, source/version, danh tính biến thể và bằng chứng kiểm được. Opus giữ mục tiêu, thiết kế, quyết định kỹ thuật trong phạm vi và tích hợp bản cách ly; tự chọn kế hoạch rồi giao Sonnet làm các phần độc lập bằng tools thật. Codex là peer thực thi/review độc lập. Đừng chỉ trả lại một kế hoạch hoặc lặp audit; làm đến đầu ra code/test/receipt review được trong phạm vi dưới đây.

BidOps là node của CEO đa nhánh, thầu bệnh viện làm mũi nhọn. CEO vẫn trực tiếp chào hàng và điều phối khi có nhân viên. Mỗi người có máy và Agent của chính mình; CEO trao mission và nhận kết quả, không điều khiển Agent/máy của họ. Không thu hệ thống thành trợ lý thầu riêng của Dũng, không đặt policy “CEO không làm phần staff”, không tự đòi apply/use phải luôn khác người. Người/quyền thật theo từng phạm vi chưa chốt thì giữ pending.

Vòng mới mở **phần code synthetic cách ly** đã được giao, không mở triển khai công ty hay duyệt P1/P2 nghiệp vụ. Những câu “vòng này chỉ audit/tài liệu” trong continuity là snapshot của vòng trước, không ngăn nhiệm vụ local mới này. Nó cũng không biến D*/LCK thành LOCKED hoặc cấp quyền gửi/nộp/master/giá. AGENTS và CLAUDE gốc của owner vẫn chi phối; không chép đè chúng bằng AGENTS/CLAUDE của pilot cũ.

## Điểm vào và baseline

Đọc owner `AGENTS.md`, `CLAUDE.md`, `context/PROJECT_STATE.md`, rồi `context/continuation-20261101/{BRIEF,SOURCE-MAP,DECISION-LOG,PLAN-VS-IMPLEMENTATION,ROADMAP-STATUS}.md`. Theo authority graph `requirements/00-README-AUTHORITY.md`; đọc node nguồn khi phần việc cần. `GAP-MAP.md` cùng gói này trỏ các thân hàm đã đối chiếu và test mong đợi; `COPY-MANIFEST.json` ghim hash, không phải authority mới.

Pilot B gốc ở C: có commit theo receipt `aac3e9428084254ae21fba4eaf0ee7b85a014b70`; **không sửa pilot gốc**. Root chuẩn bị23 file source-only tại `source-only/`; đề xuất chép nguyên allowlist vào owner `data-work/pilots/bidops-b-next-20261101/`. Bản này là code thử cách ly, không phải tích hợp sản phẩm owner. Root phải readback và đối chiếu hash trước; nếu chưa có bản chép, báo chính xác đường thiếu rồi đọc tiếp context độc lập. Không tự lấy DB/CSV/XLSX/catalog thật để bù.

Bản23 file gồm8 file src Python,9 file tests Python,3 technical contract, README, config.sample và demo.py. Không có `.git`, cache, DB, workbook, dữ liệu catalog, env, credentials, plugin/hook config hay AGENTS/CLAUDE. README/contracts của pilot có pointer lịch sử không nằm trong bundle; dùng context owner nêu trên thay vì tự chép thêm dữ liệu/quyền. Đừng dùng lời cũ “Claude chỉ review” trong README pilot để thu nhiệm vụ mới thành review-only; quyền làm code ở bản cách ly đến từ chỉ dẫn mới này, không từ README.

Kiểm baseline chỉ trong code copy được giao. Không chạy legacy `build_tender_sets.py`, không dò G/H, không sửa `sources/` hoặc file thầu/Mittaphab. Trước ghi bất kỳ file đã tồn tại: đọc và kiểm trạng thái bằng phương thức được phép; không reset/clean, không vượt Git ownership hay đổi route sau denial. Nếu cần Git để tạo lịch sử local nhưng quyền chưa rõ, giữ diff+hash/receipt và báo; không tự init/remote/commit vào owner.

## Phạm vi code cần nối

Opus đọc source hiện tại và tự chốt thứ tự, interface, file ownership; không phải triển khai mọi đề xuất thành một framework mới. Ưu tiên một đường chạy xuyên suốt các khoảng trống đã có:

1. **Case lifecycle/demand dùng chung một nghĩa giữa Ledger và catalog_lifecycle.** Dùng lại phần đúng thay vì thêm chủ trạng thái thứ ba. Close/cancel một case chỉ bỏ nhu cầu prebid của case đó, giữ case khác, lịch sử, quote và provenance. Reopen là sự kiện mới, không hồi sinh review cũ. Fulfillment chỉ được tạo theo bằng chứng synthetic case đã won, áp cùng guard ở mọi entry point. Hết thời gian chỉ ra overdue_unknown, không tự kết thúc/trúng/trượt. Phân biệt đặt hạn/correction với extension; extension phải theo nghĩa muộn hơn đã có trong CL, không âm thầm ép hai API khác nghĩa thành cùng policy. Nếu correction lùi ngày cần quyết định nghiệp vụ thật, để riêng pending và làm phần extension đã rõ.
2. **Mission/receipt/evidence nối vào state thực của pilot.** Issued, received, accepted, produced/returned, reviewed, applied, used và used_as_diagnostic phải phân biệt. Receipt nhận không thành nhận trách nhiệm; return không thành duyệt; local preparation review không thành quote được chấp nhận. Evidence ref ở vòng synthetic phải truy được tới artifact/record được phép, source/version và hash, kiểm thiếu/đổi/lệch scope thay vì chỉ nhận một chuỗi không rỗng. Chỉ tạo/đọc artifact synthetic nằm dưới output root được chỉ định; không đi mở nguồn thật theo ref tùy ý. Một local packet/return nếu dùng chỉ là mô phỏng/file exchange, có trạng thái RETURN_UNVERIFIED trước validation, không tự gọi là đã gửi tới nhân viên.
3. **Identity/variant bridge có provenance.** Nối source row/version → normalized identity/version → ledger variant/requirement/quote trong cùng thí nghiệm. Không join MPSC/tên/UOM đơn lẻ, không dùng similarity làm accepted equivalence. Cùng mã khác40mm/30mm phải giữ riêng và trả HOLD có ích; hàng thiếu danh tính vẫn unresolved. Bridge explicit synthetic binding có digest/version và receipt, source đổi phải làm downstream cũ không còn dùng được. Đây là cài thử đề xuất có nguồn, không tự khóa D11/D15 hay sửa master thật.
4. **Nối các kiểm tra sẵn có khi có đầu vào synthetic đủ.** `certificate_check` và `portfolio_check` là tài sản có thể dùng; tách danh tính chứng từ, từng trục hạn, thời điểm đánh giá/giao khi được cấp. Năm phép kiểm nghiệp vụ (hồ sơ, cung ứng, kinh tế/vốn, cạnh tranh, kết quả) tách nhau, khác ba trục hàng–chứng từ–tiền và khác phạm vi phê duyệt. Phần chưa có dữ liệu/authority giữ unknown với reason; không invent score, formula giá hay tỷ lệ thắng để lấp đủ năm ô.

Actor/node/capability của code hiện tại là **fixture do caller khai**, không phải principal đã xác thực hoặc ACL công ty. Có thể làm rõ boundary/adapter contract và test giả lập wrong sender trước side effect; không triển khai Auth/IAM/grants thật, không tự nhận spoof-proof từ matching chuỗi. Giữ exact retry và chống event ID đổi actor/type/payload, không ghi side effect lặp. WIP1 hiện chỉ chặn accept; không gọi nó là backpressure/lease mạng. Đừng tự thêm policy chặn mọi receive nếu chưa có căn cứ; mô tả đúng cái đã và chưa chứng minh.

## Case và grain phải giữ

Phạm vi kế hoạch gồm4 BV Mahosot, Settha, Me and Dek, SVNK + Komsenahak2027; Mittaphab vẫn có owner đang làm, không tiếp quản. Bối cảnh master có5 BV không đồng nghĩa pilot chứa/cập nhật mọi luồng của cả5.

Theo receipt hiện có:2.068 dòng nguồn4BV +1.455 Kom = **3.523 source intakes**,4.577 nghĩa vụ theo case; không phải3.523 sản phẩm/biến thể duy nhất. Hãy dùng fixture nhỏ giả lập các grain đó để test hành vi, không nhân bản dữ liệu thật để đạt số. Không lấy giá2026/trúng thầu189 dòng hay649 giá lịch sử Kom thành accepted current quote. Hạn Kom13/11 là mốc kế hoạch từ chat, ngày mẫu thư không phải hạn pháp lý; không ghi lifecycle thật từ mốc đó.

## Cách Opus/Sonnet làm thật và kiểm độc lập

- Opus tự chọn một hoặc vài lát cắt đủ review, khai rõ thay đổi contract, source node, ownership, exclusions và expected outcomes trước khi sửa. Sonnet chạy song song khi file tách rời; tránh hai writer cùng `ledger.py`. Có thể để Opus giữ seam tích hợp và Sonnet viết helper/tests riêng, hoặc chọn phân rã tốt hơn có giải thích.
- Dùng model Sonnet đã được cấu hình/cho phép, ghi model/tool/session thực tế; không giả spawn từ đề xuất, không đổi tài khoản/effort/plugin/quota để vượt gate. Không worker nền, scheduling hay external relay mới.
- Giữ100 test cũ làm baseline hành vi (đọc receipt, không coi100 là số bắt buộc của suite mới). Không đổi kỳ vọng để xanh khi không có quyết định nguồn. Viết regression độc lập cho các gap trước khi fix, ghi đỏ có phạm vi và xanh sau. Nếu source/contract thật bác kỳ vọng cũ, nêu riêng với nguồn thay vì giấu trong test update.
- Thử fresh SQLite synthetic ở output root rõ ràng; giữ exact command/cwd/time/exit, số pass/fail/skipped và log artifact. Không mở catalog/inbox thật. Không install dependencies, tạo access hay dùng env thật; standard library hiện có đủ cho core. Capability phụ thuộc chưa có thì báo đúng, tiếp tục phần độc lập.
- Khi thích hợp, làm demo/2process local nối lifecycle→identity→mission→return→diagnostic/use có receipt. Nếu làm L2, label rõ2process cùng máy/fixture; không gọi là2Agent/2owner thật. Không dùng lịch sử labL3 để bù L4/L5.
- Code receipt phải trỏ exact source digest/diff và final local snapshot. Test trước code rồi đổi code sau phải giữ receipt theo đúng snapshot; không report kết quả nhánh khác là của mình.

## Tiêu chí nhận vòng này

Có code cách ly review được, với một đường chạy synthetic xuyên các seam đã chọn; source facts, hypothesis, pending decision tách rõ. Regression ít nhất kiểm: fulfillment trước won bị từ chối ở cả hai API; deadline qua giờ không auto-close; shared demand còn sống khi một case đóng; reopen không kế thừa review; same MPSC khác spec không gộp; historical price không current; missing/tampered/out-of-scope evidence không được qualify/promote; exact retry giữ receipt và changed payload/actor bị từ chối; received/accepted/returned/used không nhảy bước. Phép kiểm chưa có dữ liệu không được bịa thành đạt.

Đầu ra theo cách Opus chọn nhưng phải có đường dẫn cố định, không nhiều file FINAL/v2 cùng trách nhiệm: (a) PLAN/ownership và gap đã chọn; (b) changed files/diff+hash; (c) commands/results/receipts; (d) status từng gap gồm IMPL/TEST/INTEG/REL/USED; (e) phần còn pending đúng người có quyền. Không yêu cầu tạo một app/web/broker hay toàn bộ OSER runtime mới để đủ vòng này.

Chỉ khi có biến cố/thẩm quyền thật mới đề nghị sửa D/LCK ở file chủ. Không tự nhận current commercial acceptance, quote, NCC, danh mục, giá, người ghi master/nộp, D01/D02/D06/D08/D09/D11 đã chốt. Không init Mission/OSER, đổi workflow owner, gửi thư/WhatsApp/quote/mission thật, ghi master/people, tạo repo/grants, push/merge/deploy. Bản cách ly xanh không phải owner integration hoặc nghiệm thu P2 nghiệp vụ.

## Receipt tiếp nhận và trạng thái Desktop

Ngay khi đúng phiên đọc gói: ghi exact conversation/localDesktopID, current cwd, nguồn thực đọc (path+hash), model quan sát được, task accepted/needs_input và source baseline vào receipt của vòng mới; không suy “đã đọc” vì có link. Sau đó tiếp tục phần được giao. Nếu quota/model/route hoặc quyền chặn, ghi exact action/target/reason, denied/pending/uncertain và phần đã xong; không đổi route hoặc receiver để thử lại. Luôn giữ riêng file-ready, Desktop-open, This-computer, model, route-ready, task-read, started và output.


## Cập nhật đặt file
23file source-only đã được host copy và hash-verify tại `data-work/pilots/bidops-b-next-20261101`; COPY-MANIFEST.json cùng thư mục task có receipt. Không yêu cầu mở lại C: để lấy code. Chỉ sửa bản copy local đã giao, không pilot gốc/owner sources. Các snapshot audit-only cũ không chặn vòng code mới này. Không hỏi lại các điều kiện kỹ thuật đã giải; thiếu business thật thì tự kiểm source cũ/mới/code/research trước, đưa A/B, nguồn/thẩm quyền, tác động/tradeoff và đề xuất cụ thể, chỉ dừng phần đó.
