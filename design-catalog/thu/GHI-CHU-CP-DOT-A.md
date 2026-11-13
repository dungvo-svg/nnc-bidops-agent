# Creative Production – Đợt A, 12/11/2026

**Đã hoàn tất 6 phương án ảnh mẫu, chờ Claude/Dũng chọn.** Chỉ thực hiện Đợt A. Đây là ảnh bao bì được thiết kế theo brief; không phải ảnh chụp một sản phẩm hiện có. Theo chỉ đạo hiện hành, đầu ra chỉ là ảnh mẫu để duyệt, không triển khai file in/khuôn bế trong lượt này.

## Bảng và file cuối

Bảng Creative Production: **NNC BidOps · Đợt A · 3 sản phẩm × 2 phương án**. Board ID `9f86a221-add8-4f2d-812a-1eb3a149a1eb`; đã mở đúng một bảng và giữ cùng boardId. Kiểm UI thấy đủ 6 ô ảnh; receipt cuối cả 6 trạng thái `ready`, ảnh gốc trong board có SHA-256 trùng file xuất. Bảng đang dùng các bản cuối sau sửa cỡ tên hai chai.

| Sản phẩm | A1 | A2 | Kích thước mỗi ảnh |
|---|---|---|---|
| Amitriptylin 25 mg | [Nền ngà, sóng đỏ](KOM-1017_Amitriptylin-25mg_CP-A1.png) | [Đỏ đậm, vòng cung kem](KOM-1017_Amitriptylin-25mg_CP-A2.png) | 1536 × 1024 |
| Esomex 20 | [Dải emerald bên phải](KOM-0356-0359-0363-0373-0626_Esomex-20_CP-A1.png) | [Vòng cung emerald, tên xếp tầng](KOM-0356-0359-0363-0373-0626_Esomex-20_CP-A2.png) | 1536 × 1024 |
| Lactate Ringer & Dextrose 5% | [Dải tên ngang](KOM-0029_Lactate-Ringer-Dextrose-5pct_CP-A1.png) | [Trục dọc, khối 500 ml tròn](KOM-0029_Lactate-Ringer-Dextrose-5pct_CP-A2.png) | 1024 × 1024 |

## Nguồn, phương pháp và thông số thực tế

Đã đọc theo thứ tự: `TONG-HOP-THIET-KE-BAO-BI_20261112.md` → `BRIEF-CHUAN_CODEX_v1_20261112.md` → `KE-HOACH-PHAN-CON-LAI_20261112.md`, trong `outputs/thuoc-kom-tinh-kiem-gia-20261111/v1/thiet-ke-mau/`. Chữ theo mục C/A4; tỉ lệ theo C2; chất liệu theo B. Khuôn Wealphar THU3 và ảnh đã xem từ thư mục nnclaos dùng để hiểu mức hoàn thiện, không sao màu/chữ/logo sang các hãng này.

- Dựng SVG và render PNG làm brief ảnh cho từng phương án. ImageGen vẽ lại **toàn bộ** sản phẩm, chữ và phối cảnh từ ảnh tham chiếu. Không dán SVG, không ghép chữ, không vá pixel lên ảnh sản phẩm.
- Các hộp chỉ có một vỉ mặt trước 2×5. Amitriptylin: hộp dày theo tỉ lệ quy ước 100 × 55 × 48; viên tròn trắng phẳng. Esomex: hộp mỏng theo tỉ lệ 110 × 58 × 15; nang trắng ngà. Kích thước mm là quy ước hình dáng, không phải phép đo hàng thật.
- Lactate chỉ có một chai PP bán trong, dung dịch không màu, nút/nắp trắng và khoen đáy, nhãn mô phỏng in xanh trực tiếp. Cột tiếng Anh của Lactate trống, nên không tự bổ sung bản dịch Anh; hai hộp có dòng Anh đúng mục C.
- Công cụ tạo ảnh: `image_gen__imagegen` tích hợp; `transparent_background=false`. Tên model cụ thể và giá trị quality không được công cụ cung cấp; không có tham số để đặt/kiểm `quality=high`, `size` hoặc `input_fidelity`, nên không khẳng định đã đặt chúng. Kích thước được yêu cầu trong prompt và kiểm trên file thực tế.
- Bốn ảnh hộp xuất native đúng 1536 × 1024, mỗi phương án 1 lượt. Hai chai có 1 lượt tạo + 1 targeted edit chỉ tăng khối tên thành 3 dòng lớn để cải thiện khả năng nhận diện khi thu nhỏ. Native của chai là 1254 × 1254; xuất toàn ảnh bằng Lanczos xuống 1024 × 1024 để đúng kích thước user yêu cầu. Đây chỉ là đổi kích thước toàn ảnh, không ghép hay sửa chữ.
- Board được gọi qua kênh công cụ có sẵn trong phiên; đã xác nhận app Creative Production thực sự hiển thị trong side panel, khác với tình trạng không có bảng ở những lượt trước. `BOARD-RECEIPT.json` giữ boardId/itemId/trạng thái, `EXPORT-MANIFEST.json` giữ SHA-256 và kích thước file cuối.

## Soát chữ độc lập trên ảnh cuối

Đã xem toàn ảnh và các crop phóng 3–4 lần. Trạng thái ĐẠT dưới đây nghĩa là đối chiếu trực tiếp với brief, chưa phát hiện sai ký tự/dấu/thiếu dòng; chưa thay thế quyết định duyệt visual của Claude/Dũng.

### Amitriptylin

| Dòng yêu cầu | A1 | A2 |
|---|---|---|
| Amitriptylin 25 mg | ĐẠT | ĐẠT |
| Mỗi viên nén chứa: Amitriptylin 25 mg | ĐẠT | ĐẠT |
| Viên nén · Uống | ĐẠT | ĐẠT |
| Hộp 10 vỉ x 10 viên nén | ĐẠT | ĐẠT |
| Box of 10 blisters x 10 tablets | ĐẠT | ĐẠT |
| Cơ sở sản xuất: Công ty CP Dược phẩm Khánh Hòa (Khapharco) – Việt Nam | ĐẠT | ĐẠT |
| Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng | ĐẠT | ĐẠT |
| Đọc kỹ hướng dẫn sử dụng trước khi dùng | ĐẠT | ĐẠT |
| Để xa tầm tay trẻ em | ĐẠT | ĐẠT |
| Số lô SX: / NSX: / HD: – để trống giá trị | ĐẠT | ĐẠT |

Mặt bên có tiêu đề Thành phần, Dạng bào chế, Quy cách; kiểm A1 và A2 đều đọc được khi phóng. Một vỉ mặt trước 10 viên, không khắc; không thêm vỉ mặt sau.

### Esomex 20

| Dòng yêu cầu | A1 | A2 |
|---|---|---|
| ESOMEX 20 | ĐẠT | ĐẠT |
| Mỗi viên nang cứng chứa: Esomeprazol 20 mg | ĐẠT | ĐẠT |
| Viên nang cứng · Uống | ĐẠT | ĐẠT |
| Hộp 2 vỉ x 10 viên nang cứng | ĐẠT | ĐẠT |
| Box of 2 blisters x 10 hard capsules | ĐẠT | ĐẠT |
| Cơ sở sản xuất: USA NIC – Việt Nam | ĐẠT | ĐẠT |
| Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng | ĐẠT | ĐẠT |
| Đọc kỹ hướng dẫn sử dụng trước khi dùng | ĐẠT | ĐẠT |
| Để xa tầm tay trẻ em | ĐẠT | ĐẠT |
| Số lô SX: / NSX: / HD: – để trống giá trị | ĐẠT | ĐẠT |
| Cạnh mỏng: ESOMEX 20 / Esomeprazol 20 mg | ĐẠT | ĐẠT |

Hai ảnh có một vỉ 2×5 nang trắng ngà; mặt bên giữ hẹp, câu chuẩn nằm trên mặt trước để không nhồi chữ ở cạnh.

### Lactate Ringer & Dextrose 5%

| Dòng yêu cầu | A1 cuối | A2 cuối |
|---|---|---|
| LACTATE RINGER & DEXTROSE 5% (xuống 3 dòng) | ĐẠT | ĐẠT |
| Chai nhựa 500 ml | ĐẠT | ĐẠT |
| Ringer lactat + Glucose 5% | ĐẠT | ĐẠT |
| Dung dịch tiêm truyền · Truyền tĩnh mạch | ĐẠT | ĐẠT |
| Cơ sở sản xuất: Công ty CP Hóa – Dược phẩm Mekophar – Việt Nam | ĐẠT | ĐẠT |
| Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng | ĐẠT | ĐẠT |
| Đọc kỹ hướng dẫn sử dụng trước khi dùng | ĐẠT | ĐẠT |
| Để xa tầm tay trẻ em | ĐẠT | ĐẠT |
| Số lô SX: / NSX: / HD: – để trống giá trị | ĐẠT | ĐẠT |

A1/A2 đều không thấy logo, NNC, ℞/GMP/SĐK/mã vạch, địa chỉ, giá hoặc hình cơ thể/triệu chứng. Các họa tiết là trừu tượng. Test thu nhỏ cao 90 px được dùng để phát hiện và sửa khối tên chai; chữ phụ không có mục tiêu đọc ở kích thước đó. Chỉ trạng thái duyệt trên ảnh gốc/phóng to được chốt ở bảng soát trên; Claude/Dũng vẫn cần xem thử trong ô form nếu cần chốt khả năng đọc thực tế.

## Nhật ký prompt và ảnh tham chiếu

Các prompt dưới là nội dung thực tế. Nhãn SOURCE/refs có đường dẫn đến bộ SVG/PNG brief trong `cp-dot-a-refs/`; ảnh source model gốc và receipts còn được giữ trong từng thư mục. Không sửa hoặc đăng tải workbook hay hồ sơ thầu nguồn.

### Amitriptylin · CP-A1 — tạo ảnh ban đầu

- Image 1: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\amitriptylin\CP-A1_front.png`
- Image 2: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\amitriptylin\CP-A1_side.png`

```text
USE: product packshot design concept for visual evaluation, 1536 × 1024 pixels.
SCENE: seamless white background, softly diffused studio light, subtle shadow, one product only with one blister.
SUBJECT: one thick 10-blister carton, approximately 100 × 55 × 48 proportions, upright three-quarter view showing front, right side, and top; one front-facing 2×5 aluminium–PVC blister of plain round flat white unmarked tablets. No rear-foil blister.
LABEL: Image 1 is the exact front artwork and Image 2 is the exact side artwork. Reproduce the full visual system and all Vietnamese diacritics EXACT, verbatim; keep side headings and blank batch/date fields. Preserve product geometry and label legibility exactly. Do not add, translate, invent, omit or duplicate text.
STYLE: Keep the warm ivory upper face, large crimson title and restrained crimson dose block; use the broad crimson abstract flowing ribbons on the lower face. Match Image 1 without copying other brands.
MATERIAL: matte-laminated white ivory paperboard carton (~300 gsm), offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights. aluminium–PVC blister shown FRONT SIDE ONLY (clear thermoformed PVC cavities with the tablets/capsules visible, plain silver aluminium base around them); perforation lines between cells. Do NOT show or create the back (foil) side; no second blister; no text on the blister.
CONSTRAINTS: no logos, ℞, GMP, registration numbers, barcodes, NNC, invented facts, Lao text, people, organs, symptoms, extra props or watermark. This is a generated mockup, not a photograph of real merchandise.
```

### Amitriptylin · CP-A2 — tạo ảnh ban đầu

- Image 1: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\amitriptylin\CP-A2_front.png`
- Image 2: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\amitriptylin\CP-A2_side.png`

```text
USE: product packshot design concept for visual evaluation, 1536 × 1024 pixels.
SCENE: seamless white background, softly diffused studio light, subtle shadow, one product only with one blister.
SUBJECT: one thick 10-blister carton, approximately 100 × 55 × 48 proportions, upright three-quarter view showing front, right side, and top; one front-facing 2×5 aluminium–PVC blister of plain round flat white unmarked tablets. No rear-foil blister.
LABEL: Image 1 is the exact front artwork and Image 2 is the exact side artwork. Reproduce the full visual system and all Vietnamese diacritics EXACT, verbatim; keep side headings and blank batch/date fields. Preserve product geometry and label legibility exactly. Do not add, translate, invent, omit or duplicate text.
STYLE: Keep a saturated deep-red face with bold cream typography and large sweeping cream arcs, visually distinct from ivory-first layouts. Match Image 1 without copying other brands.
MATERIAL: matte-laminated white ivory paperboard carton (~300 gsm), offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights. aluminium–PVC blister shown FRONT SIDE ONLY (clear thermoformed PVC cavities with the tablets/capsules visible, plain silver aluminium base around them); perforation lines between cells. Do NOT show or create the back (foil) side; no second blister; no text on the blister.
CONSTRAINTS: no logos, ℞, GMP, registration numbers, barcodes, NNC, invented facts, Lao text, people, organs, symptoms, extra props or watermark. This is a generated mockup, not a photograph of real merchandise.
```

### Esomex · A1 — tạo ảnh ban đầu

- Image 1: `A1_FRONT.png`
- Image 2: `A1_SIDE.png`

```text
USE: distinct Esomex concept A1.
DESIGN: airy ivory front, title large on the left, 20 emphasis to the right, bold emerald gradient diagonal flowing ribbon occupies the right and lower portion; distinct slim side in deep green. Follow Image 1 identity without copying any brand logo.
SCENE: white seamless background, soft diffused light, gentle contact shadow, no props. One single medium-view 3/4 medical carton with front, thin right side and top visible; exactly one front-facing plain aluminium-PVC blister with 2 rows of 5 unmarked ivory hard capsules. No other objects. Aspect ratio 1536x1024.
PRODUCT GEOMETRY: two-blister carton, slim flat approximately 110 x 58 x 15 mm: noticeably thin side; do not add thickness. Product is an illustrative concept, not a verified photo.
INPUTS: Image 1 is the specified front SVG-render reference; Image 2 is the narrow side reference. Create the entire realistic packshot afresh; no pasted SVG or digitally composited facades. Preserve geometry and legibility exactly. Exact text in quotes, verbatim, correct accents. Side only the vertical name and active; standard sentences and English line may be on top or front, never squeezed onto the narrow side.
FRONT/ELIGIBLE TOP TEXT EXACT: "ESOMEX 20"; "Mỗi viên nang cứng chứa: Esomeprazol 20 mg"; "Viên nang cứng · Uống"; "Hộp 2 vỉ x 10 viên nang cứng"; "Box of 2 blisters x 10 hard capsules"; "Cơ sở sản xuất: USA NIC – Việt Nam"; "Đọc kỹ hướng dẫn sử dụng trước khi dùng"; "Để xa tầm tay trẻ em"; "Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng"; "Số lô SX:"; "NSX:"; "HD:". Leave the fields blank. SIDE TEXT ONLY: "ESOMEX 20"; "Esomeprazol 20 mg".
MATERIAL: matte-laminated white ivory paperboard carton (~300 gsm), offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights. aluminium–PVC blister shown FRONT SIDE ONLY (clear thermoformed PVC cavities with the tablets/capsules visible, plain silver aluminium base around them); perforation lines between cells.
CONSTRAINTS: No Rx, logo, NNC, GMP, registration number, barcode, address, filled date/lot, extra text, no person, organ, body, symptom, or marketing claim. Typography is Vietnamese primary with subordinate English. White/ivory capsule colour is a design convention, not verified product detail.
```

### Esomex · A2 — tạo ảnh ban đầu

- Image 1: `A2_FRONT.png`
- Image 2: `A2_SIDE.png`

```text
USE: distinct Esomex concept A2.
DESIGN: a different deep-green emerald orbit/sweep and curving abstract ring on the right, stacked ESOMEX and 20 on the left, ivory text field and deep green lower strip. Follow Image 1 identity without copying any brand logo.
SCENE: white seamless background, soft diffused light, gentle contact shadow, no props. One single medium-view 3/4 medical carton with front, thin right side and top visible; exactly one front-facing plain aluminium-PVC blister with 2 rows of 5 unmarked ivory hard capsules. No other objects. Aspect ratio 1536x1024.
PRODUCT GEOMETRY: two-blister carton, slim flat approximately 110 x 58 x 15 mm: noticeably thin side; do not add thickness. Product is an illustrative concept, not a verified photo.
INPUTS: Image 1 is the specified front SVG-render reference; Image 2 is the narrow side reference. Create the entire realistic packshot afresh; no pasted SVG or digitally composited facades. Preserve geometry and legibility exactly. Exact text in quotes, verbatim, correct accents. Side only the vertical name and active; standard sentences and English line may be on top or front, never squeezed onto the narrow side.
FRONT/ELIGIBLE TOP TEXT EXACT: "ESOMEX 20"; "Mỗi viên nang cứng chứa: Esomeprazol 20 mg"; "Viên nang cứng · Uống"; "Hộp 2 vỉ x 10 viên nang cứng"; "Box of 2 blisters x 10 hard capsules"; "Cơ sở sản xuất: USA NIC – Việt Nam"; "Đọc kỹ hướng dẫn sử dụng trước khi dùng"; "Để xa tầm tay trẻ em"; "Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng"; "Số lô SX:"; "NSX:"; "HD:". Leave the fields blank. SIDE TEXT ONLY: "ESOMEX 20"; "Esomeprazol 20 mg".
MATERIAL: matte-laminated white ivory paperboard carton (~300 gsm), offset printed, crisp folded edges, no foil, no gloss UV, no specular highlights. aluminium–PVC blister shown FRONT SIDE ONLY (clear thermoformed PVC cavities with the tablets/capsules visible, plain silver aluminium base around them); perforation lines between cells.
CONSTRAINTS: No Rx, logo, NNC, GMP, registration number, barcode, address, filled date/lot, extra text, no person, organ, body, symptom, or marketing claim. Typography is Vietnamese primary with subordinate English. White/ivory capsule colour is a design convention, not verified product detail.
```

### Lactate · CP-A1 — tạo ảnh ban đầu

- Image 1: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\lactate\Lactate_CP-A1_FRONT.png`
- Image 2: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\lactate\Lactate_CP-A1_DETAIL.png`
- Image 3: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\KOM-0029_Lactate-Ringer-Dextrose-5pct_THU8.png`

```text
USE: A commercial pharmaceutical packaging design mockup for human review; create a photorealistic full product image, not a verified existing product photograph.

INPUTS: Image 1 is the complete wrap-label artwork for Lactate option A1. Image 2 is a larger typographic detail of the SAME small-print fields, not a second label: print those fields once only. Image 3 is the approved bottle shape and material reference. Use Image 3 for the container only; replace its old printed layout with Image 1. Do not copy old printing or add other words.

SCENE: One upright bottle, exactly front-facing, pure white seamless background, soft diffuse studio illumination, close gentle contact shadow. No box, blister, tray, props or extra objects. Bottle fills about 85% of image height. Target 1024 × 1024 pixels, square.

SUBJECT: One 500 ml polypropylene medical IV infusion bottle with clear colourless liquid near its sloped shoulder; rounded body, integral hanging ring below the base, rubber stopper and white plastic tear-off cap. Preserve the recognizable bottle geometry of Image 3.

DESIGN: Use a broad horizontal blue name ribbon, then a large centred volume block, ingredient and route, then two balanced smaller information columns, and a single horizontal row of empty lot/date fields. Rich but restrained abstract wave/line graphics only. One blue ink colour (#14558B and tint coverage of the same ink), no different-colour inks. The print follows the cylindrical body naturally and is printed directly on the plastic; no paper label edges, pasted flat panels or white patches.

TEXT: All wording EXACT, verbatim, Vietnamese accents and case as in Images 1 and 2. Large product name "LACTATE RINGER & DEXTROSE 5%"; emphasize "500 ml" within the field "Chai nhựa 500 ml". Other exact text: "Ringer lactat + Glucose 5%"; "Dung dịch tiêm truyền · Truyền tĩnh mạch"; "Cơ sở sản xuất: Công ty CP Hóa – Dược phẩm Mekophar – Việt Nam"; "Đọc kỹ hướng dẫn sử dụng trước khi dùng"; "Để xa tầm tay trẻ em"; "Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng"; "Số lô SX:"; "NSX:"; "HD:". Keep values after the three lot/date labels blank. Preserve product geometry and label legibility exactly. Do not translate, paraphrase, invent punctuation, add English or omit words.

MATERIAL: semi-transparent matte polypropylene IV bottle, rounded body, hanging ring at the base, rubber stopper with white plastic tear-off cap; label printed directly on the plastic in one ink colour, not a paper sticker; clear colourless solution.

CONSTRAINTS: No logos, NNC, ℞/Rx, GMP, registration number, barcode, addresses, clinical claims, extra figures, watermark, humans, organs or symptom illustrations. Matte natural plastic, no harsh shiny highlights. All text and the bottle must share coherent perspective; the model must redraw the complete packshot. No pasted SVG or composited text panels.
```

### Lactate · CP-A2 — tạo ảnh ban đầu

- Image 1: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\lactate\Lactate_CP-A2_FRONT.png`
- Image 2: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\cp-dot-a-refs\lactate\Lactate_CP-A2_DETAIL.png`
- Image 3: `D:\WORK\Agent\Agent-first\NNC BidOps Agent\design-catalog\thu\KOM-0029_Lactate-Ringer-Dextrose-5pct_THU8.png`

```text
USE: A commercial pharmaceutical packaging design mockup for human review; create a photorealistic full product image, not a verified existing product photograph.

INPUTS: Image 1 is the complete wrap-label artwork for Lactate option A2. Image 2 is a larger typographic detail of the SAME small-print fields, not a second label: print those fields once only. Image 3 is the approved bottle shape and material reference. Use Image 3 for the container only; replace its old printed layout with Image 1. Do not copy old printing or add other words.

SCENE: One upright bottle, exactly front-facing, pure white seamless background, soft diffuse studio illumination, close gentle contact shadow. No box, blister, tray, props or extra objects. Bottle fills about 85% of image height. Target 1024 × 1024 pixels, square.

SUBJECT: One 500 ml polypropylene medical IV infusion bottle with clear colourless liquid near its sloped shoulder; rounded body, integral hanging ring below the base, rubber stopper and white plastic tear-off cap. Preserve the recognizable bottle geometry of Image 3.

DESIGN: Use an asymmetric vertical blue spine, a large central product name, a circular blue volume medallion to the right, then clear information groups and two balanced smaller columns, with a single bottom row of empty lot/date fields. Rich but restrained abstract wave/line graphics only. One blue ink colour (#14558B and tint coverage of the same ink), no different-colour inks. The print follows the cylindrical body naturally and is printed directly on the plastic; no paper label edges, pasted flat panels or white patches.

TEXT: All wording EXACT, verbatim, Vietnamese accents and case as in Images 1 and 2. Large product name "LACTATE RINGER & DEXTROSE 5%"; emphasize "500 ml" within the field "Chai nhựa 500 ml". Other exact text: "Ringer lactat + Glucose 5%"; "Dung dịch tiêm truyền · Truyền tĩnh mạch"; "Cơ sở sản xuất: Công ty CP Hóa – Dược phẩm Mekophar – Việt Nam"; "Đọc kỹ hướng dẫn sử dụng trước khi dùng"; "Để xa tầm tay trẻ em"; "Chỉ định, chống chỉ định, cách dùng và các thông tin khác: xem tờ hướng dẫn sử dụng"; "Số lô SX:"; "NSX:"; "HD:". Keep values after the three lot/date labels blank. Preserve product geometry and label legibility exactly. Do not translate, paraphrase, invent punctuation, add English or omit words.

MATERIAL: semi-transparent matte polypropylene IV bottle, rounded body, hanging ring at the base, rubber stopper with white plastic tear-off cap; label printed directly on the plastic in one ink colour, not a paper sticker; clear colourless solution.

CONSTRAINTS: No logos, NNC, ℞/Rx, GMP, registration number, barcode, addresses, clinical claims, extra figures, watermark, humans, organs or symptom illustrations. Matte natural plastic, no harsh shiny highlights. All text and the bottle must share coherent perspective; the model must redraw the complete packshot. No pasted SVG or composited text panels.
```

### lactate-a1 — lượt edit khối tên

```text
USE: One narrowly targeted text-layout edit to Lactate option A1.

CHANGE ONLY THE PRODUCT-NAME BLOCK: Replace the existing two-line product name by the SAME exact wording in three larger lines:
"LACTATE"
"RINGER &"
"DEXTROSE 5%"
Use a bold, easy-to-read font at least 1.6 times the current name lettering. The three lines must be the dominant upper-label feature and remain easy to read when the image is reduced. Expand the existing horizontal blue title ribbon upward into the unused area of the bottle shoulder if space is needed; do not shrink any words or abbreviate the name.

PRESERVE EXACTLY: Keep the same bottle geometry, transparent matte PP, liquid, rubber stopper, white tear-off cap, hanging ring, light, white background, blue ink and A1 horizontal-ribbon design. Keep "Chai nhựa", "500 ml", ingredient, administration route, manufacturer, the two small-print columns and all their words, empty lot/date fields and every other line identical. Keep other elements in their current positions as far as possible.

TEXT: All text EXACT, verbatim. The full product-name order is "LACTATE RINGER & DEXTROSE 5%"; only line breaks and font size change. No other editing, new text, overlays, logos, Rx, GMP, registration, barcode or symbols. Target 1024 × 1024 pixels.
```

### lactate-a2 — lượt edit khối tên

```text
USE: One narrowly targeted text-layout edit to Lactate option A2.

CHANGE ONLY THE PRODUCT-NAME BLOCK: Replace the existing two-line product name by the SAME exact wording in three larger lines:
"LACTATE"
"RINGER &"
"DEXTROSE 5%"
Use bold blue typography at least 1.6 times the current name lettering. Make the name block dominant and legible after reduction. It may expand upward into the unused shoulder/body area above the present name, but do not move or shrink the other content. Preserve the existing A2 vertical blue spine and right-hand circular volume medallion.

PRESERVE EXACTLY: Keep the same bottle geometry, matte semi-transparent PP, liquid, white tear-off cap, rubber stopper, bottom hanging ring, soft light and pure white background. Keep "Chai nhựa", "500 ml", ingredient, administration route, manufacturer, the two small-print groups, every other word, and the empty lot/date row identical to the reference. Keep positions of all those other elements.

TEXT: All wording EXACT, verbatim. Product name remains "LACTATE RINGER & DEXTROSE 5%" in this exact order; only line breaks and type size change. No added text, logos, Rx, GMP, registration, barcode, symbols, stickers or pasted SVG panels. Preserve product geometry and label legibility exactly. Target 1024 × 1024 pixels.
```
