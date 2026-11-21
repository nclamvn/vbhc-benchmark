# Nhật ký quyết định

Mỗi quyết định ghi ngày, người quyết, nội dung, lý do và điều kiện để xem lại. Quyết định mới không xoá quyết định cũ; nếu đổi, ghi một mục mới tham chiếu mục cũ.

---

## QĐ-01 · Sửa điều kiện số nguồn của cổng M0

- **Ngày:** 21/11/2026
- **Người quyết:** Claude, theo ủy quyền của Nguyễn Cảnh Lâm ("tất cả đều uỷ thác")
- **Cũ:** ít nhất 10 nguồn hợp lệ.
- **Mới:** ít nhất 4 nguồn hợp lệ, trong đó ít nhất 2 cổng cấp tỉnh có toàn văn.
- **Lý do:** Điều kiện 10 nguồn nhằm bảo đảm khối lượng và độ đa dạng. Khối lượng đã vượt (6.282 văn bản so với mục tiêu 5.000). Phần lớn cổng tỉnh còn lại hoặc chặn truy cập tự động, hoặc tải nội dung bằng JavaScript, hoặc cấm thư mục tệp trong robots.txt. Cố đạt 10 sẽ tốn nhiều công mà không thêm loại văn bản mới.
- **Trạng thái:** Đạt (Cổng TTĐT Chính phủ, Thái Nguyên, Hưng Yên có toàn văn; Quảng Trị chỉ có chỉ mục).
- **Xem lại khi:** bản 2 của bộ dữ liệu, hoặc khi cần văn bản cấp xã.

## QĐ-02 · Chốt 5 loại văn bản cho bản đầu

- **Ngày:** 21/11/2026 · **Người quyết:** Claude, theo ủy quyền
- **Đề xuất cũ:** công văn, tờ trình, báo cáo, quyết định cá biệt, thông báo.
- **Chốt:** công văn, thông báo, quyết định cá biệt, công điện, chỉ thị.
- **Lý do:** Chọn theo dữ liệu thật. Toàn văn đang có: công văn 2.490, thông báo 1.352, quyết định cá biệt 1.054, công điện 529, chỉ thị 262. Tờ trình có 0 và báo cáo có 42, không đủ để dựng 60 tình huống chuẩn vàng mỗi loại. Cả 5 loại đã chốt đều có trong 29 loại văn bản hành chính của Nghị định 30/2020.
- **Hệ quả:** Bộ chuẩn vàng M3 chia 300 tình huống thành 5 loại × 60. Tờ trình và báo cáo chuyển sang bản 2, kèm việc tìm nguồn riêng cho hai loại này.
- **Xem lại khi:** có nguồn tờ trình, báo cáo đủ 300 văn bản mỗi loại.

## QĐ-03 · Giữ họ tên người ký, che họ tên người dân

- **Ngày:** 21/11/2026 · **Người quyết:** Claude, theo ủy quyền
- **Chốt:**
  - Giữ họ tên cán bộ khi gắn với chức vụ công: người ký, người được giao nhiệm vụ, cán bộ được bổ nhiệm.
  - Che họ tên, địa chỉ, số định danh, ngày sinh, email và số điện thoại của người dân.
  - Loại hẳn văn bản mà trích yếu nêu một người dân cụ thể.
- **Lý do:**
  - Họ tên và chức vụ người ký là một thành phần thể thức bắt buộc theo Nghị định 30. Thay bằng chỗ giữ chỗ thì bộ đánh giá không kiểm được thành phần này.
  - Đây là thông tin công vụ do chính cơ quan nhà nước công bố.
  - Thông tin của người dân thì không có lý do công vụ nào để công bố lại, nên phải che theo Luật Bảo vệ dữ liệu cá nhân 2025.
- **Rủi ro còn lại:** bộ phát hiện tên dựa trên mẫu "ông/bà/anh/chị + họ tên", nên có thể sót tên người dân viết không kèm danh xưng. Đã kiểm 100 mẫu bằng hai bộ dò độc lập, không thấy sót; người kiểm tay vẫn cần xác nhận.
- **Xem lại khi:** có phản hồi từ cơ quan ban hành hoặc người được nêu tên.

## QĐ-04 · Giấy phép

- **Ngày:** 21/11/2026 · **Người quyết:** Claude, theo ủy quyền
- **Chốt:** mã nguồn theo Apache License 2.0 (`LICENSE`); dữ liệu do dự án tạo ra (chỉ mục, nhãn, kết quả đối chiếu, bộ chuẩn vàng) theo CC BY 4.0 (`LICENSE-DATA.md`).
- **Lý do:** Văn bản gốc không thuộc đối tượng bảo hộ quyền tác giả (khoản 2 Điều 15 Luật Sở hữu trí tuệ), nhưng quy chế các cổng yêu cầu ghi nguồn. CC BY 4.0 buộc người dùng lại ghi công, khớp yêu cầu đó. Apache 2.0 cho phép dùng thương mại, có điều khoản về bằng sáng chế.

## QĐ-05 · Dời điều kiện "hai người chấm nhận lời" sang cổng vào M3

- **Ngày:** 21/11/2026 · **Người quyết:** Claude, theo ủy quyền
- **Chốt:** M0 đóng có điều kiện. Việc có hai người chấm trở thành điều kiện bắt buộc trước khi bắt đầu M3 (hạn: hết tuần 6).
- **Lý do:** M1 (luật máy kiểm thể thức) và M2 (dữ liệu) không cần người chấm. Giữ điều kiện này ở M0 sẽ chặn hai mốc làm được ngay.
- **Không giả lập:** không ghi nhận người chấm nào khi chưa có người thật nhận lời. Bộ hồ sơ mời (`docs/thu_moi_nguoi_cham.md`, `docs/mo_ta_cong_viec_nguoi_cham.md`, `docs/huong_dan_cham_v0.md`) đã sẵn sàng để gửi.

## QĐ-06 · Vai trò: đầu mối và nhóm cộng sự

- **Ngày:** 21/11/2026 · **Người quyết:** Nguyễn Cảnh Lâm
- **Chốt:**
  - Nguyễn Cảnh Lâm là đầu mối: duyệt ở các cổng, chuyển việc giữa nhóm và Claude, ký nghiệm thu.
  - Các việc cần người (chấm chuẩn vàng, kiểm tay thông tin cá nhân, xác nhận luật thể thức, chạy lại độc lập) do cộng sự của đầu mối đảm nhận.
- **Thay cho:** bản QĐ-06 trước đó ghi nhầm Nguyễn Cảnh Lâm là người chấm 1.
- **Nguyên tắc độc lập:**
  1. Hai người chấm là hai cộng sự khác nhau, làm riêng.
  2. Người chấm không tham gia viết luật thể thức hay dựng đáp án.
  3. Chấm mù: bài không ghi nguồn sinh ra.
  4. Đầu mối không chấm.
- **Trạng thái cổng vào M3:** 0/2 người chấm được chỉ định đích danh.

## QĐ-07 · Ba luật sửa sau lượt kiểm đầu tiên (bản v3)

- **Ngày:** 21/11/2026 · **Đề xuất:** người kiểm (tệp `meta/Ket-qua-kiem-VBHC-v2.xlsx`, 17 nhận định; chưa ghi tên) · **Áp dụng:** Claude, theo ủy thác · **Trạng thái:** chờ đầu mối duyệt
- **Chốt:**
  1. Khử gần trùng chỉ loại khi hai văn bản vừa gần trùng nội dung vừa cùng số ký hiệu và cùng ngày. Văn bản định kỳ chung mẫu được giữ.
  2. Văn bản có nhiều tệp đính kèm: lấy PDF có số trong tên trùng số ký hiệu; không có thì lấy PDF đầu tiên.
  3. Thêm trường `so_ky_hieu_chuan`; trường `so_ky_hieu` giữ nguyên văn trang nguồn.
- **Kết quả:** 6.294 văn bản giữ lại (v2: 6.282), 150 loại (v2: 162), 1 ô tranh chấp (v2: 2). Build digest `30c98055d74a2ebe`.
- **Còn mở:** tn-84190 và tn-84111 chờ xác minh bản chính thức; số của 218224 ghi theo xác nhận của người kiểm; lượt kiểm tay 100 mẫu thông tin cá nhân (cổng M2) chưa làm.
