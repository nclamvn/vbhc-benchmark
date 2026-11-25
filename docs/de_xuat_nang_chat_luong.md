# Đề xuất nâng chất lượng mô hình sau pilot (26/11/2026)

## 1. Có cần cào thêm nhiều vòng không?

**Có, nhưng phải cào có mục tiêu, không cào thêm đại trà.** Phần thể thức đã gần bão hòa: v4 đạt 93,5 điểm thể thức theo giao thức 1.2. Có thêm văn bản cùng loại thì cũng không tăng được bao nhiêu. Nhưng tập soạn văn bản (T1) hiện lệch nặng, và chính chỗ lệch này sinh ra các lỗi đã thấy ở lượt chạy thử.

| Đo trên 804 mẫu T1 huấn luyện | Con số | Lỗi tương ứng ở lượt chạy thử |
|---|---|---|
| Văn bản của Văn phòng Chính phủ | 619 (77%) | Mọi văn bản đều mang khối ký, nơi nhận kiểu VPCP |
| Có "PCN Nguyễn Sỹ Hiệp" trong nơi nhận | 173 (21,5%) | Tên này xuất hiện ở 4/6 bài |
| Chỉ thị | 0 | Chỉ thị bị viết thành công điện |
| Công điện | 58 | Khối ký công điện bị lẫn với khối ký của VPCP |
| UBND cấp tỉnh (chủ yếu Thái Nguyên, Hưng Yên) | khoảng 60 | Căn cứ và thẩm quyền cấp tỉnh còn yếu |
| Văn bản 2025–2026 | 300 (37%) | Tên bộ và tên tỉnh mới, cũ bị trộn lẫn |

**Các vòng cào nên làm, theo thứ tự hiệu quả:**
1. **Văn bản của Thủ tướng 2020–2026 trên vanban.chinhphu.vn:** chỉ thị, công điện, quyết định cá biệt. Cổng này đã có quy trình và chỉ mục sẵn, chỉ cần tải thêm toàn văn. Mục tiêu khoảng 300 chỉ thị và công điện.
2. **Thêm 4–6 tỉnh sau sáp nhập** có cổng văn bản cho phép robots, chia đều Bắc, Trung, Nam. Mục tiêu khoảng 600 quyết định cá biệt và thông báo cấp tỉnh. Việc này giảm phụ thuộc vào VPCP, và cho mô hình thấy khối ký "TM. ỦY BAN NHÂN DÂN".
3. **Ưu tiên văn bản có lớp chữ (PDF số)** thay vì bản quét. Bản quét để lại rác như dấu chữ ký số, "na 4", "CHỈ THÍ".
4. **Chỉ mục văn bản quy phạm có ngày, số hiệu, trích yếu và tình trạng hiệu lực**, từ Cơ sở dữ liệu quốc gia về văn bản pháp luật nếu điều khoản sử dụng cho phép. Phần này không dùng để huấn luyện. Nó dùng để tra cứu ở mục 2.2.

Mỗi vòng vẫn đi qua engine refinery như cũ: có chứng nguyên văn, có cổng kiểm, chia tập theo cụm. Mỗi vòng cũng có cổng nhận riêng, gồm số mẫu mới theo loại và theo tỉnh, và độ nhiễu chữ.

## 2. Phương án nâng chất lượng, xếp theo tác động trên chi phí

### 2.1 Làm sạch dữ liệu hiện có (rẻ, làm ngay được)
- **Che họ tên trong khối nơi nhận và khối ký**, ví dụ "PCN Nguyễn Sỹ Hiệp" thành "PCN [Họ và tên]". Bỏ rác OCR như "na 4", "Công TTĐT", "CHỈ THÍ".
- **Giảm trùng khuôn nơi nhận:** mỗi khuôn nơi nhận giống hệt chỉ giữ tối đa N lần.
- **Cân lại tập theo cơ quan và theo giai đoạn**, để VPCP không quá 40%, và văn bản trước, sau 01/3/2025 ngang nhau.

### 2.2 Tra cứu căn cứ khi soạn (giao thức 2.0; tác động lớn nhất đến lỗi bịa)
Mô hình 8B không thể nhớ 25.000 số hiệu cùng ngày ban hành. Lỗi bịa (tiêu chí D chỉ đạt 0,54) gần như không sửa được bằng huấn luyện. Sửa đúng gốc là đưa vào lời yêu cầu khoảng 5–10 văn bản quy phạm liên quan, tra từ chỉ mục theo trích yếu, kèm ngày ban hành. Đưa thêm bảng tên cơ quan đúng theo ngày ban hành. Huấn luyện mô hình chỉ được dẫn văn bản có trong danh sách đó, không có thì để "…".
- **Bộ đo:** thêm một bảng riêng T1-2.0, không trộn với bảng hiện tại. Bộ kiểm trung thực đã có sẵn để chấm.
- **Phần mềm:** đây cũng là kiến trúc thực tế của một trợ lý văn bản cho công chức.

### 2.3 Kiểm sau khi sinh (rẻ, phía phần mềm)
Chạy `kiem_trung_thuc.py` trên bản nháp. Viện dẫn không kiểm được, tên bộ hoặc tỉnh sai thời điểm, và họ tên lãnh đạo đều được tô vàng để người soạn rà. Phần này không làm mô hình giỏi hơn, nhưng làm sản phẩm an toàn hơn.

### 2.4 Huấn luyện ưu tiên chống bịa (trung bình)
Sau khi có giao thức 2.0, dựng các cặp so sánh từ chính đầu ra của mô hình. Bản được chọn là bản không bị bộ kiểm bắt lỗi, hoặc để "…" đúng chỗ. Bản bị loại là bản bịa số hiệu, sai thời điểm hoặc lặp. Sau đó huấn luyện theo DPO hoặc ORPO. mlx-lm chưa có sẵn phần này, nên cần thư viện bổ sung hoặc thuê GPU (Unsloth hỗ trợ DPO).

### 2.5 Mô hình và hạ tầng (khi các bước trên đã làm)
- **Qwen3-14B 4-bit** vừa với máy 32 GB để chạy và để QLoRA, nhưng chậm khoảng gấp đôi.
- **Thuê một GPU** (khoảng một giờ cho mỗi lượt như hiện nay, chạy Unsloth) để thử được nhiều cấu hình hơn trong cùng số ngày.

### 2.6 Đo cho đúng (bắt buộc, chạy song song)
- **Một người thật chấm lại 26 bài đã chấm mù**, để đo mức lệch giữa người chấm và AI chấm.
- **Mở rộng T1 từ 41 lên khoảng 120 đề**, có đủ chỉ thị và công điện, để mức chênh giữa các hệ có ý nghĩa thống kê.
- **Tách T3 khỏi chỉ mục cổng** bằng đáp án gán tay trên toàn văn.

## 3. Lộ trình gợi ý

| Giai đoạn | Việc | Thời gian ước tính |
|---|---|---|
| Trước 01/12 (pilot) | Chạy giao thức 1.3; người thật chấm lại 26 bài; làm sạch nơi nhận | 2–3 ngày |
| Tháng 12, vòng 1 | Cào có mục tiêu (mục 1); tập v5; T1 mở rộng 120 đề | 1–2 tuần |
| Tháng 12, vòng 2 | Giao thức 2.0 có tra cứu căn cứ; kiểm sau khi sinh | 1–2 tuần |
| Tháng 1 | Huấn luyện ưu tiên chống bịa; cân nhắc 14B hoặc GPU thuê | 2 tuần |
