# Bảng chi phí · Nhiệm vụ A và B

Người phụ trách: Trần Văn Quang — 2A202604032. Toàn bộ dữ liệu của lab là giả lập. Các tổng, tỉ lệ hoặc so sánh dùng phút `_simulated` đều mang nhãn **simulated**. Số tiền tính bằng đồng; chỉ làm tròn khi hiển thị.

Sinh lại bằng `cd src` rồi `python lab13.py --write-report`. Hai CSV và `lab13_starter.py` được giữ nguyên; không cần API key.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8) | Kết quả |
| --- | --- |
| Số lần chạy trung bình, tối đa 2 lần | 1,20 |
| Số lần chạy trung bình, chạy đến khi đúng | 1,25 |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 |

Ba phép thử ĐẠT. Công thức A1 giả định các lần thử độc lập với xác suất đúng không đổi; A2–B4 tính trực tiếp từ trace, không áp giả định độc lập lên dữ liệu.

## A2 · Mô hình chi phí từ trace

Mẫu có 1.200 yêu cầu và 1.624 lần chạy. Tử số tính mọi lần chạy, kể cả lỗi; mẫu số chỉ đếm việc thành công.

| Khoản | Giá trị | Nguồn / cách tính | Nhãn |
| --- | --- | --- | --- |
| Token | 245.585 | `logix_runs.csv` | đo từ trace giả lập |
| Tool | 84.000 | `logix_runs.csv` | đo từ trace giả lập |
| Trong đó, lần chạy thứ 2 và 3 | 93.804 | `attempt > 1` | đã nằm trong token + tool |
| Xem lại | 1.780.000 | `phut_xem_lai_simulated` | simulated |
| Làm lại | 2.264.000 | `phut_lam_lai_simulated` | simulated |
| Tổng chi phí | 4.373.585 | token + tool + xem lại + làm lại | simulated |
| Số việc thành công | 978 | `ket_qua == thanh_cong` | từ dữ liệu giả lập |
| Chi phí mỗi việc thành công | 4.472 | tổng / số việc thành công | simulated |
| Hoá đơn token và tool / số yêu cầu | 274,7 | (token + tool) / số yêu cầu | đo từ trace giả lập |

- CPS gấp 16,3 lần hoá đơn / yêu cầu [simulated].
- Làm lại lớn nhất: 51,8%; tổng giờ xem lại và làm lại chiếm 92,5% chi phí [simulated].

So sánh cùng đơn vị theo quy ước B3: (4.373.585 + 222 × 12.000) / 1.200 = **5.865 đ/yêu cầu**, 0,49× nhân viên tự làm [simulated], chưa cộng cố định. 148 ca chuyển nhân viên có 0 phút trong cột simulated; không dùng riêng CPS / 12.000 để kết luận tiết kiệm cả hệ thống.

## A3 · Tách theo loại yêu cầu

| Loại | Số yêu cầu | Thành công | Lần chạy / yêu cầu | CPS [simulated] | CPS / 12.000 [simulated] |
| --- | --- | --- | --- | --- | --- |
| noi_dia | 824 | 95,0% | 1,11 | 2.696 | 0,22× |
| hang_nang | 158 | 74,1% | 1,47 | 8.221 | 0,69× |
| quoc_te | 150 | 27,3% | 2,32 | 22.515 | 1,88× |
| doi_tac | 68 | 54,4% | 1,88 | 10.215 | 0,85× |

Tỉ lệ `status == ok` trong từng lần thử (mẫu của lần thử sau đã được chọn bởi các lần trước):

| Loại | Lần 1 | Lần 2 | Lần 3 |
| --- | --- | --- | --- |
| noi_dia | 91,0% | 75,7% | 38,9% |
| hang_nang | 70,9% | 39,1% | 17,9% |
| quoc_te | 30,0% | 11,4% | 2,2% |
| doi_tac | 51,5% | 18,2% | 14,8% |

`quoc_te` có CPS 22.515 đ = 1,88× [simulated], thành công 27,3%; tỉ lệ ok lần 3 chỉ 2,2%, nên loại khỏi phạm vi đề xuất.

`doi_tac` có CPS 0,85× [simulated] và thành công 54,4%; có điều khoản riêng, tạm loại. Phạm vi đề xuất là `noi_dia` + `hang_nang`; cần kiểm chi phí cả hệ thống và kiểm soát xem lại trước khi chốt pilot.

## A4 · Chi phí cố định: noi_dia + hang_nang [simulated]

Giữ cơ cấu mẫu và tính 40.000.000 đ cố định/tháng. Khối lượng là tổng yêu cầu công ty; việc thành công trong phạm vi/tháng = khối lượng × 900 / 1.200.

| Tổng yêu cầu / tháng | Thành công trong phạm vi / tháng | Cố định / việc | CPS + cố định | / 12.000 |
| --- | --- | --- | --- | --- |
| 45.000 | 33.750 | 1.185 | 4.599 | 0,38× |
| 22.500 | 16.875 | 2.370 | 5.784 | 0,48× |

CPS cộng cố định vẫn dưới 12.000 đ ở cả hai mức 45.000 và 22.500 yêu cầu/tháng [simulated]. Đây là kiểm tra độ nhạy, chưa đủ để kết luận tiết kiệm cả hệ thống.

Tính cả việc nhân viên làm thay trong phạm vi và cố định: 5.217 và 6.303 đ/yêu cầu trong phạm vi, lần lượt 0,43× và 0,53× [simulated].

## B1 · Đổi từng yếu tố [simulated]

Gốc: 4.472 đ/việc thành công. Mỗi dòng chỉ thay yếu tố được nêu; ca vượt giới hạn chạy được chuyển nhân viên và có phút xem lại/làm lại bằng 0.

| Kịch bản | Cách tính | CPS [simulated] | Thay đổi [simulated] |
| --- | --- | --- | --- |
| Giá token gấp đôi | 52 đ vào; 260 đ ra / 1.000 token | 4.723 | 5,6% |
| Giá token giảm một nửa | 13 đ vào; 65 đ ra / 1.000 token | 4.346 | -2,8% |
| Tỉ lệ xem lại gấp đôi | Tiền xem lại × 2 | 6.292 | 40,7% |
| Tỉ lệ xem lại giảm một nửa | Tiền xem lại × 0,5 | 3.562 | -20,3% |
| Số ca làm lại gấp đôi | Tiền làm lại × 2 | 6.787 | 51,8% |
| Số ca làm lại giảm một nửa | Tiền làm lại × 0,5 | 3.315 | -25,9% |
| Lương nhân viên tăng 25% | 2.500 đ/phút | 5.506 | 23,1% |
| Chỉ cho chạy tối đa 2 lần | Bỏ attempt > 2; ca vượt giới hạn chuyển nhân viên | 4.237 | -5,2% |
| Chỉ cho chạy 1 lần | Bỏ attempt > 1; ca vượt giới hạn chuyển nhân viên | 4.111 | -8,1% |

## B2 · Đổi một cặp và xếp hạng [simulated]

Giá token và xem lại cùng gấp đôi: 6.543 đ, tăng 46,3%. Hai tác động cộng được vì mô hình tuyến tính theo các khoản chi phí.

Xếp hạng tác động tăng: 1. Số ca làm lại gấp đôi (+51,8%); 2. Tỉ lệ xem lại gấp đôi (+40,7%); 3. Lương nhân viên tăng 25% (+23,1%).

## B3 · Giới hạn chạy lại và chi phí cả hệ thống [simulated]

Chi phí cả hệ thống = tổng trợ lý + 12.000 đ × số yêu cầu không thành công, theo quy ước của nhiệm vụ B3.

| Giới hạn | Tổng trợ lý | Không thành công | Cả hệ thống | CPS |
| --- | --- | --- | --- | --- |
| 1 | 3.621.781 | 319 | 7.449.781 | 4.111 |
| 2 | 4.093.220 | 234 | 6.901.220 | 4.237 |
| 3 | 4.373.585 | 222 | 7.037.585 | 4.472 |

Giới hạn 2 lần rẻ nhất cho công ty: 6.901.220 đ. CPS thấp nhất ở 1 lần: 4.111 đ; nhưng chuyển thêm 85 việc sang nhân viên [simulated].

## B4 · Xem lại 100% trong phạm vi noi_dia + hang_nang [simulated]

Có 982 yêu cầu; 948 yêu cầu có ít nhất một lượt ok, xem lại 5 phút/yêu cầu; 48 ca làm lại; 900 việc thành công; token + tool 224.513 đ. Không cộng lại phút xem/làm lại cũ của A2.

| Kịch bản | Phút / ca làm lại | Xem lại | Làm lại | Tổng | CPS | CPS / 12.000 | Hệ thống / yêu cầu |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Giả định đề: 9 phút | 9,00 | 9.480.000 | 864.000 | 10.568.513 | 11.743 | 0,98× | 11.764 |
| Trung bình dữ liệu | 15,30 | 9.480.000 | 1.468.541 | 11.173.054 | 12.415 | 1,03× | 12.380 |

Giả định đề cho CPS 11.743 đ = 0,98×; dùng trung bình dữ liệu 15,2973 phút/ca (trung vị 14,5) cho CPS 12.415 đ = 1,03× [simulated], đều chưa cộng cố định.

Pilot cần kiểm tra có thể giảm xem lại an toàn hay không: thời gian xem lại hoà vốn tối đa 5,12 phút khi làm lại 9 phút, hoặc 4,80 phút khi làm lại 15,30 phút [simulated].

## Nguồn và bàn giao

- Dữ liệu: `src/logix_runs.csv`, `src/logix_requests.csv` do đề cung cấp.
- Công thức và giả định: [tài liệu dữ liệu](../../docs/du_lieu_va_cong_thuc.md), [hướng dẫn A–B](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md).
- Mã nguồn: [lab13.py](../../src/lab13.py); số báo cáo được sinh từ thực thi. Chỉ làm tròn khi hiển thị nên một số giá trị khác nhẹ đáp án dùng phút đã làm tròn.
- Phan Anh nhận số A3/B3/B4 để làm D; Ân nhận A–B cho phần chỉ số/rủi ro và hồ sơ launch. Phần C/D/E và duyệt chéo chưa được xác nhận hoàn tất ở báo cáo này.
