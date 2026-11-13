# Ghi chú THU7 – Lactate Ringer, 12/11/2026

**Mẫu AI mô phỏng, chờ Dũng duyệt. Không phải ảnh sản phẩm thật; kiểu chai, chất liệu và nhãn chưa được nhà sản xuất xác nhận.** Chưa gửi hoặc nộp thầu.

## Kết quả và kiểm chữ

- Chỉ dựng lại KOM-0029; hai ảnh hộp THU6 được giữ nguyên. Artwork nhãn phẳng: `KOM-0029_Lactate-Ringer-Dextrose-5pct_THU7_ARTWORK.png`; hình: `KOM-0029_Lactate-Ringer-Dextrose-5pct_THU7.png`.
- Đã xem hình và phóng to hai cột cùng hàng cuối để so với `BRIEF-TUNG-SP_3-MAU_20261112.md`: tên, `500 ml`, `Ringer lactat + Glucose 5%`, dạng/đường dùng, tên cơ sở, ba câu chuẩn và `Số lô SX:`, `NSX:`, `HD:` được giữ; giá trị lô/ngày để trống. Không thấy ℞, logo, GMP, số đăng ký hoặc mã vạch. Các dòng được ngắt để vừa nhãn.
- Nhãn có dải tên, dung tích lớn, hai cột thông tin và hàng ba nhãn ở đáy; không thấy mảng trắng cắt lệch sau `500 ml` như THU6. Chữ nhỏ chưa được kiểm đọc khi ảnh thu xuống 90 px trong form thực tế.

## Thực thi và tham số

- Công cụ: `image_gen__imagegen` tích hợp, edit; `referenced_image_paths` theo thứ tự: Image 1 = artwork THU7 vẽ bằng code; Image 2 = ảnh chai THU6. `transparent_background=false`. Không dùng ảnh R0047 nội bộ làm đầu vào; chỉ dùng mô tả bố cục trong brief. Chưa ghép lại artwork sau edit vì nội dung chữ phóng to quan sát được khớp brief.
- Model: công cụ không cung cấp tên model. Giao diện công cụ không cho chọn hoặc xác nhận `quality=high`, `size` hay `input_fidelity`; không thể khẳng định đã dùng các tham số đó. Kết quả PNG 1254 × 1254 px.

## Prompt thực tế

```text
USE: A photorealistic product packshot concept, square composition, for review.

SCENE: White seamless background, soft diffuse light, gentle shadow. No extra props.

SUBJECT: Image 2 is the infusion bottle to preserve: upright transparent matte 500 ml bottle with liquid, white sealed port, bottom hanging ring. Preserve product geometry exactly.

LABEL: Change ONLY the bottle printing to the exact artwork in Image 1. Print directly on the bottle and follow its curved surface; avoid white cutout or pasted rectangle. Preserve layout and label legibility exactly: bold blue name band, large "500 ml", ingredient and route, then two distinct smaller columns. At the bottom place "Số lô SX:" / "NSX:" / "HD:" in one horizontal row; leave values blank.

TEXT: Reproduce Image 1 text EXACT, verbatim, correct Vietnamese spelling and diacritics, no omission, no extra characters. Each line appears once. Ensure no ℞.

MATERIAL: Translucent matte polypropylene, subtle diffuse light, soft reflections only.

CONSTRAINTS: Keep bottle and label geometry, proportions and legibility exactly. No other text, logos, GMP, barcode, registration, batch numbers, extra images or marks.
```
