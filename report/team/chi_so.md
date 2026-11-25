# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Tử số / Mẫu số | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính | Tỷ lệ đóng trong 24 giờ và không mở lại trong 7 ngày | Số yêu cầu có `dong_trong_24h = 1` và `mo_lai_trong_7_ngay = 0` / tổng số yêu cầu | 994/1.200 = **82,83%** |
| Sử dụng | Tỷ lệ bỏ qua gợi ý | Số yêu cầu được xem lại có quyết định `sua` hoặc `bo` / tổng số yêu cầu được xem lại | 48/177 = **27,12%** |
| An toàn | Tỷ lệ mở lại trong 7 ngày | Số yêu cầu có `mo_lai_trong_7_ngay = 1` / tổng số yêu cầu | 51/1.200 = **4,25%** |
| Sử dụng, bổ sung | Tỷ lệ yêu cầu thuộc nhóm can thiệp có dùng trợ lý | Số yêu cầu thuộc nhóm can thiệp có ít nhất một lần nhân viên mở trợ lý / tổng số yêu cầu thuộc nhóm can thiệp trong phạm vi pilot | Đo trong pilot |
| An toàn, bổ sung | Tỷ lệ hoàn sai tiền trong mẫu kiểm tra | Số yêu cầu trong mẫu có số tiền đã hoàn khác số tiền đúng / số yêu cầu trong mẫu đã đối soát xong | Đo trong pilot |

Ba kết quả từ hàm `chi_so_e1` trong [lab13.py](../../src/lab13.py) mô tả đợt chạy thử giả lập. Đợt này chưa có nhóm đối chứng để ước lượng tác động của trợ lý.

## Danh sách event

Tạo `trace_id` ngay khi nhận yêu cầu và dùng lại xuyên suốt, kể cả khi yêu cầu được xử lý thủ công. Mỗi event có `request_id`, `trace_id` và thời điểm xảy ra.

| Event | Ai tạo | Thuộc tính ngoài các trường chung | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | Hệ thống tiếp nhận | `loai`, `depot_id` | Khi nhận yêu cầu |
| `pilot_arm_assigned` | Hệ thống phân nhóm pilot | `arm`, `assignment_unit_id`, `staff_id` | Khi xác định nhánh xử lý trước khi nhân viên thao tác |
| `assistant_opened` | Giao diện nhân viên | `staff_id` | Khi nhân viên mở trợ lý cho yêu cầu |
| `agent_run_completed` | Trợ lý | `run_id`, `attempt`, `tokens_in`, `tokens_out`, `tool_calls`, `status` | Sau mỗi lần chạy, kể cả lần lỗi |
| `staff_review_decision` | Giao diện nhân viên | `staff_id`, `decision` (`giu`, `sua`, `bo`), `review_seconds` | Khi chốt quyết định xem lại |
| `staff_rework_completed` | Giao diện nhân viên | `staff_id`, `reason`, `rework_seconds` | Khi hoàn tất xử lý lại do kết quả trợ lý sai |
| `ticket_closed` | Hệ thống ticket | `closed_at` | Mỗi lần đóng yêu cầu |
| `ticket_reopened` | Hệ thống ticket | `reopened_at`, `previous_closed_at`, `reason` | Khi mở lại yêu cầu, kèm mốc đóng ngay trước đó |
| `audit_sample_checked` | Bộ phận đối soát | `audit_batch_id`, `actual_refund_vnd`, `expected_refund_vnd` | Khi đối soát xong một yêu cầu trong mẫu |
| `refund_ledger_write` | Dịch vụ sổ cái | `refund_key`, `idempotency_key`, `transaction_id`, `amount_vnd`, `status` | Sau mỗi lần thử ghi hoàn tiền |
| `refund_confirmation_sent` | Dịch vụ thông báo | `refund_key`, `notification_id` | Khi gửi xác nhận đã hoàn cho khách |

### Event dùng để tính chỉ số

| Chỉ số | Cách lấy tử số và mẫu số từ event |
| --- | --- |
| Đóng trong 24 giờ, không mở lại trong 7 ngày | Mẫu số là các yêu cầu tiếp nhận trong kỳ qua `refund_request_created`. Tử số lấy lần đóng đầu tiên từ `ticket_closed`, so với thời điểm tiếp nhận, và kiểm tra `ticket_reopened` trong 7 ngày sau lần đóng đó. Chờ hết cửa sổ theo dõi của các ca đóng trong 24 giờ rồi chốt tỷ lệ. |
| Bỏ qua gợi ý | Mẫu số là số yêu cầu có `staff_review_decision`. Lấy quyết định cuối của mỗi yêu cầu và đếm `sua` hoặc `bo` cho tử số. |
| Mở lại trong 7 ngày | Mẫu số lấy từ `refund_request_created`. Tử số đếm các yêu cầu có `ticket_reopened` trong 7 ngày kể từ lần đóng ngay trước đó. Ghi rõ kỳ tiếp nhận và kỳ theo dõi để đánh giá các nhóm trên cùng khoảng thời gian. |
| Yêu cầu thuộc nhóm can thiệp có dùng trợ lý | Mẫu số lấy từ `pilot_arm_assigned` với nhánh can thiệp. Tử số là các yêu cầu trong mẫu số có ít nhất một `assistant_opened`. |
| Hoàn sai tiền trong mẫu kiểm tra | Mẫu số lấy từ `audit_sample_checked` của đợt kiểm tra. Tử số đếm các yêu cầu có `actual_refund_vnd` khác `expected_refund_vnd`. |

Đếm theo `request_id` để mỗi yêu cầu chỉ xuất hiện một lần trong từng tỷ lệ. Dùng `trace_id` để nối với các lần chạy của trợ lý khi cần kiểm tra.

Khi áp luật dừng an toàn của [kế hoạch pilot](pilot_plan.yaml), tỷ lệ mở lại dùng mẫu số là các yêu cầu đã đủ 7 ngày kể từ lúc đóng. Trần **trên 6%** áp dụng ở mọi bậc. Chênh lệch với đối chứng **từ 2 điểm phần trăm** chỉ áp dụng từ bậc 10 người cùng điều kiện đủ mẫu trong kế hoạch.

Đối soát hoàn trùng bằng cách tìm nhiều `transaction_id` ghi thành công cho cùng `refund_key`, kể cả khi có nhiều `trace_id`. Đối chiếu mỗi `refund_confirmation_sent` với lần ghi sổ thành công của cùng `refund_key` trước lúc gửi. Cả hai sự cố đều áp luật dừng ngay khi phát hiện, từ bậc 4 người.

## E2 · Rủi ro kinh tế

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động đề xuất | Người phụ trách đề xuất |
| --- | --- | --- | --- | --- |
| Số ca phải làm lại tăng gấp đôi | B1: chi phí mỗi việc thành công tăng **51,8%**, từ **4.472** lên **6.787 đ** (`simulated`). | Theo dõi hằng tuần tỷ lệ yêu cầu phải làm lại và thời gian xử lý lại từ `staff_rework_completed`. | Rà trace để xác định loại yêu cầu gây tăng chi phí. Khi chạm luật dừng chi phí, đề xuất thu hẹp về nội địa. | Quản lý sản phẩm trợ lý hoàn phí |
| Phải duy trì xem lại 100% | B4: chi phí cả hệ thống là **11.764 đ/yêu cầu** với 9 phút làm lại, hoặc **12.380 đ/yêu cầu** với trung bình dữ liệu, so với mốc tự làm **12.000 đ/yêu cầu** (`simulated`, chưa tính cố định). | Theo dõi số phút xem lại thực tế và tỷ lệ yêu cầu có `staff_review_decision` theo tuần. | Rà những loại yêu cầu mất nhiều thời gian. Nếu đủ bằng chứng an toàn, trình phương án giảm xem lại để Giám đốc vận hành duyệt trước cửa sổ đo chính. | Trưởng nhóm CSKH |
| Phân bổ chi phí cố định khi số ca còn ít | Từ A4, nếu bậc 4/40 người xử lý 10% sản lượng và gánh đủ **40 triệu đ/tháng**, khoảng **3.375 việc thành công/tháng** làm chi phí cố định tăng thêm khoảng **11.852 đ/việc** (`simulated`). | Theo dõi khối lượng việc thành công và báo riêng chi phí cố định trên mỗi việc. | Rà cách phân bổ và điều khoản phí cố định nếu khối lượng thấp. Áp ngưỡng **8.000 đ/việc thành công** lên chi phí biến đổi. Khi đánh giá cuối pilot, dùng chi phí cả hệ thống gồm phần cố định. | Quản lý sản phẩm trợ lý hoàn phí |
