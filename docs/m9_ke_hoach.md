# M9 · Huấn luyện v7 trên tập v7c và đo đầu ra

Lý do: từ M8.1 đến M8.4 dữ liệu đã nâng ba bản nhưng chưa mô hình nào học trên đó. Vòng làm giàu chỉ đáng giá khi đầu ra kiểm được tốt hơn. Hạn pilot 01/12/2026.

## Mục tiêu

Mô hình v7 (Qwen3-8B 4-bit, QLoRA giữ công thức v6, tiếp từ v6) học trên v7c, chạy offline trên MacBook M1 Max 32 GB, thắng v6 trên cùng bộ đề và cùng giao thức 2.1.

## Tiêu chuẩn

| # | Đo gì | Cổng | Ghi chú |
|---|---|---|---|
| A | Bộ nhớ đỉnh, 20 vòng ở khung 6.144 token | dưới 28 GB, không swap | không đạt thì dựng lại tập ở khung 4.500 và đo lại tỷ lệ loại hiếm |
| B | Huấn luyện 1.500 vòng (khoảng 0,44 lượt), chọn checkpoint theo val loss | có checkpoint hữu hạn | `m8c_6000/qlora_qwen3_v7.yaml` |
| C1 | Bài sạch, 41 bài T1, giao thức 2.1 | không thấp hơn v6 | so cùng điều kiện |
| C2 | Viện dẫn sai mỗi bài | không cao hơn v6 | |
| C3 | Căn cứ đúng chỗ | tăng so với v6 | v6 đã công bố 50,0% |
| D | Chấm mù nội dung, thang 8, chuyên gia mô phỏng (AI) | từ 4,38 trở lên | cùng cách chấm M7b |
| E | 20 văn bản mới nhất chưa từng huấn luyện (`m9/de_moi.jsonl`) | chỉ ghi số | 10 đợt B, 10 đợt C; có kế hoạch, chỉ thị, báo cáo |

So hai điều kiện. Khối bộ máy cũ: lời yêu cầu y hệt lúc chấm v6 đã công bố, so thẳng với bảng xếp hạng. Khối bộ máy v1.1 cùng bảng đồng viện dẫn mới: điều kiện v7 được huấn luyện, chạy cả v6 lẫn v7 để so công bằng. Giới hạn sinh T1 giữ 1.800 token như v6.

Dừng: nếu v7 không qua C1–C3 ở cả hai điều kiện thì không cào thêm. Mổ dữ liệu xem loại văn bản nào kéo xuống và khung dài có làm loãng không. Pilot giữ v6.

## Chạy

- Mac: `curl -fsSL https://raw.githubusercontent.com/nclamvn/vbhc-benchmark/main/scripts/chay_m9_mac.sh | bash`. Chạy lại cùng lệnh để tiếp từ chỗ dừng.
- Chấm khi kết quả về: `python3 scripts/m9_cham.py` → `ket_qua/m9/bang_m9.md`. Bộ chấm đã chạy thử trên tệp v6 và tái lập đúng số đã công bố (bài sạch 85,4%, sai 0,05, đúng chỗ 50,0%, phủ 17,5%).

Song song (M8.5a, trong máy chứa): sửa cách tra để độ phủ tra cứu từ 75% trở lên mà không giảm căn cứ đúng chỗ.
