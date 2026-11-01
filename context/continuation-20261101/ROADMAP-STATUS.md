# Lộ trình và trạng thái (đề xuất, không cam kết ngày hay giá)

> Bản audit/plan đã được Codex đối chiếu độc lập và lưu vào project ngày 01/11/2026. Claude Opus tổng hợp, Sonnet kiểm hai nhánh. Các nhãn draft/đề xuất trong nội dung là trạng thái quyết định, không có nghĩa file còn ở ngoài project. Chưa thay runtime, tích hợp code, merge hay deploy. Chi tiết nguồn/giới hạn: SOURCES-READ.json và PUBLICATION-RECEIPT.json.


## Năm case trong phạm vi kế hoạch

Đây là phạm vi kế hoạch, **không phải trạng thái gói đã được xác minh từng ngày**. Hạn nộp lấy từ chat và cover ngày 28–30/10, chỉ dùng để lập kế hoạch. Mốc nội bộ không thay hạn pháp lý (A8 §5).

Mittaphab (hạn ghi trong chat là 04/11) do owner làm theo luồng hiện có. BidOps chỉ đưa diff hoặc ngoại lệ khi owner hỏi, không tiếp quản.

| Case | Mốc kế hoạch (nguồn, as_of) | Hạn chính thức | Dữ liệu trong B (receipt Codex) |
| --- | --- | --- | --- |
| Komsenahak 2027 | 13/11 — chỉ dựa vào tin Phét 29/10 09:55 (`3A80D142E07EE83C9B44`) và 09:58 (`3EB0A915BEF866D46BD980`). Ô `I8` trong hai sheet mẫu ("Excemple for hard copy", "Excemple for soft copy(USB") ghi "Viêng Chăn, ngày 13/11/2026" ở dòng ký của mẫu thư, **không phải giờ đóng thầu chính thức** | **Chưa có HSMT** | Nạp read-only 1.455 dòng; 0 dòng đủ danh tính. 649 dòng có giá lịch sử (giá đã chào năm 2026, theo tin Phét 30/10 09:13), **không phải quote hiện hành** |
| Mahosot | 25/11 — tin Phét 29/10 09:58; cover nội bộ | Chưa | Có trong 3.523 source intake; chưa có số theo gói |
| Settha | 26/11 — cùng nguồn | Chưa | Như trên |
| Me and Dek | 27/11 — cùng nguồn. Một aggregator ghi 26/11, chưa xác minh, PDF MOF lỗi 503 | Chưa | Như trên |
| SVNK | Chưa có hạn trong nguồn | Chưa | Như trên. Giao cả tỉnh và huyện, nhiều điểm |

## Thứ tự đề xuất (ưu tiên local, chưa gán ngày)

1. **Tài liệu và đề xuất.** Vòng này chỉ làm audit, tài liệu, readout.
   - Đã xong ngày 01/11: Codex đối chiếu và lưu bộ tài liệu vào `context/continuation-20261101`, thêm pointer vào PROJECT_STATE và README (`PUBLICATION-RECEIPT.json`). Phần còn là đề xuất ghi trong `PATCH-PROJECT_STATE-README.md`.
   - Các gói code kế tiếp (packet, năm phép kiểm, bus, principal) chỉ đề xuất cho vòng sau.
   - Bước code kế tiếp hiện **chỉ là đề xuất**: spec `export_packet` / `import_return` → `RETURN_UNVERIFIED`, kèm ca test.
   - Khi có vòng được chốt phạm vi: Opus có thể giao Sonnet cài đặt. Codex là bên thực thi ngang hàng và review độc lập. **Chưa có quyết định cài đặt.**
2. **Ma trận dòng Kom × năm phép kiểm × đầu vào có/thiếu.** Đọc read-only từ intake Kom và inbox DRAFT. Ô chưa biết ghi "chưa biết", không điền 0. Kết quả làm căn cứ cho họp D01. Không cần danh tính hay kênh.
3. **Chọn ca đầu trong họp D01.** Hai ứng viên giả thuyết:
   - Kom, phần hàng chưa có giá và các dòng có sai khác.
   - Settha 40mm/30mm (case C1 HOLD).
4. **Vòng L4 tối thiểu.** CEO và đúng một owner thật, mỗi bên dùng Agent của mình.
   - Packet chỉ đọc, gửi qua kênh được phép.
   - Return ghi `RETURN_UNVERIFIED`. Bên dùng ghi `used_in_candidate`.
   - Cần có trước: danh tính, kênh, quyền đọc nguồn. Người có quyền quyết.
5. **Phép kiểm đáp ứng hồ sơ cho ca đầu.** Cần HSMT/addenda đúng gói. Đề nghị hỏi Phét, chờ CEO xác nhận người phụ trách. Locator gồm sheet, năm, `award_granularity`.
6. **Hàng–chứng từ–tiền cho các dòng chọn chào.** Đọc read-only Excel kho/xe và App hiện có; danh tính Visa theo thương phẩm; landed cost theo tuyến.
7. **Mở rộng sang các gói 25/26/27.** Chỉ làm sau khi bước 4 có receipt thật.

## Trạng thái

- **Đã có code và test L1 synthetic, chưa tích hợp:** catalog chung, demand lifecycle, DRAFT inbox, kernel mission, ba lỗi đã vá.
- **Còn mở:**
  - Tích hợp vào owner.
  - L2 BidOps, L4, L5.
  - HSMT.
  - Quote hiện hành, biến thể có danh tính.
  - Hàng–chứng từ–tiền.
  - Kinh tế/vốn, căn cứ cạnh tranh.
  - Chủ master.
  - Repo công ty.
- **Không làm:** ghi master, chấp nhận quote, gửi hay nộp, VM, broker, push, merge, deploy.
