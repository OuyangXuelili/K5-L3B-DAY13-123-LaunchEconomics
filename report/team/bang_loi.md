# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Nguyễn Hữu Mạnh · Người gắn nhãn 2: Nguyễn Hoàng Ân. Hai bộ nhãn độc lập và nhãn thống nhất chưa được cung cấp; nhập nhãn thật sau khi hai người đã làm độc lập, trước khi so sánh.

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... |
| 6 | ... | ... | ... | ... |
| 7 | ... | ... | ... | ... |
| 8 | ... | ... | ... | ... |
| 9 | ... | ... | ... | ... |
| 10 | ... | ... | ... | ... |
| 11 | ... | ... | ... | ... |
| 12 | ... | ... | ... | ... |
| 13 | ... | ... | ... | ... |
| 14 | ... | ... | ... | ... |
| 15 | ... | ... | ... | ... |
| 16 | ... | ... | ... | ... |
| 17 | ... | ... | ... | ... |
| 18 | ... | ... | ... | ... |
| 19 | ... | ... | ... | ... |
| 20 | ... | ... | ... | ... |

### Nhãn gợi ý do AI soạn — chỉ để Mạnh rà soát

Bảng dưới đây là phân tích gợi ý theo mô tả ca và nhãn tham khảo trong hướng dẫn gốc. Đây **không phải** bộ nhãn độc lập của Mạnh hoặc Ân, không được tính vào tỉ lệ đồng thuận và không thay thế các ô nhãn phía trên. Mạnh cần tự quyết định nhãn ban đầu của mình; không xem bảng này trước khi hoàn tất quy trình gắn nhãn độc lập nếu muốn giữ tính độc lập.

| Ca | Nhãn gợi ý | Lý do theo nguyên nhân gốc |
| --: | --- | --- |
| 1 | Do người dùng | Khách cung cấp số tài khoản thiếu hai chữ số. |
| 2 | Hệ thống | Agent dùng sai tham số loại hàng nên hoàn sai tiền. |
| 3 | Ngữ cảnh | Quy trình hoàn về ví đúng thiết kế nhưng không khớp kỳ vọng nhận tiền về ngân hàng. |
| 4 | Giới hạn hệ thống | Không có dữ liệu về chặng do hãng nước ngoài giao; agent đã chuyển nhân viên. |
| 5 | Ngầm | Hoàn theo giá trước giảm là lỗi không ai phát hiện cho tới khi kiểm tra mẫu. |
| 6 | Do người dùng | Khách chọn nhầm lý do hoàn phí so với mô tả hàng bị vỡ. |
| 7 | Hệ thống | Ghi sổ cái lỗi nhưng agent vẫn báo hoàn tiền thành công. |
| 8 | Hệ thống | Agent dẫn điều khoản không tồn tại; trích dẫn sai hiển thị cho người dùng/nhân viên. |
| 9 | Do người dùng | Khách nhập mã đơn của sàn thay vì mã vận đơn được yêu cầu. |
| 10 | Ngữ cảnh | Từ chối đúng chính sách nhưng không khớp kỳ vọng từ cam kết giao 24 giờ trên ứng dụng. |
| 11 | Giới hạn hệ thống | Agent không xử lý được đầu vào âm thanh. |
| 12 | Ngầm | Thiếu trường khiến gọi tool lặp lại, làm chi phí tăng kéo dài mà không có cảnh báo. |
| 13 | Giới hạn hệ thống | Yêu cầu bảo hiểm đối tác nằm ngoài phạm vi chức năng của agent. |
| 14 | Do người dùng | Khách bấm nhầm xác nhận đã nhận tiền. |
| 15 | Hệ thống | Agent áp sai mức hoàn 100% thay vì 50%; nhân viên bắt được trước khi gửi. |
| 16 | Ngữ cảnh | Gửi thông báo lúc 2:14 sáng đúng quy trình “gửi ngay” nhưng không phù hợp hoàn cảnh khách. |
| 17 | Ngầm | Dùng bảng giá cũ làm sai lệch nhiều đơn nhưng không có ai phát hiện/cảnh báo. |
| 18 | Ngữ cảnh | Số tiền tính đúng, nhưng thiếu giải thích khiến khách hiểu là hoàn thiếu. |
| 19 | Giới hạn hệ thống | Dữ liệu quá thời hạn lưu trữ agent có thể truy cập; agent đã chuyển nhân viên. |
| 20 | Hệ thống | Thiếu khóa chống trùng dẫn tới hoàn tiền hai lần. |

**Tỉ lệ đồng thuận:** ... / 20 = ...%

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- ...

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed`; cảnh báo khi vượt 2% tổng yêu cầu/ngày. | Nhận diện mã đơn từ sàn thương mại điện tử và tra sang mã vận đơn; nếu không tra được, hướng dẫn khách gửi mã đúng kèm ảnh. | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ: tìm tin nhắn “đã hoàn” không có bản ghi sổ cái `ok` cùng `trace_id`; ngưỡng chấp nhận là 0 ca. | Chỉ xác nhận hoàn tiền sau khi sổ cái trả `ok`; nếu API lỗi 503 sau 3 lần thử, báo đang xử lý và chuyển nhân viên. | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Theo dõi hằng tuần số yêu cầu mở lại vì khách cho rằng số tiền hoàn sai; kiểm tra mẫu xác nhận số tiền có khớp chính sách. | Hiển thị cách tính trong tin nhắn, ví dụ: `30.000 đ × 50% = 15.000 đ`. | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | Đếm event `handoff_to_staff` có `reason=thieu_du_lieu`, phân tách theo loại yêu cầu và tổng hợp hằng tuần. | Giữ luồng chuyển nhân viên kèm tóm tắt; loại yêu cầu quốc tế khỏi phạm vi pilot. | PM trợ lý hoàn phí |
| 17 | Ngầm | Kiểm tra mẫu 100 đơn/tuần so với bảng giá hiện hành; cảnh báo nếu từ 1% đơn trở lên lệch giá. | Xoá bộ nhớ đệm khi bảng giá đổi và ghi phiên bản bảng giá vào trace. | Kế toán trưởng |
