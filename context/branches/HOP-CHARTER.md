# Charter nhánh HỌP — v1, 02/11/2026

**Cách làm hiện hành:** [../mission/README.md § Cách làm hiện hành từ 02/11/2026](../mission/README.md#cách-làm-hiện-hành-từ-02112026).

**Trạng thái 02/11: ĐÓNG BĂNG.** Dũng bác hướng view HTML; HỌP làm sau DATA và PHƯƠNG ÁN, không chặn hai phần đó. `outputs/hop/v1/` giữ làm lịch sử; không sửa, không thiết kế thêm.

**Chủ nhánh:** phiên Claude HỌP (con của phiên cha `a5ab430d`). Đọc luật chung ở [README.md](README.md). Bắt đầu sau DATA v2 theo chỉ đạo Dũng "Họp sau khi đủ ngữ cảnh".

## Mục tiêu

1. Dùng lại module trợ lý họp có sẵn (**đọc module trước khi dựng gì**) để soạn agenda từ dữ liệu hiện hành, hỗ trợ điều phối họp, tóm tắt sự kiện/quyết định, theo dõi việc có nguồn và người giữ.
2. Tạo **một view họp có phiên bản** từ cùng một dữ liệu: tên hàng/quy cách → nhu cầu từng BV → nguồn/giá (nhãn rõ: giá cũ / mới / tham chiếu, không chỉ bằng màu) → vấn đề → xác nhận/bước tiếp. Mã là phụ. View **không** thành nguồn nhập thứ hai, không nhiều sheet ghi chú. Raw/provenance/alias/ID nằm ở phần drilldown của cùng dữ liệu.

## Nguồn (chỉ đọc) và hash

| Nguồn | SHA256 / ghi chú |
| --- | --- |
| `outputs/data-branch/v2/DEMAND-COMMON-DERIVED.csv` (5.743 dòng nhu cầu, Kom cùng schema; khóa `demand_key`) — **nguồn dữ liệu chính của view** | ghi hash khi đọc; receipt `outputs/data-branch/v2/DATA-RECEIPT.json` |
| v4 workbook (giá, báo giá, nhóm việc theo bản ghi) | 5ad8537dc50dc2a0746b328c34bdfb9da8c3a413e2f1a606871ed5985401faba |
| `outputs/data-branch/v1/` (đề xuất 16 dòng, hàng đợi), `outputs/phuong-an/v1/` (case VT-0006, căn cứ giá, mạng người nhận) | ghi hash khi đọc |
| `outputs/company-continuation-20261102/v3-v5/BIDOPS-TODAY-WORKING-LIST-20261102.md`, brief v5 | a542e7f8…, b4f8eab5… |
| Module họp hiện có: `D:\WORK\Agent\Agent-first\personal-meeting-assistant` (đọc README/cấu trúc trước; `.local/projects/thau-bv-nnc` chỉ đọc) | ghi hash các tệp đã dùng |
| Mẫu trình bày cũ trên Drive thầu BV (chỉ đọc): thư mục `1IUDLUmc-xC1O_dJpMeRJJQN5qvR-RMy_`; tệp vt `1_Vmfsd03b83FGSHrXDcKmGja38WeTrQB`, hc `1vbg9u-ybXUGjNA_8Njd8p2oIMIbYpwGx`, thuoc `1YRBQnoPSmW7zQtRhJB9OW-Vq43l2FpbV` (sheet "Tim nguon - Tinh gia", "Danh muc chung/Tong hop") | đọc để học cách đặt tên/hành động/provenance; **không chép 21 cột rộng, hạn cũ, loại trừ 5 BV cũ** |

## Phạm vi ghi

- Ghi: `outputs/hop/<phiên-bản>/` và `data-work/hop/`. Phiên bản thư mục mới, không ghi đè.
- Không sửa module họp/PMA, không ngừng dùng làn họp cũ khi chưa kiểm thừa kế đủ dữ liệu/code/context/hash/điểm tiếp tục; không xóa nguồn cũ hay runtime PMA.
- Không upload Drive, không gửi lời mời/biên bản cho ai, không tạo lịch họp.

## Việc theo thứ tự

1. Đọc module họp hiện có, ghi cái gì tái dùng được (agenda, tóm tắt, theo dõi việc) và cái gì thiếu.
2. Đọc mẫu Drive (chỉ đọc), ghi ngắn điều học được.
3. Dựng view họp v1 từ `DEMAND-COMMON-DERIVED.csv` + v4 + kết quả PHƯƠNG ÁN: lọc BV / Thuốc-HC-VT / bước tiếp; Kom cùng cách trình bày; cộng SL chỉ khi cùng biến thể + ĐVT đã có căn cứ, còn lại hiện theo từng BV; Kom không có SL thì để trống. Phân biệt: yêu cầu BV / dữ kiện NNC nhập / trường dẫn xuất. Chưa phân công thì để chưa phân công. Phần "AI làm gì" chỉ là phụ lục ngắn.
4. Agenda họp mẫu từ view (việc theo nhóm 1/2/3, câu hỏi cần quyết: Q1 dung dịch lọc máu, người nhận VT-0006, X3 cột GM…), kèm khung theo dõi việc: mã → phần thiếu → người giữ nguồn → việc tiếp → hạn.
5. Kiểm render và các ca: VT-0014, VT-0100, TH-0166, một dòng Kom giá lịch sử, Nicox/NICOVEX, hai Syringe 50ml tiếng Lào khác nhau. Kiểm phủ alias/dòng, provenance giá.

## Đầu ra (đường cố định)

`outputs/hop/v1/`: `MODULE-REUSE.md`, `DRIVE-SAMPLE-NOTES.md`, view họp (một tệp, ví dụ `HOP-VIEW-v1.xlsx` hoặc `.html`, ghi rõ chỉ đọc + thời điểm dữ liệu), `AGENDA-v1.md`, `CASE-CHECKS.md`, `HOP-RECEIPT.json` (nguồn+hash, tệp ghi+hash, kiểm/kết quả, giới hạn, câu hỏi cho Dũng, bước tiếp).

## Kiểm

- Tổng dòng trong view truy được về 5.743 `demand_key`; không mất/không nhân dòng.
- Không có giá nào được gọi là quote hiện hành nếu nguồn là lịch sử; nhãn giá bằng chữ.
- Tên Lào giữ nguyên; hai Syringe 50ml riêng.
- Không có thông tin giá vốn đi ra ngoài máy/công ty.
