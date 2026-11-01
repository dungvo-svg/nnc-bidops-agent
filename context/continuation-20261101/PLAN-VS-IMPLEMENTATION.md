# Đối chiếu phương án A với code B

> Bản audit/plan đã được Codex đối chiếu độc lập và lưu vào project ngày 01/11/2026. Claude Opus tổng hợp, Sonnet kiểm hai nhánh. Các nhãn draft/đề xuất trong nội dung là trạng thái quyết định, không có nghĩa file còn ở ngoài project. Chưa thay runtime, tích hợp code, merge hay deploy. Chi tiết nguồn/giới hạn: SOURCES-READ.json và PUBLICATION-RECEIPT.json.


**Pilot:** `C:\Users\Admin\Documents\Codex\2026-10-31\task\output\bidops-B-pilot-20261031\project`, commit `aac3e9428084…`.

## Kết quả đọc thân hàm (01/11/2026, vòng 2)

Sonnet `scope-audit-sonnet` đọc toàn bộ thân hàm `ledger.py`, `assessments.py`, `catalog_lifecycle.py`, `workpacks.py`. Opus đọc tại chỗ `ledger.py` dòng 534–591 và 703–761 để xác nhận các điểm đánh dấu (✓).

Mức FULL / PARTIAL / ABSENT dưới đây là mức **hiện thực ở L1 synthetic**, không phải mức đã kiểm chứng nghiệp vụ.

| Yêu cầu (A8) | Mức | Bằng chứng (file:dòng) và khoảng trống |
| --- | --- | --- |
| R1 Năm phép kiểm nghiệp vụ tách riêng | **ABSENT** như đối tượng riêng | `qualify` (L:290-360) chỉ có blockers và 3 trục. `certificate_check` (A:16-50) và `portfolio_check` (A:53-115) là hàm thuần, chưa nối vào `qualify`. Không có đối tượng cho hồ sơ, vốn lưu động, căn cứ cạnh tranh, kết quả |
| R2 Phạm vi phê duyệt tách riêng | PARTIAL | Có 3 capability synthetic review/apply/use. Review bắt buộc khác proposer (L:543 ✓). `_promote` không kiểm quan hệ actor (L:555-568 ✓). Chưa có phạm vi cho giá, tương đương, NCC, nộp. **Không suy ra** quy định chung "apply/use phải do người khác". Ai được tách việc phải theo thẩm quyền thật của từng phạm vi, không tự đặt ra 3–4 người duyệt |
| R3 Ba trục hàng/chứng từ/tiền | PARTIAL | Bắt buộc có đủ 3 khóa (L:294-318). Mỗi trục chỉ ghi "có ref hay không", không kiểm nội dung |
| R4 Node = người + Agent của họ; CEO không điều khiển Agent/máy người khác | PARTIAL | Actor được so với cấu hình tĩnh (L:150-161). `receive`/`return` gắn đúng owner node (`_owned_mission`). `catalog_lifecycle`/`workpacks` dùng nhãn tự khai (CL:114-118, W:153). CEO **vẫn trực tiếp chào hàng** kể cả khi có staff (U-31A), nên không đặt luật "CEO không làm việc staff". Khoảng trống thật là **actor chưa phải principal đã xác thực** — đây là ranh giới kỹ thuật trước production, không phải policy công ty |
| R5 received/accepted/produced/used; `used` do bên tiêu thụ ghi | PARTIAL | Chuỗi trạng thái đúng. `consume_diagnostic` bắt buộc owner khác proposer (L:585 ✓). `use_candidate` không kiểm bên ghi có phải bên tiêu thụ hay không (L:573 ✓). Ai là bên tiêu thụ cần xác định theo case thật |
| R6 Idempotency, payload đổi bị từ chối | FULL (ledger) | `_event` băm cả actor (L:163-188). CL:36-62 không băm actor. `workpacks` nhận legacy checksum. Retry trả receipt trước khi authorize (không side effect) |
| R7 Biến thể chính xác, không join theo MPSC | FULL (bảo thủ) | `_variant_for` L:673-680, `variant_mismatch` L:329. Ledger và catalog có hai kho định danh riêng, chưa có cầu nối |
| R8 Nguồn đổi làm vô hiệu phần phía sau | PARTIAL | `_assert_sources_current`/`_assert_requirement_current` được gọi ở các bước chính. Quote không có head/supersede |
| R9 Demand lifecycle | PARTIAL | Có close/cancel/reopen/win, extension, overdue_unknown, tách prebid/fulfillment. **Hở:** ledger `link_demand` nhận `fulfillment` khi case chưa `won` (L:747 ✓). `set_case_deadline` cho lùi ngày (L:719-726 ✓), trong khi CL:96-97 buộc ngày mới phải muộn hơn. Ledger và CL là **hai chủ trạng thái case** |
| R10 Danh tính chứng từ ≠ generic; các hạn tách nhau | PARTIAL | `certificate_check` tách định danh khỏi 4 trục hạn. Chưa so số đăng ký; hạn tính theo ngày hôm nay, không theo ngày giao; chưa nối `qualify` |
| R11 Dùng chung năng lực, không cộng trùng chi phí | PARTIAL | Dedup theo id (A:57-60, 91-95). Chưa có chiều gói/thời gian. Cùng cam kết thật mà khác id sẽ bị tính hai lần. Thiếu khóa thì `KeyError` (A:92) |
| R12 Offline/lease/backpressure/correction | ABSENT (trừ cancel) | `cancel_mission` L:467-480. STATE-MAPPING:18 tự ghi các gap |
| R13 Xác thực sender trước side effect | ABSENT | Actor do bên gọi truyền vào (STATE-MAPPING:12) |
| WIP1 | Có, cục bộ | Chỉ ở `respond_mission` L:457-462, trong `BEGIN IMMEDIATE`. Nhận nhiều `received` vẫn được. Đây không phải backpressure |

**Nói quá trong tài liệu pilot (đề xuất Codex sửa tài liệu, chưa sửa code):**
- DATA-CONTRACT #7 ghi "reviewer principal", nhưng code chỉ lưu actor tự khai.
- DATA-CONTRACT #14 ngụ ý fulfillment chỉ có sau khi trúng thầu. Ledger không kiểm điều này.
- Kết quả `REVIEWED` của workpacks và "explicit local reviewed receipt" của CL chỉ là nhãn tự do.

100 test là L1 kỹ thuật (STATE-MAPPING:14), **không phải** kiểm chứng nghiệp vụ.

**Các cột trạng thái** (ghi tách nhau):

| Cột | Nghĩa |
| --- | --- |
| IMPL | Đã có code |
| TEST | Đã test local. L1 = fixture synthetic |
| INTEG | Đã tích hợp vào project owner |
| REL | Đã release |
| USED | Đã có người thật dùng |

**Nguồn TEST:**
- "Codex": lượt chạy 100/100 theo receipt của Codex.
- "smoke": smoke 1/1 do Claude chạy ngày 01/11, không có receipt riêng ngoài `SMOKE-RESULT.json`.

**Tên hàm** lấy từ grep `def` ngày 01/11. Chỉ đọc thân hàm của `workpacks.py` và `catalog_lifecycle.py`.

## Năng lực lõi

| Yêu cầu trong A8 / manifest B | Hàm trong B | IMPL | TEST | INTEG / REL / USED |
| --- | --- | --- | --- | --- |
| Nguồn có version và hash, idempotent | `ledger.Ledger.intake_source`, `four_bv_intake.import_four`, `catalog_intake.import_csv` | Có | L1, Codex | Không |
| Quote gắn đúng một biến thể; không join theo MPSC | `Ledger.intake_quote`, `Ledger.intake_variant`, `Ledger.qualify` | Có | L1, Codex | Không |
| Ba trục bằng chứng hàng–chứng từ–tiền; không tự động duyệt | `Ledger.qualify` | Có (synthetic) | L1, Codex | Không có dữ liệu thật |
| Mission có owner: issued / received / accepted / needs_input / rejected / returned / cancel | `Ledger.issue_mission`, `receive_mission`, `respond_mission`, `return_mission`, `cancel_mission` | Có | L1, Codex | Không. Actor chỉ là chuỗi trong fixture |
| WIP1 (một việc đang làm mỗi lúc) | Theo `docs/STATE-MAPPING.md:6` nằm trong `respond_mission`; Claude chưa đọc thân hàm, cần Codex chỉ file:dòng | Theo tài liệu | L1, Codex | Không |
| reviewed → applied → used; `used_in_candidate` cho HOLD | `Ledger.review_candidate`, `apply_candidate`, `use_candidate`, `consume_diagnostic` | Có | L1, Codex | Không |
| Demand lifecycle: close / reopen / extension / WON → fulfillment | `catalog_lifecycle.transition_case`, `extend_deadline`, `plan_closure`, `create_fulfillment`, `finish_fulfillment`; `Ledger.link_demand`, `finish_demand` | Có | L1, Codex | Không |
| Một inquiry cho mỗi dòng nguồn; qualification từng case giữ riêng | `catalog_lifecycle.source_worklist`; `workpacks.WorkpackInbox.sync/review/cancel/export_csv` | Có | L1, Codex + smoke | Ngày 31/10 Codex chạy read-only trên catalog thật: 3.523 DRAFT, 0 review. **Không phải** INTEG hay USED |
| Ba lỗi đã vá | Retry review: `WorkpackInbox.review`. CSV: `export_csv` mở `'x'`. Guard WAL: `workpacks._catalog_signature` | Có | Codex 100/100; smoke chỉ kiểm hai lỗi đầu | Không |
| Kom 1.455 dòng, giữ unresolved, Omesod là exception | `catalog_intake.import_csv` + catalog thật | Có (intake) | L1, Codex | Codex đã nạp read-only; 0 identity complete (receipt) |
| Locator theo parser index có nhãn | `four_bv_intake.import_four` (Claude chưa đọc thân hàm) | Một phần | L1, Codex | Hash XLSX gốc của bốn BV chưa biết |
| Envelope; xác thực sender và scope trước side effect | — | **Chưa** | — | — |
| Listener liên owner, offline, lease, backpressure | — (STATE-MAPPING mục "Remaining runtime gaps") | **Chưa** | — | — |
| Xuất packet / nhận return tự xưng | — | **Chưa**, chỉ đề xuất | — | — |
| Quote discovery khi chưa khai báo phạm vi quote | — | **Chưa** (ngoài core) | — | — |
| Giá theo tuyến, landed cost, SVNK giao nhiều điểm | — | **Chưa** | — | — |

## Năm phép kiểm nghiệp vụ (A8 §2)

Năm phép kiểm này tách khỏi ba trục bằng chứng và khỏi các phạm vi phê duyệt.

| Phép kiểm | Hỗ trợ trong B | IMPL | TEST | INTEG / REL / USED |
| --- | --- | --- | --- | --- |
| Đáp ứng hồ sơ | `assessments.certificate_check` (danh tính chứng từ, các loại hạn tách nhau) | Một phần, synthetic | L1, Codex | Không. Chưa có HSMT, chưa tra registry |
| Khả năng cung ứng | `assessments.portfolio_check` (nguồn lực chung, không cộng trùng chi phí) | Một phần, synthetic | L1, Codex | Không có dữ liệu kho/xe/tiền |
| Kinh tế / vốn | — | **Chưa** | — | — |
| Căn cứ cạnh tranh | — | **Chưa** | — | — |
| Kết quả thực hiện | `create_fulfillment` / `finish_fulfillment` (chỉ vòng đời nhu cầu sau trúng) | Một phần | L1, Codex | Không có giao/thu tiền thật |

Không có view gộp điểm. Đây là chủ ý theo A8.

## Mức bằng chứng

| Mức | Nội dung | Tình trạng |
| --- | --- | --- |
| L1 | Fixture synthetic | **Có** |
| L2 | Hai process local | Chưa có receipt riêng cho BidOps |
| L3 | Hai máy, cùng một owner | Chỉ là lab lịch sử về cơ chế chung, được nhắc ở `docs/STATE-MAPPING.md:14`. **Chưa kiểm lại artifact L3 trong audit này.** Không tính vào mức hiện tại của BidOps, không thay L2 |
| L4 | Hai owner thật | Không |
| L5 | Nghiệm thu nghiệp vụ | Không |

## B còn thiếu so với phần cốt lõi của A

1. Một vòng người + Agent thật: nhận, làm, trả, dùng.
2. Dữ liệu hàng–chứng từ–tiền thật trên các dòng được chọn chào.
3. HSMT chính thức.
4. Kinh tế/vốn và căn cứ cạnh tranh.
5. Danh tính, kênh và quyền.
