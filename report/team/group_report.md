# Báo cáo nhóm

## 1. Thông tin nhóm

- **Nhóm 123 · Lớp L3B**
- [Thông tin và đóng góp của thành viên](../../TEAM.md)

## 2. Mục tiêu và cách tiếp cận

Nhóm phân tích 1.200 yêu cầu hoàn phí và 1.624 lượt chạy giả lập để đánh giá chi phí, mức sử dụng và rủi ro của trợ lý LogiX-VN. Kết quả được dùng để thiết kế pilot có đối chứng và chuẩn bị đề xuất tại Gate 2a.

## 3. Giải pháp

- **A · Chi phí.** Cộng chi phí token, tool và thời gian nhân viên để tính chi phí trên mỗi yêu cầu thành công. Phân tích theo loại yêu cầu và tính chi phí cố định trong phạm vi pilot. [Bảng chi phí](bang_chi_phi.md)
- **B · Độ nhạy.** Thay đổi các giả định chi phí, so giới hạn số lần chạy và kiểm tra kịch bản xem lại toàn bộ. [Bảng độ nhạy](bang_chi_phi.md#b1--đổi-từng-yếu-tố)
- **C · Lỗi.** Mạnh và Ân đã rà soát và xác nhận các nhãn. Bảng ghi nhãn thống nhất và cách phát hiện, khắc phục cho 5 loại lỗi. [Bảng lỗi](bang_loi.md)
- **D · Pilot.** So các đơn vị phân nhóm theo cỡ mẫu hiệu dụng và nguy cơ ảnh hưởng giữa hai nhánh. Chọn cách chia, chỉ số chính, ngưỡng dừng và cách quay về quy trình thủ công. [Kế hoạch pilot](pilot_plan.yaml)
- **E · Chỉ số và hồ sơ.** Đặc tả chỉ số, event đo lường và rủi ro kinh tế, rồi tổng hợp bằng chứng để nhóm chốt đề xuất. [Chỉ số và rủi ro](chi_so.md) · [Hồ sơ launch](ho_so_launch_v0.md)

## 4. Kết quả

- **Chi phí** — 4.472 đ/việc thành công trên toàn mẫu. Trong phạm vi nội địa và hàng nặng, chi phí cả hệ thống gồm nhân viên làm thay và cố định là 5.217 đ/yêu cầu tại mức 45.000 yêu cầu/tháng, so với 12.000 đ/yêu cầu tự làm. Kịch bản xem lại 100% có thể lên 12.415 đ/việc thành công trước cố định. Các kết quả chi phí này là `simulated`.
- **Chỉ số chạy thử giả lập** — 994/1.200 đóng trong 24 giờ và không mở lại trong 7 ngày (82,83%), 48/177 sửa hoặc bỏ gợi ý (27,12%), 51/1.200 mở lại trong 7 ngày (4,25%).
- **Phân loại lỗi** — Đã xác minh hai cột nhãn sau rà soát trùng 20/20 ca. Ưu tiên kiểm tra khóa chống hoàn trùng và đối soát sổ cái trước pilot.
- **Đề xuất dự thảo** — Go có điều kiện cho pilot nội địa và hàng nặng, chờ nhóm thống nhất. Kế hoạch dùng 20 nhân viên và 5.980 yêu cầu mỗi nhánh để phát hiện chênh lệch 6 điểm phần trăm. [Hồ sơ launch](ho_so_launch_v0.md)
- **Kết quả duyệt chéo** — Bổ sung quyết định và phản hồi nhóm nhận được từ hội đồng sau buổi duyệt.

## 5. Khó khăn và cách xử lý

Phân nhóm theo nhân viên giúp giảm nguy cơ một người luân phiên giữa hai cách xử lý, nhưng với 20 người mỗi nhánh, thiết kế theo giả định của lab thiếu mẫu để phát hiện chênh lệch 5 điểm phần trăm ở mức power 0,80. Kế hoạch chọn thiết kế 6 điểm và ghi rõ đánh đổi để nhóm xem xét tại Gate 2a.

## 6. Tổng hợp đóng góp

- **Trần Văn Quang** phụ trách mô hình chi phí và độ nhạy, kiểm tra bản tích hợp và push.
- **Phan Nguyễn Phan Anh** kiểm số, phụ trách kế hoạch pilot và bổ sung phép tính E1.
- **Nguyễn Hữu Mạnh** rà soát và xác nhận cột nhãn thứ nhất, phụ trách bảng lỗi và phiếu chấm nhóm khác.
- **Nguyễn Hoàng Ân** rà soát và xác nhận cột nhãn thứ hai, phụ trách chỉ số, hồ sơ launch và báo cáo nhóm.

Chi tiết đóng góp và bằng chứng tại [TEAM.md](../../TEAM.md).

## 7. Hạn chế và hướng cải thiện

Dữ liệu chạy thử là giả lập và chưa có nhóm đối chứng. Pilot cần đo thời gian xem lại và làm lại thực tế ở cùng kỳ quan sát. Kết quả đối chiếu sau rà soát chưa xác minh tiêu chí đồng thuận khi gắn nhãn độc lập.

## 8. Tài liệu tham khảo

- [Dữ liệu và công thức của lab](../../docs/du_lieu_va_cong_thuc.md)
- [Đề bài học viên](../../docs/Ngay13_Lab13_De_bai_hoc_vien.docx)
- [Hướng dẫn chi tiết Lab 13](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md)
