# Kế hoạch M8 · nâng cấp dataset bằng SOT và các đợt cào lọc có tiêu chuẩn

Lập ngày 27/11/2026 (QĐ-18). Mục tiêu: mô hình xử lý văn bản hành chính tốt hơn v6, chạy hoàn toàn trên MacBook M1 Max 32 GB, không gửi dữ liệu ra ngoài; sau đó tích hợp quét.

Phương pháp: con người xuất hiện ở ba chỗ (rõ mục tiêu, chặt tiêu chuẩn, nghiệm thu đầu ra), cả ba đều cùng AI bàn. Bổ sung: mỗi tiêu chuẩn phải chạy thử trên dữ liệu thật trước khi dùng, và phải có cách đo cùng ngưỡng dừng.

## 1. Bộ tiêu chuẩn

### A. Ràng buộc vận hành (trượt một điều là loại)
Chạy offline; bộ nhớ lúc chạy ≤ 20 GB; soạn một văn bản ≤ 90 giây; giấy phép mô hình cho phép cơ quan nhà nước dùng.

### B. Chất lượng soạn văn bản (41 đề, giao thức 2.1)
| Tiêu chuẩn | v6 | Ngưỡng M8 |
|---|---|---|
| Bài sạch | 85,4% | ≥ 88% |
| Viện dẫn sai mỗi bài | 0,05 | ≤ 0,05 |
| Căn cứ đúng chỗ | 50,0% | ≥ 50% |
| Phủ căn cứ thật | 17,5% | ≥ 40% |
| Thể thức | 88,9 | ≥ 90 |
| Sai thời điểm | 9,8% | ≤ 5% |
| Bài lặp | 0% | 0% |
| Lỗi che tên | có | 0 bài |

### C. Không bịa
Không họ tên người ngoài đề và tư liệu; không số liệu bịa; không dẫn luật hết hiệu lực tại ngày ban hành (cần sổ SOT hiệu lực).

### D. Nhiệm vụ khác
Tìm lỗi thể thức dùng luật viết tay (≥ 95). Trích thông tin ≥ 99.

### E. Mỗi đợt cào lọc (5 lớp)
1. **Chọn nguồn:** cổng chính thức; robots.txt cho phép; ≤ 1 yêu cầu/giây; ghi trước mục tiêu bù chỗ thiếu.
2. **Chụp và truy nguồn:** lưu bản gốc, đường dẫn, ngày cào, mã băm; có bản ghi chỉ mục; chạy lại khớp từng byte.
3. **Làm sạch từng văn bản** (`scripts/kiem_dot_cao.py`): nhiễu chữ ≤ 3% (hiệu chỉnh: ngưỡng 2% loại 24% kho v4, 3% là phân vị 90); trích yếu khớp chỉ mục ≥ 90%; loại trùng; 0 thông tin người dân sót (kiểm tay 100 mẫu); che tên bằng `scripts/m8_lam_sach.py` (qua 12 phép thử, không che địa danh).
4. **Cân bằng tập:** mỗi loại văn bản dùng để soạn ≥ 8%, không loại nào > 35%; văn bản từ 03/2025 ≥ 40%; ≥ 6 cơ quan; một người ký ≤ 3% bài huấn luyện sau khi che.
5. **Nghiệm thu đợt:** độ phủ tra cứu tăng (mục tiêu ≥ 75%); 0 văn bản trùng cụm với bộ đo; mỗi đợt để riêng 10 văn bản mới nhất cho bộ đề mới; báo cáo đợt; **đợt không làm nhích chỉ số nào thì dừng hướng đó**.

### F. Nghiệm thu mô hình
Giữ bộ đo 285 câu; thêm bộ 30 đề chưa thấy; một người thật chấm nội dung 30 bài (≥ 5,0/8, không thua v6); kiểm tái lập khớp từng byte.

## 2. Mốc kho hiện có (đo 27/11, `ket_qua/dot_cao/moc_kho_v4.json`)

- **Lớp 3:** 5.530/6.294 văn bản đạt (87,9%). Loại 624 vì nhiễu, 148 vì không khớp chỉ mục, 11 vì trùng.
- **Lớp 4** (4.430 văn bản thuộc các loại dùng để soạn):

| Chỉ số | Hiện nay | Ngưỡng | Đạt |
|---|---|---|---|
| Công văn | 40,3% | ≤ 35% | ✗ |
| Thông báo | 25,6% | 8–35% | ✓ |
| Quyết định cá biệt | 18,2% | 8–35% | ✓ |
| Công điện | 9,5% | ≥ 8% | ✓ |
| Chỉ thị | 4,9% | ≥ 8% | ✗ |
| Tờ trình / Báo cáo / Kế hoạch | 0% / 0,6% / 0,9% | ≥ 8% | ✗ |
| Từ 03/2025 | 29,0% | ≥ 40% | ✗ |
| Số cơ quan | 61 mã ký hiệu | ≥ 6 | ✓ |
| Người ký nhiều nhất (văn bản thô, trước khi che) | 11,9% | ≤ 3% sau khi che | đo lại trên tập huấn luyện |

- **Phát hiện không cần cào:** kho đã có 262 chỉ thị nhưng tập soạn văn bản v6 không có chỉ thị nào. Đây là lỗi chọn mẫu khi dựng tập, sửa ở M8.1.
- **Chỉ mục trung ương đã có sẵn nhưng chưa lấy toàn văn:** 1.354 quyết định cá biệt và 120 công điện từ 03/2025. Đợt B lấy từ đây, không phải dò cổng mới.
- **Tờ trình, báo cáo gần như không được công bố trên cổng trung ương** (3 báo cáo trong 20.350 dòng chỉ mục). Đợt A phải khảo sát nguồn trước; nếu không có nguồn công khai đủ, đầu mối quyết định hạ ngưỡng hoặc bỏ hai loại này khỏi phạm vi.
- **Mạng:** từ máy làm việc, vanban.chinhphu.vn, thainguyen.gov.vn, hungyen.gov.vn truy cập được; vbpl.vn bị chặn (403), nên sổ hiệu lực văn bản phải lấy nguồn khác hoặc chạy trên máy Mac.

## 3. Các mốc

| Mốc | Việc | Cổng nghiệm thu |
|---|---|---|
| **M8.0** (xong 27/11) | Sổ SOT bộ máy v1 (99 bản ghi, có nguồn từng dòng, có Thủ tướng và Phó Thủ tướng nhiệm kỳ 2026); bộ chấm, bộ tra cứu, dữ liệu T4 cùng đọc một sổ; sửa lỗi che tên; đo mốc kho | Sổ qua 4 phép tiêm lỗi; kiểm tái lập vẫn khớp từng byte; bảng xếp hạng không đổi |
| **M8.1** | Dựng lại tập từ kho hiện có, không cào: đưa chỉ thị vào tập soạn, áp che tên mới, tư liệu dùng sổ SOT v1, dựng lại từ v4 thay vì tiếp v5/v6 | Chỉ thị ≥ 5% tập soạn; 0 "[Họ và tên], ngày"; người ký ≤ 3% |
| **M8.2** | Đợt cào B: lấy toàn văn 1.354 quyết định + 120 công điện từ 03/2025 từ chỉ mục trung ương, qua lớp 2–3 | Văn bản từ 03/2025 ≥ 40%; công văn ≤ 35% |
| **M8.3** | Đợt cào A: khảo sát nguồn tờ trình, báo cáo, kế hoạch (cổng tỉnh, cổng bộ), cào nếu có nguồn hợp lệ | Mỗi loại ≥ 8%, hoặc quyết định hạ ngưỡng có ghi lý do |
| **M8.4** | Đợt cào C: thêm 3–5 tỉnh có robots.txt cho phép | Độ phủ tra cứu ≥ 75% |
| **M8.5** | Sổ SOT hiệu lực cho khoảng 500 văn bản quy phạm hay được dẫn nhất, hai nguồn độc lập, ô mâu thuẫn để tranh chấp | Tiêu chuẩn C3 chạy được trên bộ chấm |
| **M8.6** | Bộ 30 đề mới (văn bản sau ngày chốt dữ liệu) | 30 đề, 0 trùng cụm với dữ liệu huấn luyện |
| **M8.7** | Tinh chỉnh Qwen3-14B 4-bit kèm tra cứu trên tập mới, chấm theo A–F | Đạt A–F, người thật chấm 30 bài |
| M9 | Quét: Tesseract tiếng Việt tầng một, mô hình thị giác 7–8B chạy MLX cho trang xấu | Âm tiết đúng dấu ≥ 98,5%, offline |

Mỗi mốc có một dòng trong `DECISIONS.md` khi đóng, kèm số đo trước và sau.

## 4. Kết quả M8.1 (27/11)

- **Nguyên nhân thiếu chỉ thị, quyết định:** (1) bộ lọc cũ đòi số và ngày trong toàn văn OCR phải đọc được, mà số, ngày thường viết tay hoặc dưới dấu đỏ; (2) đợt OCR cũ chỉ bóc trang 1, 2 và trang cuối, nên văn bản nhiều trang bị thiếu giữa; (3) chỉ thị dài, trung vị 3.425 token, vượt khung 3.000 token.
- **Đã làm, không cào mạng:**
  - `scripts/m8_ocr_du_trang.py`: OCR 972 trang còn thiếu của 424 văn bản (chỉ thị, công điện, quyết định, công văn) từ PDF đã có, khoảng 13 phút.
  - `scripts/m8_kho_v5.py`: kho v5 ghép trang, làm sạch và che như kho v4. 415 văn bản được bù đủ trang; 9 giữ bản cũ vì OCR kém. Máy kiểm: 0 số điện thoại, 0 số định danh, 0 email sót; 2 họ tên còn lại đều là cán bộ trong việc nhân sự (được giữ theo QĐ-03, QĐ-09).
  - `scripts/m8_du_lieu_v7.py`: viết lại dòng số, ngày ở phần đầu theo chỉ mục khi OCR hỏng; che tên M8 (16 phép thử, có xuống dòng giữa chức danh và lỗi OCR "Thú tướng"); tư liệu dùng sổ SOT v1; công văn tối đa 35%.
- **Hai bản tập, chờ đầu mối chọn khung độ dài:**

| | v6 | v7, khung 3.000 token | v7, khung 6.000 token |
|---|---|---|---|
| Bài soạn văn bản | 737 | 858 | **1.484** |
| Công văn | 77% | 35,0% | 35,0% |
| Quyết định | 10% | 28,0% | 25,3% |
| Công điện | 7% | 18,5% | 18,1% |
| Thông báo | 20% | 17,7% | 16,9% |
| Chỉ thị | 0 | 0,8% | **4,7%** |
| Lỗi che tên "[Họ và tên], ngày" | 290 bài | 0 | 0 |
| Tên người ngoài đề nhiều nhất | 21,5% | 1,5% | 1,2% |

- **Cổng M8.1:** lỗi che tên 0 ✓; người ký ≤ 3% ✓; công văn ≤ 35% ✓; chỉ thị ≥ 5% ✗ (4,7% ở khung 6.000; 0,8% ở khung 3.000).
- **Khung 6.000 token** cần huấn luyện với max-seq 6.144 và giải mã tối đa khoảng 4.000 token. Với Qwen3-8B 4-bit vừa máy 32 GB; với Qwen3-14B cần đo bộ nhớ trên Mac trước.
- Kiểm tái lập bước 7: dựng lại kho v5 và cả hai bản v7 khớp từng byte.
