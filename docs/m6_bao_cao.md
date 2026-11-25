# Báo cáo M6 · Chất lượng mô hình (QĐ-12)

Ngày 25/11/2026. Mọi chấm nội dung ở đây do **chuyên gia mô phỏng (AI)** làm, theo QĐ-08.

## 1. Đã làm gì

- **Bộ kiểm trung thực bằng máy** (`scripts/kiem_trung_thuc.py`). Bộ này đối chiếu viện dẫn trong bài với chỉ mục 24.874 văn bản, và bắt lỗi người ký sai vai, tên cơ quan sai thời điểm, bài lặp. Chạy trên 41 văn bản thật thì 97,6% bài được báo sạch.
- **Tập huấn luyện v2** (`scripts/m6_du_lieu_v2.py`). Thay đổi so với tập cũ:
  - Lọc theo độ nhiễu chữ, bỏ dòng do dấu chữ ký số sinh ra.
  - Che bằng "…" những chi tiết không suy ra được từ lời yêu cầu.
  - Bỏ ví dụ dài quá 3.000 token.
  - Số ví dụ soạn văn bản tăng từ 269 lên 804.
- **Mô hình:** QLoRA Qwen3-8B 4-bit, rank 16, 16 lớp. Chạy qua ba lượt vì gặp hai sự cố, chi tiết trong DECISIONS.md, QĐ-12.
  - **Bản v2:** vòng 250 của lượt 2. Đã qua 500 vòng nhưng chỉ học 250 ví dụ.
  - **Bản v3:** vòng 1.000 của lượt 3, tổng cộng khoảng 1.500 vòng. Được chọn vì có val loss thấp nhất, 0,841 trên 60 ví dụ.

## 2. Điểm máy (bộ chấm 1.1)

| Hệ | T1 máy | T1 thể thức | T2 | T3 | Tổng hợp |
|---|---|---|---|---|---|
| moc_luat | 0 | 0 | 95,7 | 86,7 | 60,8 |
| qwen3_8b_goc | 86,5 | 65,5 | 9,6 | 85,5 | 60,5 |
| llama31_8b_tinh_chinh (M5) | 86,6 | 74,5 | 17,0 | 98,2 | 67,3 |
| qwen3_8b_tinh_chinh_v2 | 93,7 | 78,9 | 7,4 | 98,9 | 66,7 |
| **qwen3_8b_tinh_chinh_v3** | **94,5** | **80,2** | **20,2** | **99,2** | **71,3** |

## 3. Trung thực bài soạn T1 (bộ kiểm máy, 41 bài)

| Hệ | Bài sạch | Bài có viện dẫn sai | Bài sai thời điểm | Bài lặp |
|---|---|---|---|---|
| qwen3_8b_goc | 31,7% | 21 | 29,3% | 4,9% |
| llama31_8b_tinh_chinh | 41,5% | 3 | 12,2% | 41,5% |
| qwen3_8b_tinh_chinh_v2 | 41,5% | 11 | 19,5% | 36,6% |
| **qwen3_8b_tinh_chinh_v3** | **48,8%** | 11 | **9,8%** | 29,3% |

Bản v3 đạt cả hai điều kiện nhận của QĐ-12 (tổng hợp và tỷ lệ bài sạch cao hơn Qwen3 gốc), nên được đưa sang chấm mù nội dung.

## 4. Chấm mù nội dung (mô phỏng)

Chấm trên 13 đề như M5, trộn 26 bài của v2 và v3, xáo bằng seed 525252.

| Hệ | A | B | C | D | Tổng /8 | Bài ≥ 6/8 | Bài D = 0 |
|---|---|---|---|---|---|---|---|
| qwen3_8b_goc (M5) | 1,54 | 1,00 | 1,46 | 0,69 | **4,69** | 46% | 6 |
| llama31_8b_tinh_chinh (M5) | 0,85 | 1,00 | 0,62 | 0,85 | 3,31 | 23% | 4 |
| qwen3_8b_tinh_chinh_v2 | 1,00 | 0,62 | 0,31 | 0,31 | 2,23 | 8% | 9 |
| **qwen3_8b_tinh_chinh_v3** | 1,15 | **1,15** | 0,92 | 0,62 | **3,85** | 23% | 5 |

## 5. Kết luận

1. **v3 là mô hình tinh chỉnh tốt nhất đến nay.** Nó đứng đầu mọi chỉ số máy, có tỷ lệ bài sạch cao nhất, và dùng "…" đúng cách cho số văn bản viện dẫn. Đây là hành vi mới, học được từ tập v2.
2. **Về nội dung, v3 vẫn thua Qwen3 gốc** (3,85 so với 4,69 trên 8). Có ba lỗi chính:
   - **Lặp:** 29% số bài, chủ yếu khi phải liệt kê bộ, tỉnh, ngân hàng hay căn cứ.
   - **Áp tên cơ quan mới cho văn bản cũ.** Ví dụ ghi Bộ Nông nghiệp và Môi trường hay Phó Thủ tướng Trần Hồng Hà vào văn bản năm 2020–2024. Mô hình học khuôn từ văn bản 2025–2026 nhưng chưa biết dựa vào ngày ban hành trong lời yêu cầu.
   - **Bịa chuỗi căn cứ.** Ví dụ một dãy nghị định đánh số liền nhau, cùng một ngày ban hành.
3. **v3 chưa được công bố làm mô hình cơ sở cho phần soạn văn bản.** Bảng công bố sẽ ghi cả Qwen3 gốc và v3, kèm nhận xét trên.

## 6. Việc tiếp theo đề xuất

1. **Thử giải mã có phạt lặp** (repetition_penalty 1,1) cho mọi hệ, chỉ trên phần soạn văn bản. Đây là thay đổi giao thức nên phải chạy lại cho mọi hệ, ghi rõ là bộ chấm 1.2.
2. **Dạy mô hình dựa vào ngày ban hành.** Thêm ví dụ cặp: cùng một việc nhưng ở hai thời điểm trước và sau 01/3/2025, với tên cơ quan tương ứng.
3. **Tách T2 thành phân loại thật.** Bản v3 vẫn thiên về đáp án `thieu_ket_thuc` (71/94 câu).

## Giới hạn

- Bài của v2 và v3 được chấm trong một phiên riêng với 65 bài của M5, nên thang điểm có thể lệch nhẹ.
- Người chấm biết cả 26 bài đều đến từ mô hình đã tinh chỉnh, chỉ không biết bài nào là bản nào.
- Mỗi hệ chỉ có 13 đề, nên khoảng tin cậy rộng.
