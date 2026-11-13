# 06b. Danh sách đầy đủ các lượt Dũng hỏi lại / nghi vấn (trao đổi trực tiếp Dũng ↔ Agent)

Trích tự động từ toàn bộ tin Dũng gửi Agent trong các phiên Claude (phiên chính + phiên phụ PHƯƠNG ÁN/DATA/HỌP/kiểm GV; bỏ các phiên cầu nối kỹ thuật): 424 tin. Lọc tin có dấu hỏi hoặc từ nghi vấn ("sao", "là sao", "chưa", "hả", "nhỉ", "không hiểu"…): **164 tin**. Phân nhóm bằng từ khóa (một tin vào nhóm đầu tiên khớp, có thể lệch nhóm, nhưng không bỏ tin nào). Giờ Lào. Số tiền/số lớn che bằng [số]; trích tối đa 220 ký tự. Phân tích lý do và cách tránh: xem [06-HOI-LAI-NHIEU-LAN.md](06-HOI-LAI-NHIEU-LAN.md).

## Theo ngày

| Ngày | Số tin |
|---|---|
| 30/10 | 5 |
| 31/10 | 2 |
| 01/11 | 1 |
| 02/11 | 1 |
| 03/11 | 2 |
| 04/11 | 10 |
| 05/11 | 20 |
| 09/11 | 2 |
| 10/11 | 11 |
| 11/11 | 54 |
| 12/11 | 53 |
| 13/11 | 3 |

## Theo nhóm

| Nhóm | Số tin |
|---|---|
| 1. Đã xong/đã cập nhật chưa? (báo cáo thiếu bằng chứng) | 26 |
| 2. "Là sao?" – nói khó hiểu, dùng từ nội bộ | 17 |
| 3. Sao không hỏi/tìm kỹ từ đầu – thiếu sót lòi ra | 4 |
| 4. Nhắc lại quy tắc/phạm vi | 6 |
| 5. Viết cho người đọc / trình bày | 10 |
| 6. Tiền tệ, đơn vị giá | 6 |
| 7. File nào là chuẩn / phiên bản / ở đâu | 9 |
| 8. Ảnh, thị giác, bao bì | 24 |
| 9. Quyền, git, công cụ | 3 |
| 10. Khác (hỏi thông tin, hỏi ý kiến) | 59 |

## 1. Đã xong/đã cập nhật chưa? (báo cáo thiếu bằng chứng) (26 tin)

- 30/10 12:04 — đồng thời update plugin hay do plugin chủ sở hữu chưa update ?
- 31/10 18:49 — Tiếp tục đúng phiên hiện hữu a5ab430d-1ab4-4c21-8a6a-2b597076de9f. Dũng vừa yêu cầu audit hướng build, refactor theo nghiên cứu đầy đủ và chuẩn bị B dùng thật trong workspace/project riêng. Lượt này CHỈ đọc lại context s
- 31/10 18:54 — Dũng yêu cầu nạp context liên quan đã audit và refactor đúng phiên a5ab430d-1ab4-4c21-8a6a-2b597076de9f. Đây là packet context được chọn cho BidOps B; chưa gửi ra ngoài nghiệp vụ. CHỈ đọc/audit, không dùng tools hoặc sửa
- 01/11 10:28 — # TASK — kiểm continuity đã được đặt vào đúng project Codex đã review và publish 7draft của bạn vào D:\WORK\Agent\Agent-first\NNC BidOps Agent\context\continuation-20261101. Đã thêm pointer ở context/PROJECT_STATE.md và 
- 02/11 10:45 — Tôi giao Foundry/Shin phối hợp điều hành BidOps trong phạm vi đã chốt. Claude tự phân việc và thực thi; chỉ hỏi tôi khi đổi định hướng, thiếu quyết định nghiệp vụ hoặc gặp quyền chưa được cấp. Làm Data và Phương án trước
- 04/11 16:00 — chưa thấy số lượng update vào
- 04/11 17:45 — ủa nhưng sau tổng kết và thảo luận họp vừa rồi ta update chưa update rồi mới triển khai nhé vì trong này tôi thấy bạn hỏi mấy câu trong họp gần như đã trả lời rồi nhỉ hay chúng ta tốt hơn ý kiến trong họp ?
- 05/11 19:13 — update cho file chung gốc chưa ? LOCK dữ liệu chốt hôm nay nhé (KOM chốt đợi nguồn + giá -> dữ liệu có gì sẽ refactor file gọn lớn và file chia đã có đủ cần lock vị trí và chỉnh file chung gốc kia khớp nhé nó đang có một
- 09/11 18:42 — bạn hết token nên hôm nay mới có token để update quá trình hoạt động diễn ra của thầu. chưng cất ra các kinh nghiệm làm việc với nhau như các file data dữ liệu ntn và chốt ra sao kinh nghiệm tìm hàng,... Khó của KOM inte
- 09/11 18:56 — Việc chưng cần cần tách rõ human - Agent nhé , vì mục tiêu tôi cần Agent tự chủ gói thầu phân biệt đâu là cách chia theo chủ đích cá nhân tức là cách thức thôi không phải 100% như vậy nhé có rất nhiều lỗi trong việc phối
- 10/11 18:47 — "File anh duy riêng và Tar riêng e cho nó coi cả 2 file nhé" xác nhận xem đã đọc chưa nhé
- 11/11 08:26 — hqua bạn add ảnh vào chưa không thấy báo gì nhỉ ?
- 11/11 08:29 — ý là ảnh đã điền hết vào sheet chưa ?
- 11/11 16:12 — rồi toàn bộ ảnh đợt add vừa rồi là xong r hay sao ?
- 11/11 17:23 — 6. GIÁ VỐN TAR TỰ TÍNH – Tar xác nhận 11/11: GV đã tính sẵn (gồm chi phí), không theo công thức tỷ giá chung → bảng chỉ để THAM KHẢO. Còn hỏi: KOM-348 (GM "1", chưa báo giá) và KOM-855 (GV thấp hơn GM). * xong thì bỏ đừn
- 11/11 17:23 — Thị giác xong chưa ? hay đang đợi nó xong mới làm thị giác >
- 11/11 18:25 — 68 mã còn lại lạ vậy chiều mới update ảnh của hàng này vào mà ?
- 11/11 18:38 — chiều nay tôi tar vừa làm xong với bạn để update đây ? nhìn tên hàng đừng nhìn mã Mình chưa lấy ảnh ra từ hai file này. -> lấy đi rồi đặt lại report cho đúng
- 11/11 22:55 — duyệt đề xuất nhé Theo bạn đã đúng được các yêu tố chưa ? đủ để chị tình mai vào xem không ? từ lúc nhận thấy diff mơ hồ về tar trang ta đi khá xa và thay đổi nhỏ trong khi mọi thứ thì đang phụ thuộc, GIá - hàng - nguồn 
- 12/11 10:00 — Dấu ℞ trên ảnh mẫu: bỏ hết hay giữ theo nhóm thuốc? -> phân tích xem vì trống quá thì phải làm gì cho đỡ trống kí hiệu đó là gì vậy ? còn việc đó là đã làm xong rồi hả ?
- 12/11 10:29 — hỏi chị Trang 5 sản phẩm đó nhé -> ngoài ra bạn có đề cập đến sai chính tả hayu ghi nhầm gì đó thì mình đã chỉnh lại cho đúng dựa vào thông tin chị Trang đặt chưa ?
- 12/11 11:55 — Oke nhớ WOrkflow lúc đầu làm KOM đến giờ chứ giờ cutoff được rồi veijec của KOM là bổ sung file nộp thôi Thông báo: Thầu BV – đổi lịch quan trọng: Lúc 11:09, Phet báo KOM chuyển sang tuần sau, chưa nêu ngày cụ thể. Savan
- 12/11 13:41 — Cho chạy tiếp đợt B–E bằng Creative Production theo khuôn A1? sao chưa chạy ?
- 12/11 16:55 — Bảng đối chiếu đầy đủ em đã thêm vào PLAN-SVNK-HOI-TU_v1_20261112.md, mục 3b. ->xong chưa chưa thì plan làm xong thì tôi kiểm file
- 12/11 16:57 — vậy thực tế file chị tình đang kiểm là đúng hàng của chị trang đúng không ? nếu đúng thì update thông tin vào nhé và chưa rõ tại sao chị trang báo nhập rồi mà mình không biết ?
- 12/11 19:36 — ủa chứ hôm nay xử lý được gì ? mà sao vẫn giống hqua vậy ?

## 2. "Là sao?" – nói khó hiểu, dùng từ nội bộ (17 tin)

- 30/10 12:21 — sau đó từ các tài liệu ở dự án hiện tại và các cách làm việc hiện tại thực thi nghiên cứu và đưa ra bản Định hình sản phẩm và các điểm khóa, các mâu thuẫn hoặc chưa rõ là gì đề xuất/ nêu rõ phần thiếu là thiếu gì
- 11/11 16:43 — ủa quy đổi sang COm là sao ? -> xử lý nó trước khi làm tiếp nhé
- 11/11 16:58 — cái này là sao vậy ?
- 11/11 17:01 — là sao chưa hiểu lắm Ghi chú đó nếu họ đã làm rồi k cật nhật thì sao ?
- 11/11 17:10 — còn cột Tar kiểm là sao ?
- 11/11 17:35 — Lỗi giá thật như nào ko hiểu
- 11/11 21:06 — tar còn 4 là 4 gì ?
- 11/11 21:10 — làm rõ trước ? điều tra câu nói đó là gì ? tôi cũng k hiểu
- 11/11 21:31 — hướng xử lý đúng là gì ? hội tụ đang đúng hay sai ?
- 11/11 22:07 — làm rõ 72 hàng đó là gì nhé 2 ứng cử viên không , giá và hàm lượng ntn ?
- 12/11 09:35 — trình riêng plan làm song song chỗ chị oanh tôi đọc nhé yêu cầu là gì làm rõ ntn và plan thực thi ra sao lộ trình ,...
- 12/11 09:42 — 3. điểm làm rõ Q1 ghi thẳng vào file Q2 đổi hàng thì thay luôn Q3 ghi giống chị nhé Q4 oke Q5 chưa hiểu lắm trong khi mình là người phụ trách nhóm thuốc để làm Q6 ok nhé làm luôn cũng được nhé -> data mình có rồi chỉ đổi
- 12/11 19:34 — lúc sáng chị Tar đã hoàn thành rồi còn lại của chị trang mà sao giờ thấy đẩy qua đẩy lại là sao nhỉ ?
- 12/11 20:24 — xử lý từng mã nhé 547 thiếu nguồn là sao ? -> chị trang không nhập nguồn không tính giá luôn hay sao ? thiếu quy cách tra không ra hả ? kiểm mạng cũng không có luôn hay sao ? check trong thưu mục inbox có chỗ đặt catalog
- 12/11 21:04 — quy tắc là gì ?
- 12/11 22:41 — visa không nhé có thay 206 ảnh gần đúng hoặc khác quy cách bằng ảnh đúng hàng [số] không -> là sao vậy ?
- 12/11 22:59 — đổi hãng là sao vyaja ?

## 3. Sao không hỏi/tìm kỹ từ đầu – thiếu sót lòi ra (4 tin)

- 12/11 19:46 — TÌm không ra hả
- 12/11 19:55 — nói chung anh chị báo nộp hết rồi có đầy đủ thông tin hết rồi do bạn không tìm kĩ ? sao bạn tìm không ra ?
- 12/11 20:02 — sao ban đầu bạn ko hỏi luôn nhỉ ? mơ hồ vậy hoặc không đủ để rõ thông tin nộp thầu ?
- 12/11 20:39 — theo bạn thì nếu ta điền vào thị mình có liên hệ đặt hàng kịp không ? sao không nhắc hàng anh Duy ? dùng ta tốn khá nhiều thời gian đấy nhé ảnh nào không có chuẩn bị tạo hình nhé nhé vì nó đang thiếu thật hoặc nhu cầu củ

## 4. Nhắc lại quy tắc/phạm vi (6 tin)

- 05/11 16:37 — sao không dùng thị giác này vậy đừng follow theo file mới gửi vừa rồi quá mức nhé file nguồn làm chuẩn thêm VNĐ vào đi
- 11/11 08:28 — đính cái link được rồi không cần chèn hình miễn sao bấm vào thấy ảnh -> khi nộp file thì mới cần xuất bản file có hình thật bên cạnh
- 11/11 22:39 — sao lại quy giá ? mình sửa giá của anh chị hả ?
- 11/11 22:48 — chúng ta chỉ mâu thuẫn hàng là của ai tar hay trang thôi áo lại giờ đi xa vậy ?
- 12/11 20:50 — vậy dùng quy cách đó nhé về Aciclovir -> giữ tên chị trang điền và giá bù giúp cho quy cách Báo tham khảo MINH DÂN -> bổ sung hình nữa nếu là vậy thì đúng là Nước nguồn nhập là Việt nam FK ? -> bạn đọc hiểu giùm tôi nhé 
- 12/11 22:16 — chị oanh nói không sửa thông tin của người khác chứ không phải thông tin nhóm thuốc nộp kiểm tra thử ? Tên hàng chào (W) và thành phần (X) còn tiếng Việt: có 93 đề xuất W và 14 đề xuất X. Chị Tar nêu đúng chỗ này, nhưng 

## 5. Viết cho người đọc / trình bày (10 tin)

- 04/11 18:01 — * Một file tổng duy nhất ở thư mục cha, nhiều sheet, gom cả Kom. Chỉ đọc, chỉ một người ghi. * là sheeet gì ?
- 05/11 10:06 — kiểm tra nhé chúng ta chưa đạt yêu cầu về file dữ liệu Vì KOM : Quân y đang bị chẻ thêm thay vì gộp vào nguồn 1. mã doanh mục tổng bổ sung nguồn hàng 2. Map nhóm thuốc KOM 3. Nguồn hàng thêm 1 cột giá từ file gốc Phet Gử
- 05/11 16:31 — message gửi chị trang đây ? ghi chú gì đây ? viết cho người đọc
- 11/11 10:01 — có cách nào làm song song không bị không ?
- 11/11 11:01 — Cột Ảnh chưa hiển thị ảnh nhé viết hàm cho hiển thị từ link nguồn đi
- 11/11 16:19 — đọc yêu cầu của chị oanh nữa chưa ?
- 11/11 16:44 — làm sao để biết luôn chứ không phải đặt note Cần QUy đổi nhé
- 11/11 17:06 — oke chúng ta có thể bỏ qua ghi chú mà? -> tải về làm dữ liệu rồi viết report thôi k phải viết tay cho việc kia nhỉ ? nếu đúng là bây giờ giá không sai thì qua chờ duyệt hết r
- 12/11 08:29 — điền như cũ cái quy đổi tương đương chỉ ghi note. tức là bạn giữ giá ở gói nhưng có note này dược trỏ chuột vào ? -> vì phần này chị tình phet sẽ kiểm. để mai có file nộp
- 04/11 16:07 — Kom: thêm “Kom có số lượng ở sheet Giá NNC [số] không” xem tiếng lào chưa ?

## 6. Tiền tệ, đơn vị giá (6 tin)

- 05/11 14:11 — giá đó cho 2 đơn vị quy đổi nhé USD thì giữ có thêm VN KIP nữa Thêm cột giá của SƠN,DUY,TAR, Phet, Trang để anh chị điền nhé https://docs.google.com/spreadsheets/d/1ilOLCO-ecT_2NlyGi59Irr8tHqPwOI-y/edit?gid=[số]#gid=[số]
- 05/11 16:36 — sao trong file lai la gia KIP ? khong phai vnd ?
- 11/11 15:13 — 21 mã trang kia có vấn đề gì ? bản chất giá mua có cần VAT không ? chỉnh lại tiền tệ cho đúng kiểm lại đi nhé chúng ta cần chắc thì mới báo cáo nhé chứ không phải báo cáo kiểm không ? -> tức là ưu tiên tự xử lý được trướ
- 11/11 15:25 — D18 ở đâu nhỉ hqua trao đổi này nhé giữ 1 chỗ cho tỷ giá thôi
- 11/11 16:46 — làm sao để quy về đơn vị nhỏ nhất đi nhé
- 11/11 16:49 — OTC VC [số] kíp/đv bán (NCCold (Paracetamol 500mg / Chlorphenira) – cần quy đổi sang Fl -> phải tham chiếu qua hàng chào chứ ta ? vì hàng chúng ta vừa chào vừa bán OTC nên cần xem cái đó

## 7. File nào là chuẩn / phiên bản / ở đâu (9 tin)

- 30/10 15:35 — p1/p2 kho lần trước bạn có đặt thì giờ nó ở đâu vậy ?
- 04/11 15:28 — có bản nào sạch và duy nhất giống a sơn không ?
- 04/11 18:00 — đặt ở thau BV nhé vì việc tìm hàng cần hơn là ghi giá vốn 1 file tổng hợp toàn bộ hàng tinh gọn ở cây cha gom luôn mã Kom vào -> Phân thư mục theo nhóm hàng và các bộ lọc để làm Đặc tả node: -> chưa cần làm liền có thể f
- 11/11 08:43 — làm đi nhé cứ gắn vào high ligh màu thị giác để tôi biết cái nào đúng cái nào sai quy cách cái nào gần đúng là gần đúng ntn nhé chỗ chưa file hội tụ KOM kia cần có thư mục ảnh điền thay vì link từ ib của các anh chị -> đ
- 11/11 10:12 — H:\Shared drives\004-Ban lam viec\16-CNTT-Agent\Thau BV - sao k dùng cái nyaf
- 11/11 17:00 — xử lý là xử lý ở đâu ? danh sách 60 mã KOM hả
- 12/11 10:03 — 3. Việc form chị Oanh: đã xong phần ghi -> ghi vào form chị oanh r hả ? -> thiếu là thiếu hay là dùng trùng hàng nhé ảnh còn lại của chị trang là đang làm để bổ sung đảm bảo được điểm dừng theo yêu cầu chị oanh chưa ? đư
- 12/11 15:34 — bạn nghe nhưng bạn phải nhìn thông tin trong video nữa nhé để khớp với chị tar đang nói gì và file nào ?
- 12/11 23:24 — Form chị Oanh (bản v10 trên H:): 564/564 dòng khớp sheet, 563 dòng có ảnh, kiểm tra đều đạt. V10 có phải file chị oanh đưa không ?

## 8. Ảnh, thị giác, bao bì (24 tin)

- 30/10 11:41 — https://github.com/VOSYDUNG/nnc-claude-plugins.git áp dụng phương pháp thiết lập tự chủ cho dự án này nhé vì dự án là Agent nhưng có nhiều dùng chung và có họp nữa nên tổng hợp lại toàn bộ để chuẩn bị ấy -> kiểm tra gith
- 05/11 11:07 — highlight visa chưa ? nhóm A B C D -> bỏ nhé nếu nó không hỗ trợ thúc đẩy tìm hàng , nếu có thì tìm tên khác -> vì chữ nhóm có nhóm thuốc rồi làm anh chị nhầm
- 05/11 11:34 — khi các anh chị lọc thì có ảnh hưởng nhau không ?
- 10/11 16:22 — tình hình ảnh thì sao ?
- 10/11 16:26 — tải kho ảnh của anh chị nộp về chưa để dò chưa ?
- 11/11 08:33 — bạn làm sao cũng được miễn tôi thấy được ảnh tham khảo của hàng là được
- 11/11 10:17 — nếu không bị ảnh hưởng chéo thì k cần làm bản sao nhé
- 11/11 11:00 — trùng ảnh hay sao ? hay chỗ đó 2 ứng cử viên
- 11/11 13:38 — ảnh mình done chưa ? toàn bộ ảnh
- 11/11 14:50 — xem thử plan mở thêm task chia việc để làm được không ? -> chị nói lần trước bên DL ảnh sheet đang làm là oke r có thay vài cái thôi, làm nhé
- 11/11 15:40 — anh ko đúng --- báo nó lấy ảnh Fengshi OPC bạn lấy sai ảnh hả ?
- 11/11 16:02 — tiến độ hình ntn rồi ngoài việc sửa/bổ sung đang làm này ?
- 11/11 17:54 — chưa nói gì về ảnh ?
- 11/11 17:59 — ảnh thiếu do đâu ??
- 11/11 18:44 — xong thì lưu bản sao ở thời điểm hiện tại gửi report nhóm thuốc vào THẦU BV +856 20 96 609 999 -> tình reprot trực quan và huognws dẫn gọn gửi report cho chị tar + kiểm số ảnh thiếu + hàng cần xử lý Gửi vào nhóm tiến độ 
- 12/11 09:27 — sao bạn để nó tạo lạ vậy -> tham khảo các sản phẩm có hình để hiểu thị giác của một sản phẩm hoàn chỉnh đi nhé
- 12/11 09:51 — nhìn hình giả quá và không thật nữa tôi nghĩ vẫn nhờ codex làm lại tự bổ sung thị giác của nó sao cho đẹp là được, vì cũng đang thấy đơn giản quá mức
- 12/11 10:02 — sao hàng mình được ghi và có đầy đủ rồi -> giwof làm hình lại bảo thiếu thông tin nhỉ ? hay bản chất chỉ có nhiêu thông tin đó thôi , còn hình thì bên hông đó cũng phải có thông tin gì chứ nhỉ . A Sơn nói là các thông ti
- 12/11 11:04 — sao tôi thấy nó méo méo vậy nhỉ ?
- 12/11 15:14 — * Rosuvastatin 5: cần sửa chữ “Đế”. * 6 mã đang chờ chị Trang. * 4 hàng chính hãng. * NaCl 0,9%. -> tạo ảnh hay sao ? hay hàng chưa rõ còn treo ?
- 12/11 16:51 — kiểm thử hình chị trang gửi ?
- 12/11 17:01 — có thể tar điền phụ Còn việc gì nữa về ảnh và thông tin hàng ?
- 12/11 19:38 — có thông tin của anh chị rồi ta fill cho đủ đi nhé -> ảnh cũng đã gen và nộp thì sao báo thiếu nhiều z ?
- 12/11 20:16 — báo tôi còn mã nào chưa xử lý về thông tin và hình ảnh

## 9. Quyền, git, công cụ (3 tin)

- 04/11 17:38 — oke ở điểm chặn như bạn thấy đó là điểm họp của ngày mai Q1-> chúng ta tách giá và hàng ra thì cũng đúng nhưng cần bạn cho tôi biết phân loại sao để mã nhóm đó, bạn chưa định nghĩa dữ liệu tìm được sẽ ntn. các Nhóm này c
- 13/11 09:39 — làm sao cấp quyền ? push check thử có thật đang sửa không để thay ? -> nếu không ta phải mở sheet điền tay hả ?
- 13/11 09:40 — Em thêm quyền cho phép lệnh git push vào cài đặt dự án nhé? -> thêm đi nhé

## 10. Khác (hỏi thông tin, hỏi ý kiến) (59 tin)

- 30/10 12:00 — khoan bạn đang lấy plugin cũ sao ?
- 03/11 23:00 — sao gửi 6 mấy vậy ?
- 03/11 23:01 — batch có 6 thì làm chừng nào xong ? gửi thêm đi đầy đủ càng tốt miễn nó đã được data làm xong
- 04/11 16:41 — D. Tên chưa đủ rõ để tìm -> sao chwua rõ
- 04/11 18:02 — như vậy cần chẻ nhỏ chi nữa ?
- 04/11 18:36 — mã KOM map vào đó mất tên gốc không ?
- 05/11 09:26 — hay làm file csv ? nó combine qua excel vẫn giữ giao diện fk
- 05/11 11:22 — giờ các anh chị làm việc ntn tạm gác các cây thư mục phức tạp nhé https://docs.google.com/spreadsheets/d/1ilOLCO-ecT_2NlyGi59Irr8tHqPwOI-y/edit?gid=[số]#gid=[số] file này tập trung hoàn thành vì a sơn nói cần nó là đc rồ
- 05/11 11:23 — AI dùng để điền thì sao ? -> nhiều anh chị cũng kiếm giá nhập vào 1 chỗ thì sao ?
- 05/11 11:41 — "Tên theo thầu (nguyên văn)" "Tên Kom gốc (dòng gộp)" 2 cái này khác nhau gì ?
- 05/11 11:56 — theo bạn đủ đạt để gửi anh chị chưa
- 05/11 11:59 — xem thử đạt yêu cầu nghiệp vụ của anh chị tìm hàng chưa nhé -> dùng skill /data phù hợp để audit
- 05/11 12:00 — https://docs.google.com/spreadsheets/d/1ilOLCO-ecT_2NlyGi59Irr8tHqPwOI-y/edit?gid=[số]#gid=[số] kiểm cái này thôi nhé tôi gửi cái này
- 05/11 13:24 — có bản sao local chưa
- 05/11 13:54 — bạn có phân tích trúng trật thầu từ file này chưa ?
- 05/11 14:44 — Nước khác thì để tên nước đó chứ nhỉ ?
- 05/11 15:53 — nhớ có đặt thêm dòng trạng thái của chị ấy xong việc hay chưa nhé
- 05/11 16:46 — có hướng dẫn cho Agent của chị chưa ?
- 10/11 17:17 — "File gom là chọn ra sp nào giá rẻ rồi hả e" đính chắc trong report nhé
- 10/11 18:53 — có lấy đúng giá chào [số] không đó ? so giá các thứ rồi phải không
- 10/11 19:45 — 31 mã chênh từ 5% trở lên: kết quả chọn không đổi, dù giá bên nào đã gồm 5% VAT. Ví dụ KOM-708 Tar [số], chị Trang [số], chênh 9,3%. -> vẫn có hiển thị sao cho thấy nhé
- 10/11 19:51 — BÊN chị TAR có VAT hàng nào không ?
- 10/11 19:56 — theo bạn thì sao ? chỉ so GM thôi phải không ?
- 10/11 20:24 — ứng Viên ở GM không tính VAT mà đúng không ?
- 10/11 20:26 — còn file log local Vẫn giữ độ phức tạp so giá nhé từ GM -> Giá chào -> chỗ nào so được thì so chưa đủ thì đợi, hoặc hàng không trùng thì thắng từ GM . Với của anh duy - son - c vài hàng nó trùng hoạt chất vs chị trang nh
- 10/11 20:27 — Nếu ý chị Tar là đưa mọi giá về chưa VAT thì phải trừ VAT ở 311 mã này. Việc đó em chưa làm, cần chị xác nhận. -> đúng nhé ứng cử Viên không TÍnh VAT
- 11/11 15:42 — https://nnclaos.com/ -> hàng ở đây kiểm nhé đối với các hàng chưa chắc
- 11/11 16:20 — @"C:\Users\Admin\Downloads\[số] Gia OTC ms Hoa.xlsx" chưa rõ gì thì hỏi lại nhé
- 11/11 17:40 — không có giá mua nhưng có giá vốn thì sao ?>
- 11/11 17:42 — 16 mã còn lại mã gì và cần làm gì ?
- 11/11 17:45 — A. Giá thấp được vô nhé B 2 quy cách giống nhau không ? -> trả lời chưa làm D oke rồi
- 11/11 17:52 — oke được rồi nhỉ ?
- 11/11 22:00 — nhưng mình có xử lý đc cho chị tình luôn không ?
- 11/11 22:05 — làm rõ với tôi tại sao chọn nhé tức là ô đó chọn 1 trong 2 hay chỉ duy nhất nhưng khác hàm lượng hoạt chất ?
- 11/11 22:14 — ời hoạt chất hàm lượng là do mình đánh giá fk hay thuốc file gốc của thầu nhé ? các ứng viên là của ai ? thường thuốc dù để kê đơn nên giá bạn cũng phải hiểu về thuốc dược và bác sĩ kê đơn như thế nào nhé vì đó là điều k
- 11/11 22:49 — 127 mã đó: trả cột Người PT về Trang hay để sau? -> bạn phải xem chủ yếu nó là hàng gì ở đuâ nước nào
- 11/11 23:07 — diff từ 20:43 và bản hiện tại là đổi cái gì ?
- 11/11 23:20 — ddã bảo 538 háng đó k tìm nữa mà ? bỏ phần dũng đã chốt nhé
- 12/11 08:27 — KOM-887 Belcid: giá Algelstad là chai hay hộp? --> giá hộp, hộp 20 gói chị trang gửi
- 12/11 09:15 — bạn chưa đưa plan bạn sẽ làm gì nhé
- 12/11 09:43 — kiểm Visual đi nhé Tôi nhớ Opus 5.5 bạn làm visual tốt mà sao gửi bản thiết kế cho nó tạo không hợp lý lắm nhỉ ?
- 12/11 09:55 — cái nào cũng gán thuốc kê đơn vayaaj ?
- 12/11 10:10 — 10 dòng khác: KOM-96, 261, 478, 846, 868, 873, 885, [số], [số], [số] (9 của chị Trang, 1 của chị Tar). sao còn chị tar trong này nữa ?
- 12/11 11:24 — bạn không nói nó tự dùng được hả hay user kcihs hoạt
- 12/11 15:52 — oke plan task svnk chưa ?>
- 12/11 16:09 — nhóm 2 trong Tar bạn hiểu chưa ?
- 12/11 16:49 — [16:44, 12/11/[số]] Hoàng Trang NNC- HN: KOM-1091-1092 mình điền hàng khác [16:44, 12/11/[số]] Hoàng Trang NNC- HN: nhưng chắc có bạn có hàng tốt hơn nên chọn hàng đó [số] [số] của TAR hả ?
- 12/11 16:53 — đúng rồi đức là chồng chị ấy nhưng cần biết là có bị chồng hàng khác không ? tức nugoiwf khác có hàng tốt hơn không ?
- 12/11 17:05 — [17:04, 12/11/[số]] Hoàng Trang NNC- HN: Albendazol hàm lượng 200 mg [17:05, 12/11/[số]] Hoàng Trang NNC- HN: Có thông tin tỏng file đầy đủ mà nhỉ
- 12/11 19:25 — còn hàng nào chưa đủ thông tin để kiểm giá nộp thầu không ?
- 12/11 19:47 — mã của ai mà sao không có trong Report hôm qua ?
- 12/11 19:47 — 19 mã này ?
- 12/11 19:48 — hàng của ai z ?
- 12/11 19:51 — nguồn là nguồn nhập chứ không phải xuất xứ . có hàng nào không phải của anh chị bạn bịa ra không ?
- 12/11 19:54 — làm rõ 19 háng kia bạn nói xem ?
- 12/11 20:57 — KOM-657 O-Kal-D: chưa có tên hàng. 547 kiểm file phet
- 12/11 21:04 — ủa vậy là mitaphap ? tức hàng đã nộp trước đó ?
- 12/11 22:44 — nhưng đó đúng là hàng nộp chào FK ?
- 13/11 08:48 — https://docs.google.com/spreadsheets/d/1jhP1nUUzdj45MwLszxWI5q-laozmUAui/edit?gid=[số]#gid=[số]
