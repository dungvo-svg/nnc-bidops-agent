# Hồ sơ Agent gói thầu — BẢN NHÁP (09/11/2026)

Đúc kết từ ca Thuốc 5 BV + Komsenahak, 30/10–09/11 ([kinh nghiệm](../KINH-NGHIEM-THAU-THUOC-20261109.md)). Mục tiêu (Dũng): **Agent tự chủ chạy một gói thầu**, người giữ các quyết định có hệ quả.

Trạng thái: **đề xuất** (mức R2: D2). Chưa `oser init`; Mission M01 vẫn nháp (D09). Hồ sơ này không cấp quyền mới. Quyền quyết định theo `requirements/11-ROLE-AUTHORITY-MAP.md` (CAP); kiến trúc dữ liệu theo D20 (PROPOSED). Quy trình đi kèm: [QUY-TRINH-GOI-THAU.md](QUY-TRINH-GOI-THAU.md).

## 1. Bản đồ Agent

```
Người có thẩm quyền (CEO / người điều hành) ─ quyết D3, ưu tiên, hạn
        │
AG-GOI  Agent Gói thầu (điều phối, giữ BẢN THỂ, đầu ghi duy nhất)
   ├─ AG-CHUAN   Agent Chuẩn hóa & Đối chiếu   (subagent, chỉ trả kết quả cho AG-GOI)
   ├─ AG-NHAN    Agent Nhận về / intake        (kiểm runtime trước khi vào bản thể)
   ├─ AG-HOP     Agent Họp                     (ghi, tóm tắt; chỉ đọc)
   └─ AG-CANHAN  Agent cá nhân của từng người  (chạy dưới quyền chủ của nó)
Node người: Trang · Lý · Tar · Sơn · Duy · Huyền · Tình · Phét · Linh … (theo bảng chia của nhóm)
Bể chung nhiều gói: AG-GOI giữ một bể chung cho các gói cùng mùa (gói nộp trước phủ gói sau), xem QUY-TRINH §1b
```

## 2. AG-GOI — Agent Gói thầu

| Mục | Nội dung |
|---|---|
| **Sứ mệnh** | Đưa một gói thầu từ "hồ sơ yêu cầu" tới "bộ dữ liệu sẵn sàng để người duyệt và nộp": đủ mã, đủ nguồn hoặc lý do thiếu, giá có căn cứ, ảnh/Visa/soft copy theo mẫu |
| **Một gói = một Mission** | Mỗi gói (Kom 2027, Mahosot 2027…) có một bản thể, một sổ lock và một hạn. Gói sau dùng lại kết quả gói trước theo mã |
| **Đầu vào** | Hồ sơ yêu cầu BV/Kom (nguồn thô); lịch sử (trúng/chào năm trước, nguồn chị Phét đã nộp); bảng chia của nhóm; báo giá NCC (qua runtime); chỉ đạo của người có thẩm quyền |
| **Đầu ra** | Bản thể gói (một file, chỉ Agent ghi); bộ lock theo mốc; file runtime theo người; báo cáo tiến độ theo đúng loại đếm; bộ xuất bản (soft copy, ảnh, bảng duyệt) |
| **Ghi được** | Bản thể; sổ lock; thư mục runtime (tạo file, không sửa ô người đã ghi); báo cáo |
| **Chỉ đọc** | Nguồn thô; file runtime của người (trừ khi nhận về); thư mục báo giá |
| **Tự làm (D0–D2)** | Chụp nguồn; chuẩn hóa tên; đối chiếu lịch sử; tách runtime theo bảng chia; nhận về có kiểm; nâng lock; tính lại số liệu; báo cáo; soạn câu hỏi cho người |
| **Dừng và hỏi (D3)** | Giá chào, chọn NCC, tương đương thuốc, Visa thay thế, quyền xem giá vốn, thay đổi bảng chia, nộp hoặc gửi bất cứ thứ gì ra ngoài, đổi định dạng bản thể |
| **Không bao giờ** | Giao việc cho người; sửa nguồn thô; chép đè file đang có người ghi; đưa số AI suy ra vào ô "đã xác nhận"; bịa số; gửi dữ liệu ra ngoài công ty |
| **Đo tiến độ** | Theo mã và theo loại: có nguồn / có giá mua / có giá vốn / có hàng chào / có ảnh nguồn / đã được người xác nhận / đã duyệt chào. Không cộng lẫn các loại |
| **Nhịp** | Mỗi lần có người đổi trạng thái hoặc theo mốc (sáng/chiều): nhận về → nâng lock → báo cáo ngắn |
| **Bàn giao** | Bản thể + lock + báo cáo + câu hỏi mở; trạng thái ghi vào `context/PROJECT_STATE.md` |

## 3. AG-CHUAN — Agent Chuẩn hóa & Đối chiếu

| Mục | Nội dung |
|---|---|
| Việc | Tên thương mại → hoạt chất · hàm lượng · dạng; nhóm thuốc; ghép mã giữa các đơn vị; ghép giá theo dòng nguồn; đối chiếu trúng/chào năm trước |
| Cách làm | Chia lô cho subagent song song; mỗi dòng có nhãn độ chắc (chắc / vừa / suy từ tên thương mại / không rõ) và căn cứ |
| Ra | Bảng đề xuất trả cho AG-GOI; AG-GOI quyết đưa vào bản thể ở cột "AI đề xuất" (có màu) |
| Không | Ghi thẳng bản thể; điền khi không rõ (thà để trống) |

## 4. AG-NHAN — Agent Nhận về (intake)

| Mục | Nội dung |
|---|---|
| Việc | Đọc file runtime của từng người, lấy các ô được phép (giá, kết quả, người/ngày, trạng thái), kiểm rồi đưa vào bản thể theo mã |
| Kiểm bắt buộc | Mã tồn tại; ô thuộc đúng người; tiền tệ + ĐVT có; số hợp lý; không ghi đè ô người khác; file không đổi trong lúc đọc |
| Ra | Danh sách ô nhận / ô từ chối (kèm lý do) → AG-GOI nâng lock |

## 5. AG-HOP — Agent Họp

Ghi âm, tóm tắt và rút việc **chỉ khi người dùng bật**. Gắn nhãn lời nói [L] và chỗ chưa nghe rõ. Không ghi điều gì là đã chốt; câu hỏi thẩm quyền chuyển cho AG-GOI đưa vào agenda.

## 6. AG-CANHAN — Agent cá nhân của từng người

| Mục | Nội dung |
|---|---|
| Ai dùng | Mỗi người tìm giá dùng Claude của mình (hướng dẫn agent dùng chung trong `Inbox_thau`) |
| Việc | Đọc báo giá NCC, khớp dòng trong file runtime của chủ, quy về VND / 1 ĐVT, trả bảng đề xuất |
| Quyền | Không hơn chủ của nó; chỉ đọc file của chủ; không ghi Drive; không đổi tỷ giá; không kết luận tương đương |

## 7. Vai người đối ứng (theo ca Thuốc; là CÁCH THỨC, nhóm đổi được)

| Người | Vai thấy được trong ca | Agent làm gì cho họ |
|---|---|---|
| CEO / người điều hành | Ưu tiên, hạn, quyết D3 | Bảng duyệt gọn; câu hỏi có phương án (R2 decision contract) |
| Phét | Nguồn đã nộp, công thức giá Kom, hàng hiếm, hồ sơ | Đối chiếu nguồn đã nộp; hỏi xác nhận công thức |
| Tình | Kiểm giá | Bảng so giá cùng loại (GM/GV/chào, tiền tệ, ĐVT, VAT) |
| Trang | NCC Việt Nam, giá mua, giá vốn; nhận khung ≈ 900 mã | File runtime theo NCC; hàng đợi tuần tự; danh sách cần hỏi |
| Lý | Cùng tìm thuốc phía sau phần của Trang (Dũng nêu 09/11); quy trình cước QT-CU-05 | Hàng đợi riêng tách từ phần chia theo bảng của nhóm; chưa tự gán mã |
| Tar | Xác nhận thành phần | Danh sách tra cứu cần xác nhận, có độ chắc |
| Sơn | Trung Quốc, ngoài Hà Nội | Danh sách theo hoạt chất cho NCC Trung Quốc |
| Duy | Kom thuốc, giá thuốc đang bán | Đối chiếu với danh mục đang bán |
| Huyền | Phần được chia | File runtime riêng |
| Linh | Giá Misa | Nhận giá Misa như nguồn lịch sử (không phải giá hiện hành) |
| Dũng | Dữ liệu, tổng hợp, vận hành Agent; không giao việc | Toàn bộ báo cáo, lock, câu hỏi mở |

## 8. Tiêu chí nhận (đề xuất) cho một gói

1. Bản thể có đủ 100% mã của hồ sơ yêu cầu, ghép theo mã, không trùng.
2. Mỗi mã có trạng thái đúng loại; không mã nào "đã xác nhận" mà thiếu người xác nhận.
3. Mỗi giá có tiền tệ, ĐVT, nguồn, ngày; lock cuối cùng có hash và danh sách thay đổi.
4. Câu hỏi D3 còn mở được liệt kê kèm người cần trả lời.
5. Bộ xuất bản theo mẫu của BV (soft copy, ảnh) sinh từ bản thể, không sửa tay.
