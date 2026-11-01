# P2 — Điều kiện và ca kiểm đề xuất

Theo [SOP trang 3–4](../sources/method/SOP-P1-P2-VA-CA-KHO-2-v1.pdf). Chưa có build hoặc kết quả thử ở đây. Chọn bước theo loại đầu ra, không ép một bảng tính/báo cáo qua quy trình deploy App.

Trước phần thay đổi cần yêu cầu P1 đã rõ/chốt tương đương, phiên bản đang dùng, phạm vi thay đổi, dữ liệu/môi trường được phép, expected result và cách quay lại. Giữ riêng nguồn thật/cấu hình/thông tin truy cập. Người kỹ thuật kiểm thay đổi, chủ nghiệp vụ kiểm đầu ra; người thử độc lập do Dũng chốt.

| Ca dự kiến | Kết quả mong đợi |
| --- | --- |
| Ghép cùng item khác unit/pack/600-500 ml/Com-Amp | Nêu sai khác; không tự chuyển giá hoặc nhận tương đương. |
| STT trùng/ENT khác số giữa sheet | Không ghép bằng STT duy nhất; truy được requirement và offer version. |
| Quote lịch sử, hết hiệu lực, thiếu ngày | Trạng thái chưa đủ kiểm; không gắn nhãn giá hiện hành. |
| Currency CNJ, ngày sai, thiếu FX | Nêu dòng và nguồn; chưa tính kết quả sai âm thầm. |
| Cước blank/zero/unconfirmed | Ba nghĩa khác nhau; không coi blank là zero hoặc bỏ dòng mà không thể thấy lý do. |
| Giá chốt khác công thức amount/tham số khác note | Nêu xung đột, chờ owner; kiểm lại đúng phần được thay trên bản sao. |
| Source mới ảnh hưởng nhiều BV | Có diff và lịch sử, một đầu ghi master; không ghi bộ gửi cũ. |
| Lưu/tải lại/thử lại kết quả chưa rõ | Giữ mã thao tác, đối soát trước retry; không nhân đôi hoặc ghi đè phiên bản mới. |
| Lô ảnh cũ/route bị hạn chế/capacity thiếu | Bằng chứng thiếu được trình người duyệt; không tự cam kết chọn hàng. |

Tạo dữ liệu tổng hợp trong [fixtures](../data-work/fixtures/README.md), giữ giá trị giả định ghi rõ. Đầu ra theo [outputs](../outputs/README.md). Khi chạy mới ghi môi trường, version, expected/actual, lỗi còn lại, bằng chứng, người kiểm và quyết định. Baseline thao tác và thời gian chờ tách riêng; chưa đo để trống. Không ghi Đạt từ việc có sẵn checklist.
