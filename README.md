# VBHC · Bộ dữ liệu và bộ đánh giá văn bản hành chính tiếng Việt

Bộ dữ liệu mở và bộ đánh giá đo năng lực soạn và rà soát văn bản hành chính đúng thể thức Nghị định 30/2020/NĐ-CP. Kèm mốc so sánh từ các mô hình mở nhỏ.

**Đây là bản pilot.** Theo QĐ-08, các việc cần người (kiểm thông tin cá nhân, xác nhận luật, kiểm đáp án) trong pilot do AI làm và được ghi nhãn "mô phỏng". Chưa có người kiểm lại.

## Hiện trạng (24/11/2026)

| Mốc | Trạng thái | Tài liệu |
| --- | --- | --- |
| M0 Khởi động, pháp lý | Đóng có điều kiện | `DECISIONS.md` |
| M1 Luật thể thức máy kiểm | Đạt ở mức pilot (mô phỏng) | `docs/m1_luat_the_thuc_bao_cao.md` |
| M2 Dữ liệu | Đạt ở mức pilot (mô phỏng): 6.294 văn bản toàn văn, chỉ mục 24.874 dòng, bản v4 | `docs/thay_doi_v4.md` |
| M3 Bộ đánh giá | Đạt ở mức pilot (mô phỏng): 285 mục, ba nhiệm vụ | `docs/m3_bo_danh_gia_bao_cao.md` |
| M4–M5 Mô hình, bảng điểm | Chờ chạy trên máy Mac | `docs/chay_tren_may_mac.md` |
| M6 Đóng gói, chạy lại độc lập | Chưa | |

## Chấm một mô hình

```bash
# tệp trả lời: mỗi dòng {"id": "...", "tra_loi": "..."}, id lấy từ m3/test_de.jsonl
python3 scripts/cham_diem.py ket_qua/<ten>.jsonl
python3 scripts/bang_diem.py ket_qua/*_diem.json
```

Luôn báo điểm kèm mốc luật viết tay (`m3/moc_luat.jsonl`): mốc này đạt 95,7 ở T2 và 86,7 ở T3 mà không cần mô hình ngôn ngữ.

## Dữ liệu ở đâu

Tệp lớn nằm trên Google Drive, thư mục `VBHC_Dataset_v1_2026-11-20/Vong4_2026-11-21_QD09`. Repo này giữ:

- `scripts/`: mã mọi bước cào, lọc, OCR, làm sạch, đối chiếu, xuất, dựng bộ đánh giá, chấm.
- `engine/`: engine tinh lọc và 180.308 claims có dẫn chứng của bản v4 (`engine/domains/vbhc_v4/claims.jsonl.xz`).
- `m3/`: đề, đáp án, tập huấn luyện và thẩm định, bảng chia tập theo cụm.
- `meta/`: manifest SHA-256 của các tệp đã tải, kết quả kiểm, số liệu kiểm độc lập.
- `docs/`: báo cáo từng mốc, hướng dẫn chấm, data card.

## Tái lập

Đã diễn tập ngày 24/11/2026 từ một bản clone sạch.

| Việc | Chỉ cần repo | Kết quả diễn tập |
| --- | --- | --- |
| Chấm điểm, bảng điểm, dựng lại các mốc không mô hình | Có | Chạy được |
| Dựng lại bộ đánh giá từ toàn văn | Cần `toan_van_v4.jsonl` từ Drive | Ra đúng từng byte như `m3/` (`VBHC_TOAN_VAN=<tệp> python3 scripts/m3_dung_bo.py`) |
| Kiểm lại registry bằng engine | Cần gói bản chụp `goi_snap_v4.tar.xz.phan00`–`phan15` từ Drive | Ra đúng build digest `e2d15831dda6bf98`, 0 cổng cắn |
| Cào lại từ đầu | Cần mạng và các cổng còn giữ trang cũ | Chưa diễn tập |

Lệnh kiểm lại registry:

```bash
cd engine && xz -dk domains/vbhc_v4/claims.jsonl.xz
cat <thư mục tải về>/goi_snap_v4.tar.xz.phan* | xz -dc | tar -C domains/vbhc_v4 -xf -
python3 refinery.py domains/vbhc_v4 | tail -2   # phải ra build digest e2d15831dda6bf98 và VALIDATION PASSED
```

Bản chụp toàn văn trong gói là bản đã che thông tin cá nhân, giống tệp toàn văn công bố.

## Giấy phép

Mã nguồn theo Apache 2.0 (`LICENSE`). Dữ liệu dự án theo CC BY 4.0, có ghi nguồn bắt buộc cho từng cổng (`LICENSE-DATA.md`).

## Kết quả pilot M4–M5 (24/11/2026)

Xem `docs/m4_m5_bao_cao.md`. Llama-3.1-8B tinh chỉnh QLoRA đạt tổng hợp 67,3, cao nhất điểm máy. Khi chấm nội dung T1 (mô phỏng AI, mù), Qwen3-8B gốc đứng đầu với 4,69/8. Luật viết tay vẫn thắng T2 với 95,7.

## Mô hình cơ sở của pilot (25/11/2026)

Mô hình cơ sở là Qwen3-8B tinh chỉnh QLoRA bản v4, sinh văn bản theo giao thức 1.2 (phạt lặp 1,1 cho phần soạn văn bản). Bản này đạt tổng hợp máy 71,8, và chấm mù nội dung T1 được 4,92/8 so với 3,92 của Qwen3 gốc. Đây là chấm mô phỏng bằng AI, mỗi hệ 13 đề. Phần tìm lỗi thể thức (T2) nên dùng luật viết tay. Xem `docs/m6b_bao_cao.md`.

## Bảng xếp hạng và tái lập

- Bảng xếp hạng là [BANG_XEP_HANG.md](BANG_XEP_HANG.md), tính lại bằng `python3 scripts/bang_xep_hang.py`.
- Kiểm tái lập từ bản clone sạch bằng `bash scripts/kiem_tai_lap.sh`. Thêm `VBHC_TOAN_VAN=<toan_van_v4.jsonl>` để dựng lại cả bộ đo và tập huấn luyện. Kết quả kiểm ngày 25/11/2026: khớp từng byte ở mọi bước.
- Nhật ký quyết định nằm ở [DECISIONS.md](DECISIONS.md), từ QĐ-01 đến QĐ-13.
