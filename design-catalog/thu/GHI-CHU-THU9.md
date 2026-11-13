# Ghi chú THU9 – hai bước 1a và 2a, 12/11/2026

Trạng thái: bản thử chờ Claude/Dũng duyệt. Ảnh mô phỏng AI, không phải ảnh hàng thật. Không thực hiện bước 1b, 2b hay chỉnh Lactate.

## 1a – Amitriptylin

- Ảnh gốc: `KOM-1017_Amitriptylin-25mg_THU8.png`.
- Cách làm: một lượt edit bằng công cụ tạo ảnh tích hợp; một ảnh tham chiếu là đúng THU8, `transparent_background=false`. Công cụ không trả tên model hoặc tham số chất lượng; không xác nhận được model/quality. Ảnh đầu ra 1536 × 1024.
- Prompt đúng nguyên văn mục 1a của kế hoạch:

```text
Edit Image 1 (the current packshot). Change ONLY one thing: remove the second blister on the right (the one showing the silver foil back side with printed text). Keep the remaining front-side blister with 10 white tablets; you may move it slightly to the centre-left so the composition stays balanced. Do not add any new object.
Keep everything else exactly the same: carton size and thickness, carton front artwork and all text, carton side panel and top, lighting, shadows, white background, camera angle.
```

### Soát kết quả

| Điểm | Kết quả |
|---|---|
| Bỏ vỉ mặt sau; còn 1 vỉ mặt trước 2×5 | **Đạt qua quan sát**: còn 10 viên, vỉ dời nhẹ vào giữa-trái; không thấy vật mới. |
| Kích thước, độ dày và góc hộp | **Đạt qua quan sát**, nhưng không giữ nguyên tuyệt đối theo pixel; cần duyệt visual. |
| Mặt trước và chữ | **Chưa đạt yêu cầu giữ nguyên tuyệt đối**: so pixel vùng x=200–1099, y=250–649, 352.362/360.000 pixel khác; chênh trung bình 2,773 mức/kênh. Chữ nhìn tương tự nhưng không coi là bản pixel gốc. |
| Mặt bên | **Chưa đạt tuyệt đối**: vùng x=1115–1399, y=220–609 có 107.195/111.150 pixel khác. Không chứng minh được tất cả nét chữ được giữ y nguyên. |
| Nắp | **Chưa đạt tuyệt đối**: vùng x=500–1099, y=35–139 có 61.398/63.000 pixel khác. |
| Ánh sáng, bóng và nền | **Chưa đạt tuyệt đối**: ví dụ vùng nền trên cùng x=0–1535, y=0–24 có 38.130/38.400 pixel khác. Mức khác trên là so sánh pixel RGB, không đồng nghĩa toàn bộ khác biệt nhìn thấy rõ. |

**Kết luận 1a: chưa đạt điều kiện giữ nguyên tuyệt đối; không chuyển sang 1b khi chưa được duyệt.**

## 2a – Esomex 20

- Ảnh gốc: `KOM-0356-0359-0363-0373-0626_Esomex-20_THU6.png`, không dùng THU8.
- Cách làm: dựng `KOM-0356-0359-0363-0373-0626_Esomex-20_THU9_ARTWORK-BEN.png` bằng code; nền RGB (0,96,70), chữ trắng dọc `ESOMEX 20` và `Esomeprazol 20 mg`; ánh xạ phối cảnh OpenCV lên tứ giác (1224,199), (1414,135), (1414,607), (1224,693), trong ảnh 1536 × 1024. Không chạy model tạo ảnh cho bước này.

| Điểm | Kết quả |
|---|---|
| Mặt bên xanh, chữ trắng dọc, chỉ 2 dòng yêu cầu | **Đạt theo artwork và quan sát**; chữ hoạt chất nhỏ do mặt bên hẹp, cần người duyệt xem ở kích thước sử dụng. |
| Hộp mỏng, hình học và độ dày | **Đạt về pixel ngoài vùng ghép**; ranh giới tứ giác cạnh đã đổi theo thiết kế, cần duyệt visual. |
| Mặt trước, nắp, vỉ, nền, ánh sáng | **Đạt ngoài vùng tứ giác ghép**: kiểm so sánh RGB ghi nhận 0 pixel khác ngoài mask 92.384 pixel của tứ giác; đường biên mask thuộc vùng sửa. |

File THU6/THU8 nguồn không bị ghi đè; chưa gửi, chưa nộp, chưa sửa ảnh Lactate.
