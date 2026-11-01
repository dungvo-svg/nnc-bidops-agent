# NNC BidOps — AUTHORITY GRAPH / ĐIỂM VÀO TÀI LIỆU SẢN PHẨM

Kế thừa mẫu authority graph của Kho Bậc 1.5 (`VOSYDUNG/Piops-Agent` `docs/du-an/kho-bac-1-5/00-README-AUTHORITY.md`, bản ghim trong `nnc-kho-1-5/reference/piops`, đọc 30/10/2026), thu gọn cho giai đoạn P1. Mục đích: **một việc làm một lần, sửa đúng chỗ, không refactor thiếu chủ đích.** Chỉ nhận ID node và luật; không chép nội dung nghiệp vụ Kho.

Trạng thái 30/10/2026: graph đã dựng; **chưa có node nào LOCKED**. P1 chưa duyệt; P2 chưa mở.

## 1. Luật cốt lõi

> Một fact / quyết định / người-quyền / nguồn / tiêu chí chỉ có **một file chủ**. Nơi khác chỉ tham chiếu ID, không chép lại lập luận.

Git giữ version cũ. Không tạo `V2`, `FINAL`, `new`, `rev2` cho cùng một trách nhiệm. Nếu một thay đổi buộc sửa cùng nội dung ở nhiều file thì graph đang sai — sửa graph trước.

## 2. Node và file chủ

| Node | File chủ duy nhất | Ý nghĩa |
| --- | --- | --- |
| luật graph | `requirements/00-README-AUTHORITY.md` (file này) | node, thứ tự ưu tiên, thứ tự đọc |
| WHY / outcome / ranh giới | `requirements/01-PRD-CORE.md` | sản phẩm để làm gì, không làm gì |
| `D*` | `requirements/DECISIONS.md` | quyết định (WHAT) và trạng thái |
| `P1-*` | `requirements/P1-REQUEST.md` | phiếu yêu cầu P1 (BIDOPS-P1-001) |
| `B*` (backlog + tiêu chí nhận sản phẩm) | `requirements/BACKLOG-ACCEPTANCE.md` | việc và tiêu chí nhận từng phần sản phẩm |
| `AC-*` (nghiệm thu Mission) | `context/mission/BIDOPS-M01.contract.draft.json` | mẫu số nghiệm thu Mission; trỏ `B*`/`P1-*`, không chép |
| `T-*` (ca kiểm P2) | `requirements/P2-VALIDATION.md` | ca kiểm và expected |
| `SRC-*` | `requirements/08-SOURCE-MAP.md` | nguồn ở đâu, chứng minh được tới đâu |
| `LCK-*` | `requirements/10-LOCK-REGISTER.md` | ai yêu cầu/duyệt, vì sao khóa, mở lại khi nào |
| `ACT-*`, `CAP-*` | `requirements/11-ROLE-AUTHORITY-MAP.md` | người/vai và quyền |
| `AMD-*` | `requirements/amendments/<yyyy-mm-dd>-<chu-de>.md` | thay đổi sau khi đã khóa |
| trạng thái / bước kế | `context/PROJECT_STATE.md` | đang ở đâu, chờ ai — không sở hữu business truth |
| gói Formation | `context/mission/BIDOPS-F01.formation.json` | giai đoạn Formation, ứng viên, điểm chưa giải — trỏ ID node |
| bằng chứng | `sources/` (chỉ đọc), `sources/analysis/`, `discovery/`, `context/HOP-VA-DUNG-CHUNG.md` | evidence, **không phải authority** |

**Chưa mở (chỉ mở khi qua cổng P2 theo SOP trang 3):** `DATA-*` hợp đồng dữ liệu, `FLOW-*`/`SCR-*` luồng/màn hình (nếu D07 chọn có giao diện), `LOT-*` lát xây + nghiệm thu, bản đóng băng thiết kế. Không tạo file rỗng trước.

## 3. Phụ thuộc

```text
SRC-* (08) ──evidence──> LCK-* (10) ──authorizes──> D* (DECISIONS)
                                                     ├──> ACT/CAP (11)
                                                     └──> P1-* (P1-REQUEST) ──> AC-* ──> [P2: DATA → FLOW/SCR → LOT]
WHY (01) giới hạn mọi node bên dưới. Evidence/discovery chỉ trỏ vào node, không ghi đè node.
```

Không suy ngược business truth từ bảng tính, mã, giao diện hay bản nháp. Bản nháp nằm cạnh authority không vì thế mà thành authority.

## 4. Khóa

Một quyết định chỉ được gọi **LOCKED** khi có đủ: `D*` + `LCK-*` đủ 8 trường (xem file 10) + `SRC-*`; liên quan quyền thì thêm `ACT/CAP`. Thiếu một trường → ghi `PROPOSED`/`Chưa chốt`, không ghi LOCKED/Đạt. Agent không tự khóa: chỉ người có quyền (cột Approved by) khóa, và phải có bằng chứng.

Khóa quyết định ≠ duyệt phiếu P1 ≠ mở P2 ≠ phát hành/áp dụng vận hành. Bốn mốc này tách nhau.

## 5. Mâu thuẫn và thay đổi

1. Xác định node bị mâu thuẫn.
2. Kiểm `SRC-*` + `LCK-*` của node đó.
3. Node chưa khóa: sửa một lần tại file chủ, ghi ngày/nguồn. Node đã khóa: **không sửa tại chỗ** — viết `AMD-*` (yêu cầu mới, ai yêu cầu, nguồn, phần bị ảnh hưởng, cách quay lại) → người duyệt → cập nhật file chủ + dòng LCK (re-lock). Amendment đã duyệt mới thắng tài liệu cũ.
4. Downstream chỉ sửa tham chiếu.
5. Nguồn lệch chưa giải: treo đúng phần bị ảnh hưởng (CLAUDE.md quy tắc 5), tiếp tục phần độc lập.

## 6. Chính sách chống refactor thiếu chủ đích

- Sửa lý do (WHY/D/LCK) trước, rồi mới sửa sản phẩm phía dưới; không "dọn cho đẹp" khi không có node nào đổi.
- Đã có Excel/form/công cụ dùng được → đo rồi quyết `REUSE / ADAPT / RETIRE / NEW` cho từng phần; không viết lại toàn bộ vì "sạch".
- Không dựng đường song song (bảng thứ hai, master thứ hai) để tránh sửa cái cũ.
- Mỗi thay đổi P2 gắn một node (`P1-*`/`D*`/`AMD-*`) và một ca kiểm; không có node thì không làm.
- Tài liệu/bảng cũ chỉ retire khi nó có thể làm người/agent đọc sai đời yêu cầu; retire bằng git, không xoá dấu vết.

## 7. Thứ tự đọc cho phiên mới

`CLAUDE.md` → file này → `context/PROJECT_STATE.md` → node cần cho việc (`01` / `DECISIONS` / `P1-REQUEST` / `10` / `11` / `08`) → evidence khi cần.
