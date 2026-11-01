# 01 — PRD CORE: vì sao, kết quả, ranh giới (DRAFT, chưa khóa)

Chỉ giữ WHY / outcome / ranh giới. Quyết định ở `DECISIONS.md`, người-quyền ở `11`, nguồn ở `08`. Phần lớn nội dung lấy từ `discovery/PRODUCT-FRAMING.md` (evidence) và chỉ dẫn của Dũng; **chưa được chủ nghiệp vụ duyệt** — không có `LCK-*`.

## Vì sao

Nhóm Thầu/Cung ứng kênh HC (bệnh viện, phòng khám) của **Công ty NNC** phải chọn danh mục/gói có thể chào cho nhiều BV, trong khi yêu cầu BV, giá, quy cách và phản hồi NCC rải ở nhiều file và chat. Cập nhật/ghép bằng tay qua nhiều BV dễ nhầm lịch sử với dữ liệu mới và khó thấy dòng nào đủ điều kiện chào. Bằng chứng: `SRC-WA-0918` (Oanh), `SRC-WA-0922` (CEO), `SRC-WB-BGC`, `SRC-WB-KOM`, `SRC-STEVIMED`.

## Kết quả mong muốn (giả thuyết giá trị)

- Người có quyền chọn được danh mục/lô chào dựa trên: yêu cầu đúng version, phản hồi NCC có ngày/đơn vị/hiệu lực, giá còn hiệu lực, khả năng giao/chứng từ, tiền, và ai đã duyệt.
- Cập nhật bằng chứng **một lần** và thấy ảnh hưởng tới các BV liên quan; giảm rà lại và ghi sai phiên bản.
- Thước đo: **chưa có baseline** (D-chưa mở) — không điền số.

## Ranh giới

Trong phạm vi: phân loại đủ yêu cầu để thấy cơ hội/khoảng thiếu; ghép yêu cầu ↔ chào NCC có dấu vết; trình sai khác và điều kiện để người quyết.

Ngoài phạm vi / không làm:
- Không mặc định chào 100% danh mục; 5 BV là bối cảnh đối chiếu, danh mục chào quyết theo từng gói/lô.
- Không tự công nhận tương đương, chọn NCC, giá bán hay cam kết giao.
- Không can thiệp gói Mittaphab đang có người làm; không sửa bộ thầu đã gửi.
- Không gửi tin, upload, nộp thầu, mua hàng.
- Số liệu là của Công ty NNC, không phải tập đoàn; Vimart ngoài phạm vi.

## Sản phẩm đề xuất (30/10/2026, sau nghiên cứu — chưa duyệt)

Căn cứ: [`discovery/DINH-HINH-SAN-PHAM.md`](../discovery/DINH-HINH-SAN-PHAM.md).

- **Là gì:** lớp bằng chứng và quyết định theo từng gói thầu. Mỗi dòng yêu cầu BV (đúng version, có nguồn file/sheet/dòng) được ghép với hàng NNC và chào NCC (ngày, đơn vị, quy cách, hiệu lực, nguồn), mang một trạng thái (D13) và kịch bản giá theo basis đã xác nhận, rồi trình người có quyền chọn chào/không chào. Bản xem theo BV sinh từ cùng dữ liệu đã kiểm.
- **Ai dùng:** nhóm Thầu/Cung ứng HC (người làm giá, người tìm nguồn) và người có quyền chọn danh mục (chưa chốt — `CAP-PORTFOLIO`).
- **Đầu ra tối thiểu cho ca đầu:** một bảng quyết định cho một gói/lô: dòng yêu cầu · chào khớp/sai khác · trạng thái · thiếu gì · ai cần quyết.
- **Không phải (lúc này):** app mới, master thứ hai, công cụ nộp thầu, kênh gửi tin.
- **Dùng lại trước khi xây:** BGC (khóa MPSC sạch), pipeline `thau-bv-nnc` (ghép trạng thái A–D, `SCHEMA.md`), công cụ kiểm bảng giá mua (`cung-ung-ban-do/tools`) — quyết `REUSE/ADAPT` từng phần.

## Phân công trách nhiệm (định hướng, chưa chọn kiến trúc)

Quy tắc cố định (code/công thức) giữ đổi đơn vị, tiền, kiểm tra. Agent tìm bằng chứng và đề xuất ghép còn mơ hồ. Con người duyệt tương đương, danh mục, giá, NCC, cam kết. Cách làm cụ thể chờ D07.
