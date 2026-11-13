# Nhóm 1 Wealphar – ghi chú soát hai mẫu

**Trạng thái: hai ảnh mô phỏng AI chờ Claude duyệt; không phải ảnh chụp hàng thật.** Màu, vật liệu, hình viên và tỉ lệ là quy ước thiết kế trong brief, chưa xác nhận là hàng thật. Không gửi hoặc nộp thầu.

## Cách làm

Nguồn: `outputs/thuoc-kom-tinh-kiem-gia-20261111/v1/thiet-ke-mau/nhom/NHOM-1_WEALPHAR_20261112.md`. Artwork trước 1600 × 1000 và bên 1200 × 2100 được dựng bằng code với font Arial. Hai prompt riêng gọi công cụ `image_gen__imagegen` tích hợp: Image 1 là artwork trước của chính SP; Image 2 là artwork bên của chính SP; Image 3 là Amitriptylin THU10 chỉ tham chiếu góc/ánh sáng, với chỉ dẫn không sao màu, độ dày hay chữ. Không gửi ảnh nguồn nội bộ R0145/R0790. `transparent_background=false`; công cụ không cung cấp tên model, không có tham số chọn/kiểm `quality=high`, `size` hoặc `input_fidelity`.

Sau khi tạo ảnh, mặt bên được thay bằng đúng artwork bên qua phối cảnh OpenCV. Mặt trước là phần được model thể hiện từ artwork trước; đã xem đối chiếu trực tiếp, không ghép artwork trước. Tỉ lệ 100 × 55 × 30 mm là mục tiêu mô phỏng, không có phép đo vật lý và không thể khẳng định kích thước thật từ ảnh. Mỗi ảnh có một vỉ mặt trước 2×5 viên; không có vỉ lật mặt sau.

## Soát từng dòng

| Mục | Betahistin KOM-0560 | Carvedilol KOM-0210/0211 |
|---|---|---|
| Tên, hàm lượng | `Betahistin DWP` · `12 mg` | `Carvedilol DWP` · `10 mg` |
| Thành phần | `Mỗi viên nén bao phim chứa: Betahistin mesilat 12 mg` | `Mỗi viên nén chứa: Carvedilol 10 mg` |
| Dạng, đường dùng | `Viên nén bao phim · Uống` | `Viên nén · Uống` |
| Quy cách | `Hộp 6 vỉ x 10 viên nén bao phim` | `Hộp 6 vỉ x 10 viên nén` |
| Tiếng Anh bên | `Box of 6 blisters x 10 film-coated tablets` | `Box of 6 blisters x 10 tablets` |
| Cơ sở | `Cơ sở sản xuất: Wealphar – Việt Nam` | `Cơ sở sản xuất: Wealphar – Việt Nam` |
| Câu chuẩn | `Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng.` · `Đọc kỹ hướng dẫn sử dụng trước khi dùng.` · `Để xa tầm tay trẻ em.` | Như cột Betahistin |
| Hàng đáy bên | `Số lô SX:` · `NSX:` · `HD:`, giá trị trống | Như cột Betahistin |

- Các dòng trên đã được đối chiếu với artwork gốc; mặt trước trên ảnh sản phẩm được soát bằng mắt. Mặt bên đã xem ảnh phóng to, nhưng một số nét/dấu ở chữ rất nhỏ bị suy giảm do phối cảnh và độ phân giải, nhất là câu dài và dòng tiếng Anh; không khẳng định tất cả chữ nhỏ đọc chắc chắn trong ảnh hoặc ở 90 px. Cần Claude kiểm visual.
- Betahistin dùng 12 mg đúng bảng nhóm; workbook thiết kế trước đây có ghi chú dữ liệu cột khác 6 mg, cần chủ nguồn xác nhận nếu dùng cho hàng thực tế.
- Không thấy ℞, logo, GMP hay SĐK. Không có số lô/ngày được điền.
- Quan sát: mỗi mặt bên có thể thấy viền ghép mảnh và nền hơi phẳng so với ảnh model; mặt bên được ghép tứ giác nên tỷ lệ cảm nhận cần Claude duyệt.
- Phép so sánh sau ghép cho thấy 0 pixel thay đổi ngoài từng mask mặt bên so với ảnh model trung gian. Đây không chứng minh ảnh giống kích thước vật lý hoặc ảnh hàng thật.

## Prompt riêng thực tế

### Betahistin

```text
USE: Design mockup for visual review, photorealistic Vietnamese generic medicine packshot.

SCENE: Image 3 is a reference ONLY for 3/4 camera angle, white background and soft lighting; do not copy its colours, its carton thickness, or any of its text.

SUBJECT: One standing Wealphar Betahistin DWP carton for six blisters, medium thickness (about 100 × 55 × 30 mm, clearly slimmer than image 3), front and right side and top visible; one front-facing clear PVC aluminium blister, 2×5 smooth white round film-coated tablets at the front-left. No second blister.

ARTWORK: Image 1 is exact front artwork and Image 2 is exact right side. Preserve product geometry and label legibility exactly. Text EXACT, verbatim with Vietnamese accents; especially "Betahistin DWP", "12 mg", "Betahistin mesilat 12 mg". Do not translate or add text.

MATERIAL: Matte laminated ivory paperboard, offset printing and crisp folds; clear thermoformed PVC cavities, plain silver foil behind. Preserve navy #1B3F8B left vertical stripe and purple #6A3FA0 dosage block.

CONSTRAINTS: No logos, ℞, GMP, registration number, barcode, extra marks, text or watermark; no glossy carton. This is a visual mockup and not evidence of a real product.
```


### Carvedilol

```text
USE: Design mockup for visual review, photorealistic Vietnamese generic medicine packshot.

SCENE: Image 3 is a reference ONLY for 3/4 camera angle, white background and soft lighting; do not copy its colours, its carton thickness, or any of its text.

SUBJECT: One standing Wealphar Carvedilol DWP carton for six blisters, medium thickness (about 100 × 55 × 30 mm, clearly slimmer than image 3), front and right side and top visible; one front-facing clear PVC aluminium blister, 2×5 flat unmarked white round tablets at the front-left. No second blister.

ARTWORK: Image 1 is exact front artwork and Image 2 is exact right side. Preserve product geometry and label legibility exactly. Text EXACT, verbatim with Vietnamese accents; especially "Carvedilol DWP", "10 mg", "Carvedilol 10 mg". Do not translate or add text.

MATERIAL: Matte laminated ivory paperboard, offset printing and crisp folds; clear thermoformed PVC cavities, plain silver foil behind. Preserve navy #1B3F8B left vertical stripe and teal #0F8C8C dosage block.

CONSTRAINTS: No logos, ℞, GMP, registration number, barcode, extra marks, text or watermark; no glossy carton. This is a visual mockup and not evidence of a real product.
```

## Vòng 2 – Wealphar, 12/11/2026

**Trạng thái:** mẫu visual chờ Claude/Dũng duyệt; chưa phải bộ file in nhà máy. Nguồn vòng 2: `nhom/NHOM-1_WEALPHAR_v2_20261112.md`, A8d và các ảnh tham chiếu nội bộ Cholapan, Tadimax, Fengshi, VG5, LamsayNC đã xem tại chỗ. Không chép logo, tên NNC, hình người/cơ quan hay nội dung của ảnh tham chiếu.

### Cách làm và màu

- Betahistin: `KOM-0560_Betahistin-DWP-12mg_THU2.png`, xuất từ ảnh THU1 1536 × 1024. Carvedilol: `KOM-0210-0211_Carvedilol-DWP-10mg_THU2.png`, xuất từ THU1 1666 × 944. Artwork mặt trước 1600 × 1000 và mặt bên 1200 × 2100 lưu cạnh từng ảnh.
- Màu nhận diện: navy `#1B3F8B`, nền ngà `#FAF9F4`; màu nhấn Betahistin `#6A3FA0`, Carvedilol `#0F8C8C`. Tên navy, DWP cùng dòng màu nhấn; sóng lớn và họa tiết nút/đường trừu tượng không biểu thị cấu trúc hóa học đã xác minh.
- Dựng chữ và bố cục bằng SVG/HTML, font Arial; render Chrome headless. Hai mảng sóng không chữ được tạo bằng hai prompt riêng, sau đó đưa vào vùng sóng của SVG; mảng màu chỉ là họa tiết in mô phỏng, không xác nhận vật liệu hay hiệu ứng in thực tế. Mặt trước và mặt bên được ghép phối cảnh lên chính THU1; không chạy model để viết chữ lên bao bì.
- Công cụ tạo họa tiết: `image_gen__imagegen` tích hợp, tạo mới riêng cho từng SP, `transparent_background=false`. Model không được cung cấp; công cụ không cho chọn/kiểm `quality=high` hoặc `size`. Ảnh tham chiếu nội bộ không được gửi làm đầu vào.
- Mask ghép chỉ áp lên hai mặt hộp, loại trừ vùng vỉ; so RGB sau khi lưu: **0 pixel đổi ngoài mask ghép và 0 pixel đổi trong vùng bảo vệ vỉ** so với THU1. Kiểm này giữ nắp/nền và hình học ảnh gốc theo mask, không chứng minh kích thước hộp thật.

### Soát chữ và các điểm cần duyệt

| Dòng | Betahistin | Carvedilol |
|---|---|---|
| Tên và hàm lượng | `Betahistin DWP` · `12 mg` | `Carvedilol DWP` · `10 mg` |
| Thành phần | `Mỗi viên nén bao phim chứa: Betahistin mesilat 12 mg` | `Mỗi viên nén chứa: Carvedilol 10 mg` |
| Dạng, đường dùng | `Viên nén bao phim · Uống` | `Viên nén · Uống` |
| Anh nhỏ ở mặt trước | `Film-coated tablets · Oral use` | `Tablets · Oral use` |
| Quy cách | `Hộp 6 vỉ x 10 viên nén bao phim` | `Hộp 6 vỉ x 10 viên nén` |
| Anh ở mặt bên | `Box of 6 blisters x 10 film-coated tablets` | `Box of 6 blisters x 10 tablets` |
| Cơ sở | `Cơ sở sản xuất: Wealphar – Việt Nam` | `Cơ sở sản xuất: Wealphar – Việt Nam` |

Các mục bên, ba câu chuẩn và `Số lô SX: / NSX: / HD:` được giữ theo brief, không điền giá trị; trong artwork gốc các dòng được xuống dòng để vừa mặt. Đã xem artwork và hai ảnh thành phẩm. Mặt bên sau phối cảnh có chữ nhỏ và mép ghép mảnh; chưa khẳng định toàn bộ dấu đọc chắc chắn trên ảnh thành phẩm. Thử thu cao 90 px: có thể nhận ra tên chính khi xem gần; DWP, hàm lượng và chữ phụ nhỏ, cần Claude kiểm ở form thực tế.

Đính chính ghi chú vòng 1: chỉ đạo hiện hành trong `BRIEF-CHUAN_CODEX_v1_20261112.md` mục C ghi Dũng đã chốt giữ hàng chào Betahistin **12 mg**; dòng “cần chủ nguồn xác nhận” ở ghi chú lịch sử vòng 1 không đại diện cho quyết định hiện hành.

Dù mục đích cuối là làm việc với nhà máy, hiện chỉ có PNG artwork và ảnh phối cảnh. Chưa có bản khuôn bế, kích thước sản xuất được xác nhận, thông số màu in/bleed, bằng chứng duyệt nội dung hoặc bản in thử; vì vậy chưa xác nhận sẵn sàng đưa thẳng vào sản xuất.

### Prompt riêng đã dùng để tạo họa tiết không chữ

#### Betahistin

```text
USE: original abstract pharmaceutical packaging artwork only, no text.
COMPOSITION: a wide, seamless flowing wave field in dark navy transitioning to purple, luminous soft gradients and faint abstract molecular connections, intended for the lower 45 percent of a medicine carton, with ample dark area for small white lettering.
STYLE: professional Vietnamese commercial medicine box, high quality offset print look, clear strong contrast, matte finish, abstract graphic design.
CONSTRAINTS: no words, letters, numerals, logos, marks, badges, watermark, packaging, organs, people, bodies or symptoms.
```

#### Carvedilol

```text
USE: original abstract pharmaceutical packaging artwork only, no text.
COMPOSITION: a wide, seamless flowing wave field in dark navy transitioning to teal, luminous soft gradients and faint abstract molecular connections, intended for the lower 45 percent of a medicine carton, with ample dark area for small white lettering.
STYLE: professional Vietnamese commercial medicine box, high quality offset print look, clear strong contrast, matte finish, abstract graphic design.
CONSTRAINTS: no words, letters, numerals, logos, marks, badges, watermark, packaging, organs, people, bodies or symptoms.
```

## Vòng 3 – Wealphar, 12/11/2026

**Trạng thái:** mẫu visual AI chờ duyệt; không phải ảnh chụp hàng thật và chưa là bộ file sản xuất cho nhà máy. Người dùng yêu cầu Creative Production `produce`/ImageGen; tool bảng Creative Production trong phiên chỉ hiện qua lớp gọi gián tiếp, không có cách gọi trực tiếp như workflow skill yêu cầu, nên không có bảng Creative Production được mount. Đã dùng ImageGen tích hợp cho hai ảnh, một prompt riêng cho mỗi ảnh.

### Tham chiếu và phương pháp

- Betahistin: Image 1 `KOM-0560_Betahistin-DWP-12mg_THU3_ARTWORK-TRUOC.png`, Image 2 `KOM-0560_Betahistin-DWP-12mg_THU3_ARTWORK-BEN.png`.
- Carvedilol: Image 1 `KOM-0210-0211_Carvedilol-DWP-10mg_THU3_ARTWORK-TRUOC.png`, Image 2 `KOM-0210-0211_Carvedilol-DWP-10mg_THU3_ARTWORK-BEN.png`.
- Artwork trước tạo bằng SVG/HTML từ bảng nhóm: sửa Betahistin tách hai dòng hoạt chất, ô 12 mg ngang tên; cả hai thêm chuyển màu nhẹ/hình phân tử mờ phía trên. Artwork bên SVG của THU2 được giữ làm tham chiếu vì đã có các mục và chữ lớn hơn THU1. **Không ghép/dán artwork lên ảnh thành phẩm**; hai ảnh sản phẩm là đầu ra ImageGen nguyên bản, chỉ sao chép file.
- Phong cách tham khảo NNC đã quan sát tại chỗ trong lượt trước; không dùng ảnh nội bộ làm đầu vào model. Công cụ `image_gen__imagegen`, `transparent_background=false`, hai ảnh tham chiếu mỗi sản phẩm. Công cụ không cho chọn hoặc kiểm model/quality; không khẳng định `quality=high`. Cả hai file kết quả 1536 × 1024 px.

### Soát chữ trên ảnh thành phẩm

Đã xem toàn ảnh và phóng to từng mặt bên so với bảng chữ trong `NHOM-1_WEALPHAR_20261112.md` và dòng tiếng Anh mặt trước trong v2. Các dòng dưới được ngắt trên ảnh theo bố cục, dấu cuối câu và dấu tiếng Việt được xem trực tiếp; đây là soát bằng mắt, chưa thay thế kiểm duyệt file in độc lập.

| Nội dung | Betahistin | Carvedilol |
|---|---|---|
| Tên + hàm lượng | Đạt: `Betahistin DWP 12 mg` | Đạt: `Carvedilol DWP 10 mg` |
| Thành phần | Đạt: `Mỗi viên nén bao phim chứa: Betahistin mesilat 12 mg` | Đạt: `Mỗi viên nén chứa: Carvedilol 10 mg` |
| Dạng/đường dùng | Đạt: `Viên nén bao phim · Uống` | Đạt: `Viên nén · Uống` |
| Dòng Anh mặt trước | Đạt: `Film-coated tablets · Oral use` | Đạt: `Tablets · Oral use` |
| Quy cách | Đạt: `Hộp 6 vỉ x 10 viên nén bao phim` | Đạt: `Hộp 6 vỉ x 10 viên nén` |
| Tiếng Anh mặt bên | Đạt: `Box of 6 blisters x 10 film-coated tablets` | Đạt: `Box of 6 blisters x 10 tablets` |
| Nhà sản xuất mặt trước | Đạt: `Cơ sở sản xuất: Wealphar – Việt Nam` | Đạt: `Cơ sở sản xuất: Wealphar – Việt Nam` |
| Ba mục mặt bên | Thấy `Thành phần:`, `Dạng bào chế:`, `Quy cách:` | Thấy đủ ba mục |
| Câu chỉ dẫn mặt bên | Đạt khi phóng to: `Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng.` | Đạt khi phóng to cùng câu |
| Câu đọc hướng dẫn | Đạt khi phóng to: `Đọc kỹ hướng dẫn sử dụng trước khi dùng.` | Đạt khi phóng to cùng câu |
| Câu trẻ em | Đạt khi phóng to: `Để xa tầm tay trẻ em.` | Đạt khi phóng to cùng câu |
| Hàng đáy mặt bên | `Số lô SX:`, `NSX:`, `HD:` trống | Như Betahistin |

Quan sát: mỗi hình một vỉ mặt trước, 10 viên 2×5; không thấy logo, NNC, Rx, GMP, SĐK hay mã vạch. DWP cạnh tên; Betahistin tách dòng hoạt chất và khối 12 mg ngang hàng tên; không thấy mảng trắng hở hoặc đường chấm gạch mép hộp như THU2. Không thể xác thực tỉ lệ vật lý hay vật liệu in từ ảnh AI. Chữ nhỏ chưa được kiểm khả năng đọc trong ô form 90 px. Chưa có khuôn bế, thông số màu/bleed, bản in thử hoặc phê duyệt sản xuất.

### Prompt thực tế – Betahistin

```text
USE: Photorealistic conceptual pharmaceutical product packshot for visual review. Image 1 is the authoritative exact front artwork. Image 2 is the authoritative exact side artwork.

SCENE: Pure white seamless background, soft diffuse studio light and a gentle contact shadow. Upright carton standing in three-quarter view; front, right side, and top visible, with no dotted or dashed lines along the carton edges.

SUBJECT: One medium-thickness ivory carton for 6 blisters (approximately 100 × 55 × 30 mm proportion), plus exactly one front-facing aluminium–PVC blister of 10 plain round white film-coated tablets in 2 rows of 5. No second blister and no other objects. Carton and all printed text share exactly the same perspective, without skewed, detached, bent or warped panel surfaces; no white gaps at the bottom edge.

FRONT: Reproduce Image 1 faithfully, including its ivory subtle upper gradient and faint abstract molecular pattern, lower navy-to-purple flowing waves, typography and hierarchy. Keep "Betahistin DWP" in navy/purple, DWP immediately beside the name; keep "12 mg" in a purple rounded block to the right at the same vertical level as the name without touching other text. Keep the ingredient in two separate lines exactly:
"Mỗi viên nén bao phim chứa:"
"Betahistin mesilat 12 mg"
Keep the remaining exact front text exactly as Image 1, including "Viên nén bao phim · Uống", "Film-coated tablets · Oral use", "Hộp 6 vỉ x 10 viên nén bao phim", and "Cơ sở sản xuất: Wealphar – Việt Nam".

SIDE: Reproduce all text from Image 2 EXACT, verbatim, with correct Vietnamese accents and spacing, arranged in the same clear sections with legible type filling about 75% of the side height. Keep all blank batch/date fields blank. Preserve product geometry and label legibility exactly.

MATERIAL: Matte-laminated white ivory paperboard carton, offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights. One aluminium–PVC blister shown FRONT SIDE ONLY with clear thermoformed PVC cavities and plain silver base.

CONSTRAINTS: All text EXACT, verbatim, no extra characters; no logos, no ℞, no NNC, no Lao text, no GMP, no registration numbers, no barcode, no people, organs or symptoms. Only abstract pattern. Target 1536 × 1024.
```

### Prompt thực tế – Carvedilol

```text
USE: Produce one photorealistic Vietnamese pharmaceutical packaging design mockup for human review. Do not depict an actual verified product.

INPUTS: Image 1 is the front artwork. Image 2 is the right side artwork. Use each image as the EXACT, verbatim typographic and graphic reference for its corresponding carton face. Keep the two faces and all their text, labels and proportions correct.

SCENE: Seamless pure white background, soft studio lighting, realistic subtle shadow. A single upright medium-thickness matte ivory paperboard carton, six blisters inside, 3/4 view showing the front, right side, and top with coherent planar perspective and straight edges. One unlettered aluminium–PVC blister lying in front-left, containing exactly 10 flat round white tablets in two rows of five. No extra items or second blister. Frame 1536 × 1024 pixels.

STYLE: The front retains the exact supplied navy-to-teal abstract waves and faint molecular motifs, softly tinted ivory upper region, “Carvedilol DWP” with DWP next to the name and teal “10 mg” block. This is a commercial pharmaceutical packaging design. Preserve product geometry and label legibility exactly. No bending, dotted seams, warped surface, or white gaps at box edges. The side text uses the supplied artwork, large, clearly spaced, using approximately 75 percent of the side panel height.

EXACT FRONT TEXT: “Carvedilol DWP”; “10 mg”; “Mỗi viên nén chứa: Carvedilol 10 mg”; “Viên nén · Uống”; “Tablets · Oral use”; “Hộp 6 vỉ x 10 viên nén”; “Cơ sở sản xuất: Wealphar – Việt Nam”.

EXACT SIDE TEXT: “Carvedilol DWP 10 mg”; “Thành phần:”; “Mỗi viên nén chứa: Carvedilol 10 mg”; “Dạng bào chế:”; “Viên nén · Uống”; “Quy cách:”; “Hộp 6 vỉ x 10 viên nén”; “Box of 6 blisters x 10 tablets”; “Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng.”; “Đọc kỹ hướng dẫn sử dụng trước khi dùng.”; “Để xa tầm tay trẻ em.”; “Số lô SX:”; “NSX:”; “HD:”. Leave all fields after colons empty. No other text.

MATERIAL: matte-laminated white ivory paperboard carton (~300 gsm), offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights. aluminium–PVC blister shown FRONT SIDE ONLY (clear thermoformed PVC cavities with the tablets/capsules visible, plain silver aluminium base around them); perforation lines between cells.

CONSTRAINTS: ImageGen must render everything as a coherent photographic object without pasted or overlaid panels. EXACT, verbatim text, every accent, no extra characters, no Rx, logos, NNC, GMP, registration, barcode, expiry or manufactured lot numbers. Abstract wave and molecular art only: no human, organs, symptoms, people.
```

