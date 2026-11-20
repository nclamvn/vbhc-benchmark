# VBHC · Bộ dữ liệu và bộ đánh giá văn bản hành chính tiếng Việt

Bộ dữ liệu mở và bộ đánh giá đo năng lực soạn và rà soát văn bản hành chính đúng thể thức Nghị định 30/2020, trích căn cứ còn hiệu lực. Kèm một mô hình mở nhỏ làm mốc so sánh.

## Hiện trạng (21/11/2026)

| Mốc | Trạng thái |
| --- | --- |
| M0 · Khởi động và pháp lý | Đóng có điều kiện: còn chờ hai người chấm, việc này phải xong trước M3 (xem `DECISIONS.md`) |
| M1 · Luật thể thức máy kiểm | Chưa bắt đầu |
| M2 · Dữ liệu | Vòng 2 xong: 6.282 văn bản toàn văn sạch, chỉ mục 24.874 dòng từ 4 nguồn |
| M3–M6 | Chưa bắt đầu |

## Dữ liệu ở đâu

Tệp dữ liệu lớn không để trong repo. Chúng nằm trong thư mục Google Drive `VBHC_Dataset_v1_2026-11-20/Vong2_2026-11-21`. Repo này giữ phần dựng lại và kiểm lại được:

- `scripts/`: mã của mọi vòng cào, lọc, OCR, làm sạch, đối chiếu, xuất.
- `engine/`: engine tinh lọc, cấu hình domain, 180.298 claims có dẫn chứng (`claims.jsonl.xz`).
- `meta/`: manifest SHA-256 của mọi trang danh sách và mọi tệp đã tải, kế hoạch lấy mẫu, số liệu kiểm độc lập.
- `docs/`: data card hai vòng, hướng dẫn chấm, hồ sơ mời người chấm.

## Kiểm lại

```bash
xz -d engine/domains/vbhc_v2/claims.jsonl.xz
# Cần thêm thư mục snapshots/ (bản chụp HTML và toàn văn) từ gói kiểm lại đầy đủ trên Drive
cd engine && python3 refinery.py domains/vbhc_v2 | tail -3   # phải ra "VALIDATION PASSED"
```

## Giấy phép

Mã nguồn theo Apache 2.0 (`LICENSE`). Dữ liệu dự án theo CC BY 4.0, có ghi nguồn bắt buộc cho từng cổng (`LICENSE-DATA.md`).
