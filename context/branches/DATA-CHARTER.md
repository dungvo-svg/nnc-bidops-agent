# Charter nhánh DATA — v1, 02/11/2026

**Cách làm hiện hành:** [../mission/README.md § Cách làm hiện hành từ 02/11/2026](../mission/README.md#cách-làm-hiện-hành-từ-02112026).

**Chủ nhánh:** phiên Claude DATA (con của phiên cha `a5ab430d`). **Người quyết nghiệp vụ:** Dũng / chủ nguồn theo `requirements/11-ROLE-AUTHORITY-MAP.md`. Đọc luật chung ở [README.md](README.md).

## Mục tiêu

Giữ phiên bản nguồn, từ điển dữ liệu, delta, tên gốc Unicode (Lào), truy ngược và **bảo toàn workqueue L:U**. Đưa Kom về cùng schema/nhóm/quy trình catalog chung như các BV khác, giữ nguồn thô và cổng mapping chưa giải. Nhận quyền chủ dữ liệu sau v4 (cloud writer đã dừng ghi).

## Nguồn (chỉ đọc) và hash

| Nguồn | SHA256 |
| --- | --- |
| `outputs/company-continuation-20261102/v4-final/THAU-BV-DU-LIEU-HOP-20261102-v4.xlsx` (baseline nội bộ, 4.191 bản ghi / 5.743 dòng nhu cầu / 6 BV) | 5ad8537dc50dc2a0746b328c34bdfb9da8c3a413e2f1a606871ed5985401faba |
| `outputs/company-continuation-20261102/v4-final/BIDOPS-DATA-DICTIONARY-LINEAGE-20261102-v4.md` | 0d4bb9b46c9611cc32e00c34bcb118740f29efc8e2d9bf3b77f4cca7972501b2 |
| `outputs/company-continuation-20261102/CURRENT-OUTPUTS.json` (pointer owner) | b46509a7933fc2e3a827dbdffbdfdab8e039dc2ced25ef63bfc1d2282e021a4d |
| `D:\DUNG\Foudry\work\company-home-convergence-20261101\cty-intake-20261102\CURRENT-OUTPUTS.json` (pointer CTY) | 6742820978bb46e31225515cff4cc9199c3834ff5b8a95e506306b54c8940550 |
| `C:\Users\Admin\Documents\Codex\2026-11-02\task\mtp-bridge-20261102\MTP-VERIFIED-SOURCE-BRIDGE-20261102.json` (1.145 anchor MTP) | ec45f7886173a8c6e8a6328b5787a7ef752612dae5c5203df94241fe1b648625 |
| `outputs/company-continuation-20261102/v3-v5/BIDOPS-TODAY-WORKING-LIST-20261102.md` | a542e7f8c4ee1f13a32138f46a2c093edf2dcd3ddcb12ba1e30afb0da585e20c |
| Pipeline hiện có (chỉ đọc): `D:\WORK\Agent\Agent-first\personal-meeting-assistant\.local\projects\thau-bv-nnc\work` (kom/, kom_*.py, SCHEMA.md, build_master.py, match_build.py) | ghi hash từng tệp khi đọc |
| Kom gốc F02 (6 sheet), dưới `sources/whatsapp/originals` theo `sources/inventory.json` | 1b12de819834d58c16355fe99abd8b4a18ced2757cda90cb041d71ecc5ce9692 |

Sự kiện đã có (không đếm lại để "xác nhận" nếu không cần): Kom 1.455 dòng nhu cầu; "List 2027 " A:D không có số lượng (để trống, không phải 0); hai sheet danh bạ 27 BV **không phải nhu cầu**; "Gia NNC 2027" có 202 ô #N/A cache và tham chiếu ngoài — không refresh, không suy hiệu lực giá; giá Kom là giá thầu 2026 lịch sử, không phải quote hiện hành. Nhóm Kom: II thuốc 1.067 · I dịch truyền 49 · III hóa chất 88 · IV vật tư 235 · VII lọc máu 14 · VI giấy/gel siêu âm 2. **1.439 dòng có hướng nhóm ban đầu; 16 dòng nhóm lẫn cần xem từng dòng.** Không giữ cả bộ Kom chưa chuẩn hóa chỉ vì 16 dòng này.

## Phạm vi ghi

- Ghi: `data-work/data-branch/` (bản sao làm việc, script) và `outputs/data-branch/<phiên-bản>/` (kết quả). Mỗi phiên bản thư mục mới (v1, v2…), không ghi đè.
- Không sửa: v4 workbook, pipeline PMA, `sources/`, bản dictionary cũ, Drive thầu. Không dựng lại workqueue từ CSV cũ; không tạo database thứ hai làm master.

## Việc theo thứ tự

1. **16 dòng Kom nhóm lẫn:** tự đọc nguồn, so với quy ước catalog chung (Thuốc/HC/VT; dịch truyền thuộc thuốc; lọc máu tách lọc/catheter/kim AVF (VT) và dung dịch/hóa chất; Echo Paper và Echo Gel phân loại riêng). Đề xuất nhóm từng dòng kèm lý do + bằng chứng (sheet/hàng/raw text). Chỉ đưa lên Dũng các dòng thật sự không tự quyết được, dạng câu hỏi ngắn.
2. **Schema Kom → catalog chung:** bảng ánh xạ trường Kom (73 trường intake) → schema nhu cầu chung (nhóm, tên gốc, quy cách, ĐVT, SL, nguồn, alias `KOM-<row>` chỉ là alias intake). Tách chuẩn hóa chính tả/spec/ĐVT khỏi ghép cùng sản phẩm. Crosswalk tường minh, có trạng thái quyết định.
3. **Khoảng trống importer L:U:** chứng minh bằng đọc mã pipeline hiện có rằng chưa có bước nhập lại L:U đã sửa (phạm vi hẹp, không kết luận cho mọi công cụ). Đề xuất cách nhập lại an toàn (diff theo khóa dòng, giữ lịch sử, không ghi đè thủ công). Chưa cài vào pipeline PMA.
4. Hàng đợi rà soát: 4 dòng trùng tên khác ĐVT (Strepsil, Diluent 20L, 2 Syphilis Rapid Test), 6 nhóm trùng tên+ĐVT nội bộ Kom (17 dòng), 5 dòng thiếu ĐVT — đề xuất, không xóa.

## Đầu ra (đường cố định)

`outputs/data-branch/v1/`: `KOM-MIXED-16-PROPOSAL.md` (+ `.csv`), `KOM-SCHEMA-CROSSWALK.md` (+ `.csv`), `LU-IMPORTER-GAP.md`, `KOM-REVIEW-QUEUES.csv`, `DATA-RECEIPT.json` (nguồn+hash đọc, tệp ghi+hash, lệnh/kiểm, số đếm có grain, unknown, câu hỏi cho Dũng nếu có, bước tiếp).

## Kiểm

- Mọi số đếm ghi grain và cách đếm; tổng khớp nguồn (1.455 = 1.439 + 16; 5.743 dòng nhu cầu không mất dòng nào).
- Tên Lào/Unicode giữ nguyên byte; không gộp hai Syringe 50ml đầu nhỏ/đầu lớn.
- Hash v4 và nguồn trước/sau không đổi.
- Không có đề xuất nào được ghi là đã duyệt.

## Bước tiếp sau v1

Báo phiên cha; phiên cha tích hợp và quyết bước kế (áp crosswalk vào bản dữ liệu chung có kiểm soát, cung cấp dữ liệu cho nhánh HỌP).
