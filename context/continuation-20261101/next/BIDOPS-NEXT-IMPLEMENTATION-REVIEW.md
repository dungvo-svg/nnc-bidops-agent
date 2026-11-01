# BidOps — review bước local tiếp theo (01/11/2026)

**Ba gap vẫn còn; có thể làm tiếp phần synthetic, không cần dựng lại nền tảng.** Đã đọc AGENTS/CLAUDE, `context/PROJECT_STATE.md`, authority graph, P1 và continuity BRIEF/TASK/DECISION-LOG/ROADMAP/PLAN-VS-IMPLEMENTATION. Nhánh này chỉ đọc mã/tài liệu và ghi báo cáo C:, không chạy code project/test, đọc DB/CSV/workbook nghiệp vụ, gọi Claude/relay, tạo receiver hay sửa D:.

## Artifact hiện tại

Owner: `D:\WORK\Agent\Agent-first\NNC BidOps Agent`. Source-only pilot đã có tại `data-work/pilots/bidops-b-next-20261101/`:23 file, không có AGENTS/CLAUDE/context riêng; kế thừa quy tắc project cha.

Receipt `output/readiness-materials/BIDOPS-RELOCATED-BASELINE-RECEIPT.json` ghi Codex host chạy100 tests OK/exit0 tại đúng pilot D: lúc06:32UTC; source unchanged, không copy catalog thật. Không phải Claude Desktop hay chứng minh nhân viên đã dùng. Theo checkpoint parent12:42UTC: original BidOps chưa có receiver, owner repo chưa có HEAD, scaffold/docs untracked — **không phải lỗi Git/build và không chặn thiết kế local**. Audit này không tự kiểm receiver/profile.

## Ba gap có bằng chứng mã

| Gap | File:dòng trong pilot | Hậu quả |
| --- | --- | --- |
| Hai state case chưa nối | `ledger.py:109,298,682–727`; `catalog_lifecycle.py:65–101,175–186` | Ledger dùng `case_state`, catalog dùng `tender_case`. Đóng case trên catalog chưa làm Ledger đang active đổi theo; inquiry và qualify/mission có thể khác kết luận. |
| Helpers chưa nối qualify | `assessments.py:16–50,53–115`; `ledger.py:290–360` | certificate/portfolio chỉ được gọi trong tests helper. Qualify chỉ nhận ba trục goods/documents/money dạng `{ref,source_ref}`, không kiểm nội dung chứng từ/allocation/cost. Có ref không thành có năng lực hay chứng từ đúng. |
| Packet/return chưa có | `workpacks.py:38–63,145–205,209–232` | Có sync/review/cancel/CSV, chưa có export_packet/import_return/RETURN_UNVERIFIED trong src/tests. REVIEWED vẫn owner/agent=null, dispatch/business acceptance=false. CSV không phải hợp đồng giao/nhận. |

Chi tiết mới cần xử lý khi nối:

- **Không dùng chung đường dẫn DB để “đồng bộ”:** `ledger.py:98–100` và `catalog_intake.py:101–103` cùng tạo bảng `events` nhưng schema khác nhau. Cần adapter/namespace, không chồng schema lên catalog.
- Ledger deadline là UTC instant (`:46–50,719–727`); catalog là ngày planning/observed và extension phải muộn hơn (`catalog_lifecycle:90–100`). Không biến ngày planning thành giờ nộp pháp lý; tách extension với correction có bằng chứng.
- `Ledger.link_demand:745–748` chưa đòi won khi nhận fulfillment; catalog `create_fulfillment:148–150` có đòi. Hai bên phải cùng invariant.
- Certificate helper so trade/manufacturer/strength/form/pack, tách bốn trục hạn, chưa so registration ID. Ledger variant là item_code/specification/unit/registration/identity dates (`:631–662`); cần mapping tường minh, không ghép theo generic/MPSC.
- `issue_mission:406–407` đòi quote_ids không rỗng. Không tạo quote giả để dùng mission API cho việc tìm nguồn chưa biết NCC.

## Bước triển khai nhỏ đề xuất

**Contract local tự giải:** cho flow catalog hiện tại đọc một `CaseSnapshot(case_id, version/hash, status, planning_date, official_closing_at|null, evidence_ref)` từ catalog qua adapter. Giữ Ledger history cũ; không dual-write hai bảng như hai authority. Đây là lựa chọn kỹ thuật của pilot, không đổi chủ master công ty.

**Lát1 — packet/return synthetic có đầu ra xem ngay:**

1. Fixture một source row phục vụ case A/B, một dòng độc lập và một identity unresolved. Exporter chỉ đọc catalog fixture; inbox/return receipts ở file riêng.
2. `export_packet(draft_id, expected_hash, out)` chỉ xuất current/REVIEWED/not-cancelled, ghim generation/hash/source anchors/case refs và qualification riêng. JSON exclusive-create, owner UNASSIGNED/null, không dispatch/authority. Một source row dùng chung vẫn giữ hai nghĩa vụ case.
3. File trả fictional đi qua `import_return`: kiểm packet/hash/scope; lưu `RETURN_UNVERIFIED` cùng evidence/blocker/HOLD, claimed_owner/claimed_agent chỉ là claim. Retry nguyên vẹn cùng receipt; ID cũ/payload đổi conflict. Stale/cancel return giữ history-only, không tái kích hoạt case/current draft.
4. Readout hiển thị kết quả trả và phần chưa biết. Không tự tạo mission accepted, candidate approved, apply/use hay ghi master. Quote discovery chưa có quote scope vẫn ở preparation packet.

**Lát2 — nối qualification:** adapter gọi helper bằng typed inputs/source refs, pin kết quả + requirement/quote/variant/case snapshot + ngày đánh giá/schema version vào candidate hash. Source/assessment/case đổi làm bước tiêu thụ cũ stale. Giữ từng blocker và ba trục riêng; không biến helper PASS thành duyệt pháp lý hoặc điểm thắng. Hạn giao cần evaluation basis riêng; portfolio giữ unknown và từng currency, không tự FX/profit/cash.

Packet slice có thể chuẩn bị song song với contract lifecycle, nhưng **packet chạy được không có nghĩa gap lifecycle/qualify đã đóng**. Không cần broker/listener/web/VM hay principal platform để làm các bước này.

## Acceptance lần code tiếp theo — chưa chạy

- Cùng source A/B một packet, hai case qualifications; hai source cùng tên không merge.
- Close A giữ B; close cả hai dừng prebid; reopen tạo scope mới; late return không reactivate. Fulfillment chỉ sau won, quantity null không thành0.
- Consumer cùng CaseSnapshot; stale hash bị chặn; retry giữ history; lỗi giữa chừng không để hai authority khác trạng thái.
- Packet sai hash/ID/scope bị từ chối nguyên tử; export không đè source/inbox/file cũ; duplicate không sinh việc mới.
- Return stale/cancel history-only; claimed CEO/staff/Agent không tạo quyền, ACK thật hay business state.
- Identity/chứng từ thiếu/sai từng trường, bốn loại hạn và hạn đổi sau review đều có blocker đúng; generic giống chưa đủ. Không gọi hết hạn là kết luận pháp lý tự động.
- Hai case tranh stock/xe/cash không double allocation/cost; unknown vẫn unknown, không cộng currency khác nhau. Không auto-approve/apply/master write.
- Giữ regression retry-review/CSV-exclusive/WAL và source hashes.100 baseline tests cũ không chứng minh các API mới đã tồn tại; chỉ chạy lại theo thay đổi thực.

## Tự giải và blocker thật

**Tự giải được:** schema/hash/receipt, CaseSnapshot adapter, idempotency/CAS, date semantics, fixture/tests/error handling, sửa pointer tài liệu khi được giao. Không hỏi Dũng chọn tên class; không lấy TASK audit-only cũ làm gate mới cho phần user vừa giao. Riêng nhánh này chỉ review, không tự dùng báo cáo làm lệnh build.

**Cần trước ca thật/L4 hoặc cam kết thương mại:** D01/owner master/phạm vi người duyệt, HSMT/addenda và hạn chính thức, equivalent/certificate identity, quote/NCC/giá hiện hành, hàng/xe/vốn, principal/kênh thực được phép. CEO vẫn trực tiếp chào hàng; mỗi người giữ máy/Agent của mình. Không tự thêm luật CEO không làm staff hoặc mọi bước phải có người thứ ba.

## Stale docs cần sửa đúng nơi

- Continuation BRIEF/TASK/ROADMAP còn ghi vòng trước audit-only, code chỉ ở C:, chưa có quyết định cài đặt. Không mạnh hơn chỉ dẫn mới; cũng không tự biến business nodes thành LOCKED.
- Source-only pilot đã đặt trong owner `data-work`; đặt file trong project **khác** tích hợp sản phẩm/release/USED.
- README bản copy trỏ AGENTS/CLAUDE/context không được copy, branch Git cũ và `../catalog` như dữ liệu hiện hữu. Sửa về owner context; tách demo synthetic khỏi recipe actual intake cũ. Không mở catalog thật để chữa pointer.
- DATA-CONTRACT #7 nói reviewer principal nhưng là fixture strings; #14 mô tả won→fulfillment mạnh hơn Ledger thực thi. PLAN-VS-IMPLEMENTATION đã nêu, không được coi lời hứa đó là guard đã có.

## Pins của source đã đọc

| File | SHA256 |
| --- | --- |
| src/ledger.py | 3b39bb5efbe05629badbbfde03ad7c2355b6661768fe354df6f14a817b4816f2 |
| src/catalog_lifecycle.py | b6dc9986ac978c93e73ad295638e21929bf35739d2334cfd3f57eac2ed6be15b |
| src/catalog_intake.py | e39f4062dd902b3db4faf37231c929c475331a225e52f3625c6349089bb736f8 |
| src/assessments.py | 0bd8c6a94283b850a18c3ccc63a5af77ee2a138c4c360dedae1cb216712e2dde |
| src/workpacks.py | 1c8e6192bc324b3f5e42d79ac83f2308f0965eef569ca6942aa9875b96c951d4 |

Targeted source review, không scan toàn repo hay kiểm dữ liệu công ty. Không có action denied; không sửa D:, source/master, nghiệp vụ thật hoặc receiver. Parent có thể publish report qua scoped doc write đã được giao; audit này chỉ tạo bản C: để tránh hai writer.
