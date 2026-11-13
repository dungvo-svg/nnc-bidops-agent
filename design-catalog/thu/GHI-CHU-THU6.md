# Ghi chú THU6 – 12/11/2026

**Mẫu mô phỏng AI, chờ Dũng duyệt. Không phải ảnh chụp sản phẩm thật và không chứng minh hình dạng bao bì, viên hoặc chai thực tế.** Chưa gửi hoặc nộp thầu.

## Nguồn và cách thực hiện

Chữ và phạm vi được phép lấy từ `outputs/thuoc-kom-tinh-kiem-gia-20261111/v1/thiet-ke-mau/BRIEF-TUNG-SP_3-MAU_20261112.md`. Dùng ảnh THU5 làm tham chiếu thiết kế cho công cụ tạo ảnh tích hợp; chỉnh chữ mặt bên hai hộp và phần chữ nhỏ của chai bằng code, kiểm ảnh ở kích thước đầy đủ. Các câu và dữ liệu được xuống dòng để vừa bề mặt; dấu `x` theo cột Chữ in. Không thêm số lô, ngày, số đăng ký, mã vạch, GMP, logo hoặc ℞.

## Soát chữ theo từng ảnh

- **Amitriptylin – KOM-1017:** `Amitriptylin 25 mg`; `Mỗi viên nén chứa: Amitriptylin 25 mg`; `Viên nén · Uống`; `Hộp 10 vỉ x 10 viên nén`; `Box of 10 blisters x 10 tablets`; `Cơ sở sản xuất: Công ty CP Dược phẩm Khánh Hòa (Khapharco) – Việt Nam`. Mặt bên có ba câu chuẩn và nhãn `Số lô SX:`, `NSX:`, `HD:` để trống.
- **Esomex – KOM-0356/0359/0363/0373/0626:** `ESOMEX 20`; `Mỗi viên nang cứng chứa: Esomeprazol 20 mg`; `Viên nang cứng · Uống`; `Hộp 2 vỉ x 10 viên nang cứng`; `Box of 2 blisters x 10 hard capsules`; `Cơ sở sản xuất: USA NIC – Việt Nam`. Mặt bên có ba câu chuẩn và ba nhãn để trống như trên. Chính tả hoạt chất dùng `Esomeprazol` theo brief THU6, khác chữ `Esomeprazole` trong THU5.
- **Lactate Ringer – KOM-0029:** `LACTATE RINGER & DEXTROSE 5%`; `Ringer lactat + Glucose 5%`; `Dung dịch tiêm truyền · Truyền tĩnh mạch`; `500 ml`; `Cơ sở sản xuất: Công ty CP Hóa – Dược phẩm Mekophar – Việt Nam`. Có ba câu chuẩn và ba nhãn để trống; không thêm bảng thành phần chi tiết.

Ba câu chuẩn: `Đọc kỹ hướng dẫn sử dụng trước khi dùng`; `Để xa tầm tay trẻ em`; `Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng`.

## Giới hạn cần duyệt

- Chữ mặt bên Esomex nhỏ vì góc phối cảnh; cần kiểm lại trong form thực tế. Bản chai có chữ nhỏ khá dày; chưa kiểm mức đọc khi thu nhỏ cao 90 px.
- Viên Amitriptylin trong ảnh là mô phỏng chưa có mô tả hình dạng từ nguồn; nang Esomex màu ngà trung tính là minh họa. Hộp/chai, ánh sáng và các chi tiết bề mặt không xác nhận là hình thật của nhà sản xuất.
- Nội dung trên các mặt không thấy trong góc chụp chưa được dựng riêng; nắp Amitriptylin chưa có tên in như bố cục gợi ý. Bố cục và hình thức cần Dũng duyệt.
- Excel nguồn và THU5 được giữ nguyên.

## Nhật ký công cụ, tham số và prompt đã dùng cho THU6

Đây là nhật ký thực tế của lượt THU6, không phải thông số của một lần chạy mới theo hướng dẫn vừa bổ sung.

- Công cụ: `image_gen__imagegen` tích hợp, chế độ edit với **một** ảnh THU5 tương ứng trong `referenced_image_paths`; `transparent_background=false`. Tên model thực thi không được công cụ trả về nên **không xác định**; không có tham số `model`, `quality` hay `size` trong giao diện công cụ hiện có, do đó **không xác nhận đã dùng `quality=high`**. Kích thước ảnh kết quả: hai hộp 1536 × 1024, chai 1254 × 1254 px.
- Lượt THU6 đã kết thúc trước khi nhận hướng dẫn prompt mới; không có artwork phẳng trước/sau được truyền làm hai ảnh tham chiếu và không truyền ảnh hộp thật nội bộ. Không khẳng định THU6 đã chạy theo quy trình mới.
- Sau ba lệnh edit, phần chữ mặt bên của hai hộp được dựng bằng Pillow và ghép biến đổi phối cảnh OpenCV; phần chữ nhỏ nhãn chai được xóa và dựng lại bằng Pillow/OpenCV. Các hình học, chữ và thứ tự được lấy từ `BRIEF-TUNG-SP_3-MAU_20261112.md`; đây là chỉnh sửa bằng code, không phải prompt model bổ sung.

### Amitriptylin – prompt thực tế

Ảnh tham chiếu: `KOM-1017_Amitriptylin-25mg_THU5.png`.

```text
Edit packshot while maintaining premium realistic matte printed carton and 10-tablet blister. Change view to 3/4 with broad visible side and top. Remove Rx symbol and all Rx text completely. Print only these exact texts with precise Vietnamese accents, and no other words or symbols: Front: "Amitriptylin 25 mg" / "Viên nén · Uống" / "Hộp 10 vỉ x 10 viên nén" / "Cơ sở sản xuất: Công ty CP Dược phẩm Khánh Hòa (Khapharco) – Việt Nam". Side: "Mỗi viên nén chứa: Amitriptylin 25 mg" / "Box of 10 blisters x 10 tablets" / "Đọc kỹ hướng dẫn sử dụng trước khi dùng" / "Để xa tầm tay trẻ em" / "Số lô SX:" / "NSX:" / "HD:". Leave fields after colons empty. No logo, GMP, registration, barcode or additional writing. 3D with softly lit matte paper.
```

### Esomex – prompt thực tế

Ảnh tham chiếu: `KOM-0356-0359-0363-0373-0626_Esomex-20_THU5.png`.

```text
Edit the thin carton packshot to show a broader readable side and top while retaining realistic premium matte texture and 10 white hard capsules. Ensure NO Rx. Print only exact wording, correct every letter and accent: Front: "ESOMEX 20" / "Mỗi viên nang cứng chứa: Esomeprazol 20 mg" / "Viên nang cứng · Uống" / "Hộp 2 vỉ x 10 viên nang cứng" / "Cơ sở sản xuất: USA NIC – Việt Nam". Side: "Box of 2 blisters x 10 hard capsules" / "Đọc kỹ hướng dẫn sử dụng trước khi dùng" / "Để xa tầm tay trẻ em" / "Số lô SX:" / "NSX:" / "HD:". Leave fields after colons empty. No logo, GMP, registration, barcode or other writing.
```

### Lactate Ringer – prompt thực tế

Ảnh tham chiếu: `KOM-0029_Lactate-Ringer-Dextrose-5pct_THU5.png`.

```text
Edit the infusion bottle design preserving true-to-life matte translucent 500ml bottle and hanging loop, no box. REMOVE Rx sign and text completely. Print ONLY the following exact readable Vietnamese text on the bottle, with correct diacritics and no other words: "LACTATE RINGER & DEXTROSE 5%" / "500 ml" / "Ringer lactat + Glucose 5%" / "Dung dịch tiêm truyền · Truyền tĩnh mạch" / "Cơ sở sản xuất: Công ty CP Hóa – Dược phẩm Mekophar – Việt Nam" / "Đọc kỹ hướng dẫn sử dụng trước khi dùng" / "Để xa tầm tay trẻ em" / "Số lô SX:" / "NSX:" / "HD:". Leave blank after colons, no numbers, no logo, no GMP, no registration, no barcode, no extra text. Keep label natural and legible.
```

Các prompt trên chưa có câu chuẩn dài về chỉ định/chống chỉ định; câu đó được bổ sung trong bước dựng chữ bằng code sau khi tạo ảnh. Các giới hạn về chữ nhỏ, nắp và tính mô phỏng ở trên vẫn áp dụng.
