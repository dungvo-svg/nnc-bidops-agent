# Ghi chú THU8 – kiểm chất liệu, 12/11/2026

**Ba ảnh là mô phỏng AI, chờ Dũng duyệt; không phải ảnh sản phẩm thật.** Các vật liệu chưa có nguồn xác nhận được biểu diễn theo quy ước thiết kế trong brief, không coi hình là bằng chứng chất liệu hoặc hình dáng sản phẩm.

## Đối chiếu chất liệu với hình

| Hạng mục theo brief | Kết quả quan sát và giới hạn |
|---|---|
| Amitriptylin: hộp giấy ivory cán mờ, in offset, gấp sắc | Thấy hộp giấy màu kem và mép hộp; bề mặt nhìn tương đối mờ nhưng vẫn có phản sáng trên nếp. Không thể xác minh định lượng 300 g/m², công nghệ in hoặc lớp cán từ ảnh. |
| Amitriptylin: vỉ nhôm–PVC, 10 ô 2×5 | Có một vỉ mặt hõm trong với 10 viên và một vỉ mặt bạc với 10 ô; thấy đường đứt nét phân ô và tên/hàm lượng lặp một màu. Vật liệu, độ nhám và đường xé là mô phỏng, không thể xác nhận đặc tính thật. |
| Amitriptylin: viên tròn trắng phẳng không khắc | Thấy 10 viên tròn trắng, không thấy rãnh hoặc chữ khắc; hình dạng và màu là quy ước chưa có ảnh hàng thật xác nhận. |
| Esomex: hộp giấy ivory cán mờ | Có hộp mỏng và bề mặt giấy sáng; có chút phản sáng trên mép và vùng màu. Không thể chứng minh 300 g/m², offset hoặc lớp cán qua ảnh. |
| Esomex: vỉ nhôm–PVC, 10 ô 2×5 | Có mặt hõm trong với 10 nang và mặt bạc 10 ô, đường đứt nét và “ESOMEX 20 mg” lặp một màu; hiệu ứng vỉ/nhôm là mô phỏng. |
| Esomex: nang cứng trắng ngà cỡ 2 | Thấy 10 nang một màu trắng ngà; không có thước hoặc bằng chứng để xác nhận thực tế là cỡ 2. |
| Lactate: chai PP bán trong 500 ml, thân tròn, vòng treo | Thấy chai bán trong thân tròn, vai thuôn, vòng treo dưới đáy; PP và dung tích vật lý không thể xác minh qua ảnh. |
| Lactate: nút cao su và nắp nhựa trắng giật/xé | Thấy nắp trắng có phần kéo và dải tối tại cổ; nút cao su bên dưới không thấy rõ, chưa xác nhận hình dáng hay cấu tạo. |
| Lactate: nhãn mực xanh in trực tiếp, không giấy dán | Chữ xanh nhìn nằm trên thân, không thấy viền tem giấy rõ; kỹ thuật in thực tế không kiểm chứng được. |
| Lactate: dung dịch trong, không màu, gần vai | Có mức chất lỏng trong gần vai, là chi tiết mô phỏng. |

Hai vỉ trong mỗi ảnh hộp dùng để thấy hai mặt, không nhằm thay đổi quy cách sản phẩm. Đã xem phóng to chữ trên hai lá nhôm và nhãn chai; chữ nhỏ mặt bên hộp vẫn cần kiểm tại kích thước form thực tế. Không đối chiếu được sản phẩm thật, chưa gửi hoặc nộp.

## Công cụ và tham số

Công cụ `image_gen__imagegen` tích hợp, edit từ ảnh THU6 của từng hộp hoặc THU7 của chai, `transparent_background=false`. Hộp kết quả 1536 × 1024; chai 1254 × 1254 px. Công cụ không cung cấp tên model và không cho chọn hoặc xác nhận `quality=high`, `size`, `input_fidelity`; không khẳng định đã đặt các giá trị đó. Các prompt đầu là yêu cầu một lượt thay đổi vật liệu/vỉ; Esomex có thêm một lượt sửa duy nhất trên chữ lá nhôm.

## Prompt thực tế từng ảnh

### Amitriptylin

Ảnh tham chiếu: `KOM-1017_Amitriptylin-25mg_THU6.png`.

```text
USE: material trial for a packaging mockup; image 1 is the approved composition.
SCENE: Keep the same white background, light and framing.
SUBJECT: Change ONLY the packaging materials and blister views. Keep the thick carton, all its artwork and label text exactly. Show ten round, flat, unscored, unmarked white tablets in a 2×5 blister with transparent cavities. Add a second blister turned over to show its matte silver foil and perforations. The foil shows ONLY the product name "Amitriptylin 25 mg" repeated verbatim.
MATERIAL: matte-laminated white ivory paperboard carton (~300 gsm), offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights.
aluminium–PVC blister: clear thermoformed PVC cavities on the front; silver matte aluminium lidding foil on the back printed in one colour with the product name; perforation lines between cells.
TEXT: Preserve product geometry and label legibility exactly. All carton text EXACT, verbatim, no changes, additions or omissions.
CONSTRAINTS: No ℞, logos, barcode, GMP, registration number, batch numbers or extra writing. Keep natural matte light. Blisters represent 10 units each.
```

### Esomex

Ảnh tham chiếu: `KOM-0356-0359-0363-0373-0626_Esomex-20_THU6.png`.

```text
USE: material trial for a packaging mockup; image 1 is the approved composition.
SCENE: Keep the same white background, light and framing.
SUBJECT: Change ONLY the packaging materials and blister views. Keep the thin carton, all its artwork and label text exactly. Show ten uniform ivory-white hard gelatin capsules in a 2×5 blister with transparent cavities. Add a second blister turned over to show its matte silver foil and perforations. The foil shows ONLY the product name "ESOMEX 20" repeated verbatim.
MATERIAL: matte-laminated white ivory paperboard carton (~300 gsm), offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights.
aluminium–PVC blister: clear thermoformed PVC cavities on the front; silver matte aluminium lidding foil on the back printed in one colour with the product name; perforation lines between cells.
TEXT: Preserve product geometry and label legibility exactly. All carton text EXACT, verbatim, no changes, additions or omissions.
CONSTRAINTS: No ℞, logos, barcode, GMP, registration number, batch numbers or extra writing. No contrasting capsule colours. Blisters represent 10 units each.
```

### Lactate

Ảnh tham chiếu: `KOM-0029_Lactate-Ringer-Dextrose-5pct_THU7.png`.

```text
USE: material trial for a packaging mockup; image 1 is the approved composition.
SCENE: Keep the same white background, light and framing.
SUBJECT: Change ONLY the bottle material and closure as specified; keep the full existing label artwork, layout, every word and line exactly as image 1.
MATERIAL: semi-transparent matte polypropylene IV bottle, rounded body, hanging ring at the base, rubber stopper with white plastic tear-off cap; label printed directly on the plastic in blue ink, not a paper sticker; clear colourless solution.
TEXT: Preserve product geometry and label legibility exactly. All bottle text EXACT, verbatim, correct Vietnamese diacritics, no changes, additions or omissions; keep the lower two columns and "Số lô SX:" "NSX:" "HD:" blank in a single row.
CONSTRAINTS: No ℞, logos, barcode, GMP, registration number, batch numbers, extra writing, carton or sticker. Soft natural lighting.
```

### Sửa chữ mặt nhôm Esomex

```text
USE: Local correction to a packaging material trial.

CHANGE ONLY: On the silver foil blister at lower right, change every repeated "ESOMEX 20" into "ESOMEX 20 mg" so every one of its 10 cells contains EXACT, verbatim "ESOMEX 20 mg" in one colour.

PRESERVE: Preserve product geometry and label legibility exactly. Keep the carton front, side, top, all existing carton wording, both blisters, capsule count and shape, lighting, materials, background and framing unchanged.

CONSTRAINTS: No additional words, logo, barcode, GMP, ℞, registration or numbers. No change to the carton; do not alter or remove text.
```

