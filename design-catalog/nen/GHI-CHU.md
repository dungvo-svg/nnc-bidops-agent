# Ảnh nền chai không chữ

Ảnh tạo bằng AI, dùng làm nền ghép nhãn; không phải ảnh sản phẩm thật hoặc bằng chứng xác minh kiểu chai, vật liệu hay dung tích. Nền được quan sát theo ảnh yêu cầu và tạo mới; ảnh tham chiếu R0781 nội bộ không được gửi cho công cụ tạo ảnh. Không có nhãn, chữ, logo hay vạch dung tích. Mỗi file PNG 1200 × 1200 px.

## Vùng thân gợi ý để ghép nhãn

Tọa độ `(x, y, w, h)` tính bằng pixel, gốc `(0,0)` ở góc trên trái; là vùng chữ nhật an toàn ước lượng trên mặt trước, không phải mask hoặc bề mặt phẳng vật lý. Tùy kích thước nhãn, dùng ít hơn và biến dạng nhẹ theo độ cong thân.

| File | x | y | w | h |
|---|---:|---:|---:|---:|
| `CHAI-PP-500ML_NEN.png` | 415 | 390 | 370 | 510 |
| `CHAI-PP-1000ML_NEN.png` | 455 | 300 | 290 | 650 |
| `CHAI-HDPE-500ML_NEN.png` | 410 | 360 | 390 | 650 |

Hai chai PP có cùng phong cách; chai 1000 ml có thân dài hơn trong khung, là mô phỏng chứ không biểu thị tỷ lệ kích thước hay dung tích đã đo. Với HDPE, tránh phần tay cầm bên trái và các góc bo. Phần nhựa trong có vùng phản sáng nhẹ và mực dịch; khi ghép nhãn cần tự điều chỉnh cho hợp hình.
