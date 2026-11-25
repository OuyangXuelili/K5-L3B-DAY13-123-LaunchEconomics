# Team

## Thông tin nhóm

- Tên nhóm: 123 (theo tên repo hiện tại)
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY13-123-LaunchEconomics`
- URL repo: https://github.com/OuyangXuelili/K5-L3B-DAY13-123-LaunchEconomics
- Nhánh làm việc: `main`; commit chốt bổ sung khi nhóm hoàn tất và push.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Trần Văn Quang | 2A202604032 | Không công khai email cá nhân | OuyangXuelili | Người viết code A–B, tổng hợp chi phí và tích hợp |
| 2 | Phan Nguyễn Phan Anh | 2A202604004 | Không công khai email cá nhân | alpha19102004 | Người kiểm số; nhận vai viết code sau giải lao; phụ trách D |
| 3 | Nguyễn Hữu Mạnh | 2A202604015 | Không công khai email cá nhân | nghmanh04 | Người gắn nhãn 1; phụ trách C và tổng hợp phiếu duyệt chéo |
| 4 | Nguyễn Hoàng Ân | 2A202604025 | Không công khai email cá nhân | hoangan06 | Người gắn nhãn 2 kiêm giữ hồ sơ; phụ trách E |

Bốn vai của lab:

- **Người viết code:** viết và chạy `src/lab13.py`.
- **Người kiểm số:** tính tay một con số để đối chiếu, điền bảng.
- **Người gắn nhãn 1:** đọc đề, theo dõi điều kiện "Xong khi"; gắn nhãn 20 ca độc lập ở CP3.
- **Người gắn nhãn 2, kiêm giữ hồ sơ:** điền `report/team/ho_so_launch_v0.md` từ đầu buổi; gắn nhãn 20 ca độc lập ở CP3.

Đổi người viết code sau giờ giải lao, để ít nhất hai người trong nhóm tự tay tính được chi phí.

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

## Trần Văn Quang — 2A202604032

### Phần việc phụ trách

- A1–A4: công thức chạy lại, mô hình chi phí, tách loại yêu cầu và chi phí cố định.
- B1–B4: độ nhạy, chi phí cả hệ thống và xem lại 100%.
- Danh sách nhóm và tài liệu bàn giao số liệu.

### Đóng góp cụ thể

- Triển khai `src/lab13.py` để tính và in các bảng A–B từ CSV.
- Sinh `report/team/bang_chi_phi.md` bằng `python lab13.py --write-report`.
- Chuẩn bị báo cáo cá nhân `report/team/2A202604032_TranVanQuang.md`.

### Bằng chứng

- Ba phép thử A1, các bảng và phần giải thích trong báo cáo chi phí.
- Mọi kết quả dùng hai cột `_simulated` được ghi nhãn; số chỉ làm tròn khi trình bày.
- Review chéo của thành viên khác chưa được ghi nhận.

## Phan Nguyễn Phan Anh — 2A202604004

- Phần được giao: kiểm độc lập số A–B; bổ sung D1 vào `src/lab13.py` sau bàn giao; hoàn thiện `pilot_plan.yaml`; hỗ trợ phép tính E1.
- Đóng góp: bổ sung `co_mau_hai_ty_le`, `co_mau_pilot`, `chi_so_e1` và phần in D1/E1 trong `src/lab13.py`; hoàn thiện `report/team/pilot_plan.yaml`.
- Kiểm số A–B: đối chiếu phép tính một trace và tổng hợp độc lập từ CSV; tổng 4.373.585 đ, CPS 4.472 đ/việc [simulated]; giới hạn 2 lượt cho chi phí hệ thống 6.901.220 đ [simulated]. Phép tính và kiểm chứng được ghi trong báo cáo cá nhân, có hỗ trợ Codex.
- D1: 1.251 mẫu độc lập/nhóm cho +5 điểm; phương án +6 điểm dùng 20 nhân viên/nhóm, 299 yêu cầu/người, DE 6,96; 5.980 yêu cầu thực tế/nhóm tương đương 859,20 mẫu độc lập.
- Bàn giao E1 qua output chương trình: 994/1.200 = 82,83%; 48/177 = 27,12%; 51/1.200 = 4,25% (dữ liệu giả lập); chưa kết luận tác động do không có đối chứng.
- Bằng chứng và khai báo AI: `report/team/2A202604004_PhanNguyenPhanAnh.md`. Lịch pilot và điều kiện duyệt trong YAML là đề xuất, chưa phải hoạt động hay kết quả đã thực hiện.

## Nguyễn Hữu Mạnh — 2A202604015

- Phần được giao: gắn nhãn độc lập 20 ca, tổng hợp `bang_loi.md` và `phieu_cham.md` khi có hồ sơ nhóm khác.
- Đóng góp trong workspace: Nguyễn Hữu Mạnh rà soát và chốt 20 nhãn, với Codex hỗ trợ phân loại ban đầu; nhãn được ghi trong `report/team/bang_loi.md`. Bảng khắc phục 5 loại lỗi được điền theo hướng dẫn. Báo cáo cá nhân tại `report/team/2A202604015_NguyenHuuManh.md` khai báo phần hỗ trợ AI.
- Đã xác minh hai cột trùng 20/20 ca sau rà soát. Tiêu chí đồng thuận độc lập chưa được xác minh. Phiếu duyệt chéo đang chờ giảng viên ghép nhóm.

## Nguyễn Hoàng Ân — 2A202604025

- Phần được giao: gắn nhãn độc lập với Mạnh; hoàn thiện `chi_so.md`, `ho_so_launch_v0.md` và `group_report.md`.
- Đã rà soát và xác nhận 20 nhãn. Cột thứ hai và kết quả đối chiếu nằm trong [bảng lỗi](report/team/bang_loi.md).
- Nhiệm vụ E gồm [chỉ số, event và rủi ro](report/team/chi_so.md), [hồ sơ launch](report/team/ho_so_launch_v0.md) và [báo cáo nhóm](report/team/group_report.md). Báo cáo cá nhân ghi cách dùng Codex. Hồ sơ Gate 2a đề xuất Go có điều kiện cho pilot nội địa và hàng nặng.

## Bàn giao và phối hợp

- Quang giữ phần A–B; Phan Anh nhận sửa `lab13.py` sau giải lao, tránh hai người sửa đồng thời.
- Mạnh và Ân giữ nguyên hai bộ nhãn độc lập trước khi so sánh; sau đó mới thống nhất nhãn chung.
- Ân nhận số A3/B3/B4 để viết rủi ro và hồ sơ; Phan Anh nhận phạm vi A3 và điều kiện chi phí B4 để thiết kế pilot.
- Mỗi người tự điền báo cáo cá nhân theo mẫu và khai báo công cụ đã dùng; không ghi thay hoạt động kiểm tra hoặc duyệt chéo của người khác.
