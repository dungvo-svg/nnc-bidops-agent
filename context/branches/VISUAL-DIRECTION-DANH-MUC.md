# Hướng thị giác — Danh mục đọc được (Opus cha quyết, 02/11/2026)

Theo phân vai của Dũng: Opus cha quyết hướng thị giác; Sonnet (nhánh DATA) làm trên **cùng** workbook `outputs/data-branch/v4.1/DANH-MUC-DOC-v1.1.xlsx` → bản mới `DANH-MUC-DOC-v1.2.xlsx`. **Đóng băng dữ liệu:** không đổi giá trị, số đếm, ID, raw, thứ tự bản ghi; chỉ đổi trình bày. Finding của visual reviewer phía root đến sau sẽ vào v1.3.

**Người dùng và việc:** Cung ứng/CEO mở bằng Excel desktop, lọc theo BV/nhóm/ưu tiên, đọc nhanh một dòng hàng để biết: hàng gì → BV nào cần bao nhiêu → đã có giá gì → vướng gì → làm gì tiếp.

## Quyết định

1. **Thứ tự cột** (sheet "Danh mục đọc"): A Tên hàng/quy cách (48) · B Ưu tiên (16) · C Nhóm (13) · D Số BV (7) · E BV cần (38) · F Giá (56) · G Vướng (40) · H Bước tiếp (36) · I Người giữ nguồn (24). Tên hàng luôn đầu tiên. **Freeze tại C5** để tên + ưu tiên luôn thấy khi cuộn.
2. **Đầu trang:** dòng 1 tiêu đề (bold 14); dòng 2 một câu ngắn: ngày dữ liệu · "Nội bộ — có giá vốn/NCC" · "Bản dẫn xuất chỉ để đọc, sửa ở đây không về nguồn"; dòng 3 tóm tắt đếm theo ưu tiên và theo BV (chữ, từ chính dữ liệu). Hash/nguồn dời sang Chú giải.
3. **Header dòng 4:** nền xanh đậm `1F3A5F`, chữ trắng bold, wrap, cao 32, căn giữa dọc; autofilter A4:I…
4. **Font:** `Leelawadee UI` 10 cho toàn workbook (hiển thị chữ Lào trên Windows); không trộn font.
5. **Ô dữ liệu:** wrap + căn trên. **Ghi chiều cao từng dòng tường minh** (`row_dimensions[r].height`), vì Excel desktop không tự giãn dòng khi mở file do openpyxl tạo. Cách tính: với mỗi ô trong dòng, số dòng hiển thị = tổng của ⌈độ dài từng đoạn xuống dòng ÷ (độ rộng cột × 1,1)⌉; lấy ô lớn nhất × 13,5pt + 4. Tối thiểu 18pt, tối đa 409pt (trần của Excel). **Không cắt chữ, không thu font** để vừa dòng.
6. **Ưu tiên (cột B):** chữ là chính, màu chỉ hỗ trợ: Bậc 1 "1 · Báo giá đã có" nền xanh lá nhạt `E2F0D9`; Bậc 2 vàng nhạt `FFF2CC`; Bậc 3 cam nhạt `FCE4D6`; Làm rõ hàng xám tím nhạt `E4DFEC`.
7. **Nhóm (cột C):** chữ đầy đủ; nền rất nhạt theo nhóm (Thuốc `DDEBF7`, Hóa chất `FFF2CC`, Vật tư `E2EFDA`). Nhãn Kom chờ giữ nguyên chữ "— đề xuất Thuốc (chưa duyệt)".
8. **Giá (cột F):** mỗi dòng giá bắt đầu bằng nhãn chữ IN HOA; thứ tự trong ô: BÁO GIÁ NCC → THAM CHIẾU → CŨ. Dùng rich text: nhãn bold, phần còn lại thường. Không dùng màu thay nhãn.
9. **BV cần (cột E):** mỗi BV một dòng; tên BV bold (rich text); "— yêu cầu:" và "— tên gốc:" giữ nguyên văn.
10. **Zebra nhẹ** `F5F7FA` cho dòng chẵn (conditional formatting theo ROW), viền dưới mảnh `D9D9D9`; giữ gridlines.
11. **Thứ tự sheet:** Danh mục đọc · Chú giải · Tra cứu. Tab màu: xanh đậm / xám / xám nhạt. Mở file vào sheet đầu, ô A5.
12. **Chú giải:** bảng 4 lớp (RAW · NNC đã nhập · DẪN XUẤT · APPROVED: chưa có dòng nào), nhãn giá, ưu tiên, nguồn + hash, thời điểm. Cùng style header.
13. **Tra cứu:** cùng style header, freeze B5, filter, font 9.
14. **In:** A4 ngang, vừa 1 trang chiều ngang, lặp dòng 4, lề hẹp.

## Bổ sung sau visual review của root (cloud render, 02/11)

15. **BV cần — gom yêu cầu trùng (quyết định của Opus).** Vấn đề: ô C116 lặp cùng một spec dài 4 lần (~40 dòng), vượt chiều cao đọc được. Cách làm:
    - Nếu từ 2 BV trở lên có `spec_raw` **trùng nguyên văn** (chỉ chuẩn hóa NFC và khoảng trắng để so), dòng đầu của ô ghi `Yêu cầu chung (n BV, trùng nguyên văn): <spec>`. Sau đó mỗi BV một dòng: `BV: SL ĐVT`.
    - BV nào có spec hoặc tên gốc khác thì ghi thêm `— yêu cầu riêng: …` / `— tên gốc: …` ngay trên dòng của BV đó.
    - Nếu mọi BV khác nhau thì liệt kê từng BV như v1.1.
    - Lý do: giữ đủ chữ và lượng từng BV, giảm lặp khoảng 4 lần mà không cắt nội dung.
    - Đánh đổi: người đọc có thể hiểu nhầm "trùng yêu cầu" là "cùng sản phẩm". Vì vậy nhãn ghi rõ "trùng nguyên văn". Thêm một dòng ở Chú giải: ô "BV cần" là **cách trình bày dẫn xuất**; tên/spec nguyên văn đầy đủ từng BV nằm ở sheet Tra cứu. Không gộp demand hay variant, không đổi raw.
    - Cùng quy tắc này áp cho tên gốc trùng giữa các BV: chỉ ghi một lần.
16. **Ô vẫn dài sau khi gom** (vượt 409pt): giữ đủ chữ, đặt chiều cao 409pt, ghi thêm dòng cuối `(xem đủ ở Tra cứu)`. Không cắt.
17. **Tra cứu:** cột M ("Số dòng nhu cầu (Tham_chieu_BV)") rộng 24 để header gói tối đa 2 dòng; header cao 32 như sheet chính. Quy tắc chiều cao dòng (mục 5) cũng áp cho Tra cứu.

## Kiểm (acceptance)

- So từng ô giá trị giữa v1.1 và v1.2 theo mã record + tên cột (sau khi đổi thứ tự cột): **0 khác biệt nội dung** ngoài dòng 2–3 đầu trang và vị trí cột. Số dòng, số bản ghi, ID giữ nguyên.
- Các ca VT-0006, hai Syringe 50ml, VT-0014, VT-0100, TH-0005, Kom 2026, KOM-95 hiển thị đúng.
- Font, freeze, filter, chiều rộng, tab, print setup đọc lại được bằng openpyxl; ghi rõ **chưa kiểm render Excel thật** nếu chưa có.
- Chiều cao: mọi dòng dữ liệu có height tường minh; báo phân bố (min/median/max) và danh sách dòng chạm 409pt. Kiểm riêng C116 (sau gom: số dòng hiển thị trước/sau), hai Syringe, Foley, cột Giá dài nhất, header Tra cứu M4.
- Kiểm gom: với mỗi dòng có "Yêu cầu chung", ghép lại theo từng BV phải ra đúng `spec_raw` nguyên văn của BV đó (so với Tra cứu); 0 mất chữ.
