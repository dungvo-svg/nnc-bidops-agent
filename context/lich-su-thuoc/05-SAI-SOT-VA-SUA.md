# 05. Sai sót của Agent và cách sửa

Mỗi mục ghi: sai gì, ai phát hiện, nguyên nhân, đã sửa thế nào, bài học. Nguyên nhân đánh dấu "(suy)" là suy ra, nguồn không nói thẳng.

## A. Thiết lập và tổ chức (30/10 – 09/11)
1. **Dùng plugin/skill cũ thay vì bản main R2.**
   - Phát hiện: Dũng ("khoan bạn đang lấy plugin cũ sao?", 30/10).
   - Nguyên nhân: lẫn lớp ghế từ skill cục bộ bản cũ.
   - Sửa: ghim OSER R2 `94ddf8b` tại `.claude/vendor/`.
   - Bài học: trước khi áp skill hay plugin, kiểm đó là bản nào.
2. **Thiếu hệ thống tài liệu khóa khi thiết lập; không nhớ P1/P2 đặt ở đâu.**
   - Phát hiện: Dũng, 30/10.
   - Sửa: thêm authority graph, DECISIONS, LOCK; ghi đường dẫn nguồn chuẩn vào CLAUDE.md.
3. **Gửi dữ liệu cho nhánh nghiên cứu theo lô nhỏ ("sao gửi 6 mấy vậy?").**
   - Phát hiện: Dũng, 03/11.
   - Bài học: phần data đã xong thì gửi đủ, không nhỏ giọt.
4. **Kom bị chẻ riêng, thêm lớp phân loại thừa, có nguy cơ mất tên gốc Kom khi map.**
   - Phát hiện: Dũng, 04–05/11.
   - Sửa: gộp Kom như một bệnh viện, chỉ giữ 2 sheet, giữ chữ nguyên văn.
   - Bài học: không tạo lớp phân loại không giúp tìm hàng.
5. **Viết cho người trong dự án thay vì người đọc.** Ghi tắt "… và 2 mã khác", tiêu đề chỉ tiếng Lào cho chị Trang (người Việt), ký hiệu cột X/Y, lời gửi lẫn người không liên quan.
   - Phát hiện: Dũng, 05/11, 9 lần.
   - Sửa: song ngữ, liệt kê đủ.
   - Bài học: đọc lại bằng mắt người nhận.
6. **Nhầm tiền tệ: gắn giá mua VND thành kíp do đoán theo độ lớn số.**
   - Phát hiện: Dũng, 05/11, 5 lần.
   - Sửa: lấy tiền tệ theo công thức trong file nguồn, giữ tiền gốc.
   - Bài học: không đoán tiền tệ theo số.
7. **Ô "0" làm 142 dòng bị xếp nhầm.**
   - Bài học: trống ≠ 0 ≠ chưa xác nhận (D12).
8. **Báo đã nộp/đã xong mà chưa vá file chung gốc** ("update cho file chung gốc chưa?", 05/11).
   - Bài học: vá đúng ô trên file chung rồi mới báo xong, kèm "ở đâu, đã kiểm gì".
9. **Dữ liệu tràn lan:** giá Kom nằm ≥7 nơi, chuyển xlsx↔gsheet sinh thêm bản, runtime lẫn vào file hợp nhất, bản lock chỉ có ở máy Dũng.
   - Phát hiện: Dũng nêu ngày 09/11.
   - Sửa (đề xuất): mỗi gói một bản thể, một đầu ghi (D20 PROPOSED).
10. **Chưa có hồ sơ Agent và quy trình sau nhiều ngày làm** ("tôi chưa thấy Hồ sơ Agent và Quy trình", 09/11).
    - Sửa: viết `KINH-NGHIEM`, `KHUNG-AGENT` ngày 09/11.

## B. Gộp giá và kiểm giá KOM (10/11 – 11/11)
11. **Hội tụ 10/11 có 5 lỗi quy tắc:**
    - coi tab "Tar Bổ sung" là nguồn độc lập (thực ra là bản sao tab Trang);
    - tự ghi ĐVT giá = ĐVT thầu khi ô trống;
    - chọn giá theo ô thay vì theo khối, nên sinh dòng lai;
    - không kiểm hàng chào so với yêu cầu;
    - lẫn "người phụ trách" với "giá của ai".

    Phát hiện: câu "copy cái cũ c Trang…" của chị Tar, sau đó Agent điều tra (146 mã, 93 mã không nguồn). Sửa: chặn rồi xử lý từng nhóm.
12. **Tick "giá qua đủ kiểm tra" theo vòng lặp.** Tiêu chí "ĐVT khớp" dựa trên ô do chính hội tụ tự điền.
    - Phát hiện: Agent tự phát hiện, mở lại 36 dòng.
    - Bài học: tiêu chí kiểm không được dựa vào dữ liệu do chính mình sinh ra.
13. **Tự quy đổi giá 13 mã của anh chị.**
    - Phát hiện: Dũng ("sao lại quy giá? mình sửa giá của anh chị hả?", 11/11 22:39).
    - Sửa: trả về số cũ, ghi memory "không sửa giá".
    - Bài học: quy đổi tương đương là việc của người chuyên môn.
14. **Mở rộng phạm vi quá xa** ("sao giờ đi xa vậy"). Câu hỏi chỉ là "hàng của Tar hay Trang", Agent lại rà đơn vị và hoạt chất rồi chặn hàng loạt.
    - Bài học: trả lời đúng câu hỏi trước; muốn mở rộng thì hỏi 1 câu.
15. **Lấy sai ảnh:**
    - Fengshi OPC, KOM-1048 VG-5, KOM-167/84/153/976;
    - 134 ảnh AI phải gỡ ngày 10/11;
    - lọc ảnh chỉ theo mã nên sót các dòng cùng hàng chào đã có ảnh.

    Bài học: nhìn tên hàng, đừng nhìn mã.
16. **Cột người phụ trách sai chủ.** Quy tắc "tab Tar Bổ sung → Tar" làm hàng chị Trang mang tên chị Tar (5 + 22 mã, KOM-657).
    - Phát hiện: chị Tar ("của Trang update lại nhé"), sau đó đến Dũng (KOM-657, 12–13/11).
    - Bài học: đối chiếu file của chính người đó trước khi quy chủ.
17. **Lỡ bấm nút Gemini "Tóm tắt dữ liệu này" trên Report.**
    - Sửa: đã dừng, xóa ô tạm.
    - Bài học: chụp màn hình trước khi bấm gần góc phải thanh công cụ.

## C. Thông tin hàng, form chị Oanh (12/11)
18. **Hiểu nhầm tin chị Oanh (08:53–09:01) là tin chị Trang.** Agent tự đính chính lúc ~09:15.
19. **Không hỏi sớm thông tin thiếu.** Coi các ô thông tin (thành phần, quy cách, NSX, nước) là "không cản kiểm giá" nên không đưa vào Report; chỉ đọc 2 khối cột trong file nguồn nên tìm sót.
    - Phát hiện: Dũng: "TÌm không ra hả", "sao ban đầu bạn ko hỏi luôn", "sao thông tin hqua đâu đề cập…". Có 19 mã lòi ra hôm sau.
    - Sửa: điền từ file chị Trang và các dòng cùng hàng; thêm kiểm ô trống vào Report.
    - Bài học: kiểm đủ thông tin cùng lúc với giá, gom câu hỏi hỏi một lần ngay.
20. **Báo cáo bỏ sót mã anh Duy** ("sao không nhắc hàng anh Duy?", 12/11 20:39).
    - Nguyên nhân:
      - báo cáo hôm trước không có mục kiểm đủ thông tin;
      - quy chủ theo cột F;
      - tin giao việc chỉ nêu mã chị Trang.
    - Sửa: báo cáo 22h40 liệt kê đủ mọi người phụ trách (KOM-91, 213).
    - Bài học: báo cáo phủ mọi người phụ trách, kể cả ca nhỏ.
21. **Điền nước theo xuất xứ hãng (India, France) thay vì nguồn nhập.**
    - Phát hiện: Dũng ("nguồn là nguồn nhập chứ không phải xuất xứ", "đừng ngây thơ vậy").
    - Sửa: đưa các mã thuocsi về Vietnam; ghi memory.
    - Bài học: xem cột nhà cung cấp và cách anh chị ghi ở dòng cùng nguồn.
22. **Ghi nhầm vào cột ẩn.** Name box nhảy từ cột ẩn H sang cột K, nên "Fl" vào K672/K884.
    - Phát hiện: Agent tự phát hiện, xóa ngay.
    - Bài học: tìm cột theo tiêu đề, kiểm name box trước khi ghi.
23. **Vòng dán clipboard giả lập không lưu ô.** Chữ dồn vào ô đang mở, hỏng Z21, Y926; vòng lặp báo "309 ok" nhưng thực tế không ghi.
    - Phát hiện: Agent khi so toàn sheet.
    - Sửa: gõ lại tay; chuyển sang Tìm và thay thế.
    - Bài học: sau mọi lượt ghi phải so toàn sheet với bản chụp trước.
24. **Ghi sai giờ trong tên báo cáo và bản chụp.** Ghi "23h", "2335" trong khi làm lúc khoảng 21h30.
    - Phát hiện: Agent tự đính chính với Dũng.
    - Bài học: lấy giờ từ máy, không ước lượng.
25. **Hiểu lời chị Oanh quá hẹp.** Bỏ qua 347 ô chữ 2026 của chính nhóm Thuốc.
    - Phát hiện: Dũng ("chị oanh nói không sửa thông tin của người khác…").
    - Sửa: cập nhật 435 ô, giữ 14 ô chữ 2026 đầy đủ hơn.
    - Bài học: hỏi rõ phạm vi lời dặn; "người khác" ≠ "nhóm mình".
26. **Lần đầu đè chữ 2026 tốt hơn bằng bản KOM kém hơn.** Ví dụ "Leopard Medical" → "Leopard", "Box of 2 blisters…" → "BL 2 X 5 TAB".
    - Phát hiện: Agent tự phát hiện trước khi chép.
    - Sửa: thêm luật giữ chữ 2026 (lần đầu viết luật bị lỗi gõ `\b` thành ký tự backspace, phải sửa).
    - Bài học: soát mẫu nội dung trước khi chép.
27. **NSX ghi tên nhà phân phối** (Thanh Nam, Tien Loi, Duc Duong).
    - Phát hiện: góp ý chị Tar, sau đó Dũng hỏi về FK.
    - Sửa: 5 mã có ảnh và nguồn → Fresenius Kabi, Polysan, Guerbet. KOM-798, 375 giữ theo chỉ đạo.
28. **Báo "206 ảnh gần đúng/khác quy cách cần thay", bị thổi phồng.**
    - Nguyên nhân: số 206 đếm theo nhãn trong cột nguồn ảnh của sheet; đếm ảnh thật trong form chỉ 145; xem mẫu 5 mã thì đều đúng hàng (nhãn gắn thận trọng).
    - Phát hiện: Dũng ("là sao vậy?", "đó đúng là hàng nộp chào FK?").
    - Bài học: đếm trên đối tượng thật (ảnh trong form), xem mẫu trước khi báo.
29. **Câu hỏi "đổi sang hãng thật" gây hiểu nhầm** ("đổi hãng là sao vậy?").
    - Nguyên nhân: Agent dùng chữ "đổi hãng" cho việc sửa nhãn NSX, trùng với cột "Đổi hãng" trong DS của chị Oanh (nghĩa là năm 2027 chào hãng khác năm 2026).
    - Bài học: không dùng một chữ cho hai nghĩa; nói rõ "hàng giữ nguyên, chỉ sửa chữ ở cột NSX".
30. **Ảnh bao bì do Codex tạo bị méo, giả, bóng nhựa, dùng prompt chung.**
    - Phát hiện: Dũng.
    - Sửa: nghiên cứu bao bì thật từng sản phẩm, brief riêng.
31. **Định nghĩa "thuốc đặc biệt" (SVNK) do Agent tự đặt; con số "94 MTP" không tái hiện được (thực tế 93); ghi chú bắt đầu bằng "=" làm Excel báo repair.**
    - Sửa: dùng danh sách chị Tình; sửa ghi chú.
32. **Trợ lý con báo nhầm vài số mã** (CSV đúng). Agent lọc lại tay.
    - Bài học: kiểm báo cáo của trợ lý với dữ liệu.

## D. 13/11
33. **Suýt đưa profile Chrome tạm (`_chrome-temp`, có thể chứa cookie) lên git.**
    - Phát hiện: Agent khi soát trước commit.
    - Sửa: loại khỏi commit, thêm vào `.gitignore`.
34. **Không mở thử được file SVNK đã điền bằng Excel**, vì lệnh mở Excel tự động bị chặn quyền.
    - Bù lại: tính lại bằng Python, khớp 100% với Phét ở 83 mã; kiểm XML hợp lệ; đặt tự tính lại khi mở.
