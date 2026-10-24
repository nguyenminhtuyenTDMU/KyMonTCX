# kymon_view.py
"""
Phần dùng chung giữa app Streamlit (app.py) và app offline Flet (main.py):
gọi engine lập trận rồi chuẩn hóa kết quả thành "view model" không phụ thuộc giao diện.
"""
import re
from datetime import datetime
from functools import lru_cache

import qimen
from kymon_logic import KyMonLapTran
from kymon_nien_nguyet_nhat import lap_nien_gia, lap_nguyet_gia, lap_nhat_gia
from timgio import CUNG_NHAP_MO, can_bi_hai

LOAI_CUC = ["Thời Gia", "Thời Gia (Chuyển Bàn)", "Nhật Gia", "Nguyệt Gia", "Niên Gia"]
QM_MODES = {"Chuẩn (Vương Phượng Lân)": 1, "Truyền thống (Dương bàn)": 0,
            "Khắc gia (+phút)": 2, "Tự chọn Cục": 4}

MAP_TEN_CUNG = {1: "Khảm 1", 2: "Khôn 2", 3: "Chấn 3", 4: "Tốn 4", 5: "Trung 5",
                6: "Càn 6", 7: "Đoài 7", 8: "Cấn 8", 9: "Ly 9"}
LUOI_CUNG = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
CUNG_CHI = {1: ["Tý"], 8: ["Sửu", "Dần"], 3: ["Mão"], 4: ["Thìn", "Tỵ"], 9: ["Ngọ"], 2: ["Mùi", "Thân"],
            7: ["Dậu"], 6: ["Tuất", "Hợi"]}

# --- TỨ HẠI: Kích Hình, Nhập Mộ, Môn Bách (Không Vong đã có badge riêng) ---
NGU_HANH_MON = {"Hưu": "Thủy", "Sinh": "Thổ", "Thương": "Mộc", "Đỗ": "Mộc",
                "Cảnh": "Hỏa", "Tử": "Thổ", "Kinh": "Kim", "Khai": "Kim"}
HANH_KHAC = {"Kim": "Mộc", "Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim"}


def lay_hanh(ten):
    """Ngũ hành (kim/moc/thuy/hoa/tho) của sao, cửa, can, chi hoặc quẻ — dùng để tô màu."""
    if not ten: return ""
    ten = ten.split("/")[0].strip()
    if ten in ["Tâm", "Trụ", "Khai", "Kinh", "Canh", "Tân", "Thân", "Dậu", "Càn", "Đoài"]: return "kim"
    if ten in ["Xung", "Phụ", "Thương", "Đỗ", "Giáp", "Ất", "Dần", "Mão", "Chấn", "Tốn"]: return "moc"
    if ten in ["Bồng", "Hưu", "Nhâm", "Quý", "Hợi", "Tý", "Khảm"]: return "thuy"
    if ten in ["Anh", "Cảnh", "Bính", "Đinh", "Tỵ", "Ngọ", "Ly"]: return "hoa"
    return "tho"


def hanh_cung(cung_id):
    return {1: "thuy", 9: "hoa", 3: "moc", 4: "moc", 6: "kim", 7: "kim"}.get(cung_id, "tho")


def xu_ly_don_giap(cc):
    p = cc.split()
    if p[0] == "Giáp": return {"Tý": "Mậu", "Tuất": "Kỷ", "Thân": "Canh", "Ngọ": "Tân", "Thìn": "Nhâm",
                               "Dần": "Quý"}.get(p[1], p[0])
    return p[0]


def tag_tu_tru(can, tu_tru):
    """Danh sách nhãn Y/M/D/H cho các can trùng can Năm/Tháng/Ngày/Giờ."""
    if not can: return []
    tags = []
    for c in re.split(r'[/,]', can):
        c = c.strip()
        if not c: continue
        for k in ("Y", "M", "D", "H"):
            if c == tu_tru[k]: tags.append(k)
    return tags


def tu_hai(cung_id, thien, dia, gate):
    """[(loại, chi tiết)] cho Kích Hình / Nhập Mộ (thiên bàn, địa bàn, ký can) và Môn Bách (Cửa khắc Cung).
    Chi tiết ghi tầng, vd "Ất (thiên), Kỷ (địa, ký)"."""
    def ghi(ds):
        return ", ".join(f"{can} ({tang}, ký)" if ky else f"{can} ({tang})" for can, tang, ky in ds)
    hinh, mo = can_bi_hai(cung_id, thien, dia)
    res = []
    if hinh: res.append(("hinh", ghi(hinh)))
    if mo: res.append(("mo", ghi(mo)))
    hanh_mon = NGU_HANH_MON.get(gate)
    if hanh_mon and HANH_KHAC[hanh_mon] == qimen.NGU_HANH_CUNG.get(cung_id):
        res.append(("bach", gate))
    return res


@lru_cache(maxsize=1)
def lay_km():
    return KyMonLapTran()


def tinh_truong_sinh_qimen(can, cung_id):
    """12 vòng Trường Sinh của can tại cung. Can nằm trong CUNG_NHAP_MO thì là Mộ (khớp badge Mộ)."""
    km = lay_km()
    if cung_id == 5 or can not in km.BANG_TRUONG_SINH: return ""
    if can in CUNG_NHAP_MO.get(cung_id, []): return "Mộ"
    list_chi = km.CUNG_TO_CHI.get(cung_id, [])
    if not list_chi: return ""
    # Ưu tiên Chi cùng Âm/Dương với Can (giống kymon_logic)
    pol_can = km.STEM_POLARITY[can]
    chi = next((c for c in list_chi if km.BRANCH_POLARITY.get(c) == pol_can), list_chi[0])
    return km.TEN_12_GIAI_DOAN[km.BANG_TRUONG_SINH[can][chi]]


def qimen_pan_to_dict(p):
    """Chuyển kết quả paipan() (đã dịch tiếng Việt) sang dict để export JSON, cùng kiểu với KyMonLapTran.lap_que()."""
    yy_label = "Dương Độn" if p.yy == "阳" else "Âm Độn"
    zhifu_vn = qimen.XING_VN.get(p.zhifu, "Cầm")
    zhishi_vn = qimen.MEN_VN.get(p.zhishi, "-")
    xunkong1, xunkong2 = p.xunkong

    data9cung = {}
    for g in range(1, 10):
        if g == 5:
            data9cung[g] = {}
            continue
        marks = []
        if p.kong[g] == "O": marks.append("Không")
        for zi, gong in enumerate(qimen.zhi2gong):
            if p.maw[zi] == "马" and gong == g: marks.append("Mã")
        data9cung[g] = {
            "Than": qimen.SHEN_VN.get(p.shenpan[g].strip(), "-"),
            "Sao": qimen.XING_VN.get(p.xinpan[g].strip(), "-"),
            "Cua": qimen.MEN_VN.get(p.menpan[g].strip(), "-"),
            "Thien": qimen.gan_vn(p.tiangan[g]),
            "Am": qimen.gan_vn(p.angan[g]),
            "Dia": qimen.gan_vn(p.digan[g]),
            "VuongSuyCung": p.cung_vuong_suy.get(g, ""),
            "Marks": marks,
        }

    tY, tM, tD, tH, tMin = p.ngaygio
    return {
        "GioLapTran": f"{tD:02d}/{tM:02d}/{tY} {tH:02d}:{tMin:02d}",
        "TuTru": {
            "Nam": qimen.cyclical_vn(p.cY),
            "Thang": qimen.cyclical_vn(p.cM),
            "Ngay": qimen.cyclical_vn(p.cD),
            "Gio": qimen.cyclical_vn(p.gio_tru),
        },
        "TietKhi": qimen.solarTerm_vn[p.tmp2],
        "ThongTinCuc": f"{yy_label} {p.qmju} Cục",
        "TuanThu": qimen.cyclical_vn(p.xun_num),
        "TrucPhuSu": f"Trực Phù: {zhifu_vn} | Trực Sử: {zhishi_vn}",
        "KhongVong": f"{qimen.Zhi_vn[xunkong1]}-{qimen.Zhi_vn[xunkong2]}",
        "DichMa": qimen.Zhi_vn[p.maxing],
        "NguyetLenh": f"{p.chi_nguyet} ({p.hanh_nguyet})",
        "Data9Cung": data9cung,
    }


# ------------------------------------------------------------------ VIEW MODEL
# Badge: (nhãn, loại) với loại ∈ tk_n, tk_g, ma, hinh, mo, bach

def _tu_hai_badges(cung_id, thien, dia, gate):
    nhan = {"hinh": "Hình", "mo": "Mộ", "bach": "Bách"}
    return [(nhan[k], k) for k, _ in tu_hai(cung_id, thien, dia, gate)]


def _cell_thuong(data, cid, tu_tru, tk_nhat, tk_thoi, dich_ma):
    """Ô cung cho engine kymon_logic / nien-nguyet-nhat (cùng logic render_cung_html_string)."""
    data = data or {}
    pt = data.get('PhanTich', {})
    thien = data.get('Thien') or ""
    vs_parts = [x for x in [pt.get('SaoVuongSuyCung', ""), pt.get('SaoVuongSuyThang', "")] if x]
    footer = []
    if cid != 5:
        for chi in CUNG_CHI.get(cid, []):
            badges = []
            if chi in tk_nhat: badges.append(("TK(N)", "tk_n"))
            if chi in tk_thoi: badges.append(("TK(G)", "tk_g"))
            if chi == dich_ma: badges.append(("MÃ", "ma"))
            footer.append({"text": chi, "hanh": lay_hanh(chi), "badges": badges})
    return {
        "id": cid, "ten": MAP_TEN_CUNG[cid], "bg": hanh_cung(cid),
        "than": data.get('Than') or "",
        "sao": data.get('Sao') or "", "sao_note": " | ".join(vs_parts),
        "cua": data.get('Cua') or "", "cua_note": "Mộ" if pt.get('MonNhapMo') else "",
        "thien": thien, "thien_note": pt.get('CanTruongSinh') or "",
        "tags": tag_tu_tru(thien, tu_tru),
        "dia": data.get('Dia') or "",
        "footer": footer, "footer_text": "", "footer_badges": [],
        "center": None,
    }


def _cell_qimen(p, cid, tu_tru):
    """Ô cung cho engine qimen.py (cùng logic render_cung_qimen_html)."""
    if cid == 5:
        yy_label = "Dương Độn" if p.yy == "阳" else "Âm Độn"
        return {"id": cid, "ten": MAP_TEN_CUNG[cid], "bg": hanh_cung(cid),
                "center": [f"CỤC {p.qmju}", f"({yy_label})", f"Nguyệt Lệnh: {p.chi_nguyet} ({p.hanh_nguyet})"]}
    gate = qimen.MEN_VN.get(p.menpan[cid].strip(), "-")
    thien = qimen.gan_vn(p.tiangan[cid])
    badges = []
    if p.kong[cid] == "O": badges.append(("Không", "tk_n"))
    for zi, gong in enumerate(qimen.zhi2gong):
        if p.maw[zi] == "马" and gong == cid: badges.append(("Mã", "ma"))
    badges += _tu_hai_badges(cid, thien, qimen.gan_vn(p.digan[cid]), gate)
    return {
        "id": cid, "ten": MAP_TEN_CUNG[cid], "bg": hanh_cung(cid),
        "than": qimen.SHEN_VN.get(p.shenpan[cid].strip(), "-"),
        "sao": qimen.XING_VN.get(p.xinpan[cid].strip(), "-"), "sao_note": p.cung_vuong_suy.get(cid, ""),
        "cua": gate, "cua_note": "",
        "thien": thien, "thien_note": tinh_truong_sinh_qimen(thien.split(",")[0], cid),
        "tags": tag_tu_tru(thien, tu_tru),
        "dia": qimen.gan_vn(p.digan[cid]),
        "footer": [], "footer_text": f"Ám: {qimen.gan_vn(p.angan[cid])}", "footer_badges": badges,
        "center": None,
    }


def _tu_tru_dict(tt):
    return {'Y': xu_ly_don_giap(tt['Nam']), 'M': xu_ly_don_giap(tt['Thang']),
            'D': xu_ly_don_giap(tt['Ngay']), 'H': xu_ly_don_giap(tt['Gio'])}


def lap_tran(loai, y, m, d, h=12, mi=0, qm_mode=1, qm_setju=0):
    """
    Lập trận theo loại cục và trả về view model:
      kq        : dict kết quả gốc (để export JSON)
      file_name : tên file gợi ý khi export
      tu_tru    : [(nhãn, giá trị, ghi chú)]
      lines     : các dòng thông tin (tiết khí, cục, tuần thủ, trực phù/sử...)
      badges    : [(nhãn, loại)] tổng quan (Không vong, Mã)
      cells     : {cung_id: ô cung}
    """
    datetime(y, m, d, h, mi)  # ValueError nếu ngày giờ không hợp lệ

    if loai == "Thời Gia":
        km = lay_km()
        kq = km.lap_que(y, m, d, h, mi)
        cc = kq['TuTru']
        tt = _tu_tru_dict(cc)
        tk_nhat = kq['InfoTuanKhong']['Nhat']
        tk_thoi = kq['InfoTuanKhong']['Thoi']
        dich_ma = km.tim_dich_ma(cc['Gio'].split()[1])
        tiet = kq['CanChi'].split('|')[-1].replace('Tiết ', '').strip()
        return {
            "kq": kq, "file_name": f"ky_mon_thoi_{y}_{m}_{d}_{h}_{mi}",
            "tu_tru": [("Năm", cc['Nam'], tt['Y']), ("Tháng", cc['Thang'], tt['M']),
                       ("Ngày", cc['Ngay'], tt['D']), ("Giờ", cc['Gio'], tt['H'])],
            "lines": [f"{tiet} • {kq['ThongTinCuc']} • Tuần Thủ: {kq['TuanThu']}", kq['TrucPhuSu']],
            "badges": [(f"Nhật Không: {', '.join(tk_nhat)}", "tk_n"),
                       (f"Thời Không: {', '.join(tk_thoi)}", "tk_g"), (f"Mã: {dich_ma}", "ma")],
            "cells": {cid: _cell_thuong(kq['Data9Cung'].get(cid), cid, tt, tk_nhat, tk_thoi, dich_ma)
                      for cid in range(1, 10)},
        }

    if loai == "Thời Gia (Chuyển Bàn)":
        p = qimen.paipan(datetime(y, m, d, h, mi), yinpan=qm_mode, setju=qm_setju)
        kq = qimen_pan_to_dict(p)
        cc = kq['TuTru']
        tt = _tu_tru_dict(cc)
        return {
            "kq": kq, "file_name": f"ky_mon_chuyenban_{y}_{m}_{d}_{h}_{mi}",
            "tu_tru": [("Năm", cc['Nam'], ""), ("Tháng", cc['Thang'], ""),
                       ("Ngày", cc['Ngay'], ""), ("Giờ", cc['Gio'], "")],
            "lines": [f"Tiết {kq['TietKhi']} • {kq['ThongTinCuc']} • Tuần Thủ: {kq['TuanThu']}", kq['TrucPhuSu'],
                      f"Giờ Việt Nam dùng lập trận: {kq['GioLapTran']}"],
            "badges": [(f"Không Vong: {kq['KhongVong']}", "tk_n"), (f"Mã: {kq['DichMa']}", "ma")],
            "cells": {cid: _cell_qimen(p, cid, tt) for cid in range(1, 10)},
        }

    if loai == "Nhật Gia":
        kq = lap_nhat_gia(y, m, d)
        can = kq['CanChiNgay'].split()[0]
        tt = {'Y': '', 'M': '', 'D': can, 'H': ''}
        tu_tru = [("Ngày", kq['CanChiNgay'], "")]
        lines = [f"Nhật Gia — Ngày {kq['Ngay']}", f"{kq['TietKhi']} • {kq['ThongTinCuc']} • {kq['AmDuong']}",
                 f"Tuần Thủ: {kq['TuanThu']}", kq['TrucPhuSu']]
        file_name = f"ky_mon_nhat_{y}_{m}_{d}"
    elif loai == "Nguyệt Gia":
        kq = lap_nguyet_gia(y, m, d)
        can = kq['CanChiThang'].split()[0]
        tt = {'Y': '', 'M': can, 'D': '', 'H': ''}
        tu_tru = [("Tháng", kq['CanChiThang'], "")]
        lines = [f"Nguyệt Gia — Ngày {kq['NgayHoi']}", f"{kq['TietKhi']} • {kq['ThongTinCuc']}",
                 f"Tuần Thủ: {kq['TuanThu']}", kq['TrucPhuSu']]
        file_name = f"ky_mon_nguyet_{y}_{m}_{d}"
    elif loai == "Niên Gia":
        kq = lap_nien_gia(y)
        can = kq['CanChiNam'].split()[0]
        tt = {'Y': can, 'M': '', 'D': '', 'H': ''}
        tu_tru = [("Năm", kq['CanChiNam'], f"{kq['TamNguyen']} Nguyên")]
        lines = [f"Niên Gia — Năm {kq['Nam']}", kq['ThongTinCuc'],
                 f"Tuần Thủ: {kq['TuanThu']}", kq['TrucPhuSu']]
        file_name = f"ky_mon_nien_{y}"
    else:
        raise ValueError(f"Loại cục không hợp lệ: {loai}")

    return {
        "kq": kq, "file_name": file_name, "tu_tru": tu_tru, "lines": lines, "badges": [],
        "cells": {cid: _cell_thuong(kq['Data9Cung'].get(cid), cid, tt, [], [], "") for cid in range(1, 10)},
    }
