# Bảng xếp hạng VBHC-Bench · pilot 25/11/2026

Tính lại bằng `python3 scripts/bang_xep_hang.py` từ các tệp trả lời trong `ket_qua/`. Bộ kiểm tra có 285 câu: T1 soạn văn bản 41 câu, T2 tìm lỗi thể thức 94 câu, T3 trích thông tin 150 câu. Tổng hợp là trung bình đều của ba nhiệm vụ, bộ chấm 1.1, giải mã tham lam.

## Bảng chính (giao thức 1.1)

| # | Hệ | Tổng hợp | T1 | T1 thể thức | T2 | T3 | T1 bài sạch | T1 bài lặp |
|---|---|---|---|---|---|---|---|---|
| 1 | Qwen3-8B v4 tinh chỉnh (mô hình cơ sở) | **71,8** | 94,8 | 80,7 | 21,3 | 99,3 | 22,0% | 56,1% |
| 2 | Qwen3-8B v3 tinh chỉnh | **71,3** | 94,5 | 80,2 | 20,2 | 99,2 | 24,4% | 56,1% |
| 3 | Llama-3.1-8B tinh chỉnh | **67,3** | 86,6 | 74,5 | 17,0 | 98,2 | 24,4% | 68,3% |
| 4 | Qwen3-8B v2 tinh chỉnh | **66,7** | 93,7 | 78,9 | 7,4 | 98,9 | 31,7% | 53,7% |
| 5 | Luật viết tay (không mô hình) | **60,8** | 0,0 | 0,0 | 95,7 | 86,7 | — | — |
| 6 | Qwen3-8B gốc | **60,5** | 86,5 | 65,5 | 9,6 | 85,5 | 31,7% | 7,3% |
| 7 | Llama-3.1-8B gốc | **59,0** | 79,9 | 58,5 | 12,8 | 84,3 | 26,8% | 53,7% |
| 8 | Qwen2.5-0.5B tinh chỉnh | **56,4** | 55,9 | 45,7 | 18,1 | 95,2 | 12,2% | 80,5% |
| 9 | Qwen2.5-0.5B gốc | **29,9** | 64,3 | 43,9 | 4,3 | 21,1 | 22,0% | 58,5% |

## Phần soạn văn bản với phạt lặp (giao thức 1.2)

Cấu hình: `repetition_penalty` 1,1, cửa sổ 64 token, chỉ áp cho T1. Bảng này công bố riêng, không trộn vào bảng chính.

| Hệ | T1 | T1 thể thức | Bài sạch | Bài lặp |
|---|---|---|---|---|
| Qwen3-8B v4 tinh chỉnh (mô hình cơ sở) | 96,7 | 93,5 | 51,2% | 14,6% |
| Qwen3-8B v3 tinh chỉnh | 97,9 | 89,4 | 48,8% | 22,0% |
| Llama-3.1-8B tinh chỉnh | 93,6 | 81,1 | 46,3% | 34,1% |
| Llama-3.1-8B gốc | 85,8 | 60,2 | 46,3% | 41,5% |
| Qwen3-8B gốc | 85,2 | 64,1 | 41,5% | 0,0% |

## Chấm mù nội dung T1 (chuyên gia mô phỏng · AI)

Thang 8 điểm, gồm bốn tiêu chí 0–2: đúng việc, đúng vai và thẩm quyền, văn phong, không bịa (`docs/huong_dan_cham_T1.md`). Mỗi hệ có 13 đề. Chỉ so điểm trong cùng một phiên chấm.

| Hệ | Điểm /8 (phiên, giao thức) |
|---|---|
| Qwen3-8B v4 tinh chỉnh (mô hình cơ sở) | 4,92 (M6b, phạt lặp) |
| Qwen3-8B v3 tinh chỉnh | 3,85 (M6, tham lam) |
| Llama-3.1-8B tinh chỉnh | 3,31 (M5, tham lam) |
| Qwen3-8B v2 tinh chỉnh | 2,23 (M6, tham lam) |
| Qwen3-8B gốc | 4,69 (M5, tham lam) · 3,92 (M6b, phạt lặp) |
| Llama-3.1-8B gốc | 3,62 (M5, tham lam) |
| Qwen2.5-0.5B tinh chỉnh | 0,08 (M5, tham lam) |
| Qwen2.5-0.5B gốc | 0,69 (M5, tham lam) |

## Cách đọc và giới hạn

- **Bài sạch:** bộ kiểm trung thực bằng máy (`scripts/kiem_trung_thuc.py`) không bắt được lỗi nào. Bộ kiểm đối chiếu viện dẫn với chỉ mục 24.874 văn bản, và bắt người ký sai vai, tên cơ quan sai thời điểm, bài lặp. Chạy trên 41 văn bản thật, bộ kiểm cho 97,6% bài sạch.
- **Chấm nội dung do AI đóng vai**, chưa phải chấm độc lập. Phiên M6b là phiên duy nhất so v4 với Qwen3 gốc trong cùng điều kiện: v4 thắng 8, hòa 1, thua 4 trên 13 đề, p ≈ 0,39.
- **T3 cùng phân bố với dữ liệu huấn luyện** (đáp án và dữ liệu huấn luyện đều lấy từ chỉ mục cổng). Điểm gần 100 không chứng minh mô hình tổng quát hoá.
- **T2 nên dùng luật viết tay.** Mọi mô hình đều thiên về một đáp án.
- **Qwen2.5-0.5B chạy trên CPU**, nên không có bảng giao thức 1.2.

## Gửi kết quả

Chạy hệ của bạn trên `m3/test_de.jsonl`, mỗi dòng ghi `{"id": ..., "tra_loi": ...}`, rồi chấm bằng `python3 scripts/cham_diem.py <tệp>` và `python3 scripts/kiem_trung_thuc.py m3/chi_muc_kiem_trung_thuc.csv.xz m3/test_dap_an.jsonl <tệp>`. Mở pull request thêm tệp trả lời vào `ket_qua/` và một dòng vào `HE` trong `scripts/bang_xep_hang.py`. Ghi rõ giao thức giải mã bạn dùng.
