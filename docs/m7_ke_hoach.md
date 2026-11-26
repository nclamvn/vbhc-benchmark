# M7 · Nâng chất lượng mô hình (QĐ-15)

Lập ngày 26/11/2026, xong trước hạn pilot 01/12/2026. Các bước cần người đều do **chuyên gia mô phỏng (AI)** làm, trừ bước 7.6.

## Mục tiêu

Giảm lỗi bịa căn cứ và lỗi sai thời điểm, nhưng không làm mất phần thể thức đã đạt. Hướng chính là tra cứu căn cứ khi soạn (phương án B). Song song, đo nhanh xem tăng cỡ mô hình (phương án A) giúp được bao nhiêu, để quyết định vòng tháng 12.

## Các bước

| Bước | Việc | Chạy ở | Đầu ra |
|---|---|---|---|
| 7.0 | Đo cỡ mô hình: Qwen3-14B và Qwen3-30B-A3B gốc trên 41 đề T1, giao thức 1.3 | Mac, khoảng 1–2 giờ | Có đáng nâng cỡ không |
| 7.1 | Làm sạch nơi nhận, khối ký: che họ tên kèm chức danh, bỏ rác OCR | Container | Mục tiêu T1 sạch hơn |
| 7.2 | Bộ tra cứu: tìm văn bản quy phạm trung ương ban hành trước ngày soạn, xếp theo độ gần với trích yếu. Kèm bảng bộ máy đúng theo ngày ban hành (các bộ, Thủ tướng, số cấp chính quyền, các tỉnh) | Container | `scripts/tra_cuu.py`, độ phủ đo trên văn bản thật |
| 7.3 | Giao thức 2.0: lời yêu cầu T1 kèm khối "tư liệu tra cứu". Giải mã như 1.3. Công bố thành bảng riêng | Container | `chay_mlx.py --tra-cuu` |
| 7.4 | Tập v5: T1 kèm tư liệu tra cứu. Viện dẫn trung ương không có trong tư liệu thì che bằng "…". Cộng T2 và T3 rút gọn | Container | `m7/` |
| 7.5 | Huấn luyện v5 từ v4, khoảng 1 lượt dữ liệu. Chấm theo giao thức 2.0. Có hai mốc so: Qwen3 gốc có tra cứu, và v4 có tra cứu | Mac, khoảng 7–8 giờ | Bảng 2.0 |
| 7.6 | Người thật chấm lại 26 bài đã chấm mù ở M6b, theo `docs/huong_dan_cham_T1.md` | Đầu mối nhờ người | Mức lệch giữa người và AI |
| 7.7 | Chấm mù nội dung mô phỏng: v5 có tra cứu so với Qwen3 gốc có tra cứu, 13 đề | Container | Điểm nội dung |

## Cổng nhận v5 làm mô hình cơ sở của giao thức 2.0

Điều kiện đặt trước khi có kết quả. Phải đạt đủ cả bốn:
1. **Bài sạch** (bộ kiểm trung thực có bắt lặp khối) cao hơn cả Qwen3 gốc có tra cứu và v4 có tra cứu.
2. **Số viện dẫn sai trung bình mỗi bài** không quá một nửa của v4 theo giao thức 1.3.
3. **Điểm thể thức T1** không thấp hơn v4 theo giao thức 1.3 quá 3 điểm.
4. **Chấm mù nội dung** không thua Qwen3 gốc có tra cứu.

Không đạt thì báo đầu mối kèm phân tích. v4 vẫn là mô hình cơ sở theo giao thức 1.3.

## Ngoài M7, để sang tháng 12

- Cào có mục tiêu: chỉ thị và công điện của Thủ tướng, cùng 4–6 tỉnh sau sáp nhập.
- Mở rộng T1 lên khoảng 120 đề. Tách T3 khỏi chỉ mục cổng.
- Huấn luyện ưu tiên chống bịa. Nâng cỡ mô hình, nếu kết quả bước 7.0 cho thấy đáng làm.

Xem `docs/de_xuat_nang_chat_luong.md`.

## Trạng thái phần container (26/11, trước khi chạy Mac)

- **7.1 làm sạch:** trong 737 mục tiêu T1 huấn luyện, 2.347 họ tên kèm chức danh hoặc trong nơi nhận được thay bằng "[Họ và tên]". Tên Thủ tướng đúng theo ngày (có trong tư liệu) được giữ. Bỏ 11 rác OCR "na 4". "Nguyễn Sỹ Hiệp" còn 3/737 bài, trước là 173/804.
- **7.2 bộ tra cứu:** bản đầu chỉ xếp theo độ gần trích yếu, độ phủ 7,3%. Nguyên nhân là văn bản thật dẫn căn cứ theo lĩnh vực và theo cơ quan, không theo chữ trong trích yếu. Bản hai thêm nguồn "đồng viện dẫn": tìm 30 văn bản huấn luyện có trích yếu gần nhất, lấy các văn bản quy phạm trung ương chúng đã dẫn (đã kiểm khớp chỉ mục, ban hành trước ngày soạn). Chỉ dùng tập huấn luyện, không đụng tập kiểm tra.
  - **Độ phủ trên 41 viện dẫn quy phạm trung ương thật của tập kiểm tra:** 63,4% ở k=5, 65,9% ở k=8 (mức dùng), 70,7% ở k=12.
  - Nghĩa là khoảng một phần ba căn cứ đúng vẫn không có trong tư liệu. Ở những chỗ đó, mô hình được dạy để "…" thay vì đoán.
- **7.3 giao thức 2.0:** `chay_mlx.py --tra-cuu`. Cả 41 đề T1 đều được làm giàu, đề dài nhất 1.109 token.
- **7.4 tập v5:** 1.537 ví dụ (T1 737, T2 300, T3 300, T4 200). Khi dựng T1, văn bản đó bị loại khỏi láng giềng đồng viện dẫn của chính nó, để điều kiện giống lúc kiểm tra. 285 viện dẫn trung ương không có trong tư liệu bị che, 238 được giữ. Bỏ 67 bài quá 3.000 token sau khi thêm tư liệu.
- **Phần Mac:** `scripts/chay_m7_mac.sh` gồm 7.0, 1.3, 2.0 và 7.5, khoảng 10–11 giờ.

## Kết quả Mac M7 (26/11, 20:05) và quyết định M7b

- **Giao thức 1.3, T1:** v4 63,4% bài sạch, 1,46 viện dẫn sai mỗi bài; Qwen3-8B gốc 41,5%; Llama gốc 73,2%; Llama tinh chỉnh 65,9%; v3 63,4%.
- **Dò quy mô (1.3, bản gốc):** Qwen3-14B 65,9% bài sạch, 70% viện dẫn đúng số và ngày; Qwen3-30B-A3B 58,5%, 35%. Cả hai trùng 0 căn cứ với văn bản thật: dẫn văn bản nổi tiếng nhưng không liên quan.
- **Giao thức 2.0 (có tra cứu):** Qwen3-8B gốc 36,6% bài sạch, độ chính xác căn cứ 12%; Qwen3-14B gốc 63,4%, 15%; v4 78,0%, 21%, phủ căn cứ thật 49%.
- **v5:** tổng hợp 1.1 là 75,3 (v4 71,8), T2 29,8. Theo 2.0: 90,2% bài sạch, 0 viện dẫn sai, thể thức 90,9. Nhưng phủ căn cứ thật chỉ 1,8%: v5 chọn đúng văn bản theo mô tả rồi để "…" cho số và ngày, kể cả khi văn bản có trong tư liệu (10/12 chỗ). Nguyên nhân là lỗi dựng dữ liệu v5 (văn bản cần dẫn thường vắng trong tư liệu khi huấn luyện).
- **Giao thức 2.1 (thử):** `scripts/dien_can_cu.py` điền số và ngày tất định khi mô tả khớp đúng một văn bản trong tư liệu. v5 + 2.1: 90,2% bài sạch, độ chính xác căn cứ 53,8%, phủ 12,3%.
- **Quyết định:** chưa nhận v5. Làm M7b (QĐ-16).
