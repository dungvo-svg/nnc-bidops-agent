# Charter nhánh PHƯƠNG ÁN (Tender implementation) — v1, 02/11/2026

**Cách làm hiện hành:** [../mission/README.md § Cách làm hiện hành từ 02/11/2026](../mission/README.md#cách-làm-hiện-hành-từ-02112026).

**Chủ nhánh:** phiên Claude PHƯƠNG ÁN (con của phiên cha `a5ab430d`). **Người quyết nghiệp vụ:** CEO/Dũng và người có quyền theo case. Đọc luật chung ở [README.md](README.md). Phạm vi: gói thầu bệnh viện (Lite). **SPM ngoài phạm vi.**

## Mục tiêu

Đưa Lite v6 từ thiết kế sang một vòng thật **nhận việc → làm → trả → dùng** có bằng chứng, trên Drive/Claude Team với công cụ đã có, không dựng runtime mới. Chọn một case nhỏ có offer sẵn, có đầu mối phối hợp và so giá được. Giữ ranh giới duyệt nghiệp vụ.

## Nguồn (chỉ đọc) và hash

| Nguồn | SHA256 |
| --- | --- |
| `outputs/company-continuation-20261102/lite-v6-dictionary-v1/BIDOPS-THAU-LITE-NGUOI-AGENT-20261031-v6.md` (§3–4, §7, §9) | c488a5966aa40fabc74a165a29ab64fce80cee8e70f86cb4637f1f7cb014b458 |
| `outputs/company-continuation-20261102/v3-v5/BIDOPS-BRIEF-DUNG-20261102.md` | b4f8eab505e05938ea317e2bbf92d798e5d51695fefa8613ed11d3f121f3a5ed |
| `outputs/company-continuation-20261102/v3-v5/BIDOPS-TODAY-WORKING-LIST-20261102.md` (VT-0006, TH-0005, TH-0014…) | a542e7f8c4ee1f13a32138f46a2c093edf2dcd3ddcb12ba1e30afb0da585e20c |
| v4 workbook (chỉ đọc; dòng của case được chọn) | 5ad8537dc50dc2a0746b328c34bdfb9da8c3a413e2f1a606871ed5985401faba |
| `requirements/11-ROLE-AUTHORITY-MAP.md`, `requirements/DECISIONS.md` | ghi hash khi đọc |
| Pilot synthetic đã có (mission/packet/RETURN_UNVERIFIED): `data-work/pilots/bidops-b-next-20261101/` (125→153 test L1) | xem `receipts/WORK-RECEIPT.md` |

## Phạm vi ghi

- Ghi: `outputs/phuong-an/<phiên-bản>/` và `data-work/phuong-an/`. Phiên bản thư mục mới, không ghi đè.
- Được đọc Drive/Claude Team bằng công cụ đã kết nối, **chỉ đọc**. Không upload/sửa Drive thầu, không tạo thư mục/quyền Drive, không gửi tin/email cho người hay NCC. Soạn request sẵn; việc gửi thật cần chỉ dẫn cụ thể của Dũng cho đúng người/kênh.
- Không sửa code pilot (thuộc phiên cha); có thể đề xuất.

## Việc theo thứ tự

1. **Kiểm mạng người nhận (chỉ đọc):** từ nguồn hiện có, lập danh sách đầu mối theo case (person_id, vai theo case, kênh, bằng chứng phân công). Phân biệt *đã xác minh / có nguồn nhưng chưa xác nhận / chưa phân công*. Kiểm Drive/Team có gì đọc được; không đoán link, không tạo.
2. **Chọn case nhỏ:** ứng viên VT-0006 (Catheter Foley 2 Way 16, 5 BV, có báo giá Sunshore/Henan Bide) theo Lite §6; so với TH-0014/VT-0035 nếu VT-0006 không đủ điều kiện. Tiêu chí: có dòng nguồn, khoảng thiếu rõ, người giữ nguồn, phạm vi chia sẻ được phép.
3. **Gói request đầy đủ cho case:** bản ghi tối thiểu Lite §4 (gói BV/dòng nhu cầu, biến thể/UOM/lượng theo BV, offer + tiền tệ/phần bao gồm–loại trừ/hiệu lực, người phối hợp/phần nhận, câu hỏi mở, phiên bản). So giá theo Lite §5 (cùng hàng/UOM/tiền tệ/thuế/cước/thời kỳ; không "rẻ nhất", không ngưỡng tự đặt).
4. **Vòng chạy thử trong quyền hiện có:** dùng chính máy/phiên của Dũng (owner duy nhất đã có) để chạy request→reply→dùng ở mức Drive-first, ghi bằng chứng từng bước (issued/received/accepted/returned/used, không nhảy bước). Nếu cần người nhận thật mà chưa có endpoint/quyền: dừng đúng bước, ghi blocker và hỏi Dũng câu cụ thể.

## Đầu ra (đường cố định)

`outputs/phuong-an/v1/`: `RECIPIENT-NETWORK.md`, `CASE-SELECTION.md`, `CASE-<mã>-REQUEST.md` (+ JSON theo bản ghi tối thiểu), `PRICE-BASIS-<mã>.md`, `LOOP-EVIDENCE.md`, `PHUONG-AN-RECEIPT.json` (nguồn+hash, tệp ghi+hash, bước đã chạy/blocker, câu hỏi cho Dũng, bước tiếp).

## Kiểm

- Mỗi người/vai có bằng chứng nguồn; không gán người cho đủ sơ đồ.
- Offer NCC tách khỏi cam kết nội bộ; giá lịch sử không thành quote hiện hành.
- "Đã gửi" ≠ "đã nhận" ≠ "đã nhận việc"; im lặng ≠ đồng ý.
- Không hành động bên ngoài nào được thực hiện nếu chưa có chỉ dẫn cụ thể.

## Bước tiếp sau v1

Báo phiên cha; phiên cha quyết case chạy thật với người nhận khi Dũng cấp kênh/người, và chuyển ngữ cảnh cho nhánh HỌP.
