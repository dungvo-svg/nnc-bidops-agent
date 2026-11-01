# Bản bàn giao Git private — 01/11/2026

**Bắt đầu tại [context/clone-handoff/README.md](context/clone-handoff/README.md).** Đây là source/context được lọc, có pilot23file và testsynthetic. Không có nguồn thầu thô/DB/credentials/plugin hoặc lịch sử Claude. Các mô tả setup dưới đây giữ làm lịch sử; clone-handoff ghi trạng thái/quyền mới nhất.

# NNC BidOps Agent

> Cập nhật 01/11: phương án và code B đã được đối chiếu; đọc continuity ở dưới trước các mô tả setup lịch sử. Scope hiện hành là node CEO đa nhánh, thầu BV làm mũi nhọn, không chỉ trợ lý thầu cá nhân. P1/P2 business acceptance vẫn tách khỏi test synthetic.

Trợ lý điều hành thầu & cung ứng. Workspace để Dũng và Claude chốt sản phẩm theo P1/P2, dùng lại bằng chứng đã thu và chuẩn bị một vòng thử được phép.

**Bắt đầu:** mở thư mục này trong Claude, đọc [CLAUDE.md](CLAUDE.md), [trạng thái hiện tại](context/PROJECT_STATE.md) rồi [phiếu P1](requirements/P1-REQUEST.md). Chưa có P1 được duyệt, SRS được nghiệm thu hay sản phẩm mới đã xây. Việc setup không làm thay đổi trạng thái đó.

## Các điểm vào

- [Continuity BidOps 01/11](context/continuation-20261101/BRIEF.md): mission CEO đa nhánh, nguồn/phiên bản, quyết định, đối chiếu A→B và lộ trình. B có code/test local cách ly; chưa tích hợp hay release vào owner.

- [Authority graph tài liệu sản phẩm](requirements/00-README-AUTHORITY.md): [01 PRD core](requirements/01-PRD-CORE.md), [08 nguồn](requirements/08-SOURCE-MAP.md), [10 khóa](requirements/10-LOCK-REGISTER.md), [11 người-quyền](requirements/11-ROLE-AUTHORITY-MAP.md).
- [Mission và cách làm tự chủ (OSER R2)](context/mission/README.md), [định hình sản phẩm F01](context/mission/BIDOPS-F01.formation.json), [dùng chung và họp](context/HOP-VA-DUNG-CHUNG.md).

- [Định hình sản phẩm](discovery/PRODUCT-FRAMING.md): nhu cầu, sự kiện và giả thuyết.
- [Câu hỏi và quyết định](requirements/DECISIONS.md): phần Dũng/chủ nghiệp vụ cần chốt.
- [Backlog và tiêu chí nhận](requirements/BACKLOG-ACCEPTANCE.md): việc tiếp theo có nguồn, chưa nhận là đã làm.
- [P2 và cách thử](requirements/P2-VALIDATION.md): điều kiện đầu vào và ca kiểm phù hợp rủi ro.
- [Nguồn và khả năng mang sang máy khác](sources/README.md), [inventory](sources/inventory.json): nguồn nào đã chép, nguồn nào chỉ dẫn chiếu, hash và giới hạn.
- [Không gian dữ liệu thử](data-work/README.md) và [đầu ra](outputs/README.md): tách khỏi nguồn và bộ đã gửi.

Nguồn chính đã được chép vào workspace này: 22 tệp gốc (~103 MB), gồm 17 JPEG thầu, 3 workbook, packing list và SOP. Một ảnh cài WeChat không liên quan đã loại. Có thêm snapshot text/metadata kế hoạch Cung ứng, chưa tải AMIS thô. Các tệp gốc không được sửa khi phân tích. Các snapshot v1/v2/v3 của discovery được giữ dưới sources/history; nguồn không nhân bản lại trong từng snapshot.

Snapshot setup30/10: Git lúc đó chỉ local. Đã được Dũng giao tạo/push private repo01/11; xem clone-handoff hiện hành. Nguồn thô/data/output vẫn không được publish.

## Prompt mở phiên Claude

> Tiếp tục dự án NNC BidOps Agent trong thư mục hiện tại. Đọc CLAUDE.md, context/PROJECT_STATE.md, requirements/P1-REQUEST.md và sources/README.md. Đối chiếu các bằng chứng có liên quan; giữ rõ sự kiện, giả thuyết và quyết định chưa chốt. Trước hết hoàn thiện phiếu P1 cho một ca cụ thể và đề xuất các câu hỏi cần chốt với Dũng/chủ nghiệp vụ. Tiếp tục chuẩn bị độc lập các fixture tổng hợp và ca kiểm trong data-work khi có ích. Chưa chọn sẵn webapp/framework, chưa ghi P1/P2 hoàn tất. Không chạy legacy builder, không sửa nguồn/bộ thầu đã gửi/Mittaphab, không gửi tin hoặc đẩy Git. Nếu gặp thay đổi của người dùng, giữ nguyên và chỉ bổ sung phần thiếu.
