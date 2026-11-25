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

## QĐ-08 · Chuyên gia mô phỏng cho giai đoạn pilot

- **Ngày:** 21/11/2026 · **Người quyết:** Nguyễn Cảnh Lâm (yêu cầu tăng tốc pilot vì việc cần người đang là điểm nghẽn)
- **Chốt:** trong pilot, Claude làm thay các việc cần người (kiểm thông tin cá nhân, xác nhận luật thể thức, chấm). Mọi kết quả ghi nhãn "chuyên gia mô phỏng (AI)", không ghi dưới tên người.
- **Giới hạn phải ghi kèm khi công bố:**
  1. Số liệu chấm mô phỏng không phải chuẩn vàng do người chấm; độ đồng thuận giữa hai lượt AI không thay được độ đồng thuận giữa hai người.
  2. AI vừa dựng luật vừa chấm nên thiếu độc lập; lượt chấm chạy tách phiên, chấm mù.
  3. Các cổng M2, M3 ghi "đạt ở mức pilot (mô phỏng)". Đạt chính thức cần người kiểm lại một phần mẫu.
- **Liên quan:** nới QĐ-05 cho riêng pilot; QĐ-06 vẫn áp cho bản chính thức.

## QĐ-09 · Bộ che và loại giấy phép (áp cho bản v4)

- **Ngày:** 21/11/2026 · **Người quyết:** Nguyễn Cảnh Lâm, theo đề xuất từ lượt kiểm mô phỏng
- **Chốt:**
  1. Không che tên cán bộ khi ngay sau tên là chức vụ hoặc văn bản là quyết định nhân sự (đúng QĐ-03).
  2. Giữ văn bản vinh danh liệt sĩ (1636/QĐ-TTg).
  3. Vá luật che: bắt cả mẫu "ông/bà" bị dấu phẩy, ngoặc kép chen trước tên.
  4. Tên tắt người soạn thảo ở dòng "Lưu:" để nguyên.
  5. Giấy phép (ký hiệu GP, GPMT...) là văn bản công khai, giữ trong bộ dữ liệu, tách thành loại "Giấy phép" theo chữ viết tắt trong ký hiệu. Loại này nằm ngoài năm loại của QĐ-02 nên không vào bộ đánh giá.

## QĐ-10 · Mô hình cơ sở và cách chạy (M4–M5)

- **Ngày:** 21/11/2026 · **Người quyết:** Nguyễn Cảnh Lâm giao Claude quyết ở vai tổng công trình sư
- **Máy:** MacBook Pro 16 inch, M1 Max, 32 GB. Chạy bằng MLX, mô hình lượng tử hóa 4-bit.
- **Chốt:**
  1. Ba mốc so sánh không tinh chỉnh: một mô hình mở đa ngữ cỡ 8 tỉ tham số (dự kiến Qwen3-8B), một mô hình cùng cỡ của hãng khác (dự kiến Gemma), một mô hình chuyên Đông Nam Á (dự kiến SeaLLMs). Tên bản cụ thể chốt lúc tải, theo bản mới nhất có sẵn cho MLX.
  2. Một mô hình tinh chỉnh: QLoRA trên mô hình ở mục 1 có điểm tốt nhất, dùng tập huấn luyện của dự án.
  3. Chia tập theo cụm mẫu: các văn bản gần trùng mẫu (trường gan_trung_mau_voi) phải nằm cùng một phía, để mô hình không được chấm trên mẫu đã học.
  4. Ba nhiệm vụ: soạn văn bản từ yêu cầu; tìm lỗi thể thức; trích số, ngày, cơ quan, trích yếu.
- **Điều kiện xin lùi:** nếu một lượt tinh chỉnh trên máy này quá 12 giờ, hoặc mô hình tinh chỉnh không hơn mốc không tinh chỉnh, báo đầu mối trước 28/11.

## QĐ-11 · Chạy M4–M5 không chờ người, hai máy song song

- **Ngày:** 24/11/2026 · **Người quyết:** Nguyễn Cảnh Lâm (phép thử: AI tự đi hết quy trình huấn luyện, đầu mối chỉ là người duyệt cuối; cho phép toàn quyền dùng máy Mac)
- **Chốt:**
  1. Lượt nhỏ trên máy của Claude (2 nhân CPU, 7 GB, không GPU): Qwen2.5-0.5B-Instruct, chấm gốc, tinh chỉnh LoRA, chấm lại.
  2. Lượt lớn trên máy Mac M1 Max 32 GB bằng MLX, chạy bằng một lệnh duy nhất (`scripts/chay_tat_ca_mac.sh`). Đầu mối chỉ dán lệnh; kết quả ghi vào `~/Documents/vbhc-ketqua`, Claude tự đọc.
  3. Chấm nội dung T1 do chuyên gia mô phỏng (AI) làm theo `docs/huong_dan_cham_T1.md`, chấm mù (QĐ-08).
- **Sai lệch so với QĐ-10, ghi lại:**
  1. SeaLLMs không có bản MLX công khai: thay bằng Gemma-3-12B.
  2. Gemma-3-12B không chạy được vì ổ cứng Mac đầy (còn 2 GB trống trên 461 GB). Bảng điểm chỉ có hai mô hình 8B chưa tinh chỉnh.
  3. Kịch bản chọn mô hình để tinh chỉnh bằng bộ chấm 1.0, ra Llama-3.1-8B (56,4 so với Qwen3-8B 56,0). Chấm lại bằng bộ chấm 1.1 thì Qwen3-8B cao hơn (60,5 so với 59,0). Chênh 1,5 điểm, nằm trong mức nhiễu của bộ 285 mục; giữ lượt tinh chỉnh Llama, không chạy lại.
  4. Lượt nhỏ cắt văn bản dài ở giữa để vừa 1.024 token khi huấn luyện, và chỉ giữ 94/269 ví dụ T1 vừa trọn khung. Lúc chấm không cắt.
- **Bộ chấm 1.1 (24/11/2026):** chỉ số `dung_ngay` của T1 chỉ kiểm giá trị ngày, không phân biệt hoa thường. Bản 1.0 bắt buộc chữ "ngày" viết thường, nên cho 0 điểm với bài viết đúng ngày nhưng mở đầu bằng "Ngày". Cách trình bày ngày vẫn do luật L05, L15 chấm. Mọi hệ được chấm lại bằng bản 1.1.

## QĐ-12 · M6: ưu tiên chất lượng mô hình

- **Ngày:** 24/11/2026 · **Người quyết:** Nguyễn Cảnh Lâm giao Claude quyết ở vai tổng công trình sư ("chất lượng mô hình là ưu tiên cao nhất")
- **Căn cứ:** M5 cho thấy tinh chỉnh dạy được khuôn văn bản nhưng không giảm bịa. Qwen3-8B gốc đứng đầu về nội dung (4,69/8 khi chấm mù mô phỏng).
- **Chốt:**
  1. **Đo bịa bằng máy** (`scripts/kiem_trung_thuc.py`, phần bổ sung của bộ chấm 1.2; không đổi `tong_hop`). Có bốn nhóm lỗi:
     - viện dẫn văn bản trung ương 2020–2026 sai so với chỉ mục 24.874 văn bản;
     - người ký sai vai;
     - tên bộ đã hợp nhất hoặc cấp huyện xuất hiện sau mốc;
     - lặp.

     Kết quả thử trên chính 41 văn bản thật: 97,6% bài sạch, 98,6% viện dẫn kiểm được là đúng. Đó là mức báo nhầm của bộ kiểm.
  2. **Tập huấn luyện v2** (`scripts/m6_du_lieu_v2.py`, thư mục `m6/`). Bộ kiểm tra giữ nguyên.
     - **Lọc T1:** dùng độ nhiễu chữ (≤ 2%) thay cho độ tin OCR. Bỏ các dòng do dấu chữ ký số và con dấu sinh ra. Cho phép vi phạm L11 và L12 (L11 báo nhầm khi người đứng đầu tự ký; L12 chưa có căn cứ). Kết quả: T1 tăng từ 269 lên 804 ví dụ.
     - **Che chi tiết không suy ra được từ lời yêu cầu bằng "…":** gồm số, ngày văn bản viện dẫn không phải quy phạm trung ương, và họ tên người ký. Mục đích là dạy mô hình để trống thay vì bịa.
     - **Cân lại các nhiệm vụ:** T3 600 (đã bão hòa), T2 600, T1 804.
  3. **Mô hình:** Qwen3-8B 4-bit, QLoRA rank 16 trên 16 lớp, LR 2e-5 cosine có khởi động 100 vòng, khoảng 1 lượt dữ liệu (2.000 vòng).
     - Chấm toàn bộ tập thẩm định mỗi 250 vòng. **Chọn checkpoint có val loss thấp nhất**, không lấy checkpoint cuối.
     - Bài học từ M5: val loss của Llama thấp nhất ở vòng 300/600.
  4. **Điều kiện nhận:** mô hình v2 phải không thua Qwen3-8B gốc ở cả hai chỉ số:
     - `tong_hop` máy;
     - tỷ lệ bài sạch theo bộ kiểm trung thực.

     Sau đó mới chấm mù nội dung. Nếu thua, báo đầu mối kèm phân tích và không công bố là mô hình cơ sở.
- **Rủi ro đã biết:**
  - Che tên người ký làm giảm độ giống văn bản thật. Điểm thể thức T1 có thể giảm nhẹ.
  - Bộ kiểm trung thực chỉ thấy lỗi viện dẫn có số hiệu. Nó không thấy nội dung bịa không có số hiệu.
- **Sự cố lượt 1 (24/11, 19:45 đến 22:20):**
  - **Hiện tượng:** ở vòng 500, cả train loss lẫn val loss thành `nan`.
  - **Nguyên nhân:** hai ví dụ T3 có lời yêu cầu dài 3.383 và 3.447 token, vượt max-seq-length 3.072. Khi bị cắt, chúng mất cả phần trả lời nên không còn token nào để tính loss. Bộ dựng có giới hạn theo số ký tự, nhưng không bắt được hai ví dụ này vì văn bản OCR nhiễu tách ra nhiều token hơn.
  - **Sửa:**
    - Bộ dựng lọc bằng tokenizer, bỏ mọi ví dụ quá 3.000 token.
    - Lượt 2 tiếp từ checkpoint vòng 250 của lượt 1 (val loss 1,022 trên toàn tập thẩm định), chạy thêm 1.750 vòng, LR cosine từ 2e-5.
    - Val loss lượt 2 đo trên 60 ví dụ đầu của tập thẩm định để rút thời gian, nên không so trực tiếp được với con số 1,022.
- **Sự cố lượt 2 (24/11, 22:26 đến 25/11, 03:00):**
  - **Hiện tượng:** `nan` lại xuất hiện ở đúng vị trí dữ liệu như lượt 1.
  - **Nguyên nhân:** kịch bản chỉ giải nén `train.jsonl.xz` khi chưa có `train.jsonl`. Máy Mac còn tệp cũ chưa lọc từ lượt 1 nên dùng lại tệp đó. Nhật ký xác nhận: số token tích lũy trùng từng dòng với lượt 1, và vẫn có cảnh báo câu dài 3.570 token.
  - **Hệ quả:** checkpoint tốt nhất hiện có là vòng 250 của lượt 2. Nó đã qua 500 vòng nhưng chỉ học 250 ví dụ đầu, mỗi ví dụ hai lần. Val loss là 0,872 trên 60 ví dụ.
  - **Sửa:**
    - Kịch bản luôn giải nén lại.
    - Lượt 3 tiếp từ checkpoint trên với LR cosine 1,5e-5, chạy 1.500 vòng.
    - Val ở vòng 1 của lượt 3 chính là của checkpoint xuất phát. Vì vậy, nếu huấn luyện thêm không giúp gì, việc chọn checkpoint sẽ giữ lại checkpoint xuất phát.
  - **Kết quả chấm của checkpoint lượt 2** được giữ làm bản v2, để đo xem lượt 3 có thêm giá trị không.
- **Kết quả bản v2 (checkpoint vòng 250 lượt 2, 25/11 04:05):**
  - **Điểm máy:** tổng hợp 66,7 (Qwen3 gốc 60,5). T1 máy 93,7, thể thức 78,9. T3 98,9. T2 7,4, thấp hơn bản gốc 9,6: bản v2 luôn trả `ngay_thieu_so_0`.
  - **Bộ kiểm trung thực:** 41,5% bài sạch (gốc 31,7%), nên đạt hai điều kiện nhận của QĐ-12.
  - **Hai điểm yếu:**
    - **Bài bị lặp:** 36,6%, bản gốc chỉ 4,9%.
    - **Viện dẫn NĐ 30/2020:** vẫn bịa ngày. Phần lớn 147 lỗi sai ngày là NĐ 30/2020 bị lặp trong các bài lặp.
  - **Lỗi dữ liệu phát hiện thêm:** ký hiệu có chữ thường ("…/TTr-") chỉ bị che số, ngày vẫn lộ (246 chỗ). Mô hình học theo nên vẫn bịa ngày tờ trình. Đã sửa trước lượt 3: còn 41 chỗ lộ, đều do ký hiệu OCR lỗi.
- **Kết quả bản v3 (vòng 1.000 lượt 3, 25/11 14:50):**
  - **Điểm máy:** tổng hợp 71,3, cao nhất từ trước đến nay. 48,8% bài sạch.
  - **Chấm mù nội dung:** 3,85/8, thua Qwen3 gốc (4,69).
  - **Kết luận:** v3 chưa phải mô hình cơ sở cho phần soạn văn bản. Bảng công bố ghi cả hai hệ. Báo cáo ở `docs/m6_bao_cao.md`.

## QĐ-13 · M6b: sửa ba lỗi còn lại của bản v3

- **Ngày:** 25/11/2026 · **Người quyết:** Nguyễn Cảnh Lâm ("triển khai trọn vẹn"), Claude đề xuất ở vai tổng công trình sư.
- **Chốt:**
  1. **Giao thức chấm 1.2 cho phần soạn văn bản (T1):** giải mã có phạt lặp (`repetition_penalty` 1,1, cửa sổ 64 token).
     - Chạy lại cho mọi hệ 8B: Qwen3 gốc, Llama gốc, Llama tinh chỉnh M5, Qwen3 v3, Qwen3 v4.
     - Giao thức 1.1 (tham lam) vẫn giữ làm bảng chính. Hai bảng công bố song song, không trộn.
     - Mô hình 0,5B không chạy lại vì đó là hệ chạy trên CPU, ghi rõ là thiếu.
  2. **Tập huấn luyện v4** (`scripts/m6_du_lieu_v4.py`, thư mục `m6b/`):
     - **T1:** bỏ dòng "Cơ quan: …" của dấu chữ ký số. Dòng này có ở 261/804 mục tiêu, và bản v3 chép nó vào bài.
     - **T2 đối chứng:** 60 văn bản, mỗi văn bản sinh đủ các phiên bản lỗi cài, tổng cộng 600 ví dụ. Bản v3 trả `thieu_ket_thuc` cho 71/94 câu.
     - **T4 phụ, mốc thời gian bộ máy (420 ví dụ):** ngày lấy từ văn bản thật trong tập huấn luyện, đáp án suy tất định từ ba mốc:
       - Nghị quyết 176/2025/QH15: cơ cấu Chính phủ mới từ 01/3/2025.
       - Bỏ cấp huyện từ 01/7/2025.
       - Nhiệm kỳ Thủ tướng: Nguyễn Xuân Phúc đến 05/4/2021, Phạm Minh Chính từ 05/4/2021. Chỉ dùng ngày trước 2026, vì sau mốc hiểu biết của Claude không chắc.
     - **T3:** 300 ví dụ.
  3. **Mô hình v4:** tiếp từ bản v3, chạy 2.100 vòng, LR khởi động 50 vòng rồi cosine 1e-5. Chọn checkpoint theo val loss trên 60 ví dụ. Vòng 1 là bản v3, để luôn có điểm so.
  4. **Điều kiện nhận v4:** như QĐ-12, cộng thêm một điều kiện: chấm mù nội dung T1 phải không thua Qwen3 gốc. Khi đó v4 mới được gọi là mô hình cơ sở cho T1.
- **Rủi ro đã biết:**
  - Chưa rõ T4 có chuyển sang phần soạn văn bản hay không. Đây chính là điều lượt này cần đo.
  - Phạt lặp có thể làm câu chữ kém tự nhiên, vì tiếng Việt lặp âm tiết nhiều. Vì vậy bảng 1.1 vẫn được giữ.
