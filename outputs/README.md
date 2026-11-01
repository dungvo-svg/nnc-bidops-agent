# Đầu ra thí nghiệm và bàn giao

Mỗi kết quả ở `<mã-ca>/<phiên-bản>/` với manifest nguồn, expected/actual, môi trường, kết quả kiểm và giới hạn. Không dùng tên/path bộ thầu đã gửi. Không có kết quả thử/nghiệm thu sản phẩm trong thư mục này lúc setup.

Legacy `build_tender_sets.py` trong project PMA cũ có hardcode G và output bộ thầu. Không chạy ở workspace này. Nếu cần kế thừa, đọc có giới hạn, refactor đường vào/ra thành tham số riêng, viết fixture tổng hợp và kiểm nguồn/output không bị ghi trước khi chạy. Chưa copy/chạy builder hoặc cài môi trường trong lần setup.
