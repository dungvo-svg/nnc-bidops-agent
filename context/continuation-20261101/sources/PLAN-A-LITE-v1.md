# BidOps — Khung lite người–agent cho thầu bệnh viện
**Để Dũng xem · Cập nhật 31/10/2026, 18:26 VN · Thiết kế, chưa triển khai hoặc cấp quyền**

## 1. Điểm đứng

**CEO luôn trực tiếp tham gia chào hàng và làm thầu**, kể cả khi có nhân viên. BidOps giữ đầy đủ năng lực chung với nhân viên và trách nhiệm quản trị liên gói/liên nhánh. Có thể giao một người đại diện riêng nhánh thầu, nhưng phải rõ gói, thời gian, phần được quyết và phần phải chuyển CEO; không tự biến người đó thành CEO toàn công ty.

Mỗi người có một agent Claude theo xác nhận của Dũng. **Agent của chủ dữ liệu tự đọc, xử lý và phản hồi cho agent cần dùng**, thay vì bắt người chuyển tiếp tin/tệp thường lệ. Công việc khác quanh từng người giữ nguyên; bản này chỉ lấy phần phục vụ thầu.

## 2. Người – năng lực – phần việc thầu

Đây là phạm vi đích để ghép việc, **không phải phân công đã nhận hoặc quyền mới đã cấp**. Đã audit phiên Cung ứng hiện hữu: map v18 nháp cutoff 26/10 chưa nhập hết nguồn 27–29/10. Bảng này dùng kế hoạch/hướng dẫn 28/10 cho vai mới; vai chỉ có nguồn 12/10 giữ tính lịch sử. Phân công tài liệu chưa là receipt vận hành.

| Người / agent | Phần việc phục vụ thầu | Giới hạn đáng chú ý |
|---|---|---|
| **CEO / BidOps** | Cơ hội/chào hàng, nguồn–giá, kịch bản hàng–chứng từ–tiền, trực tiếp làm và điều phối | Không điều khiển phiên agent người khác |
| **Lý** | Cung ứng OTC; nguồn VN, NCC/đơn/giao, khai quan thường lệ, khiếu nại | Không chỉ logistics; lượng mua theo đúng người quyết |
| **Trang** | Cung ứng SPM/HC; rà giá SPM, nguồn VN, đơn/giá, ảnh/chứng từ, chặng HN | Nạp bảng Lacco khác liên hệ Lacco mọi case |
| **Linh** | Cung ứng HC; nguồn nước ngoài, quote/spec/packing, NCC/forwarder, estimate toàn chặng | Không chỉ vận chuyển; kênh cá nhân theo quyền |
| **Phét / Phet** | Cung ứng HC; nguồn Lào–Thái, biên giới–xe–kho; bảng thầu/giá và phối hợp hồ sơ | Không tự duyệt tương đương hoặc coi dự kiến là đã giao |
| **Đức** | Nguồn VN/HC, đơn/đáo hạn trong map lịch sử | Chưa tự gán nhiệm vụ thầu hiện tại |
| **Hoa** | Mã hàng/spec/UOM, giá mua, đối chiếu đầy đủ dòng và chuẩn bị diff | Nhập/sửa giá khác quyền duyệt; không tự gộp MISA |
| **Yaeng** | NCC, công nợ/đáo hạn, kiểm trả trùng | Map xác nhận không nhập đơn; không tự ghép tên OCR |
| **An** | Quy tắc kế toán, phân bổ/giá vốn, chứng từ, estimate–actual | Quyền phê duyệt/import theo người được giao |
| **Namfon** | Danh mục/giá/phân bổ, nối actual với đơn/lô/hàng | Không mặc định giữ toàn bộ nhập kho/công nợ |
| **Hiền** | Kế toán/thuế/tồn SGVC; backup khai quan | Lý thường làm khai quan; backup cần bàn giao |
| **Sang** | Chứng từ chi VN, invoice–đơn–lô SGVC | Không suy quyền ký thầu Lào từ vai SGVC |
| **Laty** | Bằng chứng trả, nối NCC–đề nghị–đơn/lô | UNC có thể gộp; không tự chuyển/retry tiền |
| **Duy** | Nguồn OTC với Lý, tối ưu mã, kiểm/duyệt giá OTC | Vai nghiệp vụ không tự cấp quyền máy ảo |
| **Quốc** | Kiểm/duyệt giá SPM theo kế hoạch 28/10 | Không suy quyền ký/nộp thầu |
| **Aiy** | Tối ưu mã SPM, đánh giá cặp giữ/gộp | Không thay Quốc duyệt giá SPM |
| **NAE** | Kho nhận OTC theo B6 ngày 28/10; đối chiếu đơn–nhận–chứng từ | Chưa kiểm nhận việc/runtime/ACL thật |
| **Vylayphone** | Kho nhận HC theo B6; nối receipt lượng/lô/hạn/ngoại lệ | Không suy quyền mọi kho/hàng thầu |
| **Khem** | Kho nhận SPM theo B6; nối receipt và dữ liệu kho/đơn | Workbook lịch sử không là tồn hiện tại |

**Giữ các vai chưa đủ tên/phạm vi từng case:** xe/tài xế/điều phối, chuyên môn/đăng ký sản phẩm, người đại diện CEO nhánh thầu. Sơn là đầu mối workbook báo giá; Oanh và Dũng nối việc Kho/quy trình/nghiên cứu theo hội thoại, không phải các tên đã trích trong map.

**Năng lực chung không chia độc quyền:** đọc hiểu trao đổi, tự tìm nguồn, so spec/giá/chứng từ, tính, dự thảo, theo phụ thuộc, hỏi–đáp và kiểm đầu ra. Quyền dữ liệu, liên hệ, sửa, duyệt và cam kết vẫn khác nhau theo người/case.

**Điều đã có để tái dùng:** nhân viên có sáu tác vụ Claude được mô tả từ 28/10; người vẫn quyết/bấm app theo hướng dẫn hiện tại. Mã nội bộ MISA là gốc, không áp Y19 cũ tạo trên app trước. AI-ERA v3 có contract/provenance nhưng P0 chỉ Dũng; KIM LÝ mới MAPPED, chưa nghiệm thu kỹ thuật/owner đầy đủ. Không gọi các thiết kế này là mạng nhân viên đã vận hành.

**Komsenahak là gói hiện hành 2027:** đã có workbook, mẫu USB ghi 13/11/2026. 1.455 dòng gồm 649 giá cũ, 8 cần xem, 798 tìm nguồn; 797 annotation vì Omesod dòng 663/STT 645 thiếu dòng đích, không mất dòng gốc. Giá cũ không làm gói thành lịch sử; BGC chưa có tab Kom không loại gói khỏi mạng. Onboarding phải theo mốc gói, không đợi cuối tháng; các ngày pilot/candidate là phương án, chưa cam kết triển khai.

## 3. Vòng agent–agent tối thiểu

**Trigger:** quote/chứng từ mới; điều kiện BV đổi; thiếu dữ kiện tính giá; hàng về; khoản trả ghi nhận; đến hạn hoặc có phản hồi.

**Luồng:** agent phát hiện → gửi yêu cầu đúng agent chủ dữ liệu → chủ nguồn tự đọc/kiểm trong quyền → trả kết quả có nguồn/phiên bản → agent cần dùng kiểm và tiếp việc → xác nhận đã nhận dùng.

Mỗi vòng giữ gọn: **case + mục đích + người/agent nhận + đầu ra cần + nguồn/phiên bản + quyền + hạn/phụ thuộc + receipt**. Không bắt nhân viên nhập lại form cho từng tin. Đã gửi, đã nhận, đã làm và được dùng là bốn mốc khác nhau. Tin lặp/đến muộn không tạo hai cam kết hoặc áp giá cũ.

Dữ liệu riêng ở người giữ; không gian case chỉ chứa phần cần và được phép chia sẻ. CEO thấy tín hiệu tiến độ/rủi ro/quyết định, không phải toàn bộ chat cá nhân. Offline thì giữ việc chờ hoặc bàn giao đã được phép, không dùng tài khoản người khác. Con người xử lý quyết định cần quyền hoặc mâu thuẫn thật; không làm người chuyển tiếp thường lệ.

## 4. Hàng — chứng từ — tiền phải khép cùng case

- **Hàng:** đúng biến thể/UOM, lượng, nguồn, tồn/lô/hạn, shipment, điểm giao và thực nhận.
- **Chứng từ:** hồ sơ/giấy đúng thương phẩm, PO/packing, giao nhận/nghiệm thu, hóa đơn và căn cứ thanh toán.
- **Tiền:** giá vốn/chào/ký, cước và phân bổ, lịch chi–thu, actual và tiền đã thu.

Kho và xe **đã có Excel đo dữ liệu**, app đang xây; tái dùng và kiểm nguồn, không dựng lại từ số không. Sheet xe có 129 khoảng đo xăng/km; đó chưa là chi phí toàn phần/km. SVNK có kho tỉnh và 15 địa bàn: cần nối tuyến/đợt/điểm nhận vào giá, không lấy giá một kho cho toàn bộ.

Giữ riêng **lãi đóng góp, P&L toàn phần và lịch tiền/đỉnh thiếu vốn**. Cước đã nằm trong giá vốn không cộng lần nữa; giao Done khác nộp tiền; cùng tồn/xe/vốn không được tính đủ cho nhiều gói đồng thời.

**Audit song song:** đúng người/quyền, đúng hàng/phiên bản, không trùng việc/chi phí, đầu ra được dùng. Điểm nghẽn đang thấy chủ yếu là phối hợp, mất dấu bước tiếp và khác phiên bản — không kết luận nhân viên kém năng lực.

### Nguồn chính
[Bản đồ Cung ứng v10](https://drive.google.com/file/d/1IZoR4FFomb-tZ3bCI4suJ2rNGyc7IkAF/view) · [Kế hoạch 28/10](https://docs.google.com/document/d/1h0P86WXYO7y03lzhTCPoMX7qF7l4vZRM/edit) · [ACK Linh](https://github.com/VOSYDUNG/kim-linh-agent/pull/3#issuecomment-6496125300) · [Kho/Khem](https://docs.google.com/spreadsheets/d/11ubDlRARtR71bpum8Wh61L2D6moED7Mf/edit) · [Chi phí xe](https://docs.google.com/spreadsheets/d/1BvtBFOhNGG2yjJGY8CGpADKJds4fukqS0KF6WlH0c-s/edit).

Chưa chứng minh mạng nhân viên đã nhận việc liên máy hoặc được quyền ghi/gửi production. Chi tiết nguồn, tình huống CEO, runtime và audit nằm trong bản A đầy đủ; giới hạn này không phủ nhận test tổng hợp hai Claude đã PASS.

Nguồn bổ sung: **SUPPLY-SESSION-AUDIT.md**, audit 31/10, đọc đúng phiên Cung ứng và kiểm lại tài liệu/source; map v18 cutoff 26/10 không thay toàn bộ nguồn 28/10. Kho B6 và Kom workbook đã có neo trong A đầy đủ. Chưa có receipt chứng minh các nhân viên đã chạy trọn vòng.
