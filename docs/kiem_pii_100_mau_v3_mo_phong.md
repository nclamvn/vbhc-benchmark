# Kiểm thông tin cá nhân trên 100 mẫu v3 · lượt mô phỏng

- **Ngày:** 21/11/2026 · **Người làm:** chuyên gia mô phỏng (AI, Claude), theo QĐ-08. Không phải lượt kiểm của người.
- **Mẫu:** 100 văn bản rút ngẫu nhiên từ 6.294 văn bản v3 (seed 100): 77 trung ương, 12 Hưng Yên, 11 Thái Nguyên.
- **Cách làm:** máy gom 446 đoạn đáng ngờ theo lưới rộng hơn bộ che (họ tên theo 80 họ phổ biến không kèm chức vụ, dãy 9–12 chữ số, số điện thoại, email, tài khoản, biển số, nơi ở, ngày sinh); AI đọc ngữ cảnh từng nhóm và phân loại. Danh sách đoạn: `meta/pii_review_v3_ung_vien.json`.
- **Giới hạn:** AI đọc các đoạn do lưới bắt được, không đọc trọn 100 văn bản. Tên riêng nằm ngoài lưới họ và không kèm "ông/bà" có thể lọt.

## Kết quả

| Loại | Số | Nhận định |
| --- | --- | --- |
| Thông tin cá nhân của người dân còn sót | 0 | Không thấy trong các đoạn đã đọc |
| Địa danh, tên tổ chức bị lưới bắt nhầm | khoảng 400 | Thái Nguyên, Thái Bình, Hà Nội, Hồ Chí Minh, Đoàn Thanh niên... Không phải tên người |
| Tên người ký, lãnh đạo, nơi nhận | khoảng 35 | Giữ theo QĐ-03 |
| Mã số doanh nghiệp, mã dự án | 2 | Thông tin doanh nghiệp, không phải cá nhân |
| Biểu mẫu trống có dòng "Sinh ngày" | 1 | Không có dữ liệu |

## Bốn điểm cần đầu mối quyết

1. **Che thừa, trái QĐ-03.** Hai quyết định bổ nhiệm (940/QĐ-TTg, 1178/QĐ-TTg) bị che 5 tên cán bộ vì đứng sau "ông". QĐ-03 nói giữ tên cán bộ. An toàn nhưng làm mất dữ liệu.
2. **Liệt sĩ có quê quán.** 1636/QĐ-TTg nêu họ tên, cấp bậc và quê quán đến cấp xã của một liệt sĩ. Văn bản vinh danh công khai; đề xuất giữ, cần quyết.
3. **Lỗ hổng luật che.** Mẫu "ông, "Trần Văn Tuần" (OCR chèn dấu phẩy và ngoặc kép) không bị che. Trường hợp này là cán bộ nên không lộ gì, nhưng người dân viết kiểu đó sẽ lọt.
4. **Tên tắt người soạn thảo** ở dòng "Lưu:" (ví dụ Tungnt, Huyenntt, DungDQ) còn nguyên. Là công chức, rủi ro thấp.
