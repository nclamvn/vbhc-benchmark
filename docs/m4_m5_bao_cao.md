# Báo cáo M4–M5 · Tinh chỉnh mô hình nhỏ và chấm trên VBHC-Bench pilot

Ngày 24/11/2026. Bộ chấm phiên bản 1.1. Toàn bộ đầu ra, điểm và nhật ký nằm trong `ket_qua/pilot_2026-11-24/`.

Mọi cổng người trong chặng này đều do **chuyên gia mô phỏng (AI)** làm, theo QĐ-08. Không có người chấm thật nào tham gia.

## 1. Đã chạy gì

| Hệ | Máy | Cách làm |
|---|---|---|
| moc_luat | container | Luật viết tay, không mô hình |
| qwen25_05b_goc | container CPU, 2 nhân | Qwen2.5-0.5B-Instruct, giải mã tham lam |
| qwen25_05b_tinh_chinh | container CPU | LoRA r16/α32, 150 bước, tích lũy 4, LR 2e-4 cosine, MAX_LEN 1024; khoảng 65 giây/bước |
| qwen3_8b_goc | Mac M1 Max 32 GB, MLX 4-bit | Qwen3-8B |
| llama31_8b_goc | Mac, MLX 4-bit | Meta-Llama-3.1-8B-Instruct |
| llama31_8b_tinh_chinh | Mac, MLX 4-bit | QLoRA 8 lớp, 600 vòng, batch 1, max-seq 3072, mask-prompt; khoảng 7,5 giây/vòng; chấm 5–8 giây/mục |

Gemma-3-12B không chạy được vì máy hết dung lượng đĩa (QĐ-11).

## 2. Bảng điểm máy (bộ chấm 1.1)

| Hệ | T1 máy | T1 thể thức | T2 | T3 | T3 trích yếu | Tổng hợp |
|---|---|---|---|---|---|---|
| moc_luat | 0 | 0 | 95,7 | 86,7 | 56,2 | 60,8 |
| qwen25_05b_goc | 64,3 | 43,9 | 4,3 | 21,1 | 23,9 | 29,9 |
| qwen25_05b_tinh_chinh | 55,9 | 45,7 | 18,1 | 95,2 | 90,6 | 56,4 |
| qwen3_8b_goc | 86,5 | 65,5 | 9,6 | 85,5 | 62,7 | 60,5 |
| llama31_8b_goc | 79,9 | 58,5 | 12,8 | 84,3 | 87,4 | 59,0 |
| **llama31_8b_tinh_chinh** | **86,6** | **74,5** | 17,0 | **98,2** | **96,0** | **67,3** |

## 3. Chấm nội dung T1 (mô phỏng, mù)

Có 13 đề, chọn theo loại văn bản, mỗi đề chấm 5 hệ, tổng cộng 65 bài. Bài được xáo bằng seed 424242 và mã hoá P001–P065. Người chấm chỉ mở khoá giải mã sau khi chấm xong cả 65 bài.

Có 4 tiêu chí, mỗi tiêu chí 0–2 điểm (theo `docs/huong_dan_cham_T1.md`):

- **A:** đúng việc
- **B:** đúng vai và thẩm quyền
- **C:** văn phong
- **D:** không bịa

Điểm trung bình mỗi hệ, trên 13 bài:

| Hệ | A | B | C | D | Tổng /8 | Bài ≥ 6/8 | Bài D = 0 |
|---|---|---|---|---|---|---|---|
| qwen25_05b_goc | 0,00 | 0,00 | 0,08 | 0,62 | 0,69 | 0% | 7 |
| qwen25_05b_tinh_chinh | 0,00 | 0,00 | 0,00 | 0,08 | 0,08 | 0% | 12 |
| qwen3_8b_goc | 1,54 | 1,00 | 1,46 | 0,69 | **4,69** | **46%** | 6 |
| llama31_8b_goc | 1,23 | 1,00 | 0,77 | 0,62 | 3,62 | 8% | 7 |
| llama31_8b_tinh_chinh | 0,85 | 1,00 | 0,62 | 0,85 | 3,31 | 23% | **4** |

Chi tiết từng bài: `diem_T1_mo_phong.jsonl`. Khoá giải mã: `khoa_giai_ma_T1.json`.

## 4. Đọc kết quả

1. **Điểm máy và điểm nội dung T1 lệch nhau.**
   - Llama tinh chỉnh đứng đầu điểm máy T1 (86,6, thể thức 74,5).
   - Về nội dung, nó thua chính Llama gốc, và thua Qwen3-8B gốc rõ rệt.
   - Tinh chỉnh dạy được khuôn văn bản (số, ký hiệu, ngày, kính gửi). Tinh chỉnh chưa dạy được việc viết đúng nội dung.
   - Bài học: không được chọn mô hình T1 chỉ theo điểm máy.
2. **Bịa là lỗi phổ biến nhất ở mọi hệ.** Không hệ nào đạt D trung bình trên 0,9. Có ba kiểu bịa chính:
   - Gán sai nội dung cho Nghị định 30/2020.
   - Bịa số hiệu nghị quyết và công văn (169/NQ-CP xuất hiện ở nhiều hệ).
   - Ghi sai người ký (Chủ tịch nước thay Thủ tướng; Nguyễn Xuân Phúc ký văn bản năm 2024–2025).

   Tinh chỉnh Llama giảm số bài D = 0 từ 7 xuống 4.
3. **Mô hình 0,5B sụp đổ ở T1 sau tinh chỉnh.** 12/13 bài bị lặp hoặc lạc đề. Nguyên nhân có thể nhất:
   - Có ít mẫu T1 nguyên vẹn (94).
   - Văn bản đích còn nhiễu OCR.

   Ngược lại, T3 tăng từ 21,1 lên 95,2.
4. **T3 tăng một phần do cùng phân bố.** Đáp án và đích huấn luyện đều lấy từ trường chỉ mục của cổng. Vì vậy 98,2 không phải bằng chứng tổng quát hoá.
5. **T2 (phát hiện lỗi thể thức): luật viết tay vẫn vượt xa mọi mô hình (95,7 so với ≤ 18,1).**
   - Qwen3 và Llama có thiên lệch chọn mã đầu danh sách.
   - 0,5B tinh chỉnh trả KHONG_LOI cho 88/94 mục.
   - Với nhiệm vụ này, luật là lời giải đúng. Mô hình chỉ nên đứng sau luật.
6. **Kiến thức sau mốc huấn luyện.** Nhiều bài vẫn dùng tên bộ cũ (GTVT, NN&PTNT, LĐTBXH) và cấp huyện, dù yêu cầu ghi ngày 2025–2026. Đây là lỗi mà dữ liệu năm 2025–2026 trong kho có thể sửa nếu đưa vào huấn luyện.

## 5. Giới hạn cần nói rõ

- **Người chấm là AI, cùng họ với mô hình viết hướng dẫn chấm.** Đây không phải chấm độc lập. Văn phong có thể làm lộ danh tính hệ dù bài đã xáo, ví dụ markdown đậm của Qwen3 hay mẫu "Chủ tịch nước Thủ tướng Chính phủ" của Llama tinh chỉnh.
- **Mẫu nhỏ:** 13 đề mỗi hệ, nên khoảng tin cậy rộng. Khác biệt giữa Llama gốc và Llama tinh chỉnh (3,62 so với 3,31) nằm trong nhiễu.
- **Lệch so với kế hoạch:**
  - Llama được chọn tinh chỉnh theo bộ chấm 1.0. Theo bộ chấm 1.1, Qwen3 xếp trên (QĐ-11).
  - Không tinh chỉnh Qwen3. Không chạy được Gemma.
  - Val loss của Llama thấp nhất ở vòng 300 (0,771) rồi dao động lên 1,07. Adapter cuối (vòng 600) được dùng, có thể đã quá khớp.
- **Không tìm được căn cứ pháp lý cho L12 ("./.")** trong Phụ lục I. Điểm thể thức có dùng luật này.

## 6. Việc tiếp theo đề xuất

1. **M6:** đóng gói, rồi để một người khác chạy lại độc lập từ clone sạch.
2. **Có người thật chấm lại 65 bài T1**, so với bản mô phỏng (Cohen's κ). Đây là bước kiểm tính trung thực duy nhất còn thiếu.
3. **Tinh chỉnh Qwen3-8B** với adapter ở vòng 300, kèm bộ T1 đã làm sạch OCR và thêm văn bản 2025–2026.
4. **Tách T3 khỏi chỉ mục cổng**, dùng đáp án gán tay trên toàn văn, để đo tổng quát hoá thật.
5. **Giải phóng đĩa Mac** để chạy Gemma-3-12B.
