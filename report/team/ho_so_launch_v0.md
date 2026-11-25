# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

**Nhóm 123 · Lớp L3B**

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | **4.472 đ** toàn mẫu. Nội địa và hàng nặng là **4.599 đ** sau cộng cố định ở mức 45.000 yêu cầu/tháng (`simulated`). [A2, A4](bang_chi_phi.md) | Giả lập | Quản lý sản phẩm trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | Làm lại gấp đôi **+51,8%**, xem lại gấp đôi **+40,7%**, lương tăng 25% làm chi phí tăng **23,1%** (`simulated`). [B1–B2](bang_chi_phi.md) | Giả lập | Quản lý sản phẩm trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Theo A4, **5.217 đ/yêu cầu** trong phạm vi, gồm nhân viên làm thay và cố định, so với **12.000 đ/yêu cầu** tự làm ở mức 45.000 yêu cầu/tháng (`simulated`). [A4](bang_chi_phi.md) | Giả lập | Giám đốc vận hành |
| 4 · Chỉ số chính, sử dụng và an toàn | Đợt chạy thử giả lập: **82,83%** đóng trong 24 giờ và không mở lại trong 7 ngày, **27,12%** sửa hoặc bỏ gợi ý, **4,25%** mở lại trong 7 ngày. [E1](chi_so.md) | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và cách khắc phục | Đã xác minh hai cột nhãn trùng **20/20** sau rà soát. Tiêu chí đồng thuận độc lập chưa được xác minh. Có biện pháp cho **5 loại lỗi**, ưu tiên chống hoàn trùng và đối soát sổ cái. [Bảng lỗi](bang_loi.md) | Chưa | Kỹ sư trưởng trợ lý hoàn phí |
| 6 · Kế hoạch pilot | Nội địa và hàng nặng. Chia ngẫu nhiên theo nhân viên, **20 người và 5.980 yêu cầu mỗi nhánh**, mức chênh thiết kế **6 điểm phần trăm**, **4 luật dừng**. [Kế hoạch đề xuất](pilot_plan.yaml) | Xong, có bằng chứng | Giám đốc vận hành |
| 7 · Rủi ro kinh tế | Làm lại gấp đôi đưa chi phí lên **6.787 đ/việc thành công**. Xem lại 100% có thể đưa chi phí lên **12.415 đ/việc thành công** trước cố định (`simulated`). [E2](chi_so.md#e2--rủi-ro-kinh-tế) | Giả lập | Quản lý sản phẩm trợ lý hoàn phí |

**Căn cứ đề xuất**

Trong phạm vi nội địa và hàng nặng, A4 ước tính **5.217 đ/yêu cầu** so với **12.000 đ/yêu cầu** khi nhân viên tự làm. Trong kịch bản B4 xem lại 100% với thời gian làm lại trung bình, chi phí cả hệ thống lên **12.380 đ/yêu cầu** ngay cả khi chưa cộng chi phí cố định. Cả hai là số `simulated`. Pilot đo chi phí thực tế và tác động với nhóm đối chứng.

**Điều kiện triển khai**

- Trước **30/11/2026**, Giám đốc vận hành xác nhận đủ 40 nhân viên và chấp nhận thiết kế phát hiện chênh lệch 6 điểm. Nếu tác động thật chỉ 5 điểm, xác suất phát hiện theo thiết kế chỉ khoảng **0,64**.
- Trước **30/11/2026**, chủ dịch vụ hoàn phí kiểm tra chống hoàn trùng, đối soát sổ cái và thử rollback. Quản lý sản phẩm xác nhận các event và số phút đo thực tế.
- Trước cửa sổ đo chính dự kiến **28/12/2026**, Giám đốc vận hành chốt chính sách xem lại theo bằng chứng an toàn. Đến **26/01/2027**, chỉ đề xuất tiếp tục nếu đủ mẫu và thời gian theo dõi, cận dưới khoảng tin cậy 95% của chênh lệch chỉ số chính lớn hơn 0, đạt điều kiện an toàn và chi phí toàn hệ thống dưới **12.000 đ/yêu cầu**.

**Đề xuất Gate 2a** — **Go có điều kiện** cho pilot nội địa và hàng nặng.
