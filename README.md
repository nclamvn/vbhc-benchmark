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
| Kiểm lại registry bằng engine | Cần thêm bản chụp nguồn (`snapshots/`) | **Chưa làm được:** gói bản chụp đầy đủ chưa được đưa lên Drive |
| Cào lại từ đầu | Cần mạng và các cổng còn giữ trang cũ | Chưa diễn tập |

## Giấy phép

Mã nguồn theo Apache 2.0 (`LICENSE`). Dữ liệu dự án theo CC BY 4.0, có ghi nguồn bắt buộc cho từng cổng (`LICENSE-DATA.md`).
