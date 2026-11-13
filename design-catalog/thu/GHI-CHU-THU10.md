# Ghi chú THU10 – Amitriptylin bước 1b

**Trạng thái: mẫu thử chờ duyệt.** Ảnh gốc là `KOM-1017_Amitriptylin-25mg_THU9.png`; ảnh AI mô phỏng, không xác nhận ngoại hình bao bì thực tế. Không thay đổi Esomex hay Lactate.

## Cách làm

- Dựng artwork bằng SVG trong HTML, font Arial có dấu tiếng Việt; render PNG 1200 × 2100 px bằng Chrome headless. Dải đỏ `#92030d` được chọn từ vùng đỏ mặt trước; nền sáng hơi tối hơn mặt trước theo màu quan sát từ mặt bên gốc. Không dùng model để viết hoặc sửa chữ.
- Ghép artwork bằng biến đổi phối cảnh OpenCV vào bốn đỉnh `(1110,233)`, `(1422,108)`, `(1422,618)`, `(1110,781)` trên ảnh 1536 × 1024; gốc tọa độ ở góc trên trái. Mask bao gồm đường biên tứ giác; tứ giác nằm hơi vào trong các mép hiện hữu để giữ cạnh hộp.
- Nền dải trên và dưới được nối về phía màu đỏ mặt trước; ánh sáng được mô phỏng bằng nền sáng hơi tối và gradient nhẹ. Mặt bên vẫn là artwork ghép, cần người duyệt visual về chất liệu và mép.

## Soát chữ artwork và bản mặt bên phóng to

Đã xem artwork gốc và vùng mặt bên trong ảnh THU10 phóng to 3 lần, đối chiếu nội dung Dũng giao. Các dòng dài được ngắt dòng trong ảnh, không thay chữ:

| Nội dung | Soát |
|---|---|
| `Amitriptylin 25 mg` | Đúng |
| `Thành phần:` | Đúng |
| `Mỗi viên nén chứa: Amitriptylin 25 mg` | Đúng; tách sau dấu hai chấm |
| `Dạng bào chế:` | Đúng |
| `Viên nén · Uống` | Đúng |
| `Quy cách:` | Đúng |
| `Hộp 10 vỉ x 10 viên nén` | Đúng |
| `Box of 10 blisters x 10 tablets` | Đúng |
| `Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng.` | Đúng; xuống 3 dòng |
| `Đọc kỹ hướng dẫn sử dụng trước khi dùng.` | Đúng; xuống 2 dòng |
| `Để xa tầm tay trẻ em.` | Đúng |
| `Số lô SX:      NSX:      HD:` | Đúng nhãn, giá trị để trống |

Chữ trong ảnh thành phẩm bị thu nhỏ và nghiêng theo phối cảnh. Đã soát bản phóng to; chưa xác nhận đọc được các dòng nhỏ tại kích thước ô form 90 px.

## So sánh pixel

- Sau khi lưu và mở lại PNG, so sánh từng pixel RGB giữa THU10 và đúng ảnh gốc THU9: **0 pixel khác ngoài mask tứ giác**; 161.809 pixel khác bên trong tổng 165.890 pixel thuộc mask. Pixel biên tứ giác được tính là bên trong vùng sửa.
- SHA-256 ảnh THU9 nguồn: `fde6e9f52a2343ec26bd3cc29197aa43f6ec9b46eaae9437e4792cb5e8eb1fe8`.
- SHA-256 ảnh THU10: `3398e2d48391ecb2066f155993dd9c30110ab6841c9dfdc2eecbc5df6e2ea4fc`.
- Kết quả giữ nguyên ngoài mask là so với **THU9**, không giải quyết lại khác biệt THU9 so với THU8 đã ghi trong `GHI-CHU-THU9.md`.
