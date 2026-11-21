# VBHC v4 · Thay đổi theo QĐ-09 (21/11/2026)

Bản v4 thay bản v3. Số văn bản không đổi: 6.294 giữ, 150 loại, 1.212 dòng cần người xem.

## Thay đổi

1. **Tên cán bộ không còn bị che** khi ngay sau tên là chức vụ, hoặc câu nói về việc nhân sự (bổ nhiệm, phê chuẩn, điều động, chịu trách nhiệm thi hành...). 830 lượt tên được giữ; 504 lượt vẫn che. Trường mới trong da_che: ho_ten_can_bo_giu.
2. **Vá luật che:** tên đứng sau "ông/bà" bị dấu phẩy hoặc ngoặc kép chen giữa nay cũng bị che.
3. **Loại mới "Giấy phép"** cho văn bản có ký hiệu bắt đầu bằng GP (GP, GPMT...): 100 văn bản trong bộ toàn văn, 165 dòng trong chỉ mục. Loại này nằm ngoài năm loại dùng cho bộ đánh giá.

## Kiểm lại

- Registry: 24.874 thực thể, 180.308 claims, 1 ô tranh chấp, 0 cổng cắn, build digest e2d15831dda6bf98.
- Kiểm thông tin cá nhân (mô phỏng, AI) trên đúng 100 mẫu của lượt v3: 5 tên vừa được mở đều là cán bộ trong hai quyết định bổ nhiệm; không thấy thông tin người dân còn sót.
- Đọc mẫu 45 tên được giữ và 30 tên bị che trên 2.500 văn bản: 45/45 tên được giữ là cán bộ; mọi tên người dân gặp trong mẫu đều nằm ở nhóm bị che.

## Giới hạn

- Luật giữ tên dựa vào chức danh đứng liền sau. Người dân có chức danh kiểu "Trưởng thôn" đứng liền sau tên sẽ được giữ.
- Nhiều tên cán bộ vẫn bị che khi chức vụ không đứng liền tên (ví dụ trong bảng danh sách). Che thừa là phía an toàn.
- Lượt kiểm do AI làm (QĐ-08), chưa có người kiểm.

## Cách ghép

    cat toan_van_v4.jsonl.xz.phan00 toan_van_v4.jsonl.xz.phan01 toan_van_v4.jsonl.xz.phan02 > toan_van_v4.jsonl.xz
    xz -d toan_van_v4.jsonl.xz
    xz -d chi_muc_van_ban_v4.csv.xz

SHA-256 của toan_van_v4.jsonl sau khi ghép: 18204cdc50f74a916086d2191e72b4408ae990c12c4e21a274fef742760d99ac
