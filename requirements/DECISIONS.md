# Quyết định và câu hỏi còn mở (file chủ `D*`)

Luật graph: [`00-README-AUTHORITY.md`](00-README-AUTHORITY.md). Khóa ở [`10-LOCK-REGISTER.md`](10-LOCK-REGISTER.md); người giữ quyền ở [`11`](11-ROLE-AUTHORITY-MAP.md); nguồn ở [`08`](08-SOURCE-MAP.md).

Đã có chỉ dẫn của Dũng: dùng tên thư mục NNC BidOps Agent, setup để tiếp tục với Claude, thu hội tụ nguồn để định hình sản phẩm. 30/10/2026 (chat với Claude): áp phương pháp tự chủ từ nnc-claude-plugins; Opus giữ quyết định, Sonnet làm song song; kiểm GitHub org nhưng chưa push — đã áp vào `.claude/` và `context/mission/`. Chưa có bằng chứng phê duyệt yêu cầu/portfolio/kiến trúc. Setup được phép không thay quyết định nghiệp vụ.

| Mã | Cần chốt | Người xác nhận | Trạng thái |
| --- | --- | --- | --- |
| D01 | Một ca/gói/lô đầu tiên, đầu ra ai dùng và điều kiện chào từng phần | Dũng + chủ nghiệp vụ phù hợp | Chưa chốt |
| D02 | Master/version và quyền cập nhật/lan thay đổi | Chủ master/nhóm được chỉ định | Chưa chốt |
| D03 | Trường giá/công thức/thuế/vận chuyển và tham số theo từng mẫu | Người sở hữu quy tắc giá | Chưa chốt |
| D04 | Sai khác quy cách/chứng từ: ai có quyền nhận/từ chối | Người nghiệp vụ/kỹ thuật có quyền | Chưa chốt |
| D05 | Quote hiện hành, MOQ, lô/hạn, route/carrier và capacity/cash | Cung ứng + người duyệt cam kết | Chưa xác minh đủ |
| D06 | Người thử P1/P2 độc lập, dữ liệu/môi trường được phép | Dũng | Chưa chốt |
| D07 | Cách làm phù hợp: quy trình/Excel/cấu hình/Skill/công cụ | Chủ nghiệp vụ sau so sánh P1 | Chưa chọn |
| D08 | Nơi lưu repo: GitHub org công ty (theo Dũng: Sếp Quân đã lập; org cụ thể chưa xác định), tên repo, private, phạm vi được push (chỉ tài liệu; `sources/`/data/output vẫn ignore; chỉ org nội bộ, private — tài liệu có tên BV khách hàng, hạn nộp, thông tin nhân sự) | Dũng + Sếp Quân | Chưa chốt — kiểm 30/10: chưa xác định org, Dũng chưa là thành viên org nào |
| D09 | Duyệt Mission BIDOPS-M01 và chạy `oser init` (plugin `nnc` đã ghim theo chỉ dẫn Dũng 30/10) | Dũng | Chưa duyệt — có contract nháp ở `context/mission/` |
| D10 | Phương pháp dự án: SOP P1/P2 v1 + OSER R2 (main `94ddf8b`, plugin ghim) + authority graph/lock (`00-README-AUTHORITY.md`) | Dũng | Chỉ dẫn Dũng 30/10 (chat); đề xuất khóa `LCK-METHOD` — PROPOSED, chờ Dũng xác nhận |
| D11 | Luật ghép: yêu cầu và chào giữ riêng; không ghép bằng STT; phạm vi BGC dùng mã MPSC; nguồn khác cần bảng nối trước khi ghép | Người sở hữu master (D02) + Phet | Chưa chốt — đề xuất `LCK-MATCH-KEY` (PROPOSED), bằng chứng đo ở `discovery/DINH-HINH-SAN-PHAM.md` §3 |
| D12 | Ngữ nghĩa giá trị: trống ≠ 0 ≠ chưa xác nhận; giá năm trước/mua gần nhất là lịch sử; mã tiền chỉ VND/USD/THB/CNY/LAK | Người sở hữu quy tắc giá | Chưa chốt — đề xuất `LCK-VALUE-SEMANTICS` (PROPOSED) |
| D13 | Bộ trạng thái dòng/gói: đã giao · đã nhận · đã kiểm · đã nạp · đủ điều kiện trình · đã quyết chào/không chào | Chủ nghiệp vụ | Chưa chốt — đề xuất `LCK-STATUS` (PROPOSED) |

## Bằng chứng D10 — nguyên văn chỉ dẫn của Dũng (phiên Claude 30/10/2026)

- "áp dụng phương pháp thiết lập tự chủ cho dự án này nhé … kiểm tra github công ty có chưa … đặt kiểm tra chưa push gì nhé. Thiết lập dự án này trước théo P1/P2 đã có và định hình tự chủ"
- "chia việc song song , quyết định giữ opus còn sonnet làm song song" — **chính sách của Dũng**, không phải bảng ghim model theo vai của phương pháp.
- "main 94ddf8b … OSER R2 … này nhé"
- "ta cài để kế thừa phương án cho dự án lấy từ Repo để thiết lập chứ không cần gửi ngược về đó"
- "thiếu rồi ta ngoài P1 P2 còn có các Hệ thống tài liệu sản phẩm lock để giảm việc refactor thiếu chủ đích"
- "audit lại nhé vì có một số dữ liệu đang bị nhiễu theo tài liệu plugin cũ"

Khi có quyết định thật, thêm ngày, người, phạm vi, nguồn dẫn và tác động. Không tự đổi Chưa chốt thành Đạt. Không yêu cầu chốt mọi câu trước khi làm các phần phân tích/fixture độc lập.
