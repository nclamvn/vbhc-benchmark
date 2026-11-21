# VBHC v3 · Thay đổi sau kết quả kiểm (21/11/2026)

Bản v3 thay bản v2 trong thư mục Vong2_2026-11-21. Căn cứ: tệp Ket-qua-kiem-VBHC-v2.xlsx (17 nhận định trên 16 mục văn bản), có kèm trong thư mục này.

## Số liệu

- Toàn văn giữ lại: 6.294 văn bản (v2: 6.282). Trung ương 5.108, Thái Nguyên 621, Hưng Yên 565.
- Loại bỏ: 150 (v2: 162). Trùng tệp y hệt 70, độ tin OCR dưới 70 là 49, trích yếu nêu một người dân 23, tệp không phải PDF 7, tệp không khớp trích yếu 1.
- Cần người xem: 1.212 dòng (v2: 1.213).
- Registry: 24.874 thực thể, 180.308 claims, 1 ô tranh chấp (v2: 2). Build digest 30c98055d74a2ebe, 0 cổng cắn.

## Ba luật đã sửa

1. Khử gần trùng: chỉ loại khi hai văn bản vừa gần trùng nội dung vừa cùng số ký hiệu và cùng ngày ban hành. Văn bản định kỳ dùng chung mẫu (thông báo cấp độ dịch hằng tuần) được giữ, và ghi ở trường gan_trung_mau_voi.
2. Chọn tệp đính kèm: văn bản có nhiều tệp thì lấy PDF có số trong tên trùng số ký hiệu; không có thì lấy PDF đầu tiên. Bản v2 luôn lấy tệp đầu.
3. Số ký hiệu: thêm trường so_ky_hieu_chuan (bỏ khoảng trắng và dấu chấm cuối). Trường so_ky_hieu vẫn giữ nguyên văn như trang nguồn.

## Còn mở

- tn-84190 và tn-84111 (cùng 307/NQ-HĐND, 17/07/2026) được giữ cả hai, gắn cờ chờ xác minh bản chính thức.
- Số CT-TTg của 218224 ghi theo xác nhận của người kiểm; máy OCR vẫn đọc ra "CT-1".
- Kết quả kiểm chưa ghi tên người kiểm.
- Đây là rà soát danh sách loại bỏ và danh sách cờ. Chưa phải lượt kiểm tay 100 mẫu thông tin cá nhân của cổng M2.

## Cách ghép

Ghép các tệp toan_van_v3_phanNNof21.jsonl theo thứ tự số. Các tệp chi_muc_van_ban_v3_phanNNof04.csv mỗi tệp đều có dòng tiêu đề; khi ghép bỏ dòng tiêu đề từ tệp thứ hai.
