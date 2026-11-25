# Báo cáo cá nhân — Trần Văn Quang — 2A202604032

## 1. Thông tin thành viên

- Họ tên: Trần Văn Quang.
- MSSV: 2A202604032.
- Email cá nhân: không công khai trong repo; GitHub: `OuyangXuelili`.
- Vai trong nhóm: người viết code A–B, tổng hợp chi phí và đầu mối tích hợp.

## 2. Phần việc phụ trách

Hoàn thiện mô hình chi phí A1–A4 và độ nhạy B1–B4; bàn giao số liệu cho phần pilot và hồ sơ launch. Phan Anh phụ trách D, Mạnh phụ trách C, Ân phụ trách E. Báo cáo này chỉ xác nhận phần A–B.

## 3. Đóng góp cụ thể

- Viết ba hàm A1 và `mo_hinh` trong [lab13.py](../../src/lab13.py). Tử số tính mọi lượt chạy; mẫu số chỉ đếm `thanh_cong`.
- Tách chi phí theo bốn loại yêu cầu, cộng chi phí cố định theo khối lượng và cơ cấu yêu cầu.
- Tính chín kịch bản độ nhạy, kịch bản hai yếu tố, giới hạn 1–3 lần chạy và chi phí hệ thống có phần nhân viên làm thay.
- Tính xem lại 100% theo giả định 9 phút làm lại và trung bình phút làm lại từ dữ liệu. Không cộng trùng thời gian cũ của A2.
- Sinh [bảng chi phí](bang_chi_phi.md) từ cùng mã tính bằng `python lab13.py --write-report`; cập nhật phân công trong `TEAM.md`.

## 4. Bằng chứng

- A1: ba phép thử cho kết quả 1,20; 1,25; 1,25 và in ĐẠT.
- A2: tổng chi phí 4.373.585 đ, 978 việc thành công; CPS 4.472 đ/việc [simulated].
- B3: giới hạn 2 lần cho chi phí cả hệ thống thấp nhất, 6.901.220 đ; CPS thấp nhất lại ở giới hạn 1 lần [simulated].
- B4: xem lại 100% cho CPS 11.743 đ với 9 phút làm lại; dùng trung bình chưa làm tròn 15,2973 phút/ca cho 12.415 đ [simulated], chưa tính cố định.
- Hai CSV và bản starter được giữ nguyên. Các kết quả có thể tính lại bằng lệnh trong `src/`.
- Đã chạy đạt 10 kiểm tra bổ sung: biên A1, phép tính tay trên trace nhỏ, tính bất biến của đầu vào, đối chiếu A2/A3/A4, độ nhạy B1/B2, lựa chọn B3, đếm yêu cầu B4 và báo cáo khớp phép tính.
- Bằng chứng thay đổi: [lịch sử phần A–B](https://github.com/OuyangXuelili/K5-L3B-DAY13-123-LaunchEconomics/commits/main/src/lab13.py). Chưa có bằng chứng review của thành viên khác.

## 5. Công cụ AI đã dùng

Dùng Codex để hỗ trợ triển khai code, kiểm lỗi và soạn bản báo cáo. Kiểm chứng bằng ba phép thử A1, phép tính tay trên mẫu nhỏ, đối chiếu số tham khảo của đề và kiểm tra báo cáo khớp output thực thi. Việc chạy bài không gọi model và không sử dụng API key.

Các điểm cần kiểm kỹ là lọc toàn bộ lượt chạy theo `request_id`, không sửa DataFrame gốc khi đổi giới hạn, và dùng cùng đơn vị khi so chi phí với nhân viên. Số trung bình chưa làm tròn khiến B4 lệch khoảng 1 đ so với số tham khảo; không sửa dữ liệu để ép trùng đáp án.

## 6. Tự đánh giá

Phần A–B đã có code và bảng số để kiểm chứng lại. Chỉ tối ưu CPS có thể làm tăng số việc chuyển cho nhân viên; vì vậy cần đọc thêm chi phí cả hệ thống trước khi chọn giới hạn chạy lại. Xem lại 100% làm lợi thế chi phí gần hết hoặc đảo chiều theo thời gian làm lại [simulated].

Nhóm còn cần tự giải thích các giả định, chạy lại trên máy thành viên khác và tích hợp C–E. Chưa có kết quả duyệt chéo hoặc quyết định Gate 2a để ghi nhận.
