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
