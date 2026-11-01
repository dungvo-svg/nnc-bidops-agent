> Clone/private Git01/11: đọc `context/clone-handoff/README.md` trước. Nguồn thô và plugin cục bộ không nằm trongclone. Snapshot cũ không phủ quyết chỉ đạo mới của Dũng; không nâng businessdecision thànhLOCKED hoặc mở quyền tự động.

# Hướng dẫn workspace

Áp dụng cho toàn bộ thư mục. Đọc [CLAUDE.md](CLAUDE.md) và [PROJECT_STATE.md](context/PROJECT_STATE.md).

- Đây là discovery/P1 và chuẩn bị P2, chưa phải app đã xây hoặc yêu cầu được duyệt.
- Giữ thay đổi người dùng. Trước ghi file đã có, đọc nội dung và Git status; không overwrite mù, không reset/clean.
- Các nguồn `sources/` là bằng chứng để đọc; phân tích mới ở `discovery/`, yêu cầu ở `requirements/`, dữ liệu thử ở `data-work/`, kết quả ở `outputs/`.
- Không chạy legacy builder hoặc viết ra bộ thầu đã gửi. Chưa cài dependencies, tạo access hay automation — ngoại lệ duy nhất theo chỉ dẫn Dũng 30/10/2026: plugin `nnc` (OSER R2, main `94ddf8b`) ghim tại `.claude/vendor/`, hook cục bộ (không gửi dữ liệu đi; observer chỉ ghi khi bật `experience-enable`).
- Không commit/push dữ liệu/tài liệu nguồn; mọi publish/send/nộp thầu phải theo chỉ dẫn cụ thể của Dũng.
- Ghi rõ source fact / hypothesis / pending decision; không bịa số, dùng trống/chưa đo khi thiếu.
- Không tự dựng kiến trúc webapp hoặc OSER runtime chỉ vì tên dự án. Chọn cách làm theo đầu ra P1 và mức ảnh hưởng của P2.
