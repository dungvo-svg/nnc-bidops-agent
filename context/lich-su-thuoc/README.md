# Lịch sử quá trình làm thầu Thuốc 2027 (Công ty NNC, kênh HC)

Dũng yêu cầu ngày 13/11/2026: ghi lại toàn bộ quá trình làm thầu thuốc để rút kinh nghiệm ("ghi hết đi nhé, cái đó đáng học"). Nội dung gồm:
- các cuộc họp và sự kiện;
- việc Dũng làm với từng anh chị;
- những điểm Agent sai và cách sửa;
- những điểm Dũng phải hỏi lại nhiều lần.

| Tệp | Nội dung |
|---|---|
| [01-DONG-THOI-GIAN.md](01-DONG-THOI-GIAN.md) | Diễn biến theo ngày, 26/10 → 13/11 |
| [02-HOP.md](02-HOP.md) | Các cuộc họp: ai dự, nội dung, việc giao, cái gì chưa phải quyết định |
| [03-THEO-NGUOI.md](03-THEO-NGUOI.md) | Dũng làm việc với từng anh chị: giao gì, trao đổi gì, kết quả |
| [04-CHI-DAO-VA-QUYET-DINH.md](04-CHI-DAO-VA-QUYET-DINH.md) | Chỉ đạo của Dũng (trích ngắn) và trạng thái D-xx |
| [05-SAI-SOT-VA-SUA.md](05-SAI-SOT-VA-SUA.md) | Sai sót của Agent: ai phát hiện, nguyên nhân, cách sửa, bài học |
| [06-HOI-LAI-NHIEU-LAN.md](06-HOI-LAI-NHIEU-LAN.md) | Những chỗ Dũng phải hỏi lại, vì sao, cách tránh (gồm cả trao đổi trực tiếp Dũng ↔ Agent) |
| [06b-HOI-LAI-DAY-DU.md](06b-HOI-LAI-DAY-DU.md) | Danh sách đủ 164 tin hỏi lại/nghi vấn trong 424 tin Dũng gửi Agent, theo ngày và nhóm |
| [07-CON-MO.md](07-CON-MO.md) | Điều chưa rõ hoặc chưa có bằng chứng (không đoán) |

## Quy ước
- **Phạm vi:** số liệu của Công ty NNC, không phải tập đoàn.
- **Giờ:** theo giờ Lào (UTC+7).
- **Không ghi số tiền:** giá mua, giá vốn, giá chào, tỷ giá, công nợ, lương. Chỗ cần thì mô tả bằng lời. Số lượng mã hoặc ô thì được ghi.
- **Lời nói trong họp** là chữ máy nhận dạng (ASR), chưa xác minh. "Chốt" trong họp chưa phải quyết định nghiệp vụ, trừ khi người có thẩm quyền xác nhận.
- **Nguồn:**
  - tin nhắn của Dũng trong các phiên Claude (trích ở `.local/lich-su-trich/`, không đưa lên git);
  - `context/PROJECT_STATE.md`, `requirements/DECISIONS.md`;
  - tóm tắt họp ở `.local/hop-drafts/` và `context/meetings/`;
  - báo cáo trong `outputs/` (đều local);
  - ghi nhớ của Agent (memory).

## Cập nhật về sau
Sau mỗi phần việc có ý nghĩa, Agent ghi thêm vào đây cùng lúc với checkpoint trong PROJECT_STATE:
- sự kiện, vào `01`;
- họp, vào `02`;
- sai sót mới, vào `05`;
- câu Dũng phải hỏi lại, vào `06`.

Mỗi dòng có ngày, giờ và nguồn.
