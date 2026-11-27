# Mẫu kiểm tay thông tin cá nhân · đợt cào B (M8.2) · ĐÃ ĐIỀN

Người kiểm: **chuyên gia mô phỏng (AI)**, không phải người thật. Đầu mối giao AI quyết thay ở bước này (27/11). Cách kiểm gồm hai bước. Máy rút mọi đoạn có thể là thông tin người dân trong bản đã che (`scripts/m8_kiem_tay_mo_phong.py`, ứng viên ở `ket_qua/dot_cao/ung_vien_kiem_tay_b.jsonl`), gồm họ tên theo danh sách họ phổ biến, ngày sinh, số định danh, số điện thoại, địa chỉ thường trú, biển số xe. Chuyên gia mô phỏng đọc từng đoạn không đi cùng chức vụ, rồi soát thêm các mẫu như "hộ ông", "gia đình bà", "nạn nhân", "cháu".

**Kết luận:** 0/100 văn bản còn thông tin người dân. 0/100 văn bản còn số điện thoại của cán bộ, đã che ở bản sửa. Họ tên còn lại đều là cán bộ ký văn bản hoặc đi cùng chức vụ (giữ theo QĐ-03, QĐ-09), hoặc là tên đường, xã, cửa khẩu.

Giới hạn: không mở lại bản gốc cho từng mẫu. Phiếu kiểm câu hỏi "bản đã che còn gì không", câu hỏi "bộ che có xoá nhầm nội dung không" chỉ ghi khi bắt gặp.

100 văn bản chọn ngẫu nhiên (hạt giống 20261127) trong 872 văn bản đợt B. Mỗi dòng: mở bản gốc, đối chiếu với bản đã che trong kho v6 (`data/stage4_v6/corpus.jsonl`, tìm theo mã). Đánh dấu nếu còn họ tên người dân, địa chỉ, số định danh, số điện thoại, ngày sinh. Họ tên cán bộ đi cùng chức vụ được giữ (QĐ-03, QĐ-09).

| # | Mã | Loại | Ngày | Trích yếu | Bản gốc | Còn thông tin cá nhân? |
|---|---|---|---|---|---|---|
| 1 | 213174 | Quyết định (cá biệt) | 2025-03-21 | Về việc công nhận huyện Tam Nông, tỉnh Đồng Tháp đạt chuẩn nông thôn m | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213174) | Không |
| 2 | 217016 | Quyết định (cá biệt) | 2026-02-24 | Ban hành Kế hoạch triển khai thi hành Luật Báo chí | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217016) | Không |
| 3 | 214554 | Quyết định (cá biệt) | 2025-07-15 | Về việc chuyển Trường Đại học Cần Thơ thành Đại học Cần Thơ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214554) | Không |
| 4 | 219966 | Quyết định (cá biệt) | 2026-10-13 | Phê duyệt “Đề án thí điểm triển khai dịch vụ công qua mạng bưu chính c | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219966) | Không |
| 5 | 214824 | Quyết định (cá biệt) | 2025-08-05 | Về việc phê duyệt phương án cắt giảm, đơn giản hóa các quy định, thủ t | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214824) | Không |
| 6 | 216681 | Quyết định (cá biệt) | 2026-01-19 | Phê duyệt Chương trình Phát triển Đại học Quốc gia Thành phố Hồ Chí Mi | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216681) | Không |
| 7 | 220168 | Quyết định (cá biệt) | 2026-11-02 | Ban hành Kế hoạch triển khai thi hành Luật sửa đổi, bổ sung một số điề | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=220168) | Không |
| 8 | 213802 | Quyết định (cá biệt) | 2025-06-02 | Về việc kiện toàn Ban Chỉ đạo Quốc gia Dân số và Phát triển | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213802) | Không |
| 9 | 214018 | Quyết định (cá biệt) | 2025-06-12 | Về việc công nhận huyện Bình Đại, tỉnh Bến Tre đạt chuẩn nông thôn mới | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214018) | Không |
| 10 | 214719 | Quyết định (cá biệt) | 2025-07-24 | Về việc kiện toàn Ủy ban Quốc gia về chấm dứt bệnh lao | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214719) | Không |
| 11 | 215522 | Công điện | 2025-10-06 | V/v chủ động ứng phó nguy cơ mưa lũ, lũ ống, lũ quét, sạt lở đất do ản | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215522) | Không |
| 12 | 214303 | Quyết định (cá biệt) | 2025-06-30 | Về việc kiện toàn Ban Chỉ đạo Tổng điều tra nông thôn, nông nghiệp năm | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214303) | Không |
| 13 | 214660 | Quyết định (cá biệt) | 2025-07-18 | Ban hành Kế hoạch nâng cao chất lượng cung cấp dịch vụ công trực tuyến | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214660) | Không |
| 14 | 213457 | Công điện | 2025-04-24 | Tăng cường công tác bảo đảm an ninh, trật tự dịp Lễ 30/4 và 01/5 | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213457) | Không |
| 15 | 219788 | Quyết định (cá biệt) | 2026-09-30 | Về việc chuyển giao nguyên trạng Trường Cao đẳng nghề Việt - Xô số 1 t | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219788) | Không |
| 16 | 213901 | Quyết định (cá biệt) | 2025-06-12 | Về việc công nhận huyện Tân Trụ, tỉnh Long An đạt chuẩn nông thôn mới  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213901) | Không |
| 17 | 215943 | Công điện | 2025-11-20 | V/v tập trung ứng phó và khắc phục hậu quả mưa lũ đặc biệt lớn tại khu | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215943) | Không |
| 18 | 213147 | Quyết định (cá biệt) | 2025-03-18 | Về việc giải thể Ban Chỉ đạo xây dựng Nhà Quốc hội và Ban Chỉ đạo Chươ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213147) | Không |
| 19 | 213906 | Quyết định (cá biệt) | 2025-06-12 | Về việc công nhận huyện Châu Thành, tỉnh Bến Tre đạt chuẩn nông thôn m | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213906) | Không |
| 20 | 218972 | Quyết định (cá biệt) | 2026-07-22 | Về việc thành lập Ban Chỉ đạo Trung ương Chương trình mục tiêu quốc gi | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218972) | Không |
| 21 | 214113 | Quyết định (cá biệt) | 2025-06-24 | Chỉ định nhân sự giữ chức vụ Phó Chủ tịch Ủy ban nhân dân tỉnh Quảng N | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214113) | Không |
| 22 | 213219 | Quyết định (cá biệt) | 2025-03-24 | Về việc giao bổ sung, điều chỉnh kế hoạch đầu tư công trung hạn vốn ng | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213219) | Không |
| 23 | 216954 | Quyết định (cá biệt) | 2026-02-12 | Ban hành Kế hoạch triển khai thi hành Luật Chuyển đổi số | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216954) | Không |
| 24 | 218907 | Quyết định (cá biệt) | 2026-07-16 | Về việc kiện toàn nhân sự Ủy ban hợp tác Việt Nam - Lào trong Ủy ban l | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218907) | Không |
| 25 | 217867 | Quyết định (cá biệt) | 2026-04-20 | Về việc kéo dài thời gian giữ chức vụ Phó Tư lệnh Bộ đội Biên phòng | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217867) | Không |
| 26 | 216222 | Công điện | 2025-12-16 | Về việc Tổ chức Lễ khởi công, khánh thành, thông xe kỹ thuật các công  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216222) | Không |
| 27 | 213829 | Công điện | 2025-06-04 | Về tiếp tục đẩy mạnh cao điểm đấu tranh ngăn chặn, đẩy lùi tình trạng  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213829) | Không |
| 28 | 218503 | Quyết định (cá biệt) | 2026-06-18 | Về việc ban hành Quy chế tổ chức và hoạt động của Ban Chỉ đạo xây dựng | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218503) | Không |
| 29 | 218445 | Quyết định (cá biệt) | 2026-06-13 | Về việc mở rộng và ban hành Quy chế hoạt động của Khu Công nghệ cao Th | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218445) | Không |
| 30 | 219791 | Quyết định (cá biệt) | 2026-09-30 | Về việc chuyển giao nguyên trạng Trường Cao đẳng Xây dựng số 1, Trường | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219791) | Không |
| 31 | 213124 | Quyết định (cá biệt) | 2025-03-14 | Về việc thành lập Hội đồng thẩm định nhà nước thẩm định điều chỉnh chủ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213124) | Không |
| 32 | 213258 | Công điện | 2025-04-02 | Về việc cháy nhà dân tại số 66B và 66C đường Mạc Vân, phường Xóm Củi,  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213258) | Không. "Mạc Vân" là tên đường |
| 33 | 215780 | Quyết định (cá biệt) | 2025-11-04 | Về việc thành lập Ban Chỉ đạo Nhà nước các chương trình, công trình, d | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215780) | Không |
| 34 | 216472 | Quyết định (cá biệt) | 2025-12-31 | Về việc công bố các Thông tư trong lĩnh vực năng lượng nguyên tử của B | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216472) | Không |
| 35 | 216907 | Quyết định (cá biệt) | 2026-02-09 | Phê duyệt Chiến lược phát triển ngành thép giai đoạn đến năm 2030, tầm | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216907) | Không |
| 36 | 218810 | Quyết định (cá biệt) | 2026-07-08 | Phê duyệt Nhiệm vụ Quy hoạch chung đô thị Bắc Ninh đến năm 2050, tầm n | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218810) | Không |
| 37 | 217837 | Quyết định (cá biệt) | 2026-04-07 | Về việc giao nhiệm vụ cơ quan Bộ Quốc phòng thực hiện nhiệm vụ của Cơ  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217837) | Không |
| 38 | 218058 | Quyết định (cá biệt) | 2026-05-11 | Ban hành Quy chế phối hợp trong đấu tranh, ngăn chặn hoạt động trốn tr | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218058) | Không |
| 39 | 216696 | Quyết định (cá biệt) | 2026-01-19 | Về việc kiện toàn Ban Chỉ đạo thực hiện các Nghị quyết của Quốc hội về | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216696) | Không |
| 40 | 219015 | Quyết định (cá biệt) | 2026-07-24 | Về việc kiện toàn Hội đồng quản lý Quỹ Hỗ trợ đầu tư | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219015) | Không |
| 41 | 214665 | Công điện | 2025-07-20 | Về việc tăng cường công tác phòng, chống bệnh sốt xuất huyết | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214665) | Không |
| 42 | 216005 | Quyết định (cá biệt) | 2025-11-26 | Về việc kiện toàn thành viên Ban Chỉ đạo Trung ương các chương trình m | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216005) | Không |
| 43 | 218270 | Quyết định (cá biệt) | 2026-05-27 | Về việc kiện toàn Ban Chỉ đạo xây dựng trường học cho các xã biên giới | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218270) | Không |
| 44 | 213149 | Quyết định (cá biệt) | 2025-03-18 | Về việc thành lập Hội đồng thẩm định nhà nước thẩm định Báo cáo nghiên | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213149) | Không |
| 45 | 216621 | Quyết định (cá biệt) | 2026-01-12 | Về việc phê duyệt Kế hoạch thực hiện Hiệp định về việc chấp nhận các q | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216621) | Không |
| 46 | 213164 | Quyết định (cá biệt) | 2025-03-15 | Ban hành Kế hoạch triển khai các nhiệm vụ, giải pháp về đẩy mạnh phân  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213164) | Không |
| 47 | 216074 | Công điện | 2025-11-30 | V/v phát động, triển khai "Chiến dịch Quang Trung" thần tốc xây dựng l | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216074) | Không |
| 48 | 219585 | Quyết định (cá biệt) | 2026-09-22 | Về việc chấm dứt hiệu lực thi hành của Quyết định số 241/QĐ-TTg ngày 2 | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219585) | Không |
| 49 | 214330 | Quyết định (cá biệt) | 2025-07-01 | Về việc thành lập Ban Quản lý Khu kinh tế Hải Phòng | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214330) | Không |
| 50 | 219762 | Quyết định (cá biệt) | 2026-10-02 | Ban hành Kế hoạch triển khai thi hành Nghị quyết số 37/2026/QH16 ngày  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219762) | Không |
| 51 | 216350 | Quyết định (cá biệt) | 2025-12-29 | Về việc bổ sung, kiện toàn thành viên Ban Chỉ đạo của Chính phủ về quả | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216350) | Không |
| 52 | 213941 | Quyết định (cá biệt) | 2025-06-13 | Về việc công nhận huyện Hương Khê, tỉnh Hà Tĩnh đạt chuẩn nông thôn mớ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213941) | Không |
| 53 | 215456 | Công điện | 2025-09-29 | Về việc cháy khí Mê tan tại Công ty Than Dương Huy - TKV phường Mông D | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215456) | Không |
| 54 | 214500 | Quyết định (cá biệt) | 2025-07-08 | Về việc thành lập Ban Quản lý Khu Kinh tế Dung Quất và các Khu công ng | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214500) | Không |
| 55 | 213869 | Quyết định (cá biệt) | 2025-06-09 | Về việc kéo dài thời gian giữ chức vụ Thứ trưởng Bộ Công an đối với đồ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213869) | Không |
| 56 | 214658 | Quyết định (cá biệt) | 2025-07-21 | Về việc thành lập Ban Quản lý Khu kinh tế và Khu công nghiệp tỉnh Khán | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214658) | Không |
| 57 | 218488 | Quyết định (cá biệt) | 2026-06-16 | Thành lập Ban Chỉ đạo quốc gia thực hiện Chương trình hành động quốc g | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218488) | Không |
| 58 | 215593 | Công điện | 2025-10-12 | Về việc đánh giá và khắc phục thiệt hại do Bão số 11 gây ra đối với ng | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215593) | Không |
| 59 | 219721 | Quyết định (cá biệt) | 2026-10-01 | Về việc kéo dài thời hạn giữ chức Phó Chính ủy kiêm Chủ nhiệm Chính tr | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219721) | Không |
| 60 | 213843 | Quyết định (cá biệt) | 2025-05-29 | Định giá cụ thể sản phẩm, dịch vụ công ích thủy lợi đối với công trình | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213843) | Không |
| 61 | 215859 | Quyết định (cá biệt) | 2025-11-14 | Về việc điều chỉnh bổ sung danh mục dự án kế hoạch đầu tư công trung h | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215859) | Không |
| 62 | 217270 | Quyết định (cá biệt) | 2026-03-21 | Ban hành Kế hoạch triển khai thi hành Luật sửa đổi, bổ sung một số điề | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217270) | Không |
| 63 | 214302 | Quyết định (cá biệt) | 2025-06-30 | Thành lập Ban Chỉ đạo của Chính phủ về cải cách thủ tục hành chính và  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214302) | Không |
| 64 | 214718 | Quyết định (cá biệt) | 2025-07-24 | Về việc thành lập Hội đồng thẩm định nhà nước thẩm định hồ sơ chấp thu | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214718) | Không |
| 65 | 219285 | Quyết định (cá biệt) | 2026-08-26 | Về việc kiện toàn Ban Chỉ đạo quốc gia về ODA và vốn vay ưu đãi | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219285) | Không |
| 66 | 216327 | Quyết định (cá biệt) | 2025-12-26 | Về việc hỗ trợ khẩn cấp kinh phí cho tỉnh Quảng Trị để khắc phục hậu q | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216327) | Không |
| 67 | 216625 | Quyết định (cá biệt) | 2026-01-12 | Sửa đổi, bổ sung một số điều của Quyết định số 515/QĐ-VPCP ngày 19 thá | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216625) | Không |
| 68 | 213630 | Quyết định (cá biệt) | 2025-05-15 | Về việc phê duyệt danh sách thành viên và chức năng, nhiệm vụ của Tổ c | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213630) | Không |
| 69 | 217998 | Quyết định (cá biệt) | 2026-05-05 | Về việc thay đổi Tổ trưởng Tổ công tác về tăng cường hợp tác, chủ động | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217998) | Không |
| 70 | 218349 | Quyết định (cá biệt) | 2026-06-04 | Về việc kiện toàn thành viên Hội đồng phối hợp phổ biến, giáo dục pháp | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218349) | Không |
| 71 | 218032 | Quyết định (cá biệt) | 2026-05-06 | Về việc thành lập Phân hiệu Trường Đại học Tài chính - Marketing tại t | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218032) | Không |
| 72 | 214671 | Quyết định (cá biệt) | 2025-07-17 | Về việc bổ sung Danh sách các cửa khẩu áp dụng tờ khai hải quan dùng c | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214671) | Không |
| 73 | 213569 | Công điện | 2025-05-08 | Về việc tổ chức kỳ thi tốt nghiệp trung học phổ thông và tuyển sinh đầ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213569) | Không |
| 74 | 213763 | Quyết định (cá biệt) | 2025-05-30 | Về việc công nhận tỉnh Tiền Giang hoàn thành nhiệm vụ xây dựng nông th | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213763) | Không |
| 75 | 214888 | Công điện | 2025-08-12 | Về việc khắc phục hậu quả vụ tai nạn lao động nghiêm trọng tại Dự án đ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214888) | Không |
| 76 | 219963 | Quyết định (cá biệt) | 2026-10-10 | Về việc ban hành Quy chế tổ chức và hoạt động của Ban Chỉ đạo Trung ươ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=219963) | Không |
| 77 | 213397 | Công điện | 2025-04-17 | Về xử lý vụ việc sản xuất, phân phối sữa giả | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213397) | Không |
| 78 | 216178 | Quyết định (cá biệt) | 2025-12-11 | Ban hành Kế hoạch triển khai Bộ Công cụ ngăn ngừa và xử lý các hành vi | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216178) | Không |
| 79 | 213940 | Quyết định (cá biệt) | 2025-06-13 | Về việc công nhận huyện Đức Thọ, tỉnh Hà Tĩnh đạt chuẩn nông thôn mới  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213940) | Không |
| 80 | 216889 | Quyết định (cá biệt) | 2026-02-03 | Phê duyệt Đề án "Bồi dưỡng cán bộ Mặt trận Tổ quốc Việt Nam, các tổ ch | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=216889) | Không |
| 81 | 213410 | Công điện | 2025-04-19 | Về vụ án đối tượng mua bán trái phép chất ma túy tấn công lực lượng th | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213410) | Không. Họ tên liệt sĩ trong công điện của Thủ tướng là thông tin công bố, giữ |
| 82 | 213347 | Quyết định (cá biệt) | 2025-04-11 | Về việc kiện toàn thành viên Ban Chỉ đạo Nhà nước các công trình, dự á | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213347) | Không |
| 83 | 213108 | Quyết định (cá biệt) | 2025-03-13 | Về việc công nhận huyện Tiên Lãng, thành phố Hải Phòng đạt chuẩn nông  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213108) | Không |
| 84 | 218030 | Quyết định (cá biệt) | 2026-05-06 | Về việc sáp nhập Trường Cao đẳng Luật miền Nam vào Đại học Cần Thơ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218030) | Không |
| 85 | 217055 | Quyết định (cá biệt) | 2026-02-26 | Về việc đồng chí Thượng tướng Huỳnh Chiến Thắng thôi giữ chức Phó Tổng | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217055) | Không |
| 86 | 218332 | Quyết định (cá biệt) | 2026-06-02 | Về việc kiện toàn, tổ chức lại Ủy ban quốc gia về Thanh niên Việt Nam | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=218332) | Không |
| 87 | 220117 | Quyết định (cá biệt) | 2026-10-27 | Về việc chuyển giao Vườn quốc gia Cát Tiên - đơn vị sự nghiệp công lập | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=220117) | Không |
| 88 | 214788 | Công điện | 2025-08-04 | Về tập trung hoàn thành cắt giảm, đơn giản hóa thủ tục hành chính, điề | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214788) | Không |
| 89 | 214184 | Quyết định (cá biệt) | 2025-06-24 | Ban hành danh sách các đơn vị sự nghiệp công lập trực thuộc Bộ Văn hóa | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214184) | Không |
| 90 | 214689 | Quyết định (cá biệt) | 2025-07-22 | Ban hành Kế hoạch triển khai thi hành Luật Cán Bộ, công chức năm 2025 | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214689) | Không |
| 91 | 215026 | Công điện | 2025-08-24 | Tăng cường công tác bảo đảm an toàn, an ninh, trật tự, vệ sinh môi trư | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215026) | Không |
| 92 | 215768 | Quyết định (cá biệt) | 2025-11-03 | Thành lập Cổng thông tin điện tử Ban Chỉ đạo Phòng thủ dân sự quốc gia | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=215768) | Không |
| 93 | 217236 | Quyết định (cá biệt) | 2026-03-17 | Ban hành Kế hoạch triển khai thi hành Luật Bảo vệ bí mật nhà nước | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217236) | Không |
| 94 | 214501 | Quyết định (cá biệt) | 2025-07-08 | Về việc thành lập Ban Quản lý các khu chế xuất và công nghiệp Cần Thơ | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214501) | Không |
| 95 | 214444 | Quyết định (cá biệt) | 2025-07-04 | Về việc kiện toàn nhân sự Ủy ban hợp tác Việt Nam-Lào trong Ủy ban liê | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214444) | Không |
| 96 | 213062 | Công điện | 2025-03-09 | Về một số nhiệm vụ, giải pháp trọng tâm về cắt giảm thủ tục hành chính | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213062) | Không |
| 97 | 213535 | Quyết định (cá biệt) | 2025-05-05 | Về việc xuất cấp vắc xin Lở mồm long móng dự trữ quốc gia cho các địa  | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213535) | Không |
| 98 | 217087 | Quyết định (cá biệt) | 2026-03-03 | Phê duyệt đề án Xây dựng và công bố mức sống tối thiểu hằng năm làm că | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=217087) | Không |
| 99 | 214882 | Quyết định (cá biệt) | 2025-08-12 | Về việc thành lập Hội đồng thẩm định nhà nước thẩm định chủ trương đầu | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=214882) | Không |
| 100 | 213635 | Công điện | 2025-05-15 | Về mở đợt cao điểm đấu tranh ngăn chặn, đẩy lùi tình trạng buôn lậu, g | [mở](https://vanban.chinhphu.vn/?pageid=27160&docid=213635) | Không |
