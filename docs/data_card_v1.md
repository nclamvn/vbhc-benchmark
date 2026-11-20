# Bộ dữ liệu văn bản hành chính, vòng tinh lọc 1

Ngày chụp nguồn: 20/11/2026. Người dựng: Nguyễn Cảnh Lâm, cùng Claude. Phương pháp: cào, lọc, làm giàu theo quy trình tinh lọc, chạy năm vòng chính và ba vòng soát bổ sung.

## Bộ dữ liệu gồm gì

| Tệp | Nội dung | Số dòng |
| --- | --- | --- |
| `chi_muc_van_ban_2020_2026.csv` | Chỉ mục mọi văn bản trên Hệ thống văn bản của Cổng TTĐT Chính phủ, ban hành từ 05/3/2020 (ngày Nghị định 30/2020 có hiệu lực) đến 20/11/2026 | 20.253 |
| `toan_van_1132_van_ban.jsonl` | Toàn văn (đã che liên lạc) của 1.132 văn bản hành chính, mẫu phân tầng theo loại và năm | 1.132 |
| `doi_chieu_toan_van.csv` | Kết quả đối chiếu chỉ mục với toàn văn và tên tệp, từng văn bản | 1.132 |
| `can_nguoi_xem.csv` | Các trường hợp máy không tự kết luận được, cần người xem | 151 |
| `loai_bo.csv` | Văn bản bị loại, kèm bước và lý do | 4 |
| `goi_kiem_lai.zip` | Mã nguồn, engine tinh lọc, toàn bộ bản chụp HTML, claims có dẫn chứng, manifest tải tệp | — |

## Nguồn và điều kiện dùng lại

- Nguồn duy nhất của vòng này: vanban.chinhphu.vn (danh sách) và datafiles.chinhphu.vn (tệp gốc ký số). Khi dùng lại phải ghi nguồn "Cổng Thông tin điện tử Chính phủ".
- Văn bản quy phạm pháp luật và văn bản hành chính không thuộc đối tượng bảo hộ quyền tác giả (khoản 2 Điều 15 Luật Sở hữu trí tuệ, giữ nguyên sau Luật 131/2025/QH15).
- vbpl.vn (403) và moha.gov.vn (ngắt kết nối) chặn truy cập tự động từ máy làm việc, nên chưa có trong vòng này.

## Quy trình đã chạy

1. **Chụp nguồn.** 407 trang danh sách, mỗi trang lưu nguyên HTML kèm SHA-256 và thời điểm chụp. Nhịp 1 yêu cầu/giây.
2. **Trích có dẫn chứng.** Mỗi giá trị trong chỉ mục gắn với đoạn HTML gốc nguyên văn. Loại văn bản suy từ cấu trúc ký hiệu (Nghị định 30 cho văn bản hành chính; có năm trong ký hiệu là văn bản quy phạm).
3. **Tải toàn văn mẫu.** 1.136 tệp PDF (801 MB), phân tầng đều theo năm 2020–2026 trong từng loại.
4. **Bóc chữ.** Đa số tệp là bản quét. OCR tesseract tiếng Việt 200 dpi cho trang 1, 2 và trang cuối, nơi có đủ các thành phần thể thức. 45 tệp có lớp chữ dùng bảng mã cũ (mất dấu) được phát hiện và OCR lại.
5. **Làm sạch.** Bỏ dấu ký số và dấu "đến" của Cổng (5.325 mảnh); che 8 email và 22 số điện thoại; khử trùng y hệt và gần trùng (MinHash, ngưỡng 0,9); loại 4 văn bản có độ tin OCR dưới 70.
6. **Đối chiếu ba kênh.** Chỉ mục, toàn văn và tên tệp được so với nhau cho số ký hiệu và ngày ban hành.
7. **Kiểm độc lập.** Engine tinh lọc dựng registry 20.253 thực thể từ 142.916 claims, build hai lần cho cùng byte, auditor dựng lại khớp. Bộ răng tiêm lỗi chứng minh cả 6 cổng áp dụng cho domain này đều cắn (chạy trên domain mẫu 300 thực thể, cùng engine).

## Số liệu chính (đếm lại độc lập bằng `audit_stats.py`)

**Chỉ mục 20.253 văn bản:** hành chính 11.360; quy phạm 6.884; hợp nhất 2.000; chưa rõ 9.

**Toàn văn 1.132 văn bản:** quyết định cá biệt 300; công văn 299; thông báo 200; chỉ thị 100; công điện 100; nghị quyết cá biệt 99; kế hoạch 18; báo cáo 10; hướng dẫn 6. Mỗi năm 2020–2026 có 160–165 văn bản; 900 trước và 232 sau 01/7/2025. Tổng khoảng 4,95 triệu ký tự; độ tin OCR trung bình 92,3.

**Đối chiếu số ký hiệu chỉ mục với toàn văn:**

| Kết quả | Số văn bản | Ý nghĩa |
| --- | --- | --- |
| Khớp | 581 | Số trong toàn văn trùng chỉ mục |
| Gần khớp | 101 | Lệch 1 ký tự, gần như chắc do OCR |
| Không đọc được | 361 | Số viết tay hoặc đóng dấu, OCR không đọc ra |
| Khác | 89 | Số đọc được nhưng khác; đa số là OCR đọc nhầm chữ số viết tay |

Số trong tên tệp khớp chỉ mục ở 1.118/1.132 văn bản; ngày ban hành tìm thấy trong toàn văn ở 621 văn bản. Trong registry có 1.158 ô được hai nguồn xác nhận và 1 ô tranh chấp được giữ nguyên: chỉ mục ghi 3170/BTL-VP, nhưng cả toàn văn lẫn tên tệp đều là 1086/QĐ-TTg.

## Phát hiện phụ có ích cho bộ đánh giá

- 42 ký hiệu trong chỉ mục trình bày sai (khoảng trắng quanh "/", gạch dưới, "QD" thiếu dấu), 6 ký hiệu dùng chữ "Ð" (Latin) thay cho "Đ". Đây là mẫu lỗi thật, dùng được cho tác vụ rà soát.
- Số và ngày trên văn bản hành chính thường được viết tay sau khi ký. Bộ đánh giá không nên chấm số và ngày từ OCR; nên lấy từ chỉ mục, có đối chiếu tên tệp.

## Giới hạn đã biết

- Một nguồn, một cấp: chỉ văn bản trung ương trên Cổng Chính phủ. Chưa có văn bản cấp tỉnh, cấp xã. Không có tờ trình; báo cáo chỉ có 10.
- "Hai nguồn xác nhận" ở đây là chỉ mục và tệp gốc của cùng một cơ quan đăng tải. Nó chứng minh chỉ mục khớp bản gốc, chưa phải hai bên độc lập.
- OCR mới làm trang 1, 2 và trang cuối. Phần giữa của văn bản dài chưa có.
- Còn khoảng 17 mảnh dấu Cổng bị OCR đọc quá méo nên chưa gỡ được; còn lỗi OCR rải rác trong thân văn bản.
- Họ tên người ký được giữ nguyên, vì là thông tin công vụ công khai và là một thành phần thể thức. Kế hoạch M2 ghi thay bằng chỗ giữ chỗ; việc này cần anh quyết.
- Mốc M2 đặt mục tiêu khoảng 5.000 văn bản từ ít nhất 10 nguồn. Vòng này đạt 1.132 văn bản toàn văn và 20.253 dòng chỉ mục, từ 1 nguồn.

## Cách kiểm lại

```bash
unzip goi_kiem_lai.zip && cd engine
python3 refinery.py domains/vbhc_chinhphu | tail -3   # khoảng 6 phút; phải ra "VALIDATION PASSED"
python3 bites.py domains/vbhc_sample                   # mọi răng phải cắn
python3 ../scripts/audit_stats.py                      # cần thư mục data/ của vòng chạy; số phải khớp bảng trên
```
