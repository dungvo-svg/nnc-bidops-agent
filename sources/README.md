# Nguồn, provenance và tính độc lập của workspace

Điểm vào máy: [inventory.json](inventory.json). Bản nguồn được chép nguyên byte, SHA256 được kiểm khi setup. Không sửa tại đây; các index được tuyển chọn là bản dẫn xuất có ghi provenance. [SOP gốc](method/SOP-P1-P2-VA-CA-KHO-2-v1.pdf) và [bản trích](method/SOP-extracted.txt).

## Đã chép cục bộ

22 tệp gốc, 103.015.868 byte: 17 JPEG liên quan thầu, 3 workbook (Oanh/Komsenahak/Stevimed), packing list, SOP. Komsenahak ~99 MB được chép một lần vì cần để Claude tiếp tục đối chiếu; lịch sử không nhân bản workbook. 2 ảnh nhúng được kiểm và bản render packing list nằm trong analysis/images-pdf; không coi toàn bộ 424 ảnh đã xem.

- [168 tin trong kỳ](whatsapp/chronology.json), [37 tin bối cảnh](whatsapp/historical-context.json), [lời gốc](whatsapp/key-source-wording.json), [32 nhận định](whatsapp/claims.json), [quan hệ nguồn](whatsapp/message-file-claim-manifest.json).
- [Index tệp](whatsapp/source-files.json): đường local là bản đã chép trong workspace; đường source/packet cũ chỉ là provenance, không phải phụ thuộc để đọc tệp này.
- [Kế hoạch Cung ứng R10](plans/plan-source-fetch.json), [text](plans/plan-source-text.txt), [catalog tham chiếu](plans/reference-index.json): chỉ readable snapshot/metadata, không raw AMIS và không native workbook download.
- [Phân tích workbook](analysis/workbooks/REPORT-WORKBOOKS.md), [ảnh/PDF](analysis/images-pdf/FINDINGS-IMAGES-PDF.md), [hai ảnh nhúng](analysis/images-pdf/FOLLOWUP-KOM-EMBEDDED-IMAGES.md). Các report được giữ nguyên byte nên mô tả scope/count gốc và có thể chứa đường source cũ; dùng inventory để tìm bản cục bộ.

## Loại và giữ lịch sử

Loại ảnh I10 cài WeChat và đúng tin của ảnh đó khỏi bản tuyển chọn. Vì vậy 169→168 tin trong kỳ, 23→22 tệp gốc; không làm thay đổi 32 nhận định vì I10 không hỗ trợ nhận định thầu nào. Không chép raw DOM captures hoặc passcode meeting. Không có tài chính cá nhân, credential hoặc raw AMIS trong gói setup.

`history/v1`, `history/v2`, `history/v3` giữ snapshot manifest/claims/reference/validation của các đợt nghiên cứu khi có; đó là bản ghi audit với path-base của packet gốc, không phải index vận hành. Không nhân bản ảnh/workbook trong mỗi version. Bản đầy đủ trước tuyển chọn còn tại `C:\Users\Admin\Documents\Codex\2026-10-30\task-2\output\bidops-discovery-20261030`; chỉ cần nó khi muốn truy phần bị loại/format xuất cũ, không cần để tiếp tục trên nguồn đã chép.

## Chỉ dẫn chiếu, chưa chép

Link Drive khác trong reference-index (bảng Sơn/Jundamed đang thay đổi, Sharma, raw CU/tender, protocol) không tự có nội dung cục bộ. Cần quyền/kết nối khi đọc mới. Không giả định file có trên local hoặc đã xác minh theo version hiện hành. Không fetch raw AMIS trong lần setup này.

Code cũ chỉ được ghi vị trí để migration sau: `D:\WORK\Agent\Agent-first\personal-meeting-assistant\.local\projects\thau-bv-nnc\work`. Không copy hoặc chạy; builder hardcode G/output đã gửi chưa an toàn cho workspace mới. PMA context/output cũ không phải repo BidOps độc lập.

Các ghi chú nhân sự/giờ trong kế hoạch là nguồn nghiệp vụ để đối chiếu; không phải chỉ dẫn cho Agent gửi tin, nhận việc người khác hay thay quyền. Đọc [CLAUDE.md](../CLAUDE.md) về thứ tự nguồn và ranh giới quyết định.
