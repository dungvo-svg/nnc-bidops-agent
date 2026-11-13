# BidOps — A/P1: CEO toàn diện, mũi nhọn thầu BV và mạng người–agent
**Bản nghiên cứu đang hoàn thiện để Dũng xem · Cập nhật 31/10/2026, 18:26 giờ Việt Nam · Chưa sang B/P2, chưa triển khai hoặc nộp/gửi**

## Tóm tắt để xem trước

**A đang tiếp tục; hiện chưa có quyết định lớn buộc dừng để chờ Dũng duyệt khung.** Đã đọc sâu 12 workbook bổ sung của bốn BV và bốn cover; đối chiếu nguồn giá, vòng trao đổi, tài liệu công việc nhân viên, workbook gốc và logic tổng hợp local. Nhưng chưa khép bộ HSMT/điều chỉnh chính thức, bản đích đã áp giá và quyền/runtime từng node. Vì vậy không gọi toàn bộ nghiên cứu Thầu đã hoàn tất.

**Đính chính cần đọc trước:** Komsenahak là gói hiện hành với lịch phối hợp 13/11, không phải gói lịch sử; chỉ một số giá tham chiếu là năm trước. Đã đọc đúng phiên Cung ứng hiện hữu và audit lại nguồn: bản đồ v18 nháp cutoff 26/10 vẫn chưa chứa hết tài liệu 27–29/10; hướng dẫn/kế hoạch 28/10 được dùng để cập nhật vai và quy tắc, chưa coi là receipt live. Phần bus/onboarding ở mục 10 là phương án tác nghiệp để review, chưa triển khai.

**Điều chỉnh theo hướng mới của Dũng:** CEO vẫn trực tiếp chào/làm việc cùng nhân viên; thiết kế riêng người đại diện nhánh thầu nếu được ủy quyền. Trọng tâm mạng là agent của người giữ dữ liệu tự nhận yêu cầu, xử lý và phản hồi cho agent cần dùng, không tiếp tục bắt con người làm trung gian. Bản lite nhân sự chỉ lấy phần phục vụ thầu; công việc khác của từng người giữ nguyên ngoài phạm vi lần này.

Các kết quả đã làm thay đổi nội dung phương án, không chỉ thêm tài liệu tham khảo:

1. **Giữ đầy đủ năng lực CEO/BidOps.** Thầu BV là mũi nhọn, không xóa các nhánh khác; phần thầu phải nhìn cả cạnh tranh, kinh tế, vốn, nguồn, giao và thu tiền. CEO vẫn trực tiếp làm thầu/chào hàng khi có nhân viên; chỉ thay cách phân công, không cắt các năng lực tác nghiệp chung của CEO.
2. **Node phải là người thật + agent + việc + năng lực/quyền/quan hệ/hiện diện.** Dũng đã xác nhận mỗi thành viên có một agent Claude; đây là nền thiết kế, không hỏi lại có tài khoản hay chưa. Nguồn AS-IS xác nhận một người có thể vừa quản lý hàng, tìm nguồn, làm đơn và nối vận chuyển; không chia cứng mỗi phòng một agent.
3. **Phải đọc đúng phiên bản và thời điểm.** Cotton Ball + Acool có giá 2.190 kip trong nguồn Sơn 30/10 nhưng phần so nguồn của chính bảng tổng hợp đó trống/count 0. Danh mục chia sẻ 29/10 có trước nguồn này; không quy lỗi thiếu giá cho bản cũ từ dữ kiện xuất hiện ngày sau.
4. **Cùng mã không nhất thiết cùng hàng.** 53 mã MPSC nối ra 54 dòng catalog chung; cùng MPSC02MD00102 có kim 40mm ở một số BV và kim 30mm/EP3 ở Settha. Agent phải ghép theo BV–dòng–spec–đơn vị–phiên bản, không chỉ mã chung.
5. **SVNK là giao đa điểm.** Biểu giá nêu kho BV tỉnh và BV huyện toàn tỉnh; sheet phân phối có 16 cột điểm đến. Giá giao một kho không đủ đại diện kinh tế gói.
6. **Nhãn “done” không đồng nghĩa hoàn thành thầu.** Logic cũ dùng nhãn này khi ghép được giá vốn hoặc có giá năm trước; kết quả thật vẫn có dòng thiếu phương án giá và dữ liệu chứng từ cần kiểm.
7. **Đích tự chủ khác quyền đang cấp.** Hướng dẫn nhân viên 28/10 cho Claude đọc/so/chuẩn bị, còn người tự quyết và bấm app. Không hứa agent tự ghi production hiện nay; cũng không lấy giới hạn bước này làm trần năng lực đích của BidOps.

---

## 1. Điểm đứng đúng của A

### Hai tầng sản phẩm, không co về một trợ lý thầu của Dũng

- **CEO + BidOps:** năng lực toàn diện phục vụ CEO hiểu tình hình, chọn mục tiêu/cam kết, phân bổ nguồn lực, tự thực hiện hoặc điều phối, theo tới kết quả và học. Thầu bệnh viện là mũi nhọn cần phân tích sâu; các nhánh kinh doanh/vận hành khác vẫn tồn tại và dùng chung nguồn lực.
- **Node nhân viên:** người thật có công việc, chuyên môn, quan hệ và quyền; agent làm phần được giao quanh người đó. Không phải tiến trình con CEO tạo và điều khiển, không chỉ là người chuyển tệp cho CEO làm thay.

Cách viết trước đã trộn **phạm vi hành động được phép hôm nay** với **phạm vi năng lực của sản phẩm**. Dừng ở nghiên cứu A/P1 không có nghĩa BidOps chỉ còn năng lực viết báo cáo. Ngược lại, mô tả năng lực đầy đủ không cấp quyền thực thi mọi việc ngay.

**Phạm vi nguồn đang đi sâu:** Mahosot, Settha, Me and Dek, SVNK; thuốc nhập khẩu, hóa chất, VTTH. MTP/Mittaphab là hồ sơ đang do người phụ trách xử lý và nguồn tham chiếu, không tự nhận lại. **Komsenahak là gói đang được theo đuổi, không phải chỉ là case lịch sử.** Giá năm trước trong một số dòng là nguồn tham chiếu, không làm cả gói thành lịch sử. Tên BV/lot trong tên tệp chưa thay mã gói chính thức.

**Đính chính Komsenahak và phạm vi onboarding:** [tin nhóm 29/10, 09:50–10:07](https://drive.google.com/file/d/1cqxstMmRj-8l1fy0j2mg6uRpMDAPeOne/view) ghi Phét báo Sieng mua thêm gói Komsenahak, chị Tình xem giá 2027 và lịch ghim 13/11. [Kế hoạch 29/10](https://drive.google.com/file/d/1MWdkQrhfW8Sa44SHAyaD4EbuAYvKBlVH/view) đã đặt gói này trong pipeline; “chưa có file” chỉ là checkpoint bộ đối chiếu lúc đó, không phải khẳng định hôm nay công ty thiếu hồ sơ. Mốc 13/11 nay đã đối chiếu thêm `Excemple for soft copy(USB!I8` trong workbook gốc: 13/11/2026; vẫn chưa lấy mẫu này thay full HSMT/giờ đóng thầu/addenda. A phải tính Komsenahak trong nhánh thầu hiện hành; phạm vi 12 workbook/bốn BV đã đọc không phải trần phạm vi mạng.

**Kom đã có workbook và việc hiện hành:** chuỗi 30/10 09:13 ghi Phét gửi file làm giá, giải thích giá trong sheet 2027 là giá chào 2026; CEO 09:15 giao Dũng rà hàng chưa có giá như các BV khác. Workbook gốc `List 2027 ` có B10 ngày 28/10/2026 và A12 năm 2027; mẫu USB B14 ghi 2027, I8 ghi 13/11/2026. Mẫu hard copy B14 còn 2024 là template cũ cần rà, không đổi tình trạng gói.

Đã đối chiếu **1.455 dòng = 649 có giá cũ + 8 cần xem hàng + 798 tìm nguồn**. Chỉ có 797 annotation tìm nguồn vì **Omesod**, `List 2027 ` dòng 663/STT 645, chưa có dòng đích trong sheet giá. Dòng gốc còn nguyên: đây là thiếu mapping/destination, không mất nguồn. BGC năm BV chưa có tab Kom là khoảng trống adapter, không phải căn cứ loại gói. Case này thích hợp kiểm agent intake → nhận trách nhiệm → tìm/đối chiếu nguồn → review → candidate, không tự ghi đè master.

**Phân biệt phạm vi dữ liệu với phạm vi được giao:** ba workbook danh mục chung local có 679 dòng thuốc, 1.100 hóa chất và 957 vật tư, tổng 2.736 dòng, gồm Mittaphab và bốn BV còn lại. Phần tìm nguồn thêm tập trung bốn gói không có nghĩa danh mục bỏ Mittaphab. Đây không cùng đơn vị đếm với 2.126 mã MPSC của BGC Oanh; không dùng chênh lệch làm bằng chứng mất hàng. Các mã TH/HC/VT đánh theo thứ tự sắp xếp cũng không phải định danh bất biến.

**Ranh giới hành động:** chỉ nghiên cứu, đối chiếu, audit và viết phương án. Không sửa nguồn/master, gửi NCC, ký/nộp, cấp quyền, mở mạng agent hoặc nạp App/Done. Không cần chờ duyệt một sơ đồ mới để tiếp tục A.

## 2. Năng lực CEO/BidOps phải toàn vẹn

**Mission đích đề xuất:** giúp CEO nhận biết tình hình, lựa chọn và thúc đẩy những cam kết có giá trị, thực hiện được và kiểm chứng được kết quả trên toàn doanh nghiệp; với thầu BV, đi từ cơ hội/đường cạnh tranh đến nguồn–giá–hồ sơ–giao–thu tiền, nối tác động với các nhánh khác.

“Toàn vẹn/toàn năng” là không bỏ trống năng lực cần cho vai CEO, không có nghĩa toàn quyền dữ liệu, biết mọi sự thật hoặc được tự ký/chi tiền. Năng lực lý luận, quyền hành động và bằng chứng phải tách riêng.

Chưa tìm thấy một framework nguồn có tên/section chính xác “7 năng lực CEO” trong các workspace thầu và tài liệu đã kiểm. Bảng dưới kế thừa **bảy trục phân tích đã nêu trong bản A trước**, làm rõ cách phục vụ thầu và phần giao với doanh nghiệp. Không coi chúng là bảy phòng ban hoặc một danh sách bảy nhánh kinh doanh đã được xác nhận; các năng lực chung với nhân viên vẫn hiện diện ở CEO.

| Năng lực CEO/BidOps | Trong mũi nhọn thầu BV | Giao với phần còn lại của doanh nghiệp |
|---|---|---|
| Nhận biết tình hình | Cơ hội nào mở, ai đang làm gì, thay đổi nào ảnh hưởng kết quả | Kinh doanh, khách hàng, sản phẩm, vận hành, dữ liệu và tài sản số |
| Mục tiêu/chiến lược | Vì sao theo cơ hội này, giá trị và phạm vi tham gia, đường cạnh tranh | Danh mục hàng, quan hệ, thị trường, ưu tiên và chi phí cơ hội |
| Phân tích lựa chọn | Cùng hãng/nguồn khác, ứng viên thay thế có điều kiện, phạm vi/lô/kịch bản | So thầu với bán hàng thường và nhu cầu dùng chung vốn, hàng, người |
| Kinh tế/nguồn lực | Chi phí tham gia, mua/bán, logistics, vốn theo thời gian, hạn dùng | Công nợ, tồn kho, năng lực giao, cam kết ở các nhánh khác |
| Điều hành/tự thực hiện | CEO/BidOps vẫn trực tiếp làm/chào trong quyền dù có nhân viên; cùng chia nhánh, nối phụ thuộc và đối chiếu kết quả | Kênh liên lạc thực với khách/NCC/carrier; xử lý ngoại lệ xuyên vai |
| Quyền/rủi ro/cam kết | Quyền đổi giá/nguồn, xác nhận chuyên môn, ký/nộp, tái kiểm khi điều kiện đổi | Trách nhiệm, kế thừa, người vắng/thay đổi, bảo vệ dữ liệu |
| Kết quả/học | Tách trúng–đặt–giao–nghiệm thu–thu tiền; nguyên nhân thắng/thua/sai lệch | Nâng năng lực dùng chung sau review, không tự đổi policy từ một ca |

Năm phép kiểm nghiệp vụ giữ độc lập: **đáp ứng hồ sơ, khả năng cung ứng, kinh tế/vốn, căn cứ cạnh tranh, kết quả thực hiện**. Không cộng thành một điểm “sẵn sàng” giả; không dùng tỷ lệ điền dữ liệu làm tỷ lệ sẵn sàng chào hay xác suất thắng.

## 3. CEO luôn cùng làm; thay đổi cách phân công, không cắt năng lực

CEO vẫn trực tiếp tìm cơ hội, nghiên cứu/chào hàng, so nguồn, làm giá và xử lý hồ sơ theo phần việc nhận. Nhân viên có mặt không tước các năng lực chung đó khỏi CEO/BidOps. Khác biệt của CEO là thêm quyền và trách nhiệm về mục tiêu, phân bổ nguồn lực, quyết định liên nhánh và ngoại lệ; không phải chỉ đứng trên giao việc.

Một việc có thể do CEO + BidOps và một hoặc nhiều người + agent cùng làm, nhưng phải chia rõ đầu ra: CEO xử lý đường chào/quan hệ và phương án kinh tế; người giữ nguồn xác minh quote; người giữ hồ sơ nối chứng từ; người giữ kho/giao xác nhận khả năng thực hiện. Ai cũng có thể đọc, nghiên cứu, so, tính, dự thảo và phát hiện vấn đề trong quyền. Không chia một agent chỉ biết một chức năng; không cùng ghi một giá/chọn một hãng mà không đối chiếu phiên bản và người có quyền chốt.

Ba chế độ cùng cần có:
- CEO trực tiếp làm phần lớn: BidOps tự thực hiện trong quyền và hỏi agent đang giữ dữ liệu/phụ thuộc, không giả CEO sở hữu hết dữ liệu.
- CEO và nhân viên cùng làm: chia nhánh theo case, năng lực, hiện diện và thời hạn; ai phát hiện có thể mở vòng phối hợp đúng quyền, không đợi CEO phát lệnh từng bước.
- CEO giao người đại diện riêng nhánh thầu BV: người đó cùng agent giữ tiến trình đầu cuối của nhánh trong phạm vi ủy quyền; CEO vẫn có thể tham gia tác nghiệp và giữ phần quyết định không ủy quyền.

### Đại diện CEO trong nhánh thầu không có nghĩa trở thành CEO toàn công ty

Thiết kế cần hỗ trợ người đại diện có phạm vi hữu hạn: gói/BV, khoảng thời gian, kết quả, phần được quyết và phần chỉ chuẩn bị, các bên được liên lạc, nguồn được truy cập và ngưỡng chuyển ngoại lệ. Giao tiến trình khác giao quyền ký/nộp/giá/cam kết vốn. Không tự chọn người hoặc điền hạn mức.

Thông tin ủy quyền được agent nhận việc kiểm trước hành động và được đối tác nội bộ kiểm khi nhận yêu cầu. CEO giao nhánh không tự mở chat riêng, mật khẩu hay toàn bộ dữ liệu của nhân viên cho người đại diện. Khi thay người hoặc hết hạn: bàn giao việc mở, nguồn/phiên bản, quyết định và cam kết đã có; đổi nơi nhận trách nhiệm mới, không viết lại tác giả lịch sử. Cơ chế thu hồi/tạm dừng phải ngăn hành động mới vượt quyền nhưng vẫn giữ bằng chứng công việc.

Trong A có thể mô tả đầy đủ tình huống này mà chưa cần Dũng chỉ định ai. Chỉ trước thực thi mới cần người và quyền thật, không biến thiếu tên thành blocker nghiên cứu.


## 4. Node theo người và công việc thực

Một node cần hiểu bảy yếu tố, ưu tiên đọc nguồn hiện có thay vì bắt nhân viên điền lại form:
1. Người thật, case/phần việc đang nhận và outcome họ giữ.
2. Năng lực người: chuyên môn, ngôn ngữ, cách làm, xử lý ngoại lệ, kinh nghiệm có bằng chứng.
3. Năng lực agent đã chạy được, tách khỏi việc chỉ có skill/tài liệu.
4. Quyền đọc/sửa/gửi/duyệt/cam kết theo hành động và nguồn.
5. Quan hệ và kênh thực với NCC/BV/carrier/người giữ chứng từ.
6. Hiện diện: người sẵn sàng quyết khác máy online, khác agent đang chạy.
7. Tiếp nối: đã nhận/chờ fact/chờ quyết định/offline, người giữ phụ thuộc, hạn và bằng chứng nhận dùng.

Luôn tách **người nhận việc**, **người giữ sự thật**, **người đang giữ phụ thuộc**, **người có quyền quyết định**. Một người có thể giữ nhiều vai, không mặc định vậy cho mọi case.

**Phạm vi lite:** mô tả năng lực tổng quát và nhiệm vụ phục vụ thầu, không dựng lại toàn bộ bản thể công việc của mỗi người. Cùng một năng lực có ở nhiều người; nhiệm vụ và quyền cụ thể mới quyết ai làm/ai chốt trong case.

### Danh sách người–agent lite phục vụ thầu

Đã đọc đúng phiên **QUY TRÌNH CUNG ỨNG** và kiểm lại tài liệu, không chỉ lấy lời phiên. Bản đồ v18 nháp có cutoff 26/10, 84 node/189 edge, trong đó 39 chốt, 8 rõ, 37 cần xác nhận; đây là trạng thái tài liệu, không phải số agent đã chạy. Tài liệu 27–29/10 chưa được nhập hết vào map. Bản v10 ngày 12/10 vẫn là nguồn lịch sử cho những vai chưa có cập nhật; không dùng “map mới nhất” làm authority duy nhất.

Bảng đã cập nhật theo [kế hoạch 28/10](https://docs.google.com/document/d/1h0P86WXYO7y03lzhTCPoMX7qF7l4vZRM/edit), [hướng dẫn nhân viên 28/10](https://docs.google.com/document/d/11MiJ_XVCQA7IDs8coDhYsHeIroosKTEV/edit) và nguồn hiện trường phù hợp case. **Mỗi người có một agent Claude theo Dũng; nhiệm vụ bên dưới là phạm vi đích/phân công tài liệu, chưa phải quyền mới hoặc receipt đã nhận/chạy.** Các vai không có nguồn mới vẫn giữ mốc lịch sử riêng.

| Người / agent | Năng lực và nhiệm vụ có thể nối vào thầu | Ranh giới cần giữ |
|---|---|---|
| **CEO / BidOps** | Trực tiếp phát hiện cơ hội, chào hàng, tìm/so nguồn, lập phương án giá–hàng–chứng từ–tiền; cùng thực thi và nhìn tác động toàn gói/liên nhánh | Không chiếm quyền agent cá nhân; ký/nộp/chi theo thẩm quyền thật. Không tự đồng nhất mọi “Sếp” trong nguồn |
| **Lý** | Cung ứng OTC; tìm nguồn VN, nhận nhu cầu Lào, NCC/hợp đồng/giao, khai quan thường lệ và khiếu nại; agent nối dòng thầu→quote→ready→chặng/giấy tờ | Không chỉ logistics; không tự đổi lượng của quản lý hàng. Điều kiện một case SGVC không áp toàn thầu |
| **Trang** | Cung ứng SPM/HC theo kế hoạch mới; rà giá A11 thuộc SPM; nguồn VN, đơn/AMIS, chặng HN và chứng từ; agent so giá/đơn/ảnh nhận, cung cấp bằng chứng theo case | Plan giao nạp bảng giá Lacco/Tuấn Việt không có nghĩa liên hệ Lacco mọi case; giữ đúng quyền quỹ |
| **Linh** | Cung ứng HC; nguồn nước ngoài, NCC/hợp đồng/sản xuất, quote/spec/packing/ready date, forwarder và estimate toàn chặng; tự theo ngoại lệ | Không chỉ vận chuyển; kênh cá nhân chỉ dùng trong quyền. Giá dự tính khác actual; case 29/10 Linh liên hệ Lacco |
| **Phét / Phet** | Cung ứng HC; nguồn Lào–Thái, NCC giao biên giới, xe công ty về kho, AMIS; nối dữ kiện bảng thầu/giá/hồ sơ với agent liên quan | Vai giữ bảng thầu dựa nguồn thầu riêng; không tự chấp thuận tương đương hoặc nhận đã giao từ planned shipment |
| **Đức** | Map 12/10 ghi VN/HC, đơn, đề nghị tiền và Excel đáo hạn; có thể tái dùng bằng chứng liên quan | Vai lịch sử, không có trong nhóm B1 cuối tháng; chưa tự phân công node thầu hiện tại |
| **Hoa** | Danh mục hàng/giá mua, thiếu mã, tối ưu mã, dữ liệu nhập/phân bổ; agent so đầy đủ dòng, mã–spec–UOM, chuẩn bị diff | Không tự gộp/sửa MISA; nhập giá khác duyệt giá. Tình trạng thiếu quote 12/10 không suy ra hôm nay |
| **Yaeng** | Kiểm công nợ/trả trùng, nguồn NCC/danh mục theo plan; agent nối NCC–điều khoản–đề nghị–đáo hạn–đã trả | Map xác nhận không nhập đơn; không tự đồng nhất Yaeng với tên “Yang” từ OCR; đề xuất quyền chưa là ACL thật |
| **An** | Kế toán trưởng, quy tắc phân bổ/giá vốn, kiểm chứng từ và cấu trúc import; agent đối chiếu estimate–actual và ngoại lệ | Quyền người phê duyệt vẫn riêng; thử import trong plan giao An, không cấp cho mọi agent |
| **Namfon** | Danh mục/giá/phân bổ theo kế hoạch; chi phí và bảng giá ALC và đối chiếu phiếu nhập theo plan; agent nối actual được phép với lô/đơn/hàng/kho | Không suy tên trong map là đang nhận mọi phiếu chi phí hoặc làm chủ toàn bộ nhập kho/công nợ |
| **Hiền** | Kế toán/thuế/tồn SGVC; chuẩn bị chứng từ và backup khai quan | Lý thường khai, Hiền backup; không tự kích hoạt người thay hoặc suy có máy là đang trực |
| **Sang** | Đại diện SGVC, quỹ SG, chứng từ chi VN; agent cung cấp/đối chiếu invoice–đơn–lô đúng phạm vi | Không suy quyền ký thầu BV Lào từ vai đại diện SGVC |
| **Laty** | Quỹ Lào, UNC/bằng chứng trả; agent nối payment proof→NCC→đề nghị→đơn/lô, kiểm thiếu reference | UNC có thể gộp NCC, không mặc định một UNC một đơn; không tự retry/chuyển tiền |
| **Duy** | OTC với Lý; tối ưu mã và duyệt giá OTC theo plan; agent kiểm/chuẩn bị quyết định giá có nguồn | Vai nghiệp vụ không tự chứng minh quyền máy ảo hoặc quyền ký/nộp thầu |
| **Quốc** — bổ sung 28/10 | Duyệt giá SPM theo B2/Q6; agent nhận gói giá–lý do–tác động và lưu quyết định đúng phiên bản | Không suy quyền ký/nộp từ quyền duyệt giá trên app |
| **Aiy** — bổ sung 28/10 | Tối ưu mã SPM cùng Hoa/nguồn nghiệp vụ; agent đánh giá cặp mã giữ/gộp | Không phải người duyệt giá SPM; quyền đó được plan tách cho Quốc |
| **NAE** — nguồn B6 ngày 28/10 | Kho nhận OTC; agent đối chiếu đơn–thực nhận–chứng từ và trả receipt theo phạm vi | Phân công tài liệu, chưa kiểm ACL/runtime/nhận việc thật; không tự xác nhận hàng đã nhận |
| **Vylayphone** — nguồn B6 ngày 28/10 | Kho nhận HC; agent nối số lượng/biến thể/lô/hạn/ngoại lệ tới người dùng đầu ra | Không suy quyền trên mọi kho hoặc hàng thầu từ nhãn HC |
| **Khem** — nguồn B6 ngày 28/10 | Kho nhận SPM; agent nối receipt vật lý và dữ liệu kho/đơn theo case | Không lấy lịch sử workbook Kho làm tồn hiện hành hoặc đã nghiệm thu |

**Các điểm phải có trong mạng nhưng chưa đủ tên/phạm vi từng case:** xe/tài xế/điều phối (chuyến, điểm giao, POD và chi phí); chuyên môn/đăng ký sản phẩm (đúng thương phẩm/giấy/tương đương); người đại diện CEO nhánh thầu (chỉ khi có ủy quyền thật). Chúng có nguồn và hoạt động hiện hữu, không phải mặc định phải tuyển người hoặc dựng hệ thống mới.

**Ngoài 14 tên đã trích từ map v10 ngày 12/10:** Sơn là đầu mối workbook báo giá theo nguồn thầu; Oanh cùng việc Kho/quy trình theo hội thoại; Dũng đang điều phối nghiên cứu/test/phát triển. Giữ các liên hệ này trong case, không nói map đã chứa họ hoặc tự gán toàn bộ vai CEO. Công việc ngoài thầu quanh mỗi người chưa phân tích lại trong bản lite này.

**Bằng chứng nhân sự không đồng nghĩa xác nhận triển khai.** Nguồn AS-IS đầu tháng còn một số phân vai cũ; ACK Linh 29/10 và kế hoạch 28/10 được dùng đúng phạm vi để sửa, không áp một nguồn lên mọi đơn.

### Đã có thiết kế cho nhân viên; cần nối vòng, không bắt đầu lại

Hướng dẫn 28/10 đã mô tả sáu việc cho Claude của nhân viên: so mã MISA/app; tìm đủ dòng giá bị bỏ; đề xuất mã trùng; rà giá theo kênh; bổ sung NCC; bổ sung thông số hàng. Đây không phải khoảng trắng chỉ có CEO. Agent có thể đọc/đếm/so/tìm đầy đủ và chuẩn bị kết quả, còn tài liệu hiện tại vẫn để người có tên quyết và thao tác app. Cờ lệch giá >2% hoặc quá sáu tháng là điều kiện rà, không tự cấp quyền đổi/duyệt giá.

**Quy tắc mã hiện hành theo nguồn 28/10:** mã nội bộ MISA là gốc; sửa/gộp phải sửa MISA rồi xuất và nạp lại danh mục cùng giá. Y19 trong map cutoff 26/10 còn mô tả tạo trên app trước là nguồn cũ, không áp nguyên xi. MPSC vẫn là mã trong hồ sơ thầu, cần mapping sản phẩm/UOM/phiên bản tới mã nội bộ; không thay hai loại mã bằng một khóa tùy tiện.

**Tái dùng nghiên cứu agent đã có:** AI-ERA v3 ngày 14/10 đã có domain người + Claude + nguồn + contract, hash/view đối chiếu và khu chung/nhạy cảm; P0 chỉ Dũng, inbox đa người thuộc P1. Baseline NCC `R-NCC-BASELINE-2026.10.21.1` đã có terms/quote/delivery/event/exception/freight và acceptance N01–N27. Receipt KIM LÝ ghi **MAPPED**, chưa TECHNICALLY_VERIFIED đầy đủ và chưa OWNER_ACCEPTED; một số unit pass lịch sử không thành onboard đã xong. Tái dùng contract/provenance và tiêu chí, không bê nguyên một-writer/P0 sang mạng nhiều chủ hoặc phục hồi mod WhatsApp đã archive.

Hướng dẫn yêu cầu dùng Claude công ty cho file MISA, không chuyển raw MISA sang tài khoản cá nhân/ChatGPT/công cụ miễn phí. Lượt nghiên cứu này chỉ đọc hướng dẫn và báo cáo audit, không đọc raw MISA.

Quyết định 23–26/10 đã thay đổi một số gate mua/nhập/hải quan trước đó. Vì vậy cần pin đúng nguồn quyết định khi kích hoạt mission, không dùng toàn bộ thiết kế cũ như policy mới.

### Quyền hiện tại là một điều kiện thiết kế, không lý do dừng A

[Hướng dẫn Claude nhân viên v2 ngày 28/10](https://docs.google.com/document/d/11MiJ_XVCQA7IDs8coDhYsHeIroosKTEV/edit) quy định Claude đọc/so/chuẩn bị, người có tên tự quyết và bấm app; không đưa mật khẩu cho Claude. [Kế hoạch v4](https://docs.google.com/document/d/1h0P86WXYO7y03lzhTCPoMX7qF7l4vZRM/edit) yêu cầu mỗi người đối chiếu bằng Claude của mình, không chờ CEO; phương án cũ còn nêu người chưa có Claude nhờ đồng nhóm. Điểm chưa rõ này đã được xác nhận mới của Dũng thay thế: mỗi thành viên có một agent Claude, không hỏi lại Q8 cũ.

Vì thế A phải chỉ ra **điểm người còn chạm tay và vì sao**, không hứa tự cập nhật app. Đích giảm thao tác tay vẫn giữ, nhưng thay đổi quyền là việc riêng trước thực thi, không tự xảy ra vì thiết kế đã viết xong.

## 5. Hồ sơ bốn BV đã đọc: khác biệt nào làm thay đổi công việc?

Đã đọc 12/12 workbook NNC bổ sung và 4 cover. Hai file thuốc trả text rỗng được đọc từ bytes XLSX, không coi là không có dữ liệu. Bộ này chứa biểu mẫu, spec, thông tin sản phẩm và tham chiếu nội bộ, **chưa phải bộ HSMT đầy đủ được xác nhận**.

| Nội dung | Mahosot | Settha | Me and Dek | SVNK |
|---|---|---|---|---|
| Hạn trên cover nội bộ |25/11/2026|26/11/2026|27/11/2026|Chưa có|
| Cơ sở hạn chính thức |Chưa đọc thông báo phát hành|Như trái|Như trái|Chưa xác định|
| Giá giao |Kho Mahosot, kip|Kho Settha, kip; bản VTTH có cột kho công ty riêng|Kho BV Mẹ và Trẻ sơ sinh, kip|Kho BV tỉnh và BV huyện toàn tỉnh Savannakhet, kip|
| Cấu trúc cần giữ |Annex nhu cầu/giá và thông tin sản phẩm|Lot theo tên file, Annex từng nhóm|Thuốc Annex02 là thông tin; HC/VTTH Annex02 là phân phối|Bảng chào gộp thông tin + sheet phân phối|
| Phần chưa đủ |Chấm dòng/lô, tương đương, bảo lãnh, phiên bản cuối|Như trái|Như trái|Như trái + hạn chính thức|

Cover Settha/MeDek ghi chuẩn bị trước 25/11 gắn với đề nghị Phét nghỉ 26/11–01/12. Audit mới chưa thấy duyệt nghỉ trong phạm vi nguồn; không coi đã nghỉ hoặc tự gán người thay. Đây là tín hiệu lập kế hoạch nội bộ, không thay hạn pháp lý.

### Các điều kiện cụ thể phải đi vào năng lực agent

**Giao đa điểm SVNK:** [thuốc SVNK](https://docs.google.com/spreadsheets/d/1DGbtss7BjgMfLCNtQkC1YAeVyEIIPIIQ/edit), sheet `ສະເໜີລາຄາ!G1` nêu kho tỉnh/huyện; sheet `ແຜນແຈກຢາຍ!H1:W1` có 16 cột: BV tỉnh + 15 địa bàn. Ví dụ dòng 4, Soda lime MPSC01Aa00800, tổng G4=7; H4=5 và M4=2. Agent logistics phải giữ điểm đến/route, lượng, điều kiện bảo quản và người nhận; BidOps phải tính kịch bản chi phí nhiều điểm. Chưa có lịch giao/số đợt/phạt/thanh toán nên không chốt contribution chính thức.

**Đăng ký khác hạn dùng:** [MeDek thuốc](https://docs.google.com/spreadsheets/d/19RffHeQJrwC9W86pM4fzPuppUDa1eeU5/edit), `Annex02!M3:N3` là số và hạn đăng ký, không phải hạn dùng lô hàng. Agent phải kiểm đúng loại chứng từ/thời hạn, không lấy ô có chữ/số làm đủ pháp lý hoặc đủ shelf life.

**Biểu mẫu và bộ hồ sơ:** ghi chú MeDek thuốc ở `ຄຳແນະນຳເພີ່ມເຕີມ!B4:B9` và đối chiếu [Settha VTTH](https://docs.google.com/spreadsheets/d/1gwp1rehqrYVTrzcvhy1kOz_I3mWkH06f/edit) cho thấy: ghi nhãn USB theo phần/lot và công ty, đánh dấu các phần hồ sơ, điền đủ dòng chào, giữ nội dung danh mục/đơn vị/layout, tách USB thuốc–HC–VTTH. Đây chưa cho biết giá trị/hiệu lực bảo lãnh hoặc chấm toàn lô/từng dòng. Yêu cầu điền từng dòng không chứng minh được quyền chọn lẻ.

**Tệp 2027 có tab cũ:** [Mahosot VTTH](https://docs.google.com/spreadsheets/d/15tKHHkRw4eVstlVxIHiKYbVy_qI-zn5n/edit), đoạn trích 4 là tiêu đề 2024 và cột giá mua/GV/lãi/HH/VAT; đoạn 3 là Annex 2027. [Settha HC](https://docs.google.com/spreadsheets/d/1XRDLOcRMkph65uN5XQc1H08yJrO7Pp90/edit) có đoạn 5 tiêu đề 2023, phần Annex2 header nhu cầu 2026. Chưa có tên tab/toạ độ ô xác thực cho hai file này; không giả địa chỉ. Không tự đổi năm hoặc dùng giá/thuế tham chiếu làm giá hiện hành.

### Ca Mittaphab: giá đã có nhưng chứng từ còn phải nối phiên bản

Kiểm lại ba workbook gốc local cho thấy: thuốc có 72 dòng giá chào dương, trong đó 51 dòng số đăng ký trống/lỗi và 57 dòng hạn đăng ký trống/lỗi; HC có 95 dòng giá dương, 17 thiếu tiêu chuẩn kỹ thuật công ty; VTTH có 616 dòng giá dương, 488 dòng “mã/tên khác” trống. Đây là **kết quả kiểm ô, chưa xác định tất cả trường bắt buộc**, không phải số dòng không hợp lệ.

Sáu dòng Visa có ngày trong file trước 04/11 được nối theo tên hoạt chất/generic tới dòng có giá chào. **Đây chỉ là ứng viên đối chiếu, chưa xác minh cùng thương phẩm, nhà sản xuất và quy cách.** Không gọi là sáu giấy phép đúng sản phẩm chào đã hết hạn:

| Mã MPSC | Neo trên sheet Visa: tên / số / hạn | Dòng Annex 1 | Hạn ghi trong file |
|---|---|---|---|
| MPSC09Be00202 | B8 / M8 / N8 | 81 | 06/06/2026 |
| MPSC09Bh00101 | B9 / M9 / N9 | 83 | 18/04/2026 |
| MPSC09Ga00102 | B11 / M11 / N11 | 101 | 13/08/2026 |
| MPSC14Ca01100 | B14 / M14 / N14 | 148 | 18/04/2026 |
| MPSC18Aa01202 | B16 / M16 / N16 | 205 | 31/03/2022 |
| MPSC24Ba00101 | B19 / M19 / N19 | 275 | 16/05/2025 |

Đọc sâu còn thấy mâu thuẫn nhận diện ngay trong nguồn:
- Visa dòng 11 ghi Medskin Clovir 800/DHG, nhưng Annex 2 H100/K100 ghi Acyclovir 800mg Kharpharco/Kharpharco; cùng chép số 02I4893/20 và ngày 13/08/2026. Cùng số/ngày chưa giải được khác thương phẩm/nhà sản xuất.
- Visa dòng 16 ghi Ausmezol/HATINH, trong khi ghi chú Q trỏ Visa Omeprazole DHG.
- Visa dòng 19 ghi ACENEWS/120 AMEPHACO, ghi chú Q trỏ Visa Mitux; tên B19 ghi gói 5g nhưng J19 và Annex 2 J274 ghi 30 gói 2g.

- Levofloxacin có cùng số đăng ký 07 I5570/23 nhưng bản local là 750mg/150ml, hạn 06/06/2026; [FDD record 1975](https://fdd.gov.la/drugreg/drugreg_view.php?id=1975) ghi 500mg/100ml, chai 100ml, hạn 06/07/2026. Cùng nồng độ không chứng minh cùng biến thể đăng ký; không tự sửa ngày hoặc dùng giấy của chai 100ml cho chai 150ml.

Đối chiếu công khai cho biết [record 2012](https://fdd.gov.la/drugreg/drugreg_view.php?id=2012) của số 02 I4893/20 là MEDSKIN CLOVIR 800/DHG, chủ giấy NNC, củng cố danh tính trên Visa chứ không chứng minh áp dụng cho Kharpharco. [CARDIONID record 1955](https://fdd.gov.la/drugreg/drugreg_view.php?id=1955) và [chloramphenicol Ciron record 1957](https://fdd.gov.la/drugreg/drugreg_view.php?id=1957) phù hợp các trường nhận diện lịch sử đã đối chiếu. Không tìm được record đúng Ausmezol/ACENEWS trong lượt tìm hẹp không có nghĩa sản phẩm không đăng ký.

**Giới hạn quan trọng:** [danh sách FDD](https://fdd.gov.la/drugreg/drug_registration.php?page=68&search=) ghi cập nhật 26/12/2025. Đây không phải bằng chứng trạng thái gia hạn hiện hành ngày 31/10/2026. Chưa có chứng từ gia hạn mới được kiểm trong lượt này; không kết luận sáu sản phẩm bị loại hoặc giấy phép hiện tại hết hiệu lực.

Agent hồ sơ phải **xác minh nhận diện sản phẩm trước**, rồi mới nối đúng giấy phép, phiên bản, gia hạn và ngày áp dụng. Dữ liệu cần giữ riêng: hoạt chất, thương phẩm, nhà sản xuất, hàm lượng/dạng, đóng gói, số đăng ký và tài liệu chứng minh. Một số đăng ký được chép sang bảng khác không tự là bằng chứng cùng sản phẩm. Đầu ra phải tách bốn trạng thái: khớp danh tính lịch sử; mâu thuẫn danh tính; chưa có nguồn hiện hành; đã có chứng từ hiện hành kiểm được. Sau đó tìm chứng từ gia hạn đang có và chỉ ra phần thiếu cụ thể. Không hỏi chung “có hồ sơ chưa”, không kết luận giấy phép hiện tại hết hạn từ một file cũ, không mặc định đã gia hạn. Đây là ca đối chiếu để thiết kế năng lực, không nhận lại việc Mittaphab của người đang phụ trách.

## 6. Bốn vòng công việc cụ thể: từ nguồn và trao đổi đến đầu ra được dùng

### Vòng 1 — Có giá mới, thiếu nối nguồn hoặc chưa áp dụng

Đối chiếu [workbook Sơn](https://docs.google.com/spreadsheets/d/1PkIIemg0l3OKJfZTRIBL_XtMQ0Qcpd9T/edit?gid=789105477), mốc sửa 30/10/2026 16:52:37 VN:
- Summary có 53 dòng/53 mã MPSC; hai phần summary trích giống nhau không được đếm thành 106.
- Cột chọn NCC ghi Jundamed 33, Yangzhou 11, Sunshore 7, Henan 2. Phạm vi này là summary 4 NCC, workbook còn film/thuốc; không dùng nó bác lời tổng hợp 53 mặt hàng/6 NCC khi phạm vi khác nhau.
- **Cotton Ball + Acool, MPSC04MD01600**, phần tổng hợp STT 33 có giá chọn 2.190 kip/Jundamed, nhưng 4 cột ứng viên trống và countNCC=0. Phần JUNDAMED FOB QUẢNG CHÂU MTP2027 LOTIII, STT 48 có giá 2.190 thật. Đây là lệch truy vết/tổng hợp, chưa chứng minh lỗi formula vì chưa đọc công thức.

[Catalog VTTH thực trong bộ đã chia sẻ](https://drive.google.com/file/d/1_Vmfsd03b83FGSHrXDcKmGja38WeTrQB/view), tạo và sửa 29/10 lúc 15:22 VN trước tin chia sẻ 15:32, có nội dung trích bằng bản lưu trữ đã đọc. Catalog map Cotton thành VT-0101: MTP dòng 114/120.000, MeDek dòng 40/6.000, Mahosot dòng 137/20.000; snapshot đó còn “Tìm nguồn”. Nguồn Sơn 30/10 mới hơn gần một ngày: không chứng minh giá đã có khi tạo/chia sẻ catalog, cũng không chứng minh cả ba bản đích đã áp/duyệt sau đó. Đây là vòng cập nhật cần kiểm theo thời gian, không quy lỗi bản 29/10 bằng nguồn ngày sau. Không cộng tổng nhu cầu 146.000 thành nghĩa vụ mua, hoặc tự áp mức giá của nguồn đang tính trên lượng 120.000 cho toàn bộ nhu cầu.

**Vòng agent phải hoàn thành trong đích thiết kế:**
1. Hiểu tin gửi để báo nguồn, thay giá, hỏi ý kiến hay yêu cầu rà; đọc chuỗi và file liên quan.
2. Tìm nguồn đã có, đối chiếu mã/spec/UOM/đóng gói/chi phí/phiên bản; phân biệt thiếu nguồn và thiếu liên kết.
3. Chuẩn bị diff cụ thể, kèm nguồn chi tiết và bản đích. Theo quyền hiện hành, người giữ bảng quyết/ghi; agent không giả đã sửa.
4. Bên nhận kiểm đúng các dòng, trả kết quả áp dụng/chưa áp/lý do và đọc lại để kiểm chứng.
5. Bên làm hồ sơ dùng vào bước sau; BidOps nhận tác động tới phạm vi/giá/tiến độ. Đến đây mới đóng vòng, không chỉ “đã gửi”.

Agent ở người giữ nguồn/bảng xử lý phần thuộc mình; CEO/BidOps vẫn có thể trực tiếp nghiên cứu, so và lập phương án ở nhánh đã nhận dù có nhân viên. Hai bên nối kết quả theo phiên bản, không tranh ghi cùng đầu ra. Tiêu chí bằng chứng không đổi theo cấp bậc.

### Vòng 2 — Cùng mã, khác spec; giá mua thấp chưa phải giá vốn thấp

53 mã MPSC nối ra 54 dòng catalog chung. Cùng **MPSC02MD00102**:
- **VT-0094:** Catgut chromic No.2/0, kim 40mm, 1/2 Circle Round Bodied, chỉ 75cm; MTP/SVNK/MeDek.
- **VT-0527:** kim 30mm, 3,5 metric, EP3; Settha. Cột “Cần xem lại” đã cảnh báo khác kích cỡ/hàm lượng so với hàng đang có.

Đọc logic local thấy nhánh `match_quotes:263–265` nhận quote có mã bằng code-only; `build_master.py:312–317` lại cấp TH/HC/VT theo số thứ tự sau sắp xếp. Vì vậy không chỉ có rủi ro lý thuyết: phải kiểm nhánh nối quote và giữ neo nguồn khi đầu vào thay đổi, nhưng chưa kết luận toàn bộ matching sai.

Agent không tự sao giá 40mm sang 30mm vì mã trùng. Đầu ra phải mang **BV–gói/lot–dòng–mã nguồn–spec–UOM–phiên bản–khác biệt–người dùng**. Năng lực dùng chung có thể phát hiện/đề xuất map; người hoặc nguồn chuyên môn có thẩm quyền xác nhận đúng case. Bên nhận phải nghiệm thu đúng yêu cầu của mình, không chỉ tin một agent khác đã trả “matched”.

Nguồn Sơn còn cho thấy roll pouch 100mm: Jundamed 6,2422 USD nhưng cost 220.200 kip; Yangzhou 6,9489 USD nhưng cost 161.550 kip. Đây là số trong workbook, chưa xác nhận quote/carrier còn hiệu lực. Hệ quả: so giá mua rẻ nhất không đủ; node cần năng lực ghép cost từng chặng, BidOps nhìn kinh tế toàn phương án. Các packing note không khớp rõ phải truy định nghĩa/quote/formula trước kết luận sai hoặc sửa.

**Phân biệt giá vốn và giá chào bằng nguồn thật:** SCHEMA local xác định BV150 là Mittaphab. Ca Etomidate: `Giá NNC!M37` là giá vốn 64.000; `Giá NNC!R37` và `Annex 1!G6` là 110.300. Không cần hỏi lại chuẩn giá vốn từ đầu, cũng không lấy giá chào làm giá mua. Quy tắc kế thừa lựa chọn của Phét ở Mittaphab không tự là phê duyệt hãng/NCC cho mọi BV.

**Không kế thừa nghĩa rộng của “done”:** `build_master.py:307` gán done khi ghép giá vốn; `kom_build.py:18,65` dùng done cho “Có giá năm trước”; đó là nhãn dòng giá, không phải phân loại gói Komsenahak là lịch sử hoặc đã hoàn tất. Kiểm đầu ra thật: Mahosot HC `Annex1!O39` là “Đã có giá”, `X39` trống; Settha HC `Annax1!S32` là “Đã có giá”, `AB32` trống. Cả hai có cảnh báo giá tỉnh trong file Mittaphab lỗi. Tổng 40 lượt dòng BV mang done thiếu Giá 2 không có nghĩa 40 SKU thiếu giá bắt buộc: phải xét điều kiện giao từng gói. Agent cần tách có giá nguồn, khớp hàng, giá áp dụng theo tuyến, chứng từ, phê duyệt và đã được dùng.

### Vòng 3 — Linh gửi Sharma, Phét up rồi nhờ kiểm

Chuỗi 29/10 đã đọc cho thấy: Phét đưa list thiếu giá; Linh nói đã gửi Sharma và hỏi đã up chưa; Phét nói đã up, rồi nhờ Linh check chỗ trống. Phải tách:
- **Đã gửi theo lời người gửi:** chưa xác định exact attachment/version.
- **Đã up theo lời người xử lý:** chưa có diff hoặc phiên bản đích chứng minh nội dung.
- **Yêu cầu review:** chưa bằng chứng review xong.
- **Phê duyệt hoặc dùng trong hồ sơ cuối:** chưa có bằng chứng trong chuỗi này.

Catalog có 371 dòng chứa SHARMA/“Đã có giá”, trỏ 320 chuỗi nguồn; nhiều dòng là dữ liệu tham chiếu/giá NNC cũ. Trùng tên Sharma không đóng được lỗ hổng exact quote/version. Không nói hai người mâu thuẫn, chưa ai gửi, hoặc yêu cầu gửi lại tất cả.

**Thiết kế tác nghiệp:** agent tại người giữ nguồn tìm exact quote; agent giữ bảng tìm phiên bản đã up; đối chiếu phần đã vào/chưa vào/spec khác; phía được nhờ review kiểm và trả receipt; BidOps theo tác động. Chỉ khi cần thông tin mới thật mới hỏi đúng người một phần cụ thể.

Nguồn: [trích Sharma/Phét](https://drive.google.com/file/d/15oeQJ3MMFz91rFBsPcJmY9XjgPsbJBwG/view), [phản hồi nhóm](https://drive.google.com/file/d/1c_7lTpunHJIUyiGssZjveH5H7JYNPOD7/view). Đây là snapshot, chưa đọc chat riêng hoặc bản cuối hiện tại.

### Vòng 4 — File chia sẻ còn phụ thuộc nguồn ở máy chủ dữ liệu

**Nguồn local chưa bị mất:** đối chiếu 22 file originals ở ba vị trí đã ghi — nguồn/Downloads, BidOps originals và packet originals — đều tồn tại và khớp SHA256 manifest. Sáu ZIP có 22 thành phần, toàn bộ khớp byte với output local hiện giữ. Phạm vi bốn gói + catalog là 20 file; Mittaphab riêng hai file. Điều này chứng minh bộ local được bảo toàn, không chứng minh người nhận đã dùng nó hoặc Drive current là cùng bản.

Tin 29/10 lúc 15:14 là lời báo gửi ZIP, không phải receipt nhận ZIP. Đến 15:32 Dũng nói ZIP không gửi được vào nhóm và gửi lại link Drive. Vì vậy phải lấy đúng bản Drive tại lúc chia sẻ làm một baseline riêng, không đồng nhất Downloads/ZIP/archive với bản người nhận tiếp tục sửa.

Audit đúng [thư mục Thau BV đã gửi](https://drive.google.com/drive/folders/1IUDLUmc-xC1O_dJpMeRJJQN5qvR-RMy_) xác nhận 20 XLSX trong năm thư mục. Ba catalog chỉ có một revision được trả, tạo/sửa 29/10 lúc 15:22 trước tin gửi 15:32. Lịch sử revision không cho biết ai đã xem/tải; không nói “không ai đụng tới”.

[VTTH Mahosot trong bộ chia sẻ](https://drive.google.com/file/d/1TFYpDOehC2B9Z2cxTD_0OV7UjnUTxGvd) có revision trước gửi 15:26 và sau gửi 19:10 ngày 29/10. Bản sau có 2.426 giá trị cache `#REF!` và 35 `#DIV/0!` trong `Gia NNC`; `Annex1` không thấy các lỗi này. Công thức vẫn chứa hai tham chiếu workbook local, không phải bị thay bằng literal `#REF!`. Ví dụ `Gia NNC!G1071` lấy giá từ workbook `[2]Xương Khớp`; cache lỗi lan sang `K1071` và `O1071`. Bản trích revision trước gửi không có lỗi tương ứng. Chưa xác định người gây ra, app đã tính lại hay công thức cũ/mới khác thế nào.

**Đối chiếu raw local làm rõ thêm, nhưng không cho phép phục hồi giá mù:** cả file Mahosot gốc và output local giữ `Gia NNC!G1071=8`, `K1071=186000`, `AB1071=#N/A`, khác cache `#REF!` của Drive current. Sheet local vốn đã có 39 `#DIV/0!`, 1.256 `#N/A` và 16 `#VALUE!`; không gọi baseline local sạch lỗi. Đối chiếu 36.783 cell giữa gốc và output local giữ cell type, formula text và cache, nhưng ba shared-formula ref-range ở O368/L1356/N1356 khác nhau. Chưa kiểm tác động sau tính lại, không nói toàn bộ công thức giống tuyệt đối hoặc toàn sheet byte-identical.

Chưa có raw hash của revision Drive trước gửi để chứng minh output local chính là revision đó. Bằng chứng hiện tại cho phép phân biệt các bản, chưa xác định nguyên nhân hay người sửa. Cache số còn ở local không phải quote hiện hành hoặc quyền dùng giá cũ; không tự lấy 8/186.000 phục hồi vào production.

[VTTH SVNK trong bộ chia sẻ](https://drive.google.com/file/d/181PmA0LkOnPClEUHPz8Kf22z5CGCj8Ve) có revision 18:46 sau gửi, nhưng giá trị trích hai bản giống nhau; thay kích thước/version chưa chứng minh thay giá. Không ghi đè hoặc rollback các sửa đổi chưa hiểu.

**Tác động kiến trúc:** nguồn ở máy riêng người giữ dữ liệu là trạng thái bình thường, không có trong workspace này không có nghĩa bị mất. Agent cần nguồn phải yêu cầu agent chủ nguồn kiểm file/phiên bản trong quyền rồi trả kết quả được phép chia sẻ. Tách nguồn mới sau baseline, nguồn chưa được chia sẻ, lỗi cache/link và lỗi mapping thật; không giao lại người việc sourcing đã có.

Trước cập nhật phải so baseline–bản local hiện tại–bản chia sẻ hiện tại theo field/phiên bản, giữ xung đột cho đúng owner. Có thể đề xuất đầu ra tự chứa giá trị/bằng chứng tại mốc phát hành trong khi giữ workbook tác nghiệp và lịch sử, nhưng không tự nhúng quote riêng, bỏ link hay tính lại production. Lỗi `Gia NNC` không tự chứng minh giá nộp ở Annex sai; cần nối đúng phụ thuộc và bên dùng nhận kết quả.

**Cơ chế cập nhật đề xuất đã có kiểm thử logic hẹp:** proposal chỉ ghi field đúng owner, giữ nguồn/phiên bản và lý do; trước apply phải so cả baseline lẫn giá trị cell hiện tại. Có sửa đồng thời thì giữ WIP của owner và sinh lại proposal, không overwrite. Một writer cho cùng master ở một thời điểm không có nghĩa CEO sở hữu mọi master: các node khác trả proposal/receipt cho node chủ bảng.

Fixture tổng hợp đã đạt **10/10 tình huống**: không ghi trước review; chỉ field thuộc quyền; retry không nhân đôi; baseline cũ dừng; field của chủ khác dừng; mã giống nhưng variant khác không nối; nhận diện mơ hồ dừng; thiếu provenance dừng; sửa đồng thời bị phát hiện dù marker chưa đổi; tái tạo proposal vẫn giữ WIP. Đây là synthetic in-memory, không mở workbook thật, không kiểm ACL/live transport và không triển khai pipeline. Kết quả này bổ sung kiểm logic, không thay test hai Claude hoặc bằng chứng mạng nhân viên thật.

## 7. Những vòng việc không được khuất sau giá và file

### Nghiệp vụ thầu phải nối thị trường và kênh mua hàng

Nguồn công khai cho thấy nền dịch vụ có thay đổi: Mahosot khánh thành tòa nhà mới năm 2024; dự án nâng cấp Setthathirath/Champasak giai đoạn 2018–2025 đã kết thúc. Đây là tín hiệu để CEO và agent phát hiện nhu cầu/quan hệ/sản phẩm cần khảo sát, **không phải bằng chứng số lượng thuốc mua hoặc doanh thu sẽ tăng**. [Nguồn Mahosot](https://english.www.gov.cn/news/202410/13/content_WS670af2ebc6d0868f4e8ebc78.html), [nguồn JICA](https://www.jica.go.jp/oda/project/1760500/).

Một BV có thể đồng thời có thầu thường niên, gói thiết bị do nhà tài trợ và nhu cầu dịch vụ/bảo trì; người mua pháp lý, bên trả tiền, nhóm hàng và điều kiện khác nhau. Kết quả LuxDev 2026 cho thấy có nhiều nhà cung cấp trong gói thiết bị bốn BV tỉnh, **không xác định đối thủ hoặc giá thắng của đúng bốn gói 2027 NNC đang làm**. Agent cơ hội cần khóa đúng bên mua–BV–kênh mua–mã gói–năm–lô–phiên bản trước khi nhập dữ kiện cạnh tranh. [Kết quả LuxDev](https://luxdev.lu/en/tenders/call-tenders/procurement-medical-equipment-four-provincial-hospitals-lao-pdr-goods).

Báo cáo World Bank tháng 6/2026 ghi nhận biến động nhiên liệu và khó khăn dòng ngân sách y tế. Đây là lý do phải tái kiểm giá theo tuyến và điều khoản thu–chi, không phải căn cứ kết luận một BV đang chậm trả NNC hoặc áp tỷ lệ tăng chung lên mọi mặt hàng. So qua các năm phải tách thay đổi lượng, cơ cấu sản phẩm, đơn giá, tỷ giá, chi phí giao và thời gian tiền về; chưa đủ dữ kiện thì giữ chưa rõ, không điền 0. [World Bank](https://www.worldbank.org/en/country/lao/publication/lao-economic-monitor-jun-2026-consolidating-reform-momentum-amid-volatility-key-findings).

### Giá thấp nhưng chưa có đường thắng
Câu hỏi Oanh và phản hồi Phét về BV không dùng hàng NNC là đầu mối cần nối theo dòng/BV, không phải kết luận nguyên nhân duy nhất. BidOps phải ghép yêu cầu/cách đánh giá, lịch sử, hãng/nguồn có thể chào, chứng cứ chất lượng/giao, kịch bản giá/vốn. Không tự giảm giá, thay hãng hoặc giả xác suất thắng. Chưa có HSMT đầy đủ thì giữ kết luận phụ thuộc điều kiện, vẫn nghiên cứu phần độc lập.

### Giao hàng, tiền và quan hệ bên ngoài
Linh có năng lực xuyên NCC–packing–route–cước–ETA; từng carrier/kho/kế toán giữ các fact khác nhau. Trong case đã được Linh xác nhận, Lacco do Linh trao đổi, Trang chuyển ảnh/phiếu ALC Vinh, Linh báo kho Lào; Mee là đầu mối tra soát nếu có UNC mà NCC chưa nhận. Mee không thành người duyệt chi, agent không đổi beneficiary hoặc retry thanh toán theo chat.

Agent cần đọc câu trả lời, hiểu vì sao gửi, hỏi phần còn thiếu qua kênh được phép, theo mốc và cập nhật bên phụ thuộc. Chỉ gửi lời nhắc rồi giao con người làm hết vẫn chưa đạt đích. NCC/carrier không cần có agent; mạng phải làm việc được qua kênh đang dùng.

Nguồn họp ASR 28/10, đoạn #466–484, còn bàn giá Sama năm trước, cập nhật ước lượng cước, đường bay/Lacco/biển và CIF tới Viêng Chăn. Đây là nội dung trao đổi chưa duyệt, không tự gán người nói hoặc coi CIF là điều khoản ký. Nó cho thấy agent phải nối **giá mới → đúng hàng/NCC → cước áp dụng → giá chào → người nhận dùng**, không chỉ gom file.

Lịch sử ALC local giúp tìm đúng đầu mối: sheet `ALC_NNC` dòng 449 ngày 04/03/2026 ghi 18 thùng White Lotus/ALC Vinh, Ms Trang; dòng 522 ngày 22/03 ghi 164 thùng, Ms Lý. Header là **ngày giao ra kho ALC**, không phải giao BV. Hai bản local chỉ tới tháng 5: dùng để truy lịch sử nguồn/tuyến, không chứng minh tồn kho, năng lực giao tháng 11, hạn thanh toán hay vốn hiện có.

### Nhiều gói và nhánh khác cùng tranh nguồn lực
Các node có thể làm rất tốt từng báo giá nhưng tổng cam kết vượt vốn, nguồn hàng, coldchain hoặc đội giao. Năng lực CEO là nhìn kịch bản liên gói và đơn ngoài thầu; không lấy mỗi gói đạt riêng suy tất cả đạt đồng thời. Agent node báo fact/cam kết thật, không tự coi toàn capacity là đã dành cho mỗi case.

### Hàng — chứng từ — tiền, từ giá chào đến lãi/lỗ

Ba dòng phải nối cùng một case nhưng có chủ sự thật khác nhau:
- **Hàng:** sản phẩm/biến thể, số lượng, nguồn, tồn/lô/hạn dùng, giữ hàng, shipment, điểm giao, lượng nhận/thiếu/hỏng. Kho và vận chuyển giữ bằng chứng hiện trường, không lấy planned shipment thành đã giao.
- **Chứng từ:** hồ sơ chào, giấy đúng thương phẩm, đơn/PO/hợp đồng, packing/phiếu kho, giao nhận/nghiệm thu, hóa đơn và giấy yêu cầu thanh toán. Có file khác đúng hàng/đúng lần giao/đúng người chấp nhận.
- **Tiền:** giá vốn/giá chào/giá ký, cước và phân bổ, thuế/chi phí khác có căn cứ, lịch chi–thu, công nợ và actual. Kế toán giữ số đã hạch toán, không dùng estimate làm actual hoặc doanh thu ký làm tiền đã thu.

Trong ca SVNK giao tỉnh/huyện, agent giá yêu cầu agent vận chuyển phương án tuyến/đợt/điểm giao; agent kho trả lượng và điều kiện khả dụng; agent tài chính trả điều kiện chi–thu được phép cung cấp. Các agent trả dữ liệu có nguồn cho người lập giá, không buộc CEO thu từng file bằng chat. Chưa đủ actual vẫn có thể tính khoảng/kịch bản và chỉ ra độ nhạy, không giả một con số chắc chắn.

**Không phải chưa có đo:** [workbook Kho/Khem](https://docs.google.com/spreadsheets/d/11ubDlRARtR71bpum8Wh61L2D6moED7Mf/edit) có 26 tab, gồm `GH!A3:BD3`, `TT - CHECK IN T4!A3:AD3` và `TH- Giao bill T4!A1:P1`. Dữ liệu đã có giờ, người, nhóm hàng, bill/thùng, xe, km, trạng thái giao và nộp tiền. Bản này sửa 18/07/2026, không là tồn/đội xe live hôm nay. Done và nộp tiền là hai trường riêng; hệ số EU là điểm tải công việc, không tự là tiền hay tải trọng xe. `BANG_DIEM!D8=10 box/EU` khác tab cũ `ชีต18!D8=43`, cần giữ phiên bản khi so hiệu suất.

[Sheet chi phí xe](https://docs.google.com/spreadsheets/d/1BvtBFOhNGG2yjJGY8CGpADKJds4fukqS0KF6WlH0c-s/edit) không chỉ có sửa chữa: segment 13 có tiền xăng/công-tơ-mét; segment 14 có **129 khoảng đo**, segment 15 tổng hợp **15 biển xe**. Có thể dùng làm baseline sau kiểm, không bảo công ty chưa đo. Chưa xác minh currency, cấp xăng khác tiêu thụ đúng chuyến, và còn `#REF!` ở tổng hợp; không dùng số nhiên liệu/km làm chi phí toàn phần/km hoặc danh sách xe làm xe đang sẵn sàng. Các segment là neo bản trích, không giả địa chỉ ô.

[Bản đồ cung ứng v10](https://drive.google.com/file/d/1IZoR4FFomb-tZ3bCI4suJ2rNGyc7IkAF/view) đã có phiếu Excel chi phí chuyến ở A4b và công nợ ngoài AMIS ở Y8; G3 nói cước phân bổ ở phiếu nhập. Vì vậy ưu tiên nối nguồn hiện có, kiểm quy tắc được duyệt, không lập sổ công nợ hoặc mô hình kho/xe riêng cạnh tranh với app đang xây. Mốc chốt giá vốn 14–30 ngày là snapshot; mục tiêu tối đa 5 ngày chưa là kết quả đo đạt. Luồng xe lạnh thực phẩm không tự chứng minh cold chain thuốc.

Excel kho/kiểm soát xe đang có là điểm xuất phát. Cần đo được chi phí nào theo chuyến, theo km/giờ/điểm dừng hay theo đơn vị hàng, phần dùng chung giữa đơn và bằng chứng chi phí; tránh cộng hai lần cước đã nằm trong giá vốn. Lựa chọn cách phân bổ phải kế thừa quy tắc kế toán/công ty đã có hoặc ghi là phương án để người có quyền chốt, không tự ban hành. Sau giao, đối chiếu dự tính–actual–giá bán–thu tiền để thấy chênh lệch lãi/lỗ theo đúng tầng; không gọi chênh lệch giá mua/bán đơn thuần là lợi nhuận ròng.

**Đầu ra tài chính cần tách ba tầng:**
1. Lãi đóng góp theo gói/dòng/đợt/điểm giao: doanh thu thuần theo kịch bản trừ giá vốn và chi phí phục vụ biến đổi. Chỉ dùng lượng được gọi/giao/chấp nhận đúng trạng thái, không coi lượng Annex là đơn chắc chắn.
2. P&L toàn phần: thêm chi phí phân bổ được phê duyệt, mỗi chi phí chỉ tính một lần. Nếu AMIS đã đưa cước vào giá vốn thì không trừ lần nữa; không cộng các tiền tệ trước khi xác định tỷ giá/ngày.
3. Lịch tiền và đỉnh thiếu vốn: tách đặt cọc, trả NCC, cước/thuế, tiền giữ/bảo lãnh và tiền BV thực thu theo điều khoản thật. Không tự giả 30/60/90 ngày. Chạy cả từng gói và nhiều gói cùng trúng, không tính cùng tồn/xe/tiền là đủ cho mọi gói đồng thời.

Agent trả phép tính cùng nguồn/phiên bản/đơn vị/tiền tệ/thời điểm, phân biệt estimated–actual–approved–posted, phần chưa phân bổ và độ nhạy. Dữ liệu thuộc ai thì agent đó kiểm và trả phần cần thiết; quyết định giá, allocation, cam kết tiền hoặc điều xe vẫn theo người có quyền. Đây là hợp đồng tác nghiệp đích, chưa khởi chạy đối chiếu hoặc ghi nguồn production.

### Đúng bản chất vấn đề con người

Đã có kinh nghiệm, bảng dữ liệu, người phụ trách và công việc thực. Điểm nghẽn đã thấy là gửi nhưng chưa vào đúng bản, không rõ ai đang giữ bước tiếp, cùng tên khác hàng, nhãn done khác mục tiêu và thiếu xác nhận đầu ra được dùng. Không suy nhân viên kém năng lực. Năng lực agent cần bổ sung là đọc hiểu đầy đủ, tự tìm đúng nguồn, giữ việc mở và thúc đẩy các bên trong quyền, làm phần tác nghiệp đã có khả năng thực hiện.

Đo tác dụng qua thời gian từ tín hiệu đến đầu ra dùng được, vòng việc mở quá hạn, số lần hỏi lại thứ đã có, số lần người phải chuyển dữ liệu thủ công, lỗi/trùng phiên bản và tỷ lệ tác nghiệp được agent hoàn thành có kiểm nhận; không chỉ số tin nhắn, số task hoặc số agent online.


## 8. Tín hiệu phối hợp và Audit song song

Một thông điệp cần đủ ý nghĩa: ai gửi, case nào, nguồn/version nào, mục đích thực hiện/cung cấp fact/review/quyết định, đầu ra ai dùng, hạn và việc đang bị chặn. Không cần xây bus/portal mới để xác định hợp đồng công việc này.

Trạng thái tối thiểu phải phân biệt: **được đề nghị → đã nhận → đang làm → chờ fact/chờ quyết định/chờ bên ngoài → sẵn cho bên dùng kiểm → được nhận dùng/đóng → ngoại lệ**. Gửi, đọc, sửa file và hoàn tất mục tiêu là bốn điều khác nhau.

Audit chạy song song cần kiểm:
1. Đúng người/đúng vai, không dùng chức danh thay quyền.
2. Nguồn và phiên bản, giữ tab lịch sử khác hiện hành.
3. Mapping BV–dòng–spec–UOM, không chỉ mã chung.
4. Giá nguồn, cost dự kiến, giá được duyệt, actual là các số khác nhau.
5. Không đếm trùng nguồn/capacity/vốn giữa gói và nhánh khác.
6. Tin yêu cầu rà/ACK khác review done/approval/used.
7. Quyền nguồn và liên lạc, không hút toàn chat cá nhân để CEO xem.
8. Bằng chứng người dùng đầu ra chấp nhận, không chỉ task Done.
9. Thay đổi nguồn/điều kiện nào làm phải kiểm lại phần nào; không reset toàn bộ việc không ảnh hưởng.

Audit không sửa kết quả người khác ngoài quyền hoặc trở thành cửa duyệt mọi phép tính thường lệ.

### Không gian và đường liên lạc giữa agent

**Không gian người–agent:** agent của mỗi người dùng dữ liệu, lịch sử, công cụ và quyền của chính người đó. Dữ liệu do ai giữ thì agent tại đó truy xuất/kiểm, không buộc gom hết về máy CEO. Có thể dùng bản dùng chung đã được cấp quyền; nguyên tắc này không cấm chia sẻ hợp lệ hoặc bắt mọi nguồn phải lưu riêng.

**Không gian case:** nơi các agent nhận biết công việc chung và trao yêu cầu/đáp án/đầu ra đúng phạm vi. Nó lưu mục tiêu, người giữ từng phần, phụ thuộc, trạng thái, quyết định và nguồn được phép dẫn; không mặc định chứa toàn bộ chat/tệp cá nhân. Một node không cần đọc toàn bộ thế giới của node khác để lấy câu trả lời kiểm được.

**Đường chuyển sự kiện:** đưa yêu cầu tới đúng agent của đúng chủ dữ liệu/phần việc và làm phiên có khả năng nhận. Thư mục có file chỉ là nơi lưu; nếu không có cơ chế phát hiện, nhận, xử lý và phản hồi thì chưa là kênh agent hoạt động. Máy ảo có thể phục vụ nhận sự kiện/giữ tiến trình nếu đã được cấp đúng quyền và kiểm chứng, nhưng không tự là quyền truy cập dữ liệu nhân viên hay mạng đã chạy.

A xác định hợp đồng hành vi trước; B mới chọn công cụ cụ thể sau khi kiểm môi trường. Không dựng portal/bus mới chỉ để có sơ đồ đẹp. Các bảng Excel kho/vận chuyển đang có vẫn là nguồn làm việc khi app đang xây; agent nên đọc và nối chúng thay vì bắt người dựng lại nền dữ liệu.

### Trigger và vòng agent–agent phải thực hiện thật

| Tín hiệu kích hoạt | Agent phát hiện/nhận | Việc tự làm trong quyền | Khi nào đóng |
|---|---|---|---|
| Quote hoặc chứng từ mới | Agent giữ nguồn; phát thông tin thay đổi cho case liên quan | Kiểm danh tính, phiên bản, dòng ảnh hưởng; trả diff và bằng chứng | Agent dùng đầu ra xác nhận đã áp dụng hoặc giải thích chưa áp |
| Thiếu một dữ kiện để tính giá | BidOps/agent làm giá yêu cầu agent giữ dữ kiện | Chủ nguồn tìm trong dữ liệu của mình, trả số/đơn vị/điều kiện/độ mới hoặc thiếu đúng phần nào | Bên yêu cầu dùng được kết quả, không chỉ đã nhận tin |
| Điều kiện giao/BV hoặc spec đổi | Agent hồ sơ/cơ hội phát hiện | Xác định giá, logistics, hồ sơ và quyết định nào phải kiểm lại | Các phụ thuộc bị ảnh hưởng đã kiểm lại; không reset mọi việc |
| Đến hạn/không có phản hồi | Agent giữ case theo dõi | Kiểm đã gửi/đã nhận/đang làm/chờ quyền/offline; tiếp phần độc lập, thúc đẩy đúng đầu mối | Có bước tiếp có chủ giữ; không đánh done vì đã nhắc |
| Kết quả hoặc ý kiến review trả về | Agent bên dùng | Đọc nội dung và nguồn, phân biệt ACK, yêu cầu sửa, chấp thuận và từ chối | Output được nhận dùng hoặc trả yêu cầu cụ thể để sửa |
| Owner vắng hoặc nhiệm vụ chuyển | Agent case và agent owner | Áp bàn giao đã được phép; giữ receipt và phần đang chờ | Người mới thực sự nhận đúng quyền, không chỉ đổi tên trên task |

Trao đổi tối thiểu cần giữ: case; người/agent gửi–nhận; ý định hỏi/cung cấp/thực hiện/review/quyết định; câu hỏi hoặc đầu ra cụ thể; nguồn/phiên bản; phạm vi quyền; hạn/phụ thuộc; kết quả và trạng thái nhận dùng. Các trường này phục vụ công việc, không bắt nhân viên nhập một form mới cho mỗi tin.

Phải phân biệt **đã chuyển tới nơi nhận**, **agent đã nhận và đủ điều kiện làm**, **đã làm**, **bên dùng đã kiểm/nhận dùng**. Mỗi yêu cầu có nhận diện để tin lặp không tạo hai đơn/cam kết; kết quả đến muộn phải so phiên bản trước khi dùng. Khi gửi không rõ thành công, kiểm receipt trước khi gửi lại. Không phản hồi không tự là từ chối; ACK không là phê duyệt. Agent hiểu nội dung tin, không tự coi yêu cầu từ agent khác có thể tăng quyền của mình.

Con người được gọi ở quyết định cần quyền, dữ kiện mới thực sự không có, hoặc mâu thuẫn chưa tự giải sau kiểm nguồn; không làm người chuyển tiếp thường lệ giữa hai agent.


### Tìm đúng agent và giữ việc qua gián đoạn

Mỗi người–agent cần công bố gọn cho phạm vi thầu: phần việc/năng lực có thể nhận, loại dữ kiện có thể cung cấp, phạm vi quyền, cách nhận yêu cầu, tình trạng nhận việc và điều kiện chuyển ngoại lệ. Đây là chỉ dẫn tìm đúng người, không phải kho dữ liệu cá nhân tập trung. Cùng năng lực so quote có thể tồn tại ở CEO, Linh, Phét và người khác; quyền giữ giá gốc, liên hệ NCC hay chốt giá vẫn khác nhau.

Trước khi giao, bên yêu cầu phải biết người–agent này có đúng nguồn/quyền và có nhận được không. Khi thiếu người nhận, agent giữ case tự tìm đường hợp lệ khác hoặc tiếp phần độc lập; không mở phiên dưới danh tính người khác. Khi node offline, giữ yêu cầu bền và trạng thái chờ, không đánh mất việc hoặc đổi owner ngầm. Khi trở lại, đối chiếu phiên bản/hiệu lực trước tiếp; không tự gửi lại cam kết thương mại.

Có thể kích hoạt từ sự kiện mới, thay đổi dữ liệu được đăng ký theo dõi, lịch mốc hạn hoặc yêu cầu trực tiếp của agent khác. Chỉ theo dõi nguồn đã được cấp quyền; không ngầm quét toàn bộ chat nhân viên. Nội dung gửi vào là dữ liệu/yêu cầu cần kiểm, không phải lệnh cho phép bỏ qua giới hạn quyền. Chỉ trả phần dữ liệu hoặc kết luận được phép chia sẻ; không dùng agent khác làm đường vòng qua một đích/hành động đã bị từ chối quyền. Cơ chế hiện diện, định danh, truy cập, lưu vết và nhận sự kiện trên máy thật còn phải được kiểm chứng; danh sách mỗi người có Claude theo xác nhận của Dũng là nền thiết kế, không cần bắt họ chứng minh lại có tài khoản.

## 9. Hiện diện, quyền và runtime: còn thiếu gì để nói “tự chủ thật”?

| Yếu tố | Đã có bằng chứng | Chưa được suy |
|---|---|---|
| Hai Claude hai máy | Theo bằng chứng test đã ghi nhận trước đó: vòng tổng hợp tự nhận–đối chiếu–trả–dùng, duplicate giữ receipt, ngoài phạm vi bị từ chối | Không đồng nghĩa toàn bộ node nhân viên, kênh thật, ACL hoặc nghiệp vụ thầu đã đạt |
| Người dùng Claude riêng | Dũng xác nhận mỗi thành viên có một agent Claude; kế hoạch 28/10 là snapshot cũ | Có agent không đồng nghĩa listener/kênh nhận việc và quyền nguồn trên mọi máy đã được kiểm chứng |
| Người vắng/máy offline | Kế hoạch có phương án nếu không làm Thứ Bảy; cover có lịch nghỉ | Không coi lịch hoặc máy online là người đã nhận/sẵn sàng quyết |
| KIMLINH | Repo/thiết kế và ACK hiện trường đã đọc | Mission candidate còn owner placeholder/bindings rỗng, chưa xác minh host/runtime của Linh |
| Claude Channels | Có thể đẩy sự kiện 2 chiều vào phiên đang mở; Team/Enterprise cần enable tổ chức | Chưa chứng minh NNC đã bật hoặc có adapter WhatsApp/App |
| Desktop schedule | Chạy phiên mới khi app mở/máy thức | Không tự có quyền file/local ở cloud hoặc always-on |
| Cross-session messaging | Tài liệu mô tả phiên của chính người dùng | Không tự là mạng nhân viên khác tài khoản |

Cùng tài khoản không phủ nhận mức tự chủ của test hai Claude. Codex là proxy thử độ độc lập, không phải điều kiện đa hãng bắt buộc; các lượt chưa PASS do môi trường/model không phủ định test đã đạt.

### Máy ảo đã có phân công, chưa chứng minh sẵn sàng nhận việc agent

Tài liệu tài sản số và receipt phiên ghi: CEO giữ tài khoản Vultr, Dũng có vai OS sudo, Quốc là người thứ hai. Kết quả ngày 29/10 ghi user Duy không sudo, dùng SSH key; có app user/cổng 3100 và linger. Đây là thông tin lịch sử có nguồn, **không phải kiểm sức khỏe máy/service ngày 31/10**, không còn dùng trạng thái chờ public key 28/10 làm kết luận hiện tại.

Chưa thấy bằng chứng process agent, peer identity, endpoint/protocol, queue/receipt hoặc health hiện thời. Không cấp sudo cho agent từ vai OS của Dũng; không dùng quyền tài khoản Vultr để suy quyền dữ liệu của nhân viên. Tình trạng này độc lập với test tổng hợp hai Claude/hai máy đã PASS.

**Lựa chọn tái dùng sau xác minh:** VM có thể làm nơi nhận/định tuyến yêu cầu, lưu receipt và trạng thái case, hoặc giữ một phiên chạy bền thuộc đúng chủ đã được cấp quyền. Agent cá nhân vẫn dùng nguồn/quyền của mình; VM không mặc nhiên tập trung token và dữ liệu riêng. Trước khi dùng phải kiểm đúng host/chủ vận hành, hiện trạng service, tài khoản, đường nhận/gửi, lưu bền và phạm vi quyền; nếu chưa đạt thì giữ phương án chờ, không tự deploy/cấp quyền để làm báo cáo thành hiện thực.

### Đường chạy tối thiểu, ưu tiên công cụ đã có

Không cần chốt một platform mới ở A. Tách ba lựa chọn theo đúng phạm vi:
- **Các phiên của cùng một người:** Claude Code hiện có `ListAgents`/`SendMessage`, nội dung tới phiên nhận đang rảnh có thể mở lượt xử lý; không tự mang theo file/quyền. Đây là đường tái dùng cho các phiên của CEO hoặc từng cá nhân, **không tự là giao tiếp qua tài khoản của 14 người**. Khả năng có mặt phụ thuộc phiên bản/môi trường thật. [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging).
- **Sự kiện tới agent cá nhân đang chạy:** Channels là MCP server đẩy sự kiện vào phiên mở và có thể trả lời hai chiều; đang research preview, Claude Team/Enterprise cần tổ chức bật. Có thể phù hợp một đầu nhận sự kiện đã được cấp quyền; chưa chứng minh NNC có cấu hình hoặc kênh WhatsApp/App tương ứng. [Channels](https://code.claude.com/docs/en/channels).
- **Nguồn cục bộ/đọc theo đợt:** Desktop scheduled task mở phiên mới, truy cập file/tool local khi app mở và máy thức. Có thể là cách agent chủ dữ liệu kiểm hộp việc được phép theo lịch; khác listener phản ứng ngay, không hoạt động khi máy tắt. Cloud không mặc nhiên đọc nguồn local. [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks).

Giao thức tối thiểu nên tái dùng nơi lưu case và đường nhận được phép đang có: agent gửi yêu cầu có nhận diện → agent chủ nguồn nhận/kiểm quyền → tự đọc và trả kết quả có phiên bản → agent yêu cầu kiểm/tiếp bước → trả receipt nhận dùng. Chỉ phần nối còn thiếu mới xem xét adapter nhỏ; không bắt người copy/paste để giả agent–agent. Máy ảo cũ nếu dùng được có thể giữ đường nhận/định tuyến hoặc phiên luôn bật; phải kiểm chủ máy, tài khoản, quyền, process và khả năng nhận sự kiện trước, không đưa toàn bộ dữ liệu/token nhân viên lên máy đó.

**Chứng minh tiếp phải là vòng công việc, không chỉ mở được hai phiên:** (1) CEO và node nhân viên cùng làm hai phần của một case mà không ghi đè; (2) agent cần dữ kiện gửi cho agent chủ nguồn, chủ nguồn tự tra và trả bằng chứng, bên dùng tự tiếp; (3) hỏi bổ sung một trường thiếu, không chuyển cả việc về người; (4) tin lặp/đến muộn không tạo cam kết trùng hoặc dùng giá cũ; (5) node offline rồi trở lại vẫn giữ yêu cầu và đúng phiên bản; (6) yêu cầu vượt quyền/ủy quyền hết hạn bị giữ lại; (7) người đại diện nhánh thầu nhận việc nhưng không chiếm quyền CEO toàn công ty; (8) chi phí từ Excel đi vào mô hình giá có dấu nguồn và không tính trùng. Đây là tiêu chí kiểm thử đề xuất cho bước sau, chưa triển khai hay cấp quyền qua bản báo cáo.

Trong A, chọn mức đáp ứng công việc trước: cần phản ứng trong phiên, theo đợt hay ngoài giờ; phần nào được tiếp khi chủ vắng; ai nhận thay hợp lệ. Chưa chọn technology hoặc cấp credential. Tách agent biết làm, có nguồn, có quyền, đang online và đã được chấp nhận kết quả.

[Tài liệu Channels](https://code.claude.com/docs/en/channels), [lịch Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks), [nhắn giữa các phiên](https://code.claude.com/docs/en/cross-session-messaging) đã đọc; đây là năng lực nhà cung cấp, không chứng minh cấu hình NNC.

## 10. Từ mạng phối hợp đến onboarding có bằng chứng trong tháng 11

### “Bus” là hợp đồng phối hợp chung, không phải tên một công nghệ

Phép ví mạng ô tô hữu ích ở chỗ nhiều node làm việc riêng nhưng trao tín hiệu có quy ước, ưu tiên và cô lập lỗi. Không mặc định Dũng muốn CAN/LIN cụ thể, cũng không bê phân xử bit hay broadcast mọi dữ liệu thành quyền nhân sự. [CiA](https://can-cia.org/cia-groups/cia-glossary-of-terms) là căn cứ cho các đặc tính CAN; phần áp dụng sang nghiệp vụ dưới đây là đề xuất thiết kế.

Tách **chủ thể/nguồn**, **hợp đồng case**, **đường truyền và sổ trạng thái**, **nơi chạy/lưu**, **quyền/audit**. Drive giữ artifact được phép; VM có thể giữ dịch vụ nhận và trạng thái bền; agent chủ dữ liệu tự thực thi. Một bên không thay cả các bên còn lại. Không gom quyền tài khoản nhân viên vào bus. Adapter phải xác thực chủ thể/đích và kiểm phạm vi trước khi chuyển yêu cầu vào agent; câu chữ “Sếp yêu cầu” trong payload không phải credential hoặc quyền mới. Quyền quyết định lấy từ căn cứ ủy quyền/policy đúng phiên bản, không do LLM tự suy.

### Quy ước tác nghiệp tối thiểu

| Thành phần | Quy tắc đề xuất |
|---|---|
| Định danh | Người/agent đã xác minh + case/gói + request/event + nguồn/phiên bản; node/session ID không thay người chịu trách nhiệm |
| Loại thông điệp | Yêu cầu dữ kiện, yêu cầu làm, dữ kiện mới, câu hỏi bổ sung, đề xuất sửa, kết quả, receipt nhận dùng, ngoại lệ, đính chính, hủy |
| Ý nghĩa | Cần gì, để phục vụ bước nào, đầu ra ai dùng, hạn nào và căn cứ, phần được phép thực hiện |
| Nhận việc | Phân biệt chuyển tới endpoint, agent nhận/đủ quyền/đủ năng lực, đang xử lý, đã trả, bên dùng chấp nhận; từ chối nêu đúng nguyên nhân |
| Ưu tiên | Theo tác động/hạn thật/phụ thuộc, không vì tin do CEO gửi mà mọi việc khác luôn bị ngắt; bên nhận biết mức ưu tiên và tải hiện tại |
| Công bằng | Giới hạn việc đồng thời theo node; tăng chú ý việc chờ lâu; giữ phần năng lực cho ngoại lệ có hạn, tránh nguồn gửi nhiều làm nghẽn các node khác |
| Backpressure | Khi quá tải, báo chưa nhận/ETA có căn cứ/đề nghị chia nhỏ; không ACK nhận hết rồi âm thầm để quá hạn. Bên gửi vẫn giữ việc chưa được nhận |
| Trùng và retry | Một sự kiện/phiên bản + nội dung + đích tạo khóa chống lặp; retry trả receipt/kết quả trước, không nhân đôi giao dịch. Outcome chưa rõ thì kiểm trước khi gửi lại |
| Thứ tự | Chỉ cần thứ tự theo case/đối tượng/phiên bản, không buộc mọi tin toàn công ty xếp một hàng; kết quả đến muộn phải so trạng thái hiện tại |
| Quyền sở hữu | Nhận xử lý không tự đổi owner nghiệp vụ; giữ một writer cho cùng vùng master tại một thời điểm, node khác gửi proposal. Lease xử lý hết hạn không tự chuyển quyền ký/nộp |
| Offline | Lưu yêu cầu bền, hiện rõ không nhận được; tiếp phần độc lập. Khi trở lại kiểm nguồn/quyền/hạn rồi tiếp, không tự replay cam kết bên ngoài |
| Deadline/TTL | Hạn yêu cầu và hạn hiệu lực quote/ủy quyền tách nhau. Hết hạn xử lý thì báo stale; không xóa bằng chứng hoặc coi đầu ra cũ vẫn được dùng |
| Đính chính | Gửi revision thay thế gắn sự kiện cũ, chỉ ra kết quả phụ thuộc cần kiểm lại; không âm thầm sửa lịch sử hoặc reset phần không ảnh hưởng |
| Hủy | Phân biệt đã yêu cầu hủy với đã dừng; nêu phần đã thực hiện. Không giả thu hồi được email/đơn/nộp hồ sơ đã ra ngoài; cần hành động xử lý hậu quả đúng quyền |
| Cô lập lỗi | Dừng tự retry nguồn/node gây lỗi lặp, giữ lỗi và chuyển ngoại lệ đúng người; phần còn lại tiếp tục. Khôi phục phải kiểm điều kiện, không bỏ qua denial |
| Audit | Dấu nguồn/phiên bản, ai yêu cầu–nhận–làm–dùng, quyền, ảnh hưởng và thời gian; hạn chế dữ liệu riêng, không mirror chat nhân viên |

Đây là semantics đề xuất cho nghiệp vụ, không tuyên bố công cụ hiện tại tự cung cấp tất cả. Không hứa “exactly once” toàn mạng; mục tiêu thực tế là giao lại an toàn, xử lý idempotent và kiểm trạng thái trước tác động không lặp được.

### Drive, VM và phần còn phải làm — chọn theo case

| Cách tổ chức | Tái dùng được | Phần vẫn phải có/kiểm | Khi thích hợp |
|---|---|---|---|
| Agent local + Drive được phép chia sẻ + đường nhận hiện có | Nguồn, file/case và thử hai máy đã có | Trigger/listener hoặc poll có quyền, nhận việc bền, khóa phiên bản, receipt dùng, danh tính khác chủ, offline/retry | Bước chứng minh hẹp không cần dựng máy chủ mới; không gọi chỉ tạo file là agent–agent |
| Agent local + VM công ty làm trung chuyển/sổ case | VM và phân công lịch sử, agent tại chủ nguồn vẫn giữ dữ liệu | Health, operator, service account, queue/ledger/backup, đường vào từng agent, quota và quyền truy cập theo case | Khi cần hoạt động bền trong lúc máy người gửi tắt; chưa chứng minh VM hiện có các thành phần này |
| Claude Channels / lịch Desktop | Cơ chế nhận sự kiện hoặc chạy theo lịch đã có ở nhà cung cấp | Team enablement, phiên/host đang chạy, connector/quyền, độ bền trạng thái và acceptance nghiệp vụ | Adapter vào agent; không thay sổ công việc hay thẩm quyền |
| A2A / broker như MQTT hoặc JetStream | Chuẩn mô tả agent/task hoặc lớp chuyển tin có tính năng sẵn | Adapter vào Claude, authz theo người, key nghiệp vụ, idempotency, owner/version/receipt | Tham chiếu/ứng viên khi thật sự thiếu transport; không ghép tất cả thành platform hoặc bắt triển khai chuẩn đầy đủ trước cuối11 |

[A2A1.0.1](https://a2a-protocol.org/v1.0.1/specification/) có task lifecycle/Agent Card/cancel nhưng không tự bảo đảm mọi triển khai chống trùng SendMessage hay retry webhook. [MQTT5](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html) ACK/QoS không là xác nhận báo giá đã được dùng; [JetStream](https://docs.nats.io/learn/jetstream/delivery-and-acknowledgment) lưu/giao lại vẫn cần xử lý tác động nghiệp vụ an toàn. Đây là lý do giữ received–accepted–produced–used độc lập khỏi transport.

**Ưu tiên thực tế đề xuất:** giữ nguồn ở chủ, Drive cho artifact được phép; chứng minh hợp đồng case bằng đường nhận hiện có. Chỉ dùng VM làm phần nhận/lưu bền khi kiểm hiện trạng cho thấy cần và đủ quyền; nếu cần adapter/ledger nhỏ thì thiết kế tối thiểu, không mặc định phải dựng broker hoặc app điều phối mới. Không dùng “có Claude Team” làm bằng chứng mạng nhiều tài khoản đã liên thông.

### Các cửa chứng minh đủ để onboarding

| Cửa kiểm | Bằng chứng phải có | Khi chưa đạt |
|---|---|---|
| Đúng người/việc hiện tại | Đã audit phiên Cung ứng, map v18 và tài liệu 28/10; còn cần receipt theo case và kiểm quyền/nhận việc trên node thật | Không biến phân công tài liệu thành đã ACK hoặc đã chạy |
| Nguồn đọc được tại chủ | Agent chủ nguồn thực đọc được một dữ kiện cần cho case, trả locator/version/giới hạn chia sẻ | Tìm đúng đường đã được phép; không yêu cầu CEO đọc hộ nguồn riêng |
| Nhận–trả thật | Hai người–agent khác chủ hoặc danh tính thực được phép trao yêu cầu, hỏi bổ sung, trả kết quả và nhận dùng | Test cùng tài khoản vẫn giữ giá trị riêng nhưng chưa đạt cửa này |
| Quyền và con người | Đọc/đề xuất/ghi/gửi/duyệt được tách; agent biết phần tự làm và phần cần người | Tiếp nhánh read-only/prepare, không tự nâng quyền để đạt test |
| An toàn phiên bản | Trùng, sửa đồng thời, stale, variant khác, đính chính/hủy được kiểm; phần người làm giữ nguyên | Chỉ sinh proposal; không apply master hoặc dùng output chưa kiểm |
| Hiện diện và phục hồi | Nguồn local, máy/phiên tắt–bật, queue/receipt, nhận lại và check hạn sau restart | Không gọi always-on; có đường xử lý chờ/ngoại lệ được biết |
| Khả năng dùng thật | Một vòng C1 hoặc C3 có output được bên dùng chấp nhận, đo thời gian/người chạm tay/lỗi/lặp | Không thay quy trình đang vận hành bằng kết quả chỉ chạy demo |
| Vận hành | Chủ runtime, log phù hợp, chi phí/quota, cập nhật/version, điểm dừng/rollback và người hỗ trợ được chỉ rõ | Giới hạn pilot không đối ngoại; không để không ai giữ service |

Nhận dùng mới là cửa quan trọng: bên làm hồ sơ/giá/kho phải thực sự dùng kết quả, không chỉ phản hồi “ok”. Tiêu chí đo gồm thời gian từ yêu cầu đến dùng được, tuổi việc chờ, số vòng hỏi lại thứ đã có, số lần người chuyển dữ liệu thủ công, lỗi/retry và phần việc được agent gánh. Mức mục tiêu lấy từ baseline thực rồi chốt, không tự hứa tỷ lệ hiệu quả.

### Đường đưa vào dùng theo gói, không chờ cuối tháng mới bắt đầu

**Komsenahak có lịch phối hợp 13/11 và ngày 13/11/2026 trên mẫu USB đã đọc**, sớm hơn các mốc 25–27/11 của ba gói khác. Mittaphab có mốc 4/11 và owner đang làm, không tự chiếm hoặc ép đổi quy trình gói này. Đây là lịch ghi trong nguồn nội bộ; phải đối chiếu hạn chính thức trước cam kết. Nếu chỉ onboarding đồng loạt cuối tháng thì không phục vụ đúng vòng việc trước các mốc đó.

Phương án từ 31/10: đầu tháng xác minh roster hiện tại và đường nhận của CEO + một người giữ nguồn; tuần đầu chạy vòng nội bộ read-only/đề xuất có bên dùng thật; trước 13/11 nếu chọn Komsenahak phải có một vòng hữu dụng với chủ giá/hồ sơ, không chuyển hạ tầng sát hạn. Tuần sau thêm node giá–hồ sơ–kho/chi phí theo case; trước mốc chuẩn bị 25/11 chỉ mở phần đủ bằng chứng và quyền. Tới cuối tháng ổn định phạm vi đã đạt, không tuyên bố mọi node/toàn công ty đã tự chủ.

Lịch cụ thể để review: **Kom** — 02/11 chốt scope/vai, 05/11 pilot, 09/11 candidate, 11/11 rehearsal trước 13/11; **gói 25/26/27** — onboard vai trước 17/11, rehearsal 20/11, bàn giao candidate 24–25/11. Không tự ghi các mốc này là đã cam kết/đã đạt; giờ đóng thầu và điều chỉnh cần nguồn chính thức. SVNK chưa rõ hạn vẫn nằm trong scope.

Lịch Cung ứng khác lịch thầu: plan 28/10 dự kiến 30–31/10 trial, 01/11 kiểm sáu điểm, 02/11 chạy đơn mới và 13/11 xét bỏ Google Sheet sau hai tuần. Chưa có receipt live các mốc đó trong lượt audit. Các mức ≥90% mã hay đặt có giá và ≥3 đơn thật/người thuộc đề xuất chờ chốt, không biến thành chính sách đã duyệt; D6 gom đợt/việc gấp/người giữ bóng để sau 02/11, chưa là bus đang chạy.

Các khoảng này là **đề xuất lập kế hoạch**, không cam kết thời gian triển khai chưa được phép. Mục tiêu đủ onboarding là có người/agent thật, nguồn thật, nhận–làm–hỏi–trả–dùng thật và người vận hành hỗ trợ, không phải số tài khoản tạo xong. Dùng kết quả read-only/proposal ngay trong quy trình hiện có; chỉ chuyển từng bước ghi/gửi khi đã đạt gate và có quyền. Khi lỗi, dừng phần tự động liên quan, quay lại owner trên cùng case/version; không rollback toàn file làm mất sửa của người khác.

Bốn case làm căn cứ: (1) CEO cùng node quote/giá hoàn thiện một dòng chào, (2) nối đúng sản phẩm–certificate rồi kiểm gia hạn, (3) SVNK nhiều điểm nối kho/xe/chi phí/lịch tiền, (4) người đại diện nhánh BV trong ủy quyền hữu hạn. Mỗi case phải có thử trùng, stale, offline, crash sau xử lý trước ACK, sửa đồng thời, quá tải, hủy/đính chính và quyền khác nhau. Test hai Claude và fixture10/10 vẫn là bằng chứng đã có, không thay cửa vận hành nhân viên thật.

Không cần quyết lại nguyên tắc CEO luôn làm hoặc mỗi người một agent. Các quyết định cần trước hành động là host/kênh sau kiểm, người vận hành, phạm vi chia sẻ và quyền ghi/gửi/đại diện cụ thể; chúng không chặn nghiên cứu A tiếp.

## 11. A tiếp tục thế nào, lúc nào mới có quyết định cần Dũng?

### Những việc nghiên cứu tiếp được ngay
- Truy đúng HSMT/addenda/thông báo phát hành và điều kiện xét dòng/lô/tương đương/bảo lãnh. Đã có 12 Annex không cần yêu cầu gửi lại; chỉ tìm phần còn thiếu.
- Giải các lệch thương phẩm/nhà sản xuất/quy cách của sáu ứng viên Visa trước; chỉ sau khi nhận diện đúng sản phẩm mới đối chiếu giấy phép và gia hạn mới nhất; phân loại trường thực sự bắt buộc theo hồ sơ phát hành, không dùng tỷ lệ ô trống làm tỷ lệ đủ điều kiện.
- Nối exact quote Sharma, bản Phét đã up và receipt rà; nối giá Sơn vào đúng bản đích/khác biệt kỹ thuật, không tự áp giá.
- Đối chiếu bản lịch sử NNC trúng 2026 với đúng file/row/version và loại số; không gọi giá trúng là giá vốn 2027 hoặc doanh thu đã thu.
- Hoàn thiện hồ sơ node theo case: người, phần việc, quyền, kênh, khả năng agent, hiện diện và bên nhận dùng. Nguồn/nhân viên chưa rõ không trở thành câu hỏi rộng ngay.
- Đưa những phát hiện này vào phương án CEO đầy đủ và các chế độ thực thi; audit mâu thuẫn nguồn thêm một lượt trước kết luận.

### Đề xuất A hiện tại, không phải lệnh triển khai
Giữ năng lực CEO đầy đủ, gồm các năng lực tác nghiệp chung với nhân viên. Hỗ trợ CEO làm phần lớn, CEO cùng nhân viên làm, hoặc người đại diện giữ riêng nhánh thầu trong ủy quyền. Human–agent node tự nhận và xử lý phần thực sự nhận trong quyền, trao yêu cầu–kết quả trực tiếp giữa agent thay vì bắt người chuyển tiếp. Không cố định task vào phòng ban, không dồn mọi thứ về CEO, không chiếm quyền chủ node.

**Chưa có quyết định lớn đang chặn toàn bộ A.** Chỉ đưa Dũng quyết định khi còn mâu thuẫn thực sự về mục tiêu/phạm vi/thẩm quyền mà nguồn không giải được, kèm các lựa chọn và hệ quả. Không dừng ở bước “xin duyệt khung” trước khi nghiên cứu đủ.

Các cửa trước B khi cần thật: mở rộng quyền agent trên app/kênh; chuyển chủ việc khi người vắng; chốt cam kết/tiêu chí tham gia; chọn vòng nghiệp vụ đầu có người thật, nguồn/kênh được phép và bên nhận dùng. Chưa kích hoạt các cửa này và chưa cần Dũng trả lời thay phần research.

---

## Nguồn và giới hạn kiểm chứng

**Nguồn người/công việc đọc trực tiếp:** [Job Story Linh](https://docs.google.com/document/d/1SeWsRG4NKk8V3SjfIdMxnNI8yPoLr5wnWSd0r6L4_Wc/edit), [Evidence Log 02–04/10](https://docs.google.com/document/d/1Pc2ayN3fPdxgrPB1z8S1D-dI7ASdzyiNQEy-4iBHhKU/edit), [baseline KIMLINH v0.3](https://github.com/VOSYDUNG/kim-linh-agent/blob/main/product/PERSONAL-TASK-SHARED-CAPABILITY-BASELINE-v0.3.md), [ACK 29/10](https://github.com/VOSYDUNG/kim-linh-agent/pull/3#issuecomment-6496125300), [current authority](https://github.com/VOSYDUNG/kim-linh-agent/blob/main/locks/CURRENT-AUTHORITY.md), [mission candidate](https://github.com/VOSYDUNG/kim-linh-agent/blob/main/oser/MISSION-CONTRACT.candidate.json). AS-IS/plan/draft không tự là policy đã ban hành hoặc UAT PASS. Nội dung cũ “remote chưa tạo” đã lỗi thời so với repo đọc được; không dùng làm blocker.

**Bộ bốn BV đã đọc:**

| BV | Cover | Thuốc | HC | VTTH |
|---|---|---|---|---|
| Mahosot |[cover](https://docs.google.com/spreadsheets/d/19WRLhTzJqGGAXfr5-Az0dwK3pSy7ygQo/edit)|[thuốc](https://docs.google.com/spreadsheets/d/1COXneQlON4pDEpy8zTY7amorDr8c-41P/edit)|[HC](https://docs.google.com/spreadsheets/d/1pAXFvCicN5wniDC7YRdlbJgUk3j3XP8-/edit)|[VTTH](https://docs.google.com/spreadsheets/d/15tKHHkRw4eVstlVxIHiKYbVy_qI-zn5n/edit)|
| Settha |[cover](https://docs.google.com/spreadsheets/d/164X5bSfg_7l30H8jfBizUboqrk4oW08r/edit)|[thuốc](https://docs.google.com/spreadsheets/d/13yK4Fs6h6lMIciLLsUhUs8oHKyk2Ox63/edit)|[HC](https://docs.google.com/spreadsheets/d/1XRDLOcRMkph65uN5XQc1H08yJrO7Pp90/edit)|[VTTH](https://docs.google.com/spreadsheets/d/1-dUJVsYt70nv7I5sITkT_e4CkvPfwg74/edit)|
| MeDek |[cover](https://docs.google.com/spreadsheets/d/1rZqEHoxMjIzPsLqq-DkiIjc0iU8NVyll/edit)|[thuốc](https://docs.google.com/spreadsheets/d/19RffHeQJrwC9W86pM4fzPuppUDa1eeU5/edit)|[HC](https://docs.google.com/spreadsheets/d/1ic5puqCWqI1VOfrapslJ7yse2hgwGpVP/edit)|[VTTH](https://docs.google.com/spreadsheets/d/1X8siUES-BPuhkBgTsiFlOg7JA658ai7R/edit)|
| SVNK |[cover](https://docs.google.com/spreadsheets/d/18FgY-TrCzW2mtuxTIvs4v6Tnm8T_OqIW/edit)|[thuốc](https://docs.google.com/spreadsheets/d/1DGbtss7BjgMfLCNtQkC1YAeVyEIIPIIQ/edit)|[HC](https://docs.google.com/spreadsheets/d/1O8D4waWwuyUG5dYVAezCCfudBLCwSsBe/edit)|[VTTH](https://docs.google.com/spreadsheets/d/1PbspVn7kyd8D3qtGwc3ql0FhMJ3leyFg/edit)|

Tìm kiếm theo tên BV, HSMT/addendum, tiếng Việt/Lào và manifest đã mở thêm một vòng nhưng chưa thấy bộ HSMT đầy đủ đúng bốn gói. Kết quả không tìm thấy không chứng minh công ty không có. Không dùng điều kiện LuxDev/UNOPS gói khác áp sang bốn gói.

**Nguồn báo giá:** Sơn chỉ có một revision API hiện hành, chưa chứng minh trước/sau hoặc người phê duyệt. Text trích một số file không có tên sheet/toạ độ ô; báo cáo giữ neo tiêu đề/STT/record thay vì giả địa chỉ Excel. Catalog 29/10 là snapshot lịch sử, không phải bảng production hôm nay. Chưa kiểm độ hiệu lực quote, công thức hoặc cam kết carrier.

Bản lite đi kèm tách danh sách người–agent và vòng phối hợp để xem nhanh; bản A này giữ phần nghiên cứu sâu.

Bản này không chứa xác nhận chọn NCC, giá chào, giá ký, hồ sơ đủ điều kiện, doanh thu/lợi nhuận đạt, hay node nhân viên đã tự vận hành. Những kết luận ấy cần bằng chứng riêng ở đúng bước.

### Nguồn local bổ sung và giới hạn thời điểm

Các đối chiếu local ở trên dựa trên báo cáo **RESEARCH-A-LOCAL-31-10.md**, đọc đầy đủ ngày 31/10, và bằng chứng kèm của lượt kiểm tại máy công ty. Thư mục dự án: `D:\WORK\Agent\Agent-first\personal-meeting-assistant\.local\projects\thau-bv-nnc`; thư mục BidOps: `D:\WORK\Agent\Agent-first\NNC BidOps Agent`. Neo workbook/script/ô đã ghi ngay tại từng kết luận. Bản đối chiếu local ghi tên, hash và mốc sửa trong `LOCAL-SOURCE-EVIDENCE.json`, `ACTUAL-OUTPUT-CELL-CHECK.json`, `OUTPUT-GRAIN-AND-PACKAGES.json`, `STATUS-SEMANTICS-AUDIT.json`, `ALC-TENDER-TRACE.json`.

Đây là snapshot công việc 28–30/10, workbook nguồn và sổ ALC lịch sử tới tháng 5; không phải dữ liệu vận hành mới của mọi người ngày 31/10. Các ZIP hiện có chỉ chứng minh bộ file tồn tại, không chứng minh WhatsApp đã nhận hoặc dùng. ID phiên ghi trong receipt 29/10 chưa xác minh đang chạy nên không tự resume. **Chưa có kiểm chứng vòng nghiệp vụ nhân viên thật liên máy; giới hạn này không phủ nhận test tổng hợp hai Claude đã PASS.** Chưa có full HSMT, gia hạn mới, quote đích cuối, cam kết giao/thu–chi hoặc giới hạn vốn được xác nhận. Lượt đối chiếu đăng ký bổ sung đã dừng một nguồn Drive do 403 không có quyền đọc và một nguồn do lỗi kết nối; không dùng các lỗi đọc làm bằng chứng thiếu hồ sơ, không vượt quyền để tìm tiếp. Các record FDD công khai nêu trên là đối chiếu lịch sử, không thay toàn văn quy định và điều kiện HSMT hiện hành.

### Đối chiếu bổ sung local và VM, 31/10

Báo cáo **Audit phiên bản thầu local — 31/10/2026** (`REPORT.md`) được đọc đủ 114 dòng. Chứng cứ gồm `PRESERVED-SOURCE-HASHES.json`, `BUNDLE-CURRENT-COMPARISON.json`, XML raw Mahosot, fixture tổng hợp và tài liệu tài sản số/receipt phiên. Các kết luận bảo toàn file, cache/công thức, phân công VM ở trên phân biệt rõ quan sát raw với lịch sử cấu hình. Không probe/SSH vào server, không mở external-link private target, không refresh hoặc sửa workbook. Bộ bảy năng lực tiếp tục là synthesis để review, không được gán là framework người dùng đã chốt.

### Nguồn Cung ứng hiện hữu và Komsenahak đã audit ngày 31/10

Đã đọc đầy đủ **SUPPLY-SESSION-AUDIT.md** (140 dòng). Nguồn xác định đúng phiên QUY TRÌNH CUNG ỨNG, kiểm lại map v18/BRIEF, kế hoạch tiếp26/10, quyết định CEO–An26/10, hướng dẫn/kế hoạch28/10, AI-ERA v3 và receipt KIM LÝ; local checkout HEAD `89e8c567` sạch không chứng minh máy nhân viên/remote cùng version. Phản hồi phiên là đầu mối truy nguồn, không tự là bằng chứng mọi việc đã làm.

Kom được đọc từ workbook F02 gốc, SHA256 `1b12de819834d58c16355fe99abd8b4a18ced2757cda90cb041d71ecc5ce9692`; các neo sheet/ô và số dòng ở mục1. Chưa đọc full HSMT/giờ đóng thầu, chưa kiểm current app/runtime/ACL nhân viên hoặc kết quả M1–M6. Không đọc raw MISA, credentials, private profile; không khởi động lại kênh cũ hoặc vượt denial để nạp báo cáo vào Claude.
