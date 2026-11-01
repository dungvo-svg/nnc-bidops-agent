# BIDOPS-P1-001 — Yêu cầu cải tiến, chưa duyệt

Nguồn phương pháp: [SOP P1/P2](../sources/method/SOP-P1-P2-VA-CA-KHO-2-v1.pdf), trang 1–2. Phiếu này là điểm bắt đầu, không phải SRS hoàn tất.

| Trường | Nội dung hiện tại |
| --- | --- |
| Khó khăn | Giá/quy cách/NCC ở nhiều file và chat; nhập/cập nhật/ghép qua nhiều BV, dễ nhầm lịch sử và dữ liệu mới. |
| Bằng chứng | Oanh/CEO/Phet 30/10; workbook/ảnh/Stevimed và kế hoạch R10 trong sources. |
| Người sử dụng đầu ra | Nhóm Thầu/Cung ứng; người cụ thể cho ca đầu chờ xác nhận. |
| Chủ nghiệp vụ/người duyệt | Chờ Dũng/chủ nghiệp vụ chốt theo phạm vi; không mặc định Oanh duyệt toàn BidOps từ vai ở ca Kho. |
| Phạm vi đề xuất | Một ca cập nhật/ghép có sai khác và một đầu ra để quyết định; chọn gói/lô/dòng cụ thể sau. |
| Không gian hiện tại | 5 BV để đối chiếu; danh mục chào được chọn riêng, không mặc định 100%. Không can thiệp Mittaphab đang làm. |
| Baseline | Chưa đo; chưa điền số 0 hoặc số tiết kiệm. |
| Trạng thái | Thu thập/đối chiếu xong một đợt; as-is, phương án và tiêu chí chưa được nghiệp vụ chấp nhận. |

## As-is tái dựng, cần xác nhận

BV phát hành yêu cầu → Phet/nhóm tập hợp file → Cung ứng tìm/nhận phản hồi → ghép vào bảng giá/bảng gốc → tính/so sánh → người có quyền chốt → đầu ra từng gói. Các chỗ sửa tay, quyền cập nhật, cách lan thay đổi và vòng kiểm thực tế chưa được xác nhận toàn bộ.

## Đầu vào / đầu ra đề xuất

Đầu vào: yêu cầu đúng version, file master hiện hành, phản hồi/quote NCC có ngày/đơn vị/hiệu lực, quy tắc giá được người sở hữu xác nhận, vai/quyền, ví dụ được phép. Đầu ra: một dòng quyết định có liên kết nguồn, sai khác, giá theo basis, tình trạng chứng từ/giao/capacity và người cần chốt; bản xem theo BV từ cùng dữ liệu đã kiểm.

Không tự công nhận tương đương, chọn NCC, giá bán hay cam kết giao. Chưa biết ghi chưa biết; treo phần có xung đột nhưng tiếp tục phần độc lập. Việc “đã được giao”, “đã nhận file”, “đã kiểm”, “đã nạp”, “được phép dùng chào” là các trạng thái khác nhau.

## Các cách cần so sánh

1. Thống nhất quy trình/form/chủ master và tận dụng Excel có sẵn.
2. Chuẩn hóa cấu hình/Skill hoặc thêm một bước đối chiếu có dấu vết.
3. Xây/cập nhật công cụ nếu hai cách trên chưa đủ; chọn giao diện sau khi hiểu ca.

## Tiêu chí P1 cần người nghiệp vụ chấp nhận

Phiếu có mã ca, hiện trạng được xác nhận, luồng đề xuất, vai/IO/ngoại lệ/phần người giữ, ví dụ được phép và tiêu chí đúng/sai. Người mới giải thích được phương án và tự dựng hồ sơ với mức hỗ trợ ghi thật. Chủ nghiệp vụ chấp nhận đầu ra. Người thử độc lập do Dũng xác nhận sau, không tự nhận người soạn là đã thử độc lập.

Các quyết định và bằng chứng nhận: [DECISIONS.md](DECISIONS.md). Chỉ chuyển phần cần xây/cập nhật sang P2 khi đầu vào đã rõ/chốt tương đương theo SOP.
