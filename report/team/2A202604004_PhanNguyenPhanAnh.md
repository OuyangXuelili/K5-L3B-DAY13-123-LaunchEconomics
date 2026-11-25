# Báo cáo cá nhân — Phan Nguyễn Phan Anh — 2A202604004

## 1. Thông tin thành viên

- Họ tên: Phan Nguyễn Phan Anh.
- MSSV: 2A202604004; GitHub: `alpha19102004`.
- Email: không công khai email cá nhân trong repo.
- Vai được giao: người kiểm số A–B, người viết code D1/E1 và phụ trách kế hoạch pilot D.

## 2. Phần việc phụ trách

Kiểm độc lập số A–B của Quang; bổ sung năm câu D1 và ba phép tính E1 vào `src/lab13.py`; hoàn thiện `pilot_plan.yaml`. Phạm vi bàn giao E1 là code và số tính thử để người phụ trách E dùng trong hồ sơ.

## 3. Đóng góp cụ thể

- Viết `co_mau_hai_ty_le` theo công thức z hai tỉ lệ của đề, luôn làm tròn cỡ mẫu lên; dùng `NormalDist` lấy phân vị chính xác.
- Viết `co_mau_pilot` tính đủ D1 a–e, phân biệt mẫu thực và mẫu hiệu dụng, kiểm power khi tác động chỉ 5 điểm bằng `statsmodels`.
- Viết `chi_so_e1` và `tao_bao_cao_d1_e1`: in tử số, mẫu số và tỉ lệ; xử lý trường hợp không có ca được xem lại bằng giá trị chưa xác định thay vì chia cho 0.
- Hoàn thiện [kế hoạch pilot](pilot_plan.yaml): phạm vi, đối chứng, ngẫu nhiên theo nhân viên, rollout, bốn luật dừng, rollback, lịch đo và ngày quyết định đề xuất.
- Cập nhật đúng mục đóng góp cá nhân trong `TEAM.md`; giữ nguyên các hàm A–B, CSV và hồ sơ thuộc thành viên khác.

## 4. Bằng chứng

### Kiểm số A–B bằng phép tính độc lập

Trace `run_00001` có 4.759 token vào, 492 token ra, 5 tool: `4.759 / 1.000 × 26 + 492 / 1.000 × 130 + 5 × 15 = 262,694 đ`. Đây là token + tool của một lượt trong trace giả lập, không gồm thời gian nhân viên.

Tổng hợp độc lập từ hai CSV: token 245.585,132 đ + tool 84.000 đ + xem lại 1.780.000 đ + làm lại 2.264.000 đ = **4.373.585,132 đ**; chia cho **978** việc thành công được **4.471,968 đ/việc**, hiển thị **4.472 đ [simulated]**. Tử số lấy mọi lượt kể cả lỗi; mẫu số chỉ đếm `thanh_cong`.

Đối chiếu B3: giới hạn 1/2/3 lượt có chi phí hệ thống lần lượt **7.449.781 / 6.901.220 / 7.037.585 đ [simulated]** theo quy ước cộng 12.000 đ cho mỗi ca không thành công. Giới hạn **2 lượt** rẻ nhất toàn hệ thống; CPS thấp nhất lại ở 1 lượt, nên không chọn chỉ theo CPS.

### Kết quả D1

| Câu | Kết quả mỗi nhóm | Ý nghĩa |
| --- | --- | --- |
| a · Theo yêu cầu, +5 điểm | 1.251 yêu cầu, DE = 1 | Đủ mẫu độc lập nhưng có rủi ro tràn tác động giữa các ca của cùng nhân viên |
| b · Theo nhân viên, m = 75 | DE = 2,48; 3.103 yêu cầu; 42 người | Cần 84 người, vượt 40 người công ty có |
| c · 20 nhân viên | Mẫu hiệu dụng luôn < 1.000 | Không thể đạt 1.251 bằng cách kéo dài thời gian |
| d · 6 depot | Mẫu hiệu dụng luôn < 300 | Thiếu mẫu và chỉ có 6 cụm mỗi nhóm |
| e · Theo nhân viên, +6 điểm | 859 mẫu độc lập; 299 ca/người; DE = 6,96 | 20 × 299 = 5.980 ca thực, tương đương 859,1954 mẫu độc lập |

Chọn **20 nhân viên mỗi nhóm**, phân tầng theo depot, chấp nhận MDE **6 điểm phần trăm** theo giả định lab. Nếu tác động thật chỉ 5 điểm, power xấp xỉ **0,64175**, dưới 0,80. Đây là giới hạn thiết kế, chưa phải tác động hay kết quả pilot.

Trong YAML, `n_per_arm: 5980` là số yêu cầu thực tế; `independent_n_per_arm: 859` là số mẫu độc lập yêu cầu. CSV hiện chỉ có 20 staff/6 depot; điều kiện trước pilot là xác nhận roster đủ 40 người của 12 depot.

### Số E1 bàn giao

| Chỉ số trong đợt chạy thử | Tử số / mẫu số | Kết quả |
| --- | --- | --- |
| Đóng trong 24h và không mở lại trong 7 ngày | 994 / 1.200 | 82,83% |
| Sửa hoặc bỏ gợi ý / ca được xem lại | 48 / 177 | 27,12% |
| Mở lại trong 7 ngày / tổng yêu cầu | 51 / 1.200 | 4,25% |

Trong phạm vi `noi_dia + hang_nang`, mở lại là **39/982 = 3,97%**. Các số trên mô tả dữ liệu giả lập không có đối chứng; không thể nói trợ lý đã nâng chỉ số từ baseline 0,70.

### Cách chạy và kiểm chứng

Từ thư mục `src/`, chạy `python lab13.py` khi đã cài `requirements.txt`. Môi trường cục bộ của phiên hỗ trợ có thể chạy bằng `..\.venv\python.exe -B lab13.py`; `.venv/` được Git bỏ qua.

Bộ kiểm chứng của phiên hỗ trợ đạt **32 kiểm tra**: D1 khớp năm đáp án tham khảo; E1 khớp số đếm độc lập từ CSV; xử lý được trường hợp không có ca xem lại và giữ nguyên DataFrame. YAML đọc được bằng `yaml.safe_load`, đủ trường, không còn dấu hỏi, có bốn luật dừng đủ bốn vế; chương trình chạy hết từ `src/`.

Các hàm A–B được so với bản gốc; báo cáo A–B sinh trong bộ nhớ khớp file hiện hữu. Không chạy tùy chọn ghi báo cáo của Quang trong quá trình kiểm phần D/E1.

## 5. Công cụ AI đã dùng

Dùng Codex hỗ trợ triển khai D1/E1, tính đối chiếu, soạn kế hoạch pilot và chạy kiểm chứng. Các phép kiểm nêu trên được thực thi trong phiên hỗ trợ; thành viên cần tự đọc, kiểm lại và giải thích được công thức khi bảo vệ.

Nguồn: hai CSV của đề; [công thức](../../docs/du_lieu_va_cong_thuc.md); [hướng dẫn D–E](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md); phân công được cung cấp trong `đ.txt`. Không gọi model thật hoặc dùng API key khi chạy bài.

## 6. Tự đánh giá

Phần D1/E1 và kế hoạch D đã có mã tính, số đối chiếu và giả định rõ ràng. Mức power 0,80 là xấp xỉ theo ICC 0,02; số cụm hữu hạn và ICC thực tế có thể làm hiệu lực thấp hơn, nên pilot phải báo khoảng tin cậy có xét cụm.

Pilot đề xuất bắt đầu 2026-11-30, có tuần chờ dữ liệu 7 ngày giữa các bậc, đo chính 2026-12-28 đến 2027-01-17, theo dõi đến 2027-01-25 và quyết định 2027-01-26 (GMT+7). Thiếu mẫu hoặc chậm rollout thì ghi chưa đủ bằng chứng, không rút ngắn theo dõi.

Rủi ro kinh tế cần giữ trong quyết định: xem lại 100% cho CPS B4 khoảng **11.743–12.415 đ [simulated]**, chưa cố định; phương án pilot 2 lượt phải đo lại chi phí thật. Quyết định Gate 2a, đóng góp tại lớp và duyệt chéo của nhóm chưa được xác nhận trong báo cáo này.
