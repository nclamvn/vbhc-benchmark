# Bảng xếp hạng VBHC-Bench · pilot (cập nhật 27/11/2026)

Tính lại bằng `python3 scripts/bang_xep_hang.py` từ các tệp trả lời trong `ket_qua/`. Bộ kiểm tra có 285 câu: T1 soạn văn bản 41 câu, T2 tìm lỗi thể thức 94 câu, T3 trích thông tin 150 câu. Tổng hợp là trung bình đều của ba nhiệm vụ, bộ chấm 1.1, giải mã tham lam.

## Bảng chính (giao thức 1.1)

| # | Hệ | Tổng hợp | T1 | T1 thể thức | T2 | T3 | T1 bài sạch | T1 bài lặp |
|---|---|---|---|---|---|---|---|---|
| 1 | Qwen3-8B v6 tinh chỉnh (mô hình cơ sở, dùng với giao thức 2.1) | **75,9** | 96,4 | 85,0 | 31,9 | 99,5 | 41,5% | 48,8% |
| 2 | Qwen3-8B v5 tinh chỉnh | **75,3** | 96,6 | 85,9 | 29,8 | 99,5 | 46,3% | 29,3% |
| 3 | Qwen3-8B v4 tinh chỉnh | **71,8** | 94,8 | 80,7 | 21,3 | 99,3 | 22,0% | 56,1% |
| 4 | Qwen3-8B v3 tinh chỉnh | **71,3** | 94,5 | 80,2 | 20,2 | 99,2 | 24,4% | 56,1% |
| 5 | Llama-3.1-8B tinh chỉnh | **67,3** | 86,6 | 74,5 | 17,0 | 98,2 | 24,4% | 68,3% |
| 6 | Qwen3-8B v2 tinh chỉnh | **66,7** | 93,7 | 78,9 | 7,4 | 98,9 | 31,7% | 53,7% |
| 7 | Luật viết tay (không mô hình) | **60,8** | 0,0 | 0,0 | 95,7 | 86,7 | — | — |
| 8 | Qwen3-8B gốc | **60,5** | 86,5 | 65,5 | 9,6 | 85,5 | 31,7% | 7,3% |
| 9 | Llama-3.1-8B gốc | **59,0** | 79,9 | 58,5 | 12,8 | 84,3 | 26,8% | 53,7% |
| 10 | Qwen2.5-0.5B tinh chỉnh | **56,4** | 55,9 | 45,7 | 18,1 | 95,2 | 12,2% | 80,5% |
| 11 | Qwen2.5-0.5B gốc | **29,9** | 64,3 | 43,9 | 4,3 | 21,1 | 22,0% | 58,5% |

## Phần soạn văn bản với phạt lặp (giao thức 1.2)

Cấu hình: `repetition_penalty` 1,1, cửa sổ 64 token, chỉ áp cho T1. Bảng này công bố riêng, không trộn vào bảng chính.

| Hệ | T1 | T1 thể thức | Bài sạch | Bài lặp |
|---|---|---|---|---|
| Qwen3-8B v4 tinh chỉnh | 96,7 | 93,5 | 51,2% | 14,6% |
| Qwen3-8B v3 tinh chỉnh | 97,9 | 89,4 | 48,8% | 22,0% |
| Llama-3.1-8B tinh chỉnh | 93,6 | 81,1 | 46,3% | 34,1% |
| Llama-3.1-8B gốc | 85,8 | 60,2 | 46,3% | 41,5% |
| Qwen3-8B gốc | 85,2 | 64,1 | 41,5% | 0,0% |

## Phần soạn văn bản, giao thức 1.3 (phạt lặp + dừng khi lặp nguyên đoạn)

**Căn cứ đúng chỗ:** tỷ lệ viện dẫn văn bản quy phạm trung ương trong bài trùng với văn bản bài thật đã dẫn (`m3/can_cu_tham_chieu_T1.json`). **Phủ:** tỷ lệ căn cứ của bài thật được bài viết dẫn lại.

| Hệ | T1 | Thể thức | Bài sạch | Viện dẫn sai mỗi bài | Sai thời điểm | Lặp | Căn cứ đúng chỗ | Phủ căn cứ |
|---|---|---|---|---|---|---|---|---|
| Llama-3.1-8B gốc | 85,8 | 60,0 | 73,2% | 0,15 | 14,6% | 4,9% | 0,0% | 0,0% |
| Llama-3.1-8B tinh chỉnh | 91,6 | 78,7 | 65,9% | 0,12 | 12,2% | 0,0% | 0,0% | 0,0% |
| Qwen3-14B gốc | 91,7 | 73,5 | 65,9% | 0,15 | 26,8% | 0,0% | 0,0% | 0,0% |
| Qwen3-8B v4 tinh chỉnh | 95,7 | 91,2 | 63,4% | 1,46 | 14,6% | 0,0% | 31,6% | 21,1% |
| Qwen3-8B v3 tinh chỉnh | 97,6 | 88,3 | 63,4% | 0,83 | 22,0% | 2,4% | 16,4% | 15,8% |
| Qwen3-30B-A3B gốc | 90,9 | 72,0 | 58,5% | 0,32 | 17,1% | 0,0% | 0,0% | 0,0% |
| Qwen3-8B gốc | 85,2 | 64,1 | 41,5% | 0,68 | 26,8% | 0,0% | 0,0% | 0,0% |

## Phần soạn văn bản có tra cứu (giao thức 2.0 và 2.1)

Giao thức 2.0: lời yêu cầu T1 kèm 8 văn bản quy phạm tra được (`scripts/tra_cuu.py`, chỉ dùng chỉ mục công khai và tập huấn luyện; phủ 65,9% căn cứ thật) và bảng bộ máy theo ngày ban hành; giải mã như 1.3. Giao thức 2.1: 2.0 cộng bước điền số và ngày tất định, không dùng mô hình (`scripts/dien_can_cu.py`). Đề bài khác bảng chính nên không so trực tiếp với bảng 1.x.

| Hệ | Giao thức | T1 | Thể thức | Bài sạch | Viện dẫn sai mỗi bài | Sai thời điểm | Lặp | Căn cứ đúng chỗ | Phủ căn cứ |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-8B v6 tinh chỉnh | 2.1 | 97,7 | 88,9 | 85,4% | 0,05 | 9,8% | 0,0% | 50,0% | 17,5% |
| Qwen3-8B v6 tinh chỉnh | 2.0 | 97,7 | 88,9 | 87,8% | 0,02 | 9,8% | 0,0% | 57,1% | 7,0% |
| Qwen3-8B v5 tinh chỉnh | 2.1 | 98,1 | 90,9 | 90,2% | 0,00 | 9,8% | 0,0% | 53,8% | 12,3% |
| Qwen3-8B v5 tinh chỉnh | 2.0 | 98,1 | 90,9 | 90,2% | 0,00 | 9,8% | 0,0% | 25,0% | 1,8% |
| Qwen3-8B v4 tinh chỉnh | 2.0 | 96,5 | 84,9 | 78,0% | 0,27 | 9,8% | 0,0% | 20,7% | 49,1% |
| Qwen3-14B gốc | 2.0 | 91,2 | 73,5 | 63,4% | 0,29 | 14,6% | 0,0% | 14,6% | 43,9% |
| Qwen3-8B gốc | 2.0 | 79,8 | 66,0 | 36,6% | 0,63 | 22,0% | 2,4% | 11,9% | 42,1% |

## Chấm mù nội dung T1 (chuyên gia mô phỏng · AI)

Thang 8 điểm, gồm bốn tiêu chí 0–2: đúng việc, đúng vai và thẩm quyền, văn phong, không bịa (`docs/huong_dan_cham_T1.md`). Mỗi hệ có 13 đề. Chỉ so điểm trong cùng một phiên chấm.

| Hệ | Điểm /8 (phiên, giao thức) |
|---|---|
| Qwen3-8B v6 tinh chỉnh (mô hình cơ sở, dùng với giao thức 2.1) | 4,38 (M7, giao thức 2.1) |
| Qwen3-8B v4 tinh chỉnh | 4,92 (M6b, phạt lặp) · 3,92 (M7, giao thức 2.0) |
| Qwen3-8B v3 tinh chỉnh | 3,85 (M6, tham lam) |
| Llama-3.1-8B tinh chỉnh | 3,31 (M5, tham lam) |
| Qwen3-8B v2 tinh chỉnh | 2,23 (M6, tham lam) |
| Qwen3-8B gốc | 4,69 (M5, tham lam) · 3,92 (M6b, phạt lặp) · 3,77 (M7, giao thức 2.0) |
| Llama-3.1-8B gốc | 3,62 (M5, tham lam) |
| Qwen2.5-0.5B tinh chỉnh | 0,08 (M5, tham lam) |
| Qwen2.5-0.5B gốc | 0,69 (M5, tham lam) |

## Cách đọc và giới hạn

- **Bài sạch:** bộ kiểm trung thực bằng máy (`scripts/kiem_trung_thuc.py`) không bắt được lỗi nào. Bộ kiểm đối chiếu viện dẫn với chỉ mục 24.874 văn bản, và bắt người ký sai vai, tên cơ quan sai thời điểm, bài lặp. Chạy trên 41 văn bản thật, bộ kiểm cho 97,6% bài sạch.
- **Chấm nội dung do AI đóng vai**, chưa phải chấm độc lập. Phiên M6b: v4 thắng Qwen3 gốc 8, hòa 1, thua 4 trên 13 đề, p ≈ 0,39. Phiên M7 (có tra cứu): v6 + 2.1 thắng v4 + 2.0 6–2–5, thắng Qwen3 gốc + 2.0 5–5–3; chưa có ý nghĩa thống kê.
- **Mô hình cơ sở v6 phải dùng kèm giao thức 2.1.** Không tra cứu và giải mã tham lam, v6 lặp ở 48,8% số bài. Theo 2.1, v6 trượt điều kiện phủ căn cứ (17,5% so với mốc 49%): v6 thường để "…" cho số căn cứ thay vì chép từ tư liệu. v4 + 2.0 phủ cao hơn nhưng 79% căn cứ là thừa.
- **Lỗi dữ liệu đã biết ở v5, v6:** bước che họ tên che nhầm "Hà Nội" sau ký hiệu "TTg" (290 bài huấn luyện) và chữ "Bộ Tài" trong "Bộ trưởng Bộ Tài nguyên…", nên bài có thể ra "[Họ và tên], ngày…". Sẽ sửa ở M8.
- **T3 cùng phân bố với dữ liệu huấn luyện** (đáp án và dữ liệu huấn luyện đều lấy từ chỉ mục cổng). Điểm gần 100 không chứng minh mô hình tổng quát hoá.
- **T2 nên dùng luật viết tay.** Mọi mô hình đều thiên về một đáp án.
- **Qwen2.5-0.5B chạy trên CPU**, nên không có bảng giao thức 1.2.

## Gửi kết quả

Chạy hệ của bạn trên `m3/test_de.jsonl`, mỗi dòng ghi `{"id": ..., "tra_loi": ...}`, rồi chấm bằng `python3 scripts/cham_diem.py <tệp>` và `python3 scripts/kiem_trung_thuc.py m3/chi_muc_kiem_trung_thuc.csv.xz m3/test_dap_an.jsonl <tệp>`. Mở pull request thêm tệp trả lời vào `ket_qua/` và một dòng vào `HE` trong `scripts/bang_xep_hang.py`. Ghi rõ giao thức giải mã bạn dùng.
