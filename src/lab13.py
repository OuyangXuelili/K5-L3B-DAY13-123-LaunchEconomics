"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong src/: python lab13.py; thêm --write-report để cập nhật bảng chi phí.
Phần A–B tính từ hai CSV giả lập. Phan Anh bổ sung D1 và phép tính E1.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import argparse
import math
from pathlib import Path
from statistics import NormalDist

import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)
CO_DINH_THANG = 40_000_000
YEU_CAU_THANG = 45_000
PHAM_VI = ('noi_dia', 'hang_nang')
LOAI_YEU_CAU = (*PHAM_VI, 'quoc_te', 'doi_tac')


def _kiem_tra_p_k(p, k):
    if isinstance(p, bool) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('p phải nằm trong [0, 1] và hữu hạn')
    if k is not None and (isinstance(k, bool) or not isinstance(k, int) or k < 1):
        raise ValueError('k phải là số nguyên dương hoặc None')


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    _kiem_tra_p_k(p, k)
    if p == 0:
        return math.inf if k is None else float(k)
    return 1 / p if k is None else ti_le_thanh_cong(p, k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    _kiem_tra_p_k(p, k)
    if p == 0:
        return 0.0
    if k is None or p == 1:
        return 1.0
    return -math.expm1(k * math.log1p(-p))


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    thanh_cong = ti_le_thanh_cong(p, k)
    return so_lan_chay_ky_vong(p, k) / thanh_cong if thanh_cong else math.inf


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    if max_lan_chay is not None:
        _kiem_tra_p_k(1, max_lan_chay)
    for value in (gia_vao, gia_ra, gia_tool, luong_phut, he_so_xem_lai, he_so_lam_lai):
        if isinstance(value, bool) or not math.isfinite(value) or value < 0:
            raise ValueError('Giá và hệ số phải không âm, hữu hạn')
    reqs = reqs.copy(deep=True)
    runs = runs.loc[runs.request_id.isin(reqs.request_id)].copy()
    if max_lan_chay is not None:
        runs = runs.loc[runs.attempt <= max_lan_chay]
        vuot = reqs.so_lan_chay > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    token_tung_luot = runs.tokens_in * gia_vao / 1000 + runs.tokens_out * gia_ra / 1000
    tool_tung_luot = runs.tool_calls * gia_tool
    token, tool = float(token_tung_luot.sum()), float(tool_tung_luot.sum())
    xem_lai = float(reqs.phut_xem_lai_simulated.sum() * luong_phut * he_so_xem_lai)
    lam_lai = float(reqs.phut_lam_lai_simulated.sum() * luong_phut * he_so_lam_lai)
    tong = token + tool + xem_lai + lam_lai
    thanh_cong = int(reqs.ket_qua.eq('thanh_cong').sum())
    so_yc = len(reqs)
    khong_thanh_cong = so_yc - thanh_cong
    # Quy ước B3 của đề: cộng 12.000đ cho MỌI yêu cầu không thành công.
    he_thong = tong + khong_thanh_cong * BASELINE
    return dict(token=token, tool=tool,
                chay_lai=float((token_tung_luot + tool_tung_luot)[runs.attempt > 1].sum()),
                xem_lai=xem_lai, lam_lai=lam_lai, tong=tong, thanh_cong=thanh_cong,
                cps=tong / thanh_cong if thanh_cong else math.inf,
                hoa_don_moi_yc=(token + tool) / so_yc if so_yc else 0.0,
                so_yc=so_yc, so_luot=len(runs), khong_thanh_cong=khong_thanh_cong,
                he_thong=he_thong, he_thong_moi_yc=he_thong / so_yc if so_yc else 0.0)


def bang_theo_loai(runs, reqs):
    return {loai: mo_hinh(runs, reqs.loc[reqs.loai == loai]) for loai in LOAI_YEU_CAU}


def bang_do_nhay(runs, reqs):
    scenarios = [
        ('Giá token gấp đôi', '52 đ vào; 260 đ ra / 1.000 token', dict(gia_vao=52, gia_ra=260)),
        ('Giá token giảm một nửa', '13 đ vào; 65 đ ra / 1.000 token', dict(gia_vao=13, gia_ra=65)),
        ('Tỉ lệ xem lại gấp đôi', 'Tiền xem lại × 2', dict(he_so_xem_lai=2)),
        ('Tỉ lệ xem lại giảm một nửa', 'Tiền xem lại × 0,5', dict(he_so_xem_lai=0.5)),
        ('Số ca làm lại gấp đôi', 'Tiền làm lại × 2', dict(he_so_lam_lai=2)),
        ('Số ca làm lại giảm một nửa', 'Tiền làm lại × 0,5', dict(he_so_lam_lai=0.5)),
        ('Lương nhân viên tăng 25%', '2.500 đ/phút', dict(luong_phut=2500)),
        ('Chỉ cho chạy tối đa 2 lần', 'Bỏ attempt > 2; ca vượt giới hạn chuyển nhân viên', dict(max_lan_chay=2)),
        ('Chỉ cho chạy 1 lần', 'Bỏ attempt > 1; ca vượt giới hạn chuyển nhân viên', dict(max_lan_chay=1)),
    ]
    goc = mo_hinh(runs, reqs)['cps']
    rows = []
    for ten, cach, kwargs in scenarios:
        model = mo_hinh(runs, reqs, **kwargs)
        rows.append(dict(ten=ten, cach_tinh=cach, ket_qua=model,
                         thay_doi=100 * (model['cps'] / goc - 1)))
    return rows


def bang_co_dinh(runs, reqs):
    scope = reqs.loc[reqs.loai.isin(PHAM_VI)]
    model = mo_hinh(runs, scope)
    rows = []
    for volume in (YEU_CAU_THANG, YEU_CAU_THANG / 2):
        # volume là TỔNG yêu cầu công ty; chỉ phần trong scope được chạy trợ lý.
        successes = volume * model['thanh_cong'] / len(reqs)
        scope_volume = volume * len(scope) / len(reqs)
        fixed = CO_DINH_THANG / successes
        rows.append(dict(khoi_luong=volume, thanh_cong_thang=successes,
                         co_dinh_moi_viec=fixed, cps_cong_co_dinh=model['cps'] + fixed,
                         he_thong_moi_yc=model['he_thong_moi_yc'] + CO_DINH_THANG / scope_volume))
    return rows


def xem_lai_100(runs, reqs, phut_lam_lai=9, phut_xem_lai=5):
    """B4: xem mỗi yêu cầu có ít nhất một lượt ok đúng một lần, không đếm theo run."""
    scope = reqs.loc[reqs.loai.isin(PHAM_VI)]
    model = mo_hinh(runs, scope)
    ok = runs.loc[runs.request_id.isin(scope.request_id) & runs.status.eq('ok'), 'request_id'].nunique()
    sai = int(scope.ket_qua.eq('lam_lai').sum())
    ha_tang = model['token'] + model['tool']
    xem_lai = ok * phut_xem_lai * LUONG_PHUT
    lam_lai = sai * phut_lam_lai * LUONG_PHUT
    tong = ha_tang + xem_lai + lam_lai
    return dict(so_yc=len(scope), thanh_cong=model['thanh_cong'], so_yc_ok=ok,
                so_ca_lam_lai=sai, ha_tang=ha_tang, xem_lai=xem_lai, lam_lai=lam_lai,
                tong=tong, cps=tong / model['thanh_cong'], phut_lam_lai=phut_lam_lai,
                he_thong_moi_yc=(tong + model['khong_thanh_cong'] * BASELINE) / len(scope),
                phut_xem_lai_hoa_von=(BASELINE * model['thanh_cong'] - ha_tang - lam_lai) / (ok * LUONG_PHUT))


def _so(value, decimals=0):
    return f'{value:,.{decimals}f}'.translate(str.maketrans({',': '.', '.': ','}))


def _bang(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                      '| ' + ' | '.join(['---'] * len(headers)) + ' |',
                      *['| ' + ' | '.join(map(str, row)) + ' |' for row in rows]])


def tao_bao_cao(runs, reqs):
    """Sinh A–B từ cùng hàm tính; không chép số đáp án vào báo cáo."""
    goc = mo_hinh(runs, reqs)
    loai = bang_theo_loai(runs, reqs)
    nhay = bang_do_nhay(runs, reqs)
    co_dinh = bang_co_dinh(runs, reqs)
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)
    gioi_han = {k: mo_hinh(runs, reqs, max_lan_chay=k) for k in (1, 2, 3)}
    re_he_thong = min(gioi_han, key=lambda k: gioi_han[k]['he_thong'])
    re_cps = min(gioi_han, key=lambda k: gioi_han[k]['cps'])
    tang = sorted((nhay[i] for i in (0, 2, 4, 6)), key=lambda r: r['thay_doi'], reverse=True)[:3]
    muc_lam_lai = reqs.loc[reqs.ket_qua.eq('lam_lai'), 'phut_lam_lai_simulated']
    trung_binh = float(muc_lam_lai.mean())
    b4 = xem_lai_100(runs, reqs)
    # Dùng trung bình chưa làm tròn; chỉ làm tròn khi trình bày.
    b4_nhay = xem_lai_100(runs, reqs, phut_lam_lai=trung_binh)
    ok_tung_lan = runs.merge(reqs[['request_id', 'loai']], on='request_id', validate='many_to_one')
    ok_tung_lan = ok_tung_lan.assign(ok=ok_tung_lan.status.eq('ok'))
    ty_le_ok = ok_tung_lan.groupby(['loai', 'attempt']).ok.mean()
    ca_chuyen = int(reqs.ket_qua.eq('chuyen_nhan_vien').sum())
    a2_rows = [
        ['Token', _so(goc['token']), '`logix_runs.csv`', 'đo từ trace giả lập'],
        ['Tool', _so(goc['tool']), '`logix_runs.csv`', 'đo từ trace giả lập'],
        ['Trong đó, lần chạy thứ 2 và 3', _so(goc['chay_lai']), '`attempt > 1`', 'đã nằm trong token + tool'],
        ['Xem lại', _so(goc['xem_lai']), '`phut_xem_lai_simulated`', 'simulated'],
        ['Làm lại', _so(goc['lam_lai']), '`phut_lam_lai_simulated`', 'simulated'],
        ['Tổng chi phí', _so(goc['tong']), 'token + tool + xem lại + làm lại', 'simulated'],
        ['Số việc thành công', _so(goc['thanh_cong']), '`ket_qua == thanh_cong`', 'từ dữ liệu giả lập'],
        ['Chi phí mỗi việc thành công', _so(goc['cps']), 'tổng / số việc thành công', 'simulated'],
        ['Hoá đơn token và tool / số yêu cầu', _so(goc['hoa_don_moi_yc'], 1), '(token + tool) / số yêu cầu', 'đo từ trace giả lập'],
    ]
    a3_rows = [[name, _so(m['so_yc']), _so(100*m['thanh_cong']/m['so_yc'], 1)+'%',
                _so(m['so_luot']/m['so_yc'], 2), _so(m['cps']), _so(m['cps']/BASELINE, 2)+'×']
               for name, m in loai.items()]
    theo_lan_rows = [[name, *[_so(100*ty_le_ok.get((name, k), 0), 1)+'%' for k in (1, 2, 3)]]
                     for name in LOAI_YEU_CAU]
    a4_rows = [[_so(r['khoi_luong']), _so(r['thanh_cong_thang']), _so(r['co_dinh_moi_viec']),
               _so(r['cps_cong_co_dinh']), _so(r['cps_cong_co_dinh']/BASELINE, 2)+'×'] for r in co_dinh]
    b1_rows = [[r['ten'], r['cach_tinh'], _so(r['ket_qua']['cps']), _so(r['thay_doi'], 1)+'%'] for r in nhay]
    b3_rows = [[str(k), _so(m['tong']), _so(m['khong_thanh_cong']), _so(m['he_thong']),
                _so(m['cps'])] for k, m in gioi_han.items()]
    b4_rows = [[label, _so(m['phut_lam_lai'], 2), _so(m['xem_lai']), _so(m['lam_lai']),
               _so(m['tong']), _so(m['cps']), _so(m['cps']/BASELINE, 2)+'×',
               _so(m['he_thong_moi_yc'])] for label, m in [('Giả định đề: 9 phút', b4), ('Trung bình dữ liệu', b4_nhay)]]
    sections = [
        '# Bảng chi phí · Nhiệm vụ A và B',
        ('Người phụ trách: Trần Văn Quang — 2A202604032. Toàn bộ dữ liệu của lab là giả lập. '
         'Các tổng, tỉ lệ hoặc so sánh dùng phút `_simulated` đều mang nhãn **simulated**. '
         'Số tiền tính bằng đồng; chỉ làm tròn khi hiển thị.'),
        ('Sinh lại bằng `cd src` rồi `python lab13.py --write-report`. '
         'Hai CSV và `lab13_starter.py` được giữ nguyên; không cần API key.'),
        '## A1 · Ba phép thử đáp án biết trước',
        _bang(['Phép thử (p = 0,8)', 'Kết quả'], [
            ['Số lần chạy trung bình, tối đa 2 lần', _so(so_lan_chay_ky_vong(0.8, 2), 2)],
            ['Số lần chạy trung bình, chạy đến khi đúng', _so(so_lan_chay_ky_vong(0.8), 2)],
            ['Hệ số chi phí mỗi việc thành công, tối đa 3 lần', _so(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3), 2)]]),
        ('Ba phép thử ĐẠT. Công thức A1 giả định các lần thử độc lập với xác suất đúng không đổi; '
         'A2–B4 tính trực tiếp từ trace, không áp giả định độc lập lên dữ liệu.'),
        '## A2 · Mô hình chi phí từ trace',
        f"Mẫu có {_so(len(reqs))} yêu cầu và {_so(len(runs))} lần chạy. Tử số tính mọi lần chạy, kể cả lỗi; mẫu số chỉ đếm việc thành công.",
        _bang(['Khoản', 'Giá trị', 'Nguồn / cách tính', 'Nhãn'], a2_rows),
        (f"- CPS gấp {_so(goc['cps']/goc['hoa_don_moi_yc'], 1)} lần hoá đơn / yêu cầu [simulated].\n"
         f"- Làm lại lớn nhất: {_so(100*goc['lam_lai']/goc['tong'], 1)}%; tổng giờ xem lại và làm lại chiếm "
         f"{_so(100*(goc['xem_lai']+goc['lam_lai'])/goc['tong'], 1)}% chi phí [simulated]."),
        (f"So sánh cùng đơn vị theo quy ước B3: ({_so(goc['tong'])} + {_so(goc['khong_thanh_cong'])} × {_so(BASELINE)}) / "
         f"{_so(len(reqs))} = **{_so(goc['he_thong_moi_yc'])} đ/yêu cầu**, {_so(goc['he_thong_moi_yc']/BASELINE, 2)}× "
         f"nhân viên tự làm [simulated], chưa cộng cố định. {_so(ca_chuyen)} ca chuyển nhân viên có 0 phút trong cột simulated; "
         'không dùng riêng CPS / 12.000 để kết luận tiết kiệm cả hệ thống.'),
        '## A3 · Tách theo loại yêu cầu',
        _bang(['Loại', 'Số yêu cầu', 'Thành công', 'Lần chạy / yêu cầu', 'CPS [simulated]', 'CPS / 12.000 [simulated]'], a3_rows),
        'Tỉ lệ `status == ok` trong từng lần thử (mẫu của lần thử sau đã được chọn bởi các lần trước):',
        _bang(['Loại', 'Lần 1', 'Lần 2', 'Lần 3'], theo_lan_rows),
        (f"`quoc_te` có CPS {_so(loai['quoc_te']['cps'])} đ = {_so(loai['quoc_te']['cps']/BASELINE, 2)}× [simulated], "
         f"thành công {_so(100*loai['quoc_te']['thanh_cong']/loai['quoc_te']['so_yc'], 1)}%; tỉ lệ ok lần 3 chỉ "
         f"{_so(100*ty_le_ok[('quoc_te', 3)], 1)}%, nên loại khỏi phạm vi đề xuất."),
        (f"`doi_tac` có CPS {_so(loai['doi_tac']['cps']/BASELINE, 2)}× [simulated] và thành công "
         f"{_so(100*loai['doi_tac']['thanh_cong']/loai['doi_tac']['so_yc'], 1)}%; có điều khoản riêng, tạm loại. "
         'Phạm vi đề xuất là `noi_dia` + `hang_nang`; cần kiểm chi phí cả hệ thống và kiểm soát xem lại trước khi chốt pilot.'),
        '## A4 · Chi phí cố định: noi_dia + hang_nang [simulated]',
        (f"Giữ cơ cấu mẫu và tính {_so(CO_DINH_THANG)} đ cố định/tháng. Khối lượng là tổng yêu cầu công ty; "
         f"việc thành công trong phạm vi/tháng = khối lượng × {_so(b4['thanh_cong'])} / {_so(len(reqs))}."),
        _bang(['Tổng yêu cầu / tháng', 'Thành công trong phạm vi / tháng', 'Cố định / việc', 'CPS + cố định', '/ 12.000'], a4_rows),
        (f"CPS cộng cố định vẫn dưới 12.000 đ ở cả hai mức {_so(co_dinh[0]['khoi_luong'])} và {_so(co_dinh[1]['khoi_luong'])} "
         'yêu cầu/tháng [simulated]. Đây là kiểm tra độ nhạy, chưa đủ để kết luận tiết kiệm cả hệ thống.'),
        (f"Tính cả việc nhân viên làm thay trong phạm vi và cố định: {_so(co_dinh[0]['he_thong_moi_yc'])} và "
         f"{_so(co_dinh[1]['he_thong_moi_yc'])} đ/yêu cầu trong phạm vi, lần lượt "
         f"{_so(co_dinh[0]['he_thong_moi_yc']/BASELINE, 2)}× và {_so(co_dinh[1]['he_thong_moi_yc']/BASELINE, 2)}× [simulated]."),
        '## B1 · Đổi từng yếu tố [simulated]',
        (f"Gốc: {_so(goc['cps'])} đ/việc thành công. Mỗi dòng chỉ thay yếu tố được nêu; "
         'ca vượt giới hạn chạy được chuyển nhân viên và có phút xem lại/làm lại bằng 0.'),
        _bang(['Kịch bản', 'Cách tính', 'CPS [simulated]', 'Thay đổi [simulated]'], b1_rows),
        '## B2 · Đổi một cặp và xếp hạng [simulated]',
        (f"Giá token và xem lại cùng gấp đôi: {_so(cap['cps'])} đ, tăng {_so(100*(cap['cps']/goc['cps']-1), 1)}%. "
         'Hai tác động cộng được vì mô hình tuyến tính theo các khoản chi phí.'),
        'Xếp hạng tác động tăng: ' + '; '.join(f"{i}. {r['ten']} (+{_so(r['thay_doi'], 1)}%)" for i, r in enumerate(tang, 1)) + '.',
        '## B3 · Giới hạn chạy lại và chi phí cả hệ thống [simulated]',
        'Chi phí cả hệ thống = tổng trợ lý + 12.000 đ × số yêu cầu không thành công, theo quy ước của nhiệm vụ B3.',
        _bang(['Giới hạn', 'Tổng trợ lý', 'Không thành công', 'Cả hệ thống', 'CPS'], b3_rows),
        (f"Giới hạn {re_he_thong} lần rẻ nhất cho công ty: {_so(gioi_han[re_he_thong]['he_thong'])} đ. "
         f"CPS thấp nhất ở {re_cps} lần: {_so(gioi_han[re_cps]['cps'])} đ; nhưng chuyển thêm "
         f"{_so(gioi_han[re_cps]['khong_thanh_cong']-gioi_han[re_he_thong]['khong_thanh_cong'])} việc sang nhân viên [simulated]."),
        '## B4 · Xem lại 100% trong phạm vi noi_dia + hang_nang [simulated]',
        (f"Có {_so(b4['so_yc'])} yêu cầu; {_so(b4['so_yc_ok'])} yêu cầu có ít nhất một lượt ok, xem lại 5 phút/yêu cầu; "
         f"{_so(b4['so_ca_lam_lai'])} ca làm lại; {_so(b4['thanh_cong'])} việc thành công; "
         f"token + tool {_so(b4['ha_tang'])} đ. Không cộng lại phút xem/làm lại cũ của A2."),
        _bang(['Kịch bản', 'Phút / ca làm lại', 'Xem lại', 'Làm lại', 'Tổng', 'CPS', 'CPS / 12.000', 'Hệ thống / yêu cầu'], b4_rows),
        (f"Giả định đề cho CPS {_so(b4['cps'])} đ = {_so(b4['cps']/BASELINE, 2)}×; dùng trung bình dữ liệu "
         f"{_so(trung_binh, 4)} phút/ca (trung vị {_so(float(muc_lam_lai.median()), 1)}) cho CPS "
         f"{_so(b4_nhay['cps'])} đ = {_so(b4_nhay['cps']/BASELINE, 2)}× [simulated], đều chưa cộng cố định."),
        (f"Pilot cần kiểm tra có thể giảm xem lại an toàn hay không: thời gian xem lại hoà vốn tối đa "
         f"{_so(b4['phut_xem_lai_hoa_von'], 2)} phút khi làm lại 9 phút, hoặc "
         f"{_so(b4_nhay['phut_xem_lai_hoa_von'], 2)} phút khi làm lại {_so(trung_binh, 2)} phút [simulated]."),
        '## Nguồn và bàn giao',
        ('- Dữ liệu: `src/logix_runs.csv`, `src/logix_requests.csv` do đề cung cấp.\n'
         '- Công thức và giả định: [tài liệu dữ liệu](../../docs/du_lieu_va_cong_thuc.md), '
         '[hướng dẫn A–B](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md).\n'
         '- Mã nguồn: [lab13.py](../../src/lab13.py); số báo cáo được sinh từ thực thi. '
         'Chỉ làm tròn khi hiển thị nên một số giá trị khác nhẹ đáp án dùng phút đã làm tròn.\n'
         '- Phan Anh nhận số A3/B3/B4 để làm D; Ân nhận A–B cho phần chỉ số/rủi ro và hồ sơ launch. '
         'Phần C/D/E và duyệt chéo chưa được xác nhận hoàn tất ở báo cáo này.'),
    ]
    return '\n\n'.join(sections) + '\n'


# ---------- Phan Nguyễn Phan Anh · Nhiệm vụ D1 và phép tính E1 ----------
def co_mau_hai_ty_le(p1, p2, alpha=0.05, power=0.8):
    """Cỡ mẫu độc lập MỖI nhóm theo công thức z hai tỉ lệ của đề, làm tròn lên."""
    if not (0 < p1 < 1 and 0 < p2 < 1 and p1 != p2
            and 0 < alpha < 1 and 0 < power < 1):
        raise ValueError('Hai tỉ lệ phải khác nhau và mọi tham số phải nằm trong (0, 1)')
    normal = NormalDist()
    za = normal.inv_cdf(1 - alpha / 2)
    zb = normal.inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
                     / (p2 - p1) ** 2)


def co_mau_pilot():
    """D1 a–e: số liệu thiết kế của lab; không suy diễn tác động từ mẫu không đối chứng."""
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize

    icc, so_cum = 0.02, 20
    n5 = co_mau_hai_ty_le(0.70, 0.75)
    n6 = co_mau_hai_ty_le(0.70, 0.76)
    de75 = 1 + (75 - 1) * icc
    n_theo_nv = math.ceil(n5 * de75)
    # Giải c*m / (1 + (m-1)*ICC) >= n6; c > n6*ICC ở phương án này.
    m6 = math.ceil(n6 * (1 - icc) / (so_cum - n6 * icc))
    de6 = 1 + (m6 - 1) * icc
    n_thuc = so_cum * m6
    n_hieu_dung = n_thuc / de6
    power5 = NormalIndPower().power(
        effect_size=abs(proportion_effectsize(0.70, 0.75)),
        nobs1=n_hieu_dung, alpha=0.05, ratio=1, alternative='two-sided')
    return dict(n_5_diem=n5, de_75=de75, n_theo_nhan_vien=n_theo_nv,
                nhan_vien_moi_nhom=math.ceil(n_theo_nv / 75),
                gioi_han_20_nv=so_cum / icc, gioi_han_6_depot=6 / icc,
                n_6_diem=n6, yeu_cau_moi_nv=m6, de_6_diem=de6,
                n_thuc_moi_nhom=n_thuc, n_hieu_dung=n_hieu_dung,
                power_neu_chi_5_diem=float(power5))


def chi_so_e1(reqs):
    """Trả về tử số, mẫu số, tỉ lệ E1; giữ nguyên đầu vào và không suy ra quan hệ nhân quả."""
    if reqs.empty:
        raise ValueError('Cần ít nhất một yêu cầu để tính E1')
    xem = reqs.loc[reqs.duoc_xem_lai.eq(1)]
    counts = {
        'dong_trong_24h_khong_mo_lai_7_ngay': (
            int((reqs.dong_trong_24h.eq(1) & reqs.mo_lai_trong_7_ngay.eq(0)).sum()), len(reqs)),
        'bo_qua_goi_y': (int(xem.quyet_dinh_xem_lai.isin(['sua', 'bo']).sum()), len(xem)),
        'mo_lai_trong_7_ngay': (int(reqs.mo_lai_trong_7_ngay.eq(1).sum()), len(reqs)),
    }
    return {name: dict(tu_so=num, mau_so=den, ti_le=num / den if den else None)
            for name, (num, den) in counts.items()}


def tao_bao_cao_d1_e1(reqs):
    """In phần bàn giao của Phan Anh; không ghi vào báo cáo A–B hay hồ sơ của thành viên khác."""
    d1 = co_mau_pilot()
    e1 = chi_so_e1(reqs)
    scope = chi_so_e1(reqs.loc[reqs.loai.isin(PHAM_VI)])
    d1_rows = [
        ['a · Chia theo yêu cầu, +5 điểm', f"{_so(d1['n_5_diem'])} yêu cầu / nhóm"],
        ['b · Theo nhân viên, m = 75',
         f"DE {_so(d1['de_75'], 2)}; {_so(d1['n_theo_nhan_vien'])} yêu cầu; "
         f"{d1['nhan_vien_moi_nhom']} người / nhóm, tổng {2*d1['nhan_vien_moi_nhom']} > 40"],
        ['c · 20 nhân viên / nhóm', f"n hiệu dụng < {_so(d1['gioi_han_20_nv'])} < {_so(d1['n_5_diem'])}; không đủ cho +5 điểm"],
        ['d · 6 depot / nhóm', f"n hiệu dụng < {_so(d1['gioi_han_6_depot'])}; không đủ cho +5 điểm"],
        ['e · 20 nhân viên / nhóm, +6 điểm',
         f"n độc lập {_so(d1['n_6_diem'])}; {d1['yeu_cau_moi_nv']} yêu cầu / người; "
         f"DE {_so(d1['de_6_diem'], 2)}; {_so(d1['n_thuc_moi_nhom'])} yêu cầu thực tế / nhóm; "
         f"n hiệu dụng {_so(d1['n_hieu_dung'], 2)}"],
    ]
    names = {
        'dong_trong_24h_khong_mo_lai_7_ngay': 'Chính: đóng 24h và không mở lại 7 ngày',
        'bo_qua_goi_y': 'Dùng: sửa hoặc bỏ / được xem lại',
        'mo_lai_trong_7_ngay': 'An toàn: mở lại 7 ngày / tổng yêu cầu',
    }
    e1_rows = [[names[name], f"{m['tu_so']} / {m['mau_so']}",
                _so(100*m['ti_le'], 2)+'%' if m['ti_le'] is not None else 'Không có mẫu xem lại']
               for name, m in e1.items()]
    safety = scope['mo_lai_trong_7_ngay']
    return '\n\n'.join([
        '# Phần Phan Anh · D1 và phép tính E1',
        '## D1 · Cỡ mẫu theo công thức của đề',
        _bang(['Câu', 'Kết quả mỗi nhóm'], d1_rows),
        (f"Nếu tác động thật chỉ +5 điểm, power xấp xỉ {_so(d1['power_neu_chi_5_diem'], 3)} "
         '(khoảng 0,64), thấp hơn mục tiêu 0,80; không được tuyên bố đủ mẫu cho +5 điểm.'),
        '## E1 · Chỉ số mô tả trong đợt chạy thử (dữ liệu giả lập)',
        _bang(['Chỉ số', 'Tử số / mẫu số', 'Kết quả'], e1_rows),
        (f"Mở lại trong phạm vi noi_dia + hang_nang: {safety['tu_so']} / {safety['mau_so']} "
         f"= {_so(100*safety['ti_le'], 2)}%. Không có đối chứng nên chưa kết luận trợ lý nâng chỉ số."),
        'Chi tiết D2, rollout, luật dừng và rollback: report/team/pilot_plan.yaml.',
    ]) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tính phần A–B từ CSV của Lab 13')
    parser.add_argument('--write-report', action='store_true', help='Cập nhật report/team/bang_chi_phi.md')
    args = parser.parse_args()
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    report = tao_bao_cao(runs, reqs)
    print(report, end='')
    if args.write_report:
        target = Path(__file__).resolve().parents[1] / 'report/team/bang_chi_phi.md'
        target.write_text(report, encoding='utf-8', newline='\n')
        print('\nĐã cập nhật report/team/bang_chi_phi.md')
    print('\n' + tao_bao_cao_d1_e1(reqs), end='')
