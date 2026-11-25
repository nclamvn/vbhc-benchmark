# Báo cáo M6b · Phạt lặp và tập huấn luyện v4 (QĐ-13)

Ngày 25/11/2026. Mọi chấm nội dung ở đây do **chuyên gia mô phỏng (AI)** làm, theo QĐ-08.

## 1. Giao thức 1.2: phạt lặp khi giải mã (chỉ áp cho T1)

Cấu hình là `repetition_penalty` 1,1 với cửa sổ 64 token. Các hệ còn lại giữ nguyên cách chấm.

| Hệ | T1 máy 1.1 → 1.2 | Thể thức | Bài sạch | Bài lặp | Sai thời điểm |
|---|---|---|---|---|---|
| Qwen3-8B gốc | 86,5 → 85,2 | 65,5 → 64,1 | 31,7 → 41,5 | 4,9 → 0 | 29,3 → 26,8 |
| Llama-3.1-8B gốc | 79,9 → 85,8 | 58,5 → 60,2 | 51,2 → 73,2 | 17,1 → 4,9 | 19,5 → 14,6 |
| Llama tinh chỉnh (M5) | 86,6 → 93,6 | 74,5 → 81,1 | 41,5 → 58,5 | 41,5 → 7,3 | 12,2 → 17,1 |
| Qwen3 v3 | 94,5 → 97,9 | 80,2 → 89,4 | 48,8 → 65,9 | 29,3 → 2,4 | 9,8 → 17,1 |
| **Qwen3 v4** | 94,8 → 96,7 | 80,7 → **93,5** | 39,0 → 63,4 | 39,0 → **0** | 14,6 → 14,6 |

Phạt lặp có ích nhất với mô hình đã tinh chỉnh, vì đó là những mô hình hay lặp. Bộ kiểm lặp hiện chỉ đếm chuỗi 8 âm tiết, nên chưa bắt được khối căn cứ bị lặp nguyên khối (thấy ở một bài của v3).

## 2. Bản v4 (vòng 900, tiếp từ v3 trên tập m6b)

- **Điểm máy theo giao thức 1.1:**
  - Tổng hợp 71,8 (v3: 71,3).
  - T1 94,8, T3 99,3.
  - T2 21,3. Bản v4 vẫn trả `thieu_ket_thuc` cho 81/94 câu, nên dạng đối chứng **không** sửa được thiên lệch này.
- **Sai thời điểm theo giao thức 1.2:** 14,6%, còn v3 là 17,1%. Mức giảm nhỏ, nên chưa thấy rõ nhiệm vụ phụ T4 có chuyển sang bài soạn hay không.

## 3. Chấm mù nội dung T1 (giao thức 1.2, cùng một phiên)

Chấm trên 13 đề như M5, 26 bài, xáo bằng seed 626262.

| Hệ | A | B | C | D | Tổng /8 | Bài ≥ 6/8 | Bài D = 0 |
|---|---|---|---|---|---|---|---|
| Qwen3-8B gốc (1.2) | 1,31 | 0,69 | 1,31 | 0,62 | 3,92 | 23% | 7 |
| **Qwen3 v4 (1.2)** | **1,46** | **1,46** | **1,46** | 0,54 | **4,92** | **38%** | 7 |

Đối đầu theo từng đề: v4 thắng 8, hòa 1, thua 4. Phép thử dấu hai phía cho p ≈ 0,39, nên mức chênh **chưa có ý nghĩa thống kê** với 13 đề.

## 4. Kết luận theo điều kiện nhận của QĐ-13

| Điều kiện | Qwen3 gốc | v4 | Đạt |
|---|---|---|---|
| Tổng hợp máy (1.1) | 60,5 | 71,8 | ✓ |
| Bài sạch (1.1 / 1.2) | 31,7 / 41,5 | 39,0 / 63,4 | ✓ |
| Nội dung chấm mù, cùng giao thức 1.2 | 3,92 | 4,92 | ✓ |

**v4 đạt cả ba điều kiện.** Đây là mô hình cơ sở của pilot, với điều kiện ghi kèm là T1 phải giải mã theo giao thức 1.2. Nếu giải mã tham lam (1.1), v4 lặp ở 39% số bài, nên không nên dùng cách đó.

**Điểm yếu còn lại, cần công bố rõ:**
1. **Bịa vẫn là lỗi lớn nhất.** Tiêu chí D của v4 là 0,54, không tốt hơn bản gốc. Có ba kiểu hay gặp:
   - NĐ 30/2020 ghi sai ngày và sai nội dung;
   - một dãy nghị định cùng ngày ban hành;
   - họ tên lãnh đạo tỉnh.
2. **Vẫn áp tên bộ mới cho văn bản cũ**, ví dụ Bộ NN&MT, Bộ GTVT sau 3/2025.
3. **T2:** luật viết tay (95,7) vẫn là lời giải đúng. Mô hình không nên dùng cho nhiệm vụ này.

## 5. Giới hạn

- Người chấm là AI, nên chưa phải chấm độc lập.
- Mỗi hệ có 13 đề, và mức chênh chưa có ý nghĩa thống kê.
- Ba phiên chấm (M5, M6, M6b) được so trong cùng bảng, nhưng thang điểm giữa các phiên có thể lệch. Vì vậy so sánh chính thức chỉ dùng hai hệ chấm trong cùng phiên M6b.
- Checkpoint được chọn theo val loss trên 60 ví dụ, mà chuỗi val loss dao động mạnh (0,92–1,08).
