# Báo cáo M7 và M7b · nâng chất lượng mô hình bằng tra cứu

Ngày 27/11/2026. Quyết định liên quan: QĐ-15, QĐ-16, QĐ-17. Các bước cần người do **chuyên gia mô phỏng (AI)** làm (QĐ-08).

## 1. Câu hỏi

v4 bịa viện dẫn: theo giao thức 1.3, mỗi bài có 1,46 viện dẫn sai, phần lớn sai ngày. M7 thử hai hướng:

1. **Tra cứu:** đưa vào lời yêu cầu danh sách văn bản quy phạm có thật, ban hành trước ngày soạn, kèm bảng bộ máy theo ngày.
2. **Nâng cỡ mô hình:** đo Qwen3-14B và Qwen3-30B-A3B bản gốc.

## 2. Bộ tra cứu (`scripts/tra_cuu.py`)

- Bản đầu chỉ xếp theo độ gần với trích yếu, phủ được 7,3% căn cứ thật. Văn bản thật dẫn căn cứ theo lĩnh vực và cơ quan, không theo chữ trong trích yếu.
- Bản dùng thêm nguồn **đồng viện dẫn**: lấy 30 văn bản huấn luyện có trích yếu gần nhất và các căn cứ chúng đã dẫn. Chỉ dùng tập huấn luyện và chỉ mục công khai.
- **Phủ trên 57 căn cứ thật của 41 đề T1:** 65,9% ở k=8. Một phần ba căn cứ đúng không có trong tư liệu.

## 3. Kết quả chính (41 đề T1)

| Hệ | Giao thức | Bài sạch | Viện dẫn sai mỗi bài | Thể thức | Căn cứ đúng chỗ | Phủ căn cứ | Nội dung /8 (phiên M7) |
|---|---|---|---|---|---|---|---|
| v4 | 1.3 | 63,4% | 1,46 | 91,2 | 31,6% | 21,1% | — |
| Qwen3-14B gốc | 1.3 | 65,9% | 0,15 | 73,5 | 0% | 0% | — |
| Qwen3-30B-A3B gốc | 1.3 | 58,5% | 0,32 | 72,0 | 0% | 0% | — |
| Qwen3-8B gốc | 2.0 | 36,6% | 0,63 | 66,0 | 11,9% | 42,1% | 3,77 |
| Qwen3-14B gốc | 2.0 | 63,4% | 0,29 | 73,5 | 14,6% | 43,9% | — |
| v4 | 2.0 | 78,0% | 0,27 | 84,9 | 20,7% | 49,1% | 3,92 |
| v5 | 2.0 | 90,2% | 0,00 | 90,9 | 25,0% | 1,8% | — |
| v6 | 2.0 | 87,8% | 0,02 | 88,9 | 57,1% | 7,0% | — |
| **v6** | **2.1** | **85,4%** | **0,05** | **88,9** | **50,0%** | **17,5%** | **4,38** |

Đầy đủ ở `BANG_XEP_HANG.md`. "Căn cứ đúng chỗ" và "phủ" so với căn cứ của chính bài thật (`m3/can_cu_tham_chieu_T1.json`).

## 4. Đọc kết quả

1. **Tra cứu chặn bịa mạnh hơn nâng cỡ.** Chỉ thêm tư liệu, chưa huấn luyện lại, v4 đã giảm viện dẫn sai từ 1,46 xuống 0,27 mỗi bài. Hai bản 14B và 30B-A3B gốc nhớ đúng số và ngày hơn, nhưng không trùng căn cứ nào với văn bản thật: chúng dẫn văn bản nổi tiếng, không liên quan đến bài.
2. **Khi cùng có tra cứu, 8B tinh chỉnh thắng 14B gốc ở mọi chỉ số.** Nâng cỡ chỉ đáng làm nếu tinh chỉnh cả bản lớn.
3. **Tra cứu kéo theo chép thừa.** Qwen3-8B gốc chép gần hết danh sách (4,9 viện dẫn mỗi bài, 12% đúng chỗ). Bộ kiểm trung thực tính các viện dẫn này là đúng vì văn bản có thật, nên bài sạch ở 2.0 phải đọc cùng cột "căn cứ đúng chỗ".
4. **v5 học quá tay việc để "…".** Khi dựng tập v5, văn bản cần dẫn thường vắng trong tư liệu, nên mô hình học rằng "để trống là an toàn". v5 chọn đúng văn bản theo mô tả nhưng không chép số, kể cả khi số có trong tư liệu.
5. **v6 (M7b) sửa được một phần.** Tập v6 luôn đưa căn cứ thật vào tư liệu ở 70% bài. Căn cứ đúng chỗ tăng từ 1 lên 4, và lên 10 khi có bước điền 2.1. Nhưng thói quen để "…" qua v3–v5 vẫn mạnh: v6 còn 38 chỗ để trống.
6. **Chấm mù nội dung (phiên M7, 13 đề × 3 hệ):** v6 + 2.1 được 4,38/8, v4 + 2.0 được 3,92, Qwen3 gốc + 2.0 được 3,77. Khác biệt nằm ở tiêu chí "không bịa": v6 có 3 bài điểm 0, v4 có 7, bản gốc có 9. v6 kém ở văn phong (0,92) vì lặp và vì lỗi dữ liệu che tên. Đối đầu từng đề: v6 thắng v4 6–2–5, thắng bản gốc 5–5–3, chưa có ý nghĩa thống kê.

## 5. Lỗi phát hiện trong lượt này

- **Che họ tên che nhầm** (`m7_du_lieu_v5.lam_sach`): "Hà Nội" đứng sau ký hiệu "…/CĐ-TTg" bị coi là họ tên (290 bài huấn luyện), và "Bộ Tài" trong "Bộ trưởng Bộ Tài nguyên…" cũng bị che. Bài của v5, v6 vì thế có "[Họ và tên], ngày…" thay địa danh, và cụm "Bộ trưởng [Họ và tên] nguyên và Môi trường". Sửa ở M8.
- **Bộ chặn lặp không bắt được lặp trong một đoạn dài không xuống dòng trống** (bài M001 của phiên chấm mù lặp một khối căn cứ nhiều lần).
- **v6 lặp 48,8% khi giải mã tham lam không tra cứu.** v6 chỉ dùng kèm 2.0/2.1.

## 6. Quyết định (QĐ-17)

- **Mô hình cơ sở của pilot: v6 + giao thức 2.1.** Đạt 4/5 điều kiện của QĐ-16 và điều kiện nội dung. **Trượt điều kiện phủ căn cứ** (17,5% so với mốc 49%). Bảng công bố ghi rõ điều này và giữ cột v4 + 2.0 để người dùng tự so: v4 dẫn nhiều hơn nhưng 4/5 căn cứ là thừa, v6 dẫn ít nhưng đúng một nửa và để trống phần còn lại cho cán bộ tự điền.
- **Không huấn luyện thêm trước hạn pilot 01/12.**
- **M8 (sau pilot):** sửa lỗi che tên; dựng lại dữ liệu từ v4 hoặc từ bản gốc thay vì tiếp từ v5/v6 để gỡ thói quen để "…"; cân nhắc tinh chỉnh Qwen3-14B kèm tra cứu; người thật chấm lại 26 bài phiên M6b và 39 bài phiên M7.

## 7. Tệp

- Tệp trả lời: `ket_qua/p13/`, `ket_qua/m7/`, `ket_qua/m7b/`.
- Phiếu chấm mù: `ket_qua/m7b/diem_T1_m7.jsonl`, khoá giải mã `ket_qua/m7b/khoa_giai_ma_T1_m7.json`, tổng `ket_qua/m7b/diem_T1_mo_phong_tong.json`.
- Phụ lục cách chấm tiêu chí D khi có tra cứu: viện dẫn văn bản có trong tư liệu nhưng không đúng việc tính tối đa 1 điểm; từ 3 văn bản không đúng việc trở lên, hoặc gán sai nội dung cho một văn bản, tính 0.
- Kiểm tái lập: `VBHC_TOAN_VAN=<toàn văn> bash scripts/kiem_tai_lap.sh` (bước 5–6 dựng lại tập v5, v6).
