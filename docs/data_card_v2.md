# Bộ dữ liệu văn bản hành chính, vòng tinh lọc 2

Ngày chụp nguồn: 20–21/11/2026. Người dựng: Nguyễn Cảnh Lâm, cùng Claude. Vòng 2 mở rộng vòng 1: thêm 4.014 văn bản trung ương, thêm 3 nguồn cấp tỉnh, và thêm bước che thông tin cá nhân của người dân.

## Kết luận về cổng M2

| Tiêu chí cổng M2 | Kết quả | Đạt |
| --- | --- | --- |
| Khoảng 5.000 văn bản sạch | 6.282 văn bản toàn văn | Đạt |
| 100% có nguồn | Mỗi văn bản có URL chỉ mục, URL tệp gốc và SHA-256 tệp | Đạt |
| Kiểm 100 bản ngẫu nhiên, không sót thông tin cá nhân | Máy dò và tôi đọc ngữ cảnh: 0 họ tên, địa chỉ, số định danh, email hay số điện thoại của người dân còn sót | Đạt phần máy; còn chờ người kiểm tay |

Cổng M0 (ít nhất 10 nguồn hợp lệ) vẫn chưa đạt: vòng này dùng 4 nguồn.

## Tệp trong thư mục

| Tệp | Nội dung | Số dòng |
| --- | --- | --- |
| `chi_muc_van_ban_v2_phanNN.csv` | Chỉ mục 4 nguồn, từ 05/3/2020 | 24.874 |
| `toan_van_v2_phanNN.jsonl` | Toàn văn đã làm sạch và che thông tin cá nhân | 6.282 |
| `doi_chieu_toan_van_v2.csv` | Đối chiếu chỉ mục với toàn văn và tên tệp | 6.294 |
| `can_nguoi_xem_v2.csv` | Trường hợp máy không tự kết luận được | 1.213 |
| `loai_bo_v2.csv` | Văn bản bị loại, kèm bước và lý do | 162 |
| `goi_kiem_lai_v2_ma_nguon_claims.zip` | Mã nguồn các vòng, engine, 180.298 claims có dẫn chứng (nén xz) | — |
| `goi_kiem_lai_v2_manifest.zip` | Manifest SHA-256 của mọi trang danh sách và mọi tệp tải về, số liệu kiểm độc lập | — |

Các tệp lớn được chia theo dòng; mỗi phần là một tệp hợp lệ, mở riêng được. Cách ghép: xem `01_CACH_GHEP_CAC_PHAN.txt` (áp dụng như vòng 1).

## Nguồn

| Nguồn | Cấp | Chỉ mục | Toàn văn giữ | Ghi chú |
| --- | --- | --- | --- | --- |
| vanban.chinhphu.vn | Trung ương | 20.253 | 5.107 | robots.txt cho phép toàn bộ |
| thainguyen.gov.vn | Tỉnh | 1.500 | 620 | 150 trang mới nhất; tệp trên kho lưu trữ VNPT |
| hungyen.gov.vn | Tỉnh | 2.301 | 555 | Gồm văn bản tỉnh Thái Bình trước sáp nhập |
| tracuuvanban.quangtri.gov.vn | Tỉnh | 820 | 0 | robots.txt cấm /api/, nơi chứa tệp, nên chỉ lấy chỉ mục |

Khi dùng lại phải ghi nguồn từng cổng. Văn bản hành chính không thuộc đối tượng bảo hộ quyền tác giả (khoản 2 Điều 15 Luật Sở hữu trí tuệ).

## Toàn văn 6.282 văn bản

- **Theo loại:** công văn 2.490; thông báo 1.352; quyết định cá biệt 1.054; công điện 529; nghị quyết cá biệt 456; chỉ thị 262; kế hoạch 91; báo cáo 42; hướng dẫn 6.
- **Theo năm:** 2020: 867; 2021: 838; 2022: 805; 2023: 774; 2024: 1.023; 2025: 1.107; 2026: 868.
- **Theo thời kỳ:** 4.879 trước và 1.403 sau 01/7/2025 (chính quyền hai cấp).
- **Bóc chữ:** OCR tiếng Việt 5.408 văn bản (trang 1, 2 và trang cuối), lớp chữ PDF 874 văn bản (toàn bộ). Độ tin OCR trung bình 92,3. Tổng khoảng 39 triệu ký tự.

## Che thông tin cá nhân

Đã che: 1.323 họ tên người dân (sau "ông/bà/anh/chị…"), 794 địa chỉ, 5 số định danh, 14 ngày sinh, 22 email, 90 số điện thoại. Loại hẳn 23 văn bản mà trích yếu nêu một người dân cụ thể.

Giữ nguyên họ tên cán bộ khi gắn với chức vụ công (người ký, "Phó Thủ tướng…"), vì đây là thông tin công vụ và là thành phần thể thức. Việc này vẫn chờ anh quyết.

Bước che địa chỉ chọn che thừa: một số địa chỉ cơ quan hoặc địa chỉ trang web sau chữ "địa chỉ" cũng bị che.

## Đối chiếu ba kênh

| Số ký hiệu trong toàn văn so với chỉ mục | Số văn bản |
| --- | --- |
| Khớp | 3.753 |
| Gần khớp (lệch 1 ký tự) | 349 |
| Không đọc được (thường viết tay) | 1.840 |
| Khác | 340 |

Số trong tên tệp khớp chỉ mục ở 5.589 văn bản; ngày ban hành tìm thấy trong toàn văn ở 3.997 văn bản. Registry có 7.222 ô được hai nguồn xác nhận và 2 tranh chấp được giữ nguyên để người quyết: 3170/BTL-VP (tệp là 1086/QĐ-TTg) và 2062/PC-VP của Hưng Yên (tệp là Thông tư 19/2022/TT-BNNPTNT).

## Loại bỏ 162 văn bản

70 trùng tệp y hệt (cùng một PDF gắn vào nhiều mục); 49 độ tin OCR dưới 70; 23 về một người dân cụ thể; 11 gần trùng; 8 không phải PDF; 1 nội dung tệp không khớp trích yếu.

## Kiểm độc lập

Engine tinh lọc dựng 24.874 thực thể từ 180.298 claims. Build hai lần cho cùng byte, auditor dựng lại khớp, digest b770eac24328d6fb. Bộ răng trên domain mẫu 300 thực thể: cả 6 cổng áp dụng đều cắn. Số liệu trong tài liệu này được đếm lại bằng `audit_stats_v2.py`, độc lập với các bước dựng.

## Giới hạn đã biết

- Chỉ 2 tỉnh có toàn văn. Thái Nguyên chỉ có văn bản gần đây (150 trang mới nhất). Hưng Yên không có quyết định cá biệt trong mẫu toàn văn.
- Báo cáo (42) và hướng dẫn (6) còn ít; chưa có tờ trình.
- Còn lỗi OCR rải rác và khoảng vài chục mảnh dấu Cổng bị đọc méo.
- "Hai nguồn xác nhận" là chỉ mục và tệp gốc của cùng cơ quan đăng tải, chưa phải hai bên độc lập.
