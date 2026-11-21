# M3 · Bộ đánh giá VBHC-Bench bản pilot · báo cáo

- **Ngày:** 21/11/2026 · **Người dựng và người kiểm đáp án:** chuyên gia mô phỏng (AI, Claude), theo QĐ-08. Chưa có người kiểm.
- **Mã:** `scripts/m3_dung_bo.py`, `scripts/cham_diem.py`, `scripts/moc_khong_mo_hinh.py`. Dữ liệu: thư mục `m3/`. Nguồn: bộ toàn văn v4.

## Bộ đánh giá gồm gì

285 mục kiểm tra trên năm loại văn bản của QĐ-02, mục tiêu ban đầu là 300.

| Nhiệm vụ | Số mục | Đầu vào | Đáp án lấy từ đâu | Ai chấm |
| --- | --- | --- | --- | --- |
| T1 Soạn văn bản | 41 | Cơ quan, số, ngày, trích yếu | Văn bản thật làm tham chiếu | Máy chấm thể thức; nội dung cần người chấm |
| T2 Tìm lỗi thể thức | 94 | Văn bản thật có một lỗi cài, hoặc không lỗi | Chính lỗi đã cài (11 kiểu, 18 mục không lỗi) | Máy |
| T3 Trích thông tin | 150 | Văn bản quét đã bóc chữ | Chỉ mục cổng, chỉ lấy ô mà toàn văn cũng xác nhận | Máy |

T1 thiếu chỉ thị (1 mục) và T2 thiếu quyết định, công điện, chỉ thị (4 mục) vì ít văn bản loại này vừa đủ sạch vừa đủ ngắn.

## Chia tập theo cụm mẫu

- Văn bản gần trùng mẫu, hoặc cùng cơ quan và cùng trích yếu sau khi bỏ số và ngày tháng, được gom thành một cụm. Có 329 cụm nhiều hơn một văn bản; cụm lớn nhất 80 văn bản (thông báo kết quả chỉ đạo điều hành hằng tuần).
- 285 văn bản kiểm tra; 222 văn bản cùng cụm với chúng bị giữ ngoài, không dùng huấn luyện; 5.454 huấn luyện; 333 thẩm định.
- Kịch bản tự kiểm: không văn bản kiểm tra nào, và không cụm nào của chúng, nằm trong tập huấn luyện.
- Tập huấn luyện: 2.069 ví dụ dạng hội thoại (T3 1.200, T2 khoảng 600, T1 269). Tập thẩm định: 132.

## Ba mốc không dùng mô hình ngôn ngữ

| Mốc | T1 | T2 | T3 | Ý nghĩa |
| --- | --- | --- | --- | --- |
| Trả đúng đáp án | 98,8 | 100 | 100 | Bộ chấm chạy đúng; T1 không đạt 100 vì 2 văn bản tham chiếu có dòng ngày bị OCR làm méo |
| Trả lời rỗng | 0 | 0 | 0 | Sàn |
| Biểu thức chính quy và bộ luật M1 | không làm được | 95,7 | 86,7 | Mốc phải vượt |

Chi tiết T3 của mốc luật: số ký hiệu 96,0; ngày 98,7; loại 96,0; trích yếu 56,2.

**Hệ quả cho thiết kế:** T2 và ba trường đầu của T3 gần như giải được bằng luật viết tay. Phần phân biệt được mô hình tốt với mô hình kém là T1 và trường trích yếu của T3. Khi báo cáo điểm phải nêu mốc luật bên cạnh, nếu không điểm T2 cao sẽ gây hiểu nhầm.

## Kiểm đáp án

- **Hai nguồn độc lập cho T3:** mỗi đáp án số ký hiệu và ngày đều khớp giữa trang chỉ mục của cổng và toàn văn bóc từ tệp PDF. Ô nào hai nguồn lệch thì không được vào bộ kiểm tra.
- **Lượt đọc mô phỏng:** 24 mục T3 ngẫu nhiên. Số ký hiệu, ngày, loại: 24/24 đúng với văn bản. Trích yếu: 23/24; mục còn lại (T3-0078) chỉ mục của cổng ghi một câu diễn đạt lại, khác trích yếu in trên văn bản.
- **Giới hạn:** khoảng 4% trích yếu trong đáp án có thể là câu diễn đạt lại của cổng. Điểm trích yếu tính theo F1 nên bị trừ một phần chứ không mất hết. Chưa có người thứ hai đọc.

## Bốn điều chưa đạt chuẩn chính thức

1. Đáp án chưa được người kiểm. QĐ-08 yêu cầu người đọc lại một phần mẫu trước khi công bố.
2. Điểm nội dung T1 chưa có: cần hướng dẫn chấm và người chấm sau khi có bài của mô hình.
3. Đầu vào T2, T3 là chữ bóc từ bản quét, còn lỗi OCR. Phản ánh đúng việc thật nhưng làm nhiễu phép đo.
4. Đáp án kiểm tra đang để công khai trong kho mã. Tiện cho việc chạy lại; đổi lại, mô hình về sau có thể đã học phải.

## Đề xuất cổng M3

Đạt ở mức pilot (mô phỏng). Sang M4 được.
