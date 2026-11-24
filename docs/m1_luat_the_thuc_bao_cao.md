# M1 · Bộ luật thể thức NĐ 30/2020 máy kiểm được · báo cáo pilot

- **Ngày:** 21/11/2026 · **Người dựng và người xác nhận:** chuyên gia mô phỏng (AI, Claude), theo QĐ-08. Chưa có người xác nhận.
- **Mã:** `scripts/the_thuc_nd30.py` (12 luật), `scripts/the_thuc_nd30_v2.py` (thêm 3 luật), `scripts/m1_danh_gia.py`. Dữ liệu thử: thư mục `m1/`.

## Kết luận

1. Bộ luật dùng được để chấm **văn bản chữ sạch** (bản nháp do người hoặc mô hình soạn): bắt 58/60 lỗi cài trên ba bộ thử giữ riêng, không có cờ thừa.
2. Bộ luật **không dùng được để kết luận văn bản quét có lỗi thể thức**: trên 20 văn bản thật ngẫu nhiên có 13 cờ, không cờ nào là lỗi thật của văn bản.
3. Bộ luật chỉ kiểm thành phần thể thức có mặt và đúng mẫu chữ. Phông, cỡ chữ, lề, vị trí trình bày nằm ngoài phạm vi vì bản chữ không mang bố cục.

## 15 luật

| Mã | Kiểm gì | Căn cứ (Phụ lục I, Phần I của NĐ 30/2020) |
| --- | --- | --- |
| L01 | Có Quốc hiệu đầy đủ | Mục II.1 |
| L02 | Có Tiêu ngữ | Mục II.1.b |
| L03 | Có dòng "Số:" | Mục II.3.c: sau từ "Số" có dấu hai chấm |
| L04 | Ký hiệu đúng cấu trúc | Mục II.3.b |
| L05 | Có địa danh, ngày tháng năm ở phần đầu | Mục II.4.b |
| L06 | Dòng tên loại viết hoa | Mục II.5.b: tên loại trình bày bằng chữ in hoa |
| L07 | Công văn có trích yếu "V/v" | Mục II.5.b |
| L08 | Công văn có "Kính gửi" | Mục II.9 |
| L09 | Có "Nơi nhận" | Mục II.9 |
| L10 | Nơi nhận có "Lưu: VT" | Mục II.9.d |
| L11 | Có quyền hạn người ký (TM., KT., TL., TUQ.) và chức vụ | Mục II.7.b |
| L12 | Nội dung kết thúc bằng "./." | **Chưa xác minh.** Không tìm thấy trong Phụ lục I; có thể chỉ là cách trình bày theo mẫu |
| L13 | Tiêu ngữ: chữ cái đầu mỗi cụm viết hoa | Mục II.1.b |
| L14 | Ký hiệu mang chữ viết tắt tên loại | Mục II.3.b |
| L15 | Ngày dưới 10 và tháng 1, 2 có số 0 ở trước | Mục II.4.b |

Cột căn cứ đã đối chiếu ngày 24/11/2026 với bản Phụ lục I đăng trên trang của Trường ĐHSP Hà Nội 2 (hcmyu.hpu2.edu.vn) và bản của Thư viện Pháp luật. Đây là bản đăng lại, chưa phải Công báo. L12 chưa tìm được căn cứ: trước khi công bố phải tìm ra điều khoản, hoặc hạ L12 thành luật khuyến nghị và loại khỏi điểm chính.

**Phát hiện thêm khi đối chiếu:** mục II.3.c còn yêu cầu số văn bản nhỏ hơn 10 phải có số 0 ở trước (ví dụ "Số: 05/..."). Bộ luật chưa kiểm điều này.

## Phép thử 1 · lỗi cài (đo độ bắt lỗi)

Mỗi bộ gồm 20 văn bản thật đã đạt mọi luật, mỗi văn bản được cài đúng một lỗi thuộc 11 kiểu.

| Bộ | Bắt đúng | Cờ thừa | Ghi chú |
| --- | --- | --- | --- |
| Lượt đầu, 12 luật bản 1 | 11/20 | 0 | Sót các kiểu: hoa thường Tiêu ngữ, ký hiệu đảo, ngày dạng số, ngày thiếu số 0, tên loại viết thường. Lượt này có 2 văn bản cài hỏng (lỗi cài rơi ngoài chỗ luật áp dụng), đã dựng lại bộ |
| Bộ dùng để chỉnh luật (seed 11), bản 2 | 19/20 | 0 | Không tính làm kết quả vì luật được chỉnh trên chính bộ này |
| Giữ riêng, seed 99 | 19/20 | 0 | |
| Giữ riêng, seed 2026 | 19/20 | 0 | |
| Giữ riêng, seed 7 | 20/20 | 0 | |

Hai lỗi sót ở bộ giữ riêng cùng một kiểu: ngày ban hành viết dạng số ("Hà Nội, 18/02/2025") nhưng trích yếu ngay dưới có một ngày viết chữ của văn bản khác, làm L05 tưởng đã có ngày. Chưa sửa, để lại làm giới hạn đã biết.

**Giới hạn của phép thử:** 11 kiểu lỗi do chính người dựng luật nghĩ ra. Lỗi thật của người soạn hoặc mô hình sẽ đa dạng hơn; con số 58/60 là trần, không phải ước lượng ngoài thực tế.

## Phép thử 2 · 20 văn bản thật ngẫu nhiên (đo báo nhầm)

20 văn bản rút ngẫu nhiên từ 6.294 (seed 30). Máy báo 13 cờ trên 10 văn bản. Người xác nhận mô phỏng đọc ngữ cảnh từng cờ:

| Phân loại | Số cờ |
| --- | --- |
| Lỗi thể thức thật của văn bản | 0 |
| OCR làm mất hoặc méo chữ (Nơi nhận, chức vụ người ký, "./.", "V/v") | 10 |
| Không kết luận được nếu không xem ảnh gốc (câu kết không có "./.") | 2 |
| Quy ước riêng của cơ quan (Nghị quyết UBTVQH ghi "Lưu: HC") | 1 |

Trên cả 6.294 văn bản, 45,8% không có cờ nào. Luật báo nhiều nhất là L11 (23,0%) và L12 (14,4%), đúng các chỗ con dấu và chữ ký che chữ.

## Phát hiện phụ

- 100 văn bản mang ký hiệu giấy phép (GP, GPMT...) đang bị xếp loại là công văn trong bộ toàn văn. Cần thêm loại hoặc loại khỏi năm loại văn bản của QĐ-02.
- L15 báo 1,1% văn bản có ngày tháng thiếu số 0 ("ngày 8 tháng 4 năm 2020"). Chữ số đọc rõ nên nhiều khả năng là lỗi thật ở văn bản nguồn; cần người xem ảnh xác nhận vài ca.

## Đề xuất cổng M1

Đạt ở mức pilot (mô phỏng), phạm vi: chấm bản chữ sạch. Để đạt chính thức cần một người kiểm xác nhận 13 cờ ở phép thử 2 và đối chiếu cột căn cứ.
