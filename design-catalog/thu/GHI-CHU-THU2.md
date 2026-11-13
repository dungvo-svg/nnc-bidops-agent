# Ghi chú mẫu thử 2 – 12/11/2026

**Trạng thái: mẫu thiết kế do AI dựng, chờ Claude/Dũng duyệt; không phải ảnh chụp hàng thật và chưa có xác nhận dùng làm bằng chứng nộp thầu.** Không làm các hàng khác trong lượt thử này.

## Nguồn và cách thực hiện

Nguồn nội dung: `outputs/thuoc-kom-tinh-kiem-gia-20261111/v1/thiet-ke-mau/THIET-KE-BAO-BI_36-MA-THIEU-ANH_20261112.xlsx`, tab **Brief thiết kế**, các ô dưới đây; cấu trúc nhãn lấy từ tab **Khung nội dung hộp** và khuôn v1/đính chính trong `BRIEF-CODEX_MAU-PHANG_20261112.md`. Artwork mặt chính được dựng bằng code, hình dáng packshot được AI tạo với artwork tham chiếu, sau đó ghép artwork bằng biến đổi phối cảnh. Các màu, vật liệu, hình khối, vỉ và viên là minh họa thiết kế, không xác nhận là ngoại hình hàng thực tế.

### KOM-1017 – Amitriptylin
- `AMITRIPTYLIN 25 mg`, `Amitriptylin 25 mg/viên`: B2/E2, áp dụng đính chính brief bỏ `(HCl)`; không khẳng định dạng muối.
- `Viên nén · Uống`: F2/G2; `Hộp 10 vỉ × 10 viên`: H2; `Sản xuất bởi: Khapharco – Việt Nam`: J2.
- Vỉ trong hình là mô phỏng; hình dạng, màu và rãnh viên chưa có nguồn xác nhận.

### KOM-0356 / 0359 / 0363 / 0373 / 0626 – Esomex 20
- `ESOMEX 20`: B8; `Esomeprazole 20 mg/viên`: E8; `Viên nang cứng · Uống`: F8/G8.
- `Hộp 2 vỉ × 10 viên nang cứng`: H8 kết hợp F8; `Sản xuất bởi: USA NIC – Việt Nam`: J8.
- Vỉ minh họa có 10 viên, nhưng màu và hình viên chưa có ảnh gốc để xác nhận. Dải hình học xanh là họa tiết đề xuất, không phải nhận diện đã xác minh của hãng.

### KOM-0029 – Lactate Ringer & Dextrose 5%
- `LACTATE RINGER & DEXTROSE 5%`: B12; `500 ml`: H12; `Ringer lactat + Glucose 5%`: E12; `Dung dịch tiêm truyền` / `Truyền tĩnh mạch`: F12/G12; `Sản xuất bởi: Mekophar – Việt Nam`: J12.
- `Thành phần trong 500 ml: theo công bố NSX` là ô giữ chỗ theo brief, không phải công thức đã xác nhận. Kiểu chai và nhãn chỉ là minh họa.

## Các chữ/ô giữ chỗ chung

- `Rx – Thuốc bán theo đơn`: giữ trên Amitriptylin và Lactate Ringer theo chỉ đạo Dũng; phân loại cần được đối chiếu hồ sơ sản phẩm. Esomex 20: chờ xác nhận phân loại kê đơn theo SĐK; ô Rx đã được bỏ trên hình. Không in ghi chú chờ xác nhận lên bao bì.
- `SĐK: …`, `Mã vạch`, `Lô: …`, `HSD: …`: giữ chỗ theo brief và tab Khung nội dung hộp; không có số thật hoặc mã thật. Không thêm logo, địa chỉ, tá dược, hay công bố GMP.
- Nhãn `Sản xuất bởi` là từ khuôn; tên NSX/nước theo cột J, cần xác minh bằng hồ sơ nhà sản xuất trước khi sử dụng.

## File và hạn chế kiểm

- 3 file `_THU2.png` là ảnh thử 1600×1200; 3 file `_ARTWORK.png` là mặt chính/nhãn bằng code. Mặt bên hộp trong packshot để trống, chưa dựng artwork riêng.
- Ảnh 85 px chiều cao chưa được người dùng kiểm đọc thực tế. Các đường ghép mặt hộp còn thấy viền mảnh; chai có độ sáng bề mặt nhẹ. Claude/Dũng cần duyệt visual.
- Vỉ, viên và hình chai không có bằng chứng đối chiếu ảnh gốc. Không dùng các hình này để khẳng định diện mạo hoặc quy cách thực tế của hàng.
- File Excel nguồn không chỉnh sửa. Chưa gửi, nộp hoặc cập nhật sheet.

## Ảnh lượt trước được giữ nguyên

Thực tế có 25 ảnh, không phải 15; toàn bộ đã chuyển từ gốc `design-catalog/` sang `design-catalog/nhap-v0/`, không xóa. Đây là nháp cũ chưa kiểm và chưa đạt chuẩn; danh sách:

- `KOM-0029_Lactate-Ringer-Dextrose-5pct_MAU-PHANG.png`
- `KOM-0053_Sodium-Chloride-09pct_MAU-PHANG.png`
- `KOM-0192_Calci-Doremi_MAU-PHANG.png`
- `KOM-0210-0211_Carvedilol-DWP-10mg_MAU-PHANG.png`
- `KOM-0242_Cimetidin-400_MAU-PHANG.png`
- `KOM-0296_Vindexa-8mg-2ml_MAU-PHANG.png`
- `KOM-0337_Paracetamol-05g_MAU-PHANG.png`
- `KOM-0356-0359-0363-0373-0626_Esomex-20_MAU-PHANG.png`
- `KOM-0366_Etodolac-300mg_MAU-PHANG.png`
- `KOM-0375_Famotidin-40mg_MAU-PHANG.png`
- `KOM-0383_Deferasirox-250mg_MAU-PHANG.png`
- `KOM-0560_Betahistin-DWP-12mg_MAU-PHANG.png`
- `KOM-0569_Mecobalamin-500_MAU-PHANG.png`
- `KOM-0650_Nufotin-20mg_MAU-PHANG.png`
- `KOM-0658_Olanz-10_MAU-PHANG.png`
- `KOM-0687_Paracetamol-AT-inj_MAU-PHANG.png`
- `KOM-0745_Povidone-Iodine-10pct_MAU-PHANG.png`
- `KOM-0784_Povidone-10pct-500ml_MAU-PHANG.png`
- `KOM-0941_Docolin_MAU-PHANG.png`
- `KOM-1017_Amitriptylin-25mg_MAU-PHANG.png`
- `KOM-1026_Valbitrin-100_MAU-PHANG.png`
- `KOM-1032-0836-0838_Rosuvastatin-10_MAU-PHANG.png`
- `KOM-1034_Rosuvastatin-5_MAU-PHANG.png`
- `KOM-1091_Mekozetel-200mg_MAU-PHANG.png`
- `KOM-1092_Mekozetel-400_MAU-PHANG.png`
