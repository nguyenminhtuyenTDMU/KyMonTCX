# kymon_nien_nguyet_nhat.py
from calendar_provider import CachedCalendarProvider
from datetime import date, datetime, timedelta


THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
CUU_TINH = {1: "Bồng", 2: "Nhuế", 3: "Xung", 4: "Phụ", 5: "Cầm", 6: "Tâm", 7: "Trụ", 8: "Nhậm", 9: "Anh"}
BAT_MON = {1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 5: "", 6: "Khai", 7: "Kinh", 8: "Sinh", 9: "Cảnh"}
THU_TU_BAT_MON = ["Hưu", "Sinh", "Thương", "Đỗ", "Cảnh", "Tử", "Kinh", "Khai"]
BAT_THAN = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]
VONG_TRON_8_CUNG = [1, 8, 3, 4, 9, 2, 7, 6]


def can_chi_from_year(year: int) -> tuple[str, str]:
    can = THIEN_CAN[(year - 4) % 10]
    chi = DIA_CHI[(year - 4) % 12]
    return can, chi


def can_chi_from_sexagenary_index(idx: int) -> tuple[str, str]:
    return THIEN_CAN[idx % 10], DIA_CHI[idx % 12]


def sexagenary_index(can: str, chi: str) -> int:
    c = THIEN_CAN.index(can)
    z = DIA_CHI.index(chi)
    # find n such that n%10==c and n%12==z
    for n in range(60):
        if n % 10 == c and n % 12 == z:
            return n
    return 0


def tim_tuan_thu(can_str: str, chi_str: str) -> tuple[str, str]:
    """Tìm tuần thủ (can của Giáp đầu tuần) từ can-chi bất kỳ."""
    c_idx = THIEN_CAN.index(can_str)
    z_idx = DIA_CHI.index(chi_str)
    diff = (z_idx - c_idx) % 12
    mapping_can = {0: "Mậu", 10: "Kỷ", 8: "Canh", 6: "Tân", 4: "Nhâm", 2: "Quý"}
    mapping_ten = {0: "Giáp Tý", 10: "Giáp Tuất", 8: "Giáp Thân", 6: "Giáp Ngọ", 4: "Giáp Thìn", 2: "Giáp Dần"}
    return mapping_can.get(diff, "Mậu"), mapping_ten.get(diff, "Giáp Tý")


def an_dia_ban(cuc_so: int, am_duong: int) -> dict:
    """Bố địa bàn 9 cung. am_duong=1 Dương thuận, -1 Âm nghịch."""
    thu_tu = ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Đinh", "Bính", "Ất"]
    dia_ban = {}
    curr = cuc_so
    for can in thu_tu:
        dia_ban[curr] = can
        if am_duong == 1:
            curr = (curr % 9) + 1
        else:
            curr = (curr - 2) % 9 + 1
    return dia_ban


def tim_truc_phu_truc_su(dia_ban: dict, can_tuan_thu: str) -> tuple[str, str, int]:
    cung_vi = next((c for c, v in dia_ban.items() if v == can_tuan_thu), 5)
    sao_tp = CUU_TINH.get(cung_vi, "Cầm")
    cua_ts = BAT_MON.get(cung_vi, "Tử")
    if cung_vi == 5:
        sao_tp, cua_ts = "Cầm", "Tử"
    return sao_tp, cua_ts, cung_vi


def an_thien_ban_theo_can(dia_ban: dict, cung_tp_goc: int, target_can: str) -> dict:
    """Xoay thiên bàn dựa trên can đích (Trị Phù tùy can)."""
    cung_can = next((c for c, v in dia_ban.items() if v == target_can), cung_tp_goc)
    start_node = cung_tp_goc if cung_tp_goc != 5 else 2
    end_node = cung_can if cung_can != 5 else 2
    try:
        shift = VONG_TRON_8_CUNG.index(end_node) - VONG_TRON_8_CUNG.index(start_node)
    except ValueError:
        shift = 0
    thien_ban = {}
    for cung in VONG_TRON_8_CUNG:
        idx_goc = (VONG_TRON_8_CUNG.index(cung) - shift) % 8
        cung_goc = VONG_TRON_8_CUNG[idx_goc]
        can_bay = dia_ban.get(cung_goc, "")
        if cung_goc == 2:
            can_5 = dia_ban.get(5, "")
            can_bay = f"{can_bay}/{can_5}"
        thien_ban[cung] = {"Sao": CUU_TINH.get(cung_goc, ""), "Can": can_bay}
    thien_ban[5] = {"Sao": "", "Can": ""}
    return thien_ban


def an_bat_mon_theo_chi(cung_ts_goc: int, chi_dich: str, chi_tuan_thu: str, am_duong: int) -> dict:
    """Bố bát môn: Trị Sứ tùy chi, Âm nghịch hành."""
    idx_chi_tuan = DIA_CHI.index(chi_tuan_thu)
    idx_chi_dich = DIA_CHI.index(chi_dich)
    so_buoc = (idx_chi_dich - idx_chi_tuan) % 12
    if am_duong == 1:
        curr = (cung_ts_goc - 1 + so_buoc) % 9 + 1
    else:
        curr = (cung_ts_goc - 1 - so_buoc) % 9 + 1
        if curr <= 0:
            curr += 9
    cung_ts_dich = curr if curr != 5 else 2
    cung_lay_ten = cung_ts_goc if cung_ts_goc != 5 else 2
    ten_cua = BAT_MON.get(cung_lay_ten, "Hưu")
    idx_cua = THU_TU_BAT_MON.index(ten_cua)
    idx_cung = VONG_TRON_8_CUNG.index(cung_ts_dich)
    bat_mon = {}
    for i in range(8):
        cua = THU_TU_BAT_MON[(idx_cua + i) % 8]
        cung = VONG_TRON_8_CUNG[(idx_cung + i) % 8]
        bat_mon[cung] = cua
    bat_mon[5] = ""
    return bat_mon


def an_bat_than(cung_sao_tp_thien_ban: int, am_duong: int) -> dict:
    start = cung_sao_tp_thien_ban if cung_sao_tp_thien_ban != 5 else 2
    try:
        idx_start = VONG_TRON_8_CUNG.index(start)
    except ValueError:
        idx_start = 0
    bat_than = {}
    for i in range(8):
        idx_dest = (idx_start + i) % 8 if am_duong == 1 else (idx_start - i) % 8
        bat_than[VONG_TRON_8_CUNG[idx_dest]] = BAT_THAN[i]
    bat_than[5] = ""
    return bat_than


def build_data9cung(dia_ban, thien_ban, bat_mon, bat_than) -> dict:
    return {
        c: {
            "Dia": dia_ban.get(c, ""),
            "Thien": thien_ban[c]["Can"],
            "Sao": thien_ban[c]["Sao"],
            "Cua": bat_mon.get(c, ""),
            "Than": bat_than.get(c, ""),
        }
        for c in range(1, 10)
    }


# ================================================================
# 1. NIÊN GIA KỲ MÔN
# ================================================================

def xac_dinh_tam_nguyen_nien(year: int) -> tuple[str, int]:
    """
    Tam Nguyên Cửu Vận theo mốc:
      Thượng Nguyên: 1864, 1924+60=1984-60=1924... chu kỳ 60 năm mỗi Nguyên
      Thực ra mỗi 'Vận' là 20 năm, 3 Vận = 1 Nguyên = 60 năm, 3 Nguyên = 1 Hội = 180 năm.
      Mốc: Thượng 1864, Trung 1924, Hạ 1984, Thượng 2044...
    """
    moc = 1864
    offset = (year - moc) % 180
    if offset < 60:
        return "Thượng", 1      # Âm 1 cục
    elif offset < 120:
        return "Trung", 4      # Âm 4 cục
    else:
        return "Hạ", 7         # Âm 7 cục


def tinh_can_chi_nam_tiet_khi(year: int, lich: CachedCalendarProvider | None = None) -> tuple[str, str]:
    """Can chi của năm tiết khí `year` (Bính Ngọ cho 2026, v.v.)."""
    return THIEN_CAN[(year - 4) % 10], DIA_CHI[(year - 4) % 12]


def solar_year_of_date(year: int, month: int, day: int,
                       lich: CachedCalendarProvider) -> int:
    """Năm tiết khí chứa ngày year/month/day (so sánh với Lập Xuân)."""
    import pytz
    ds_tiet = lich.lay_danh_sach_tiet_khi_ca_nam(year)
    lap_xuan = next((t["ThoiGianTinh"] for t in ds_tiet if t["Ten"] == "Lập Xuân"), None)
    if lap_xuan is None:
        return year
    ref = pytz.timezone("Asia/Ho_Chi_Minh").localize(datetime(year, month, day, 12, 0))
    return year if ref >= lap_xuan else year - 1


def lap_nien_gia(year: int, lich: CachedCalendarProvider | None = None) -> dict:
    """
    Lập bàn Niên Gia Kỳ Môn cho năm dương lịch `year`.
    - Chỉ dùng Âm độn (am_duong = -1).
    - Cục: Thượng=1, Trung=4, Hạ=7.
    - Trị Phù tùy năm can, Trị Sứ tùy năm chi.
    """
    lich = lich or CachedCalendarProvider()
    nguyen, cuc_so = xac_dinh_tam_nguyen_nien(year)
    am_duong = -1  # Niên gia chỉ dùng Âm độn

    can_nam, chi_nam = tinh_can_chi_nam_tiet_khi(year, lich)

    dia_ban = an_dia_ban(cuc_so, am_duong)
    can_tuan_thu, ten_tuan = tim_tuan_thu(can_nam, chi_nam)
    sao_tp, cua_ts, cung_tp_goc = tim_truc_phu_truc_su(dia_ban, can_tuan_thu)

    # Trị Phù tùy năm can → xoay Thiên bàn
    thien_ban = an_thien_ban_theo_can(dia_ban, cung_tp_goc, can_tuan_thu)

    # Tìm cung TP mới (trên Thiên bàn sau khi xoay)
    cung_sao_tp_moi = next(
        (c for c in VONG_TRON_8_CUNG if thien_ban[c]["Sao"] == sao_tp), cung_tp_goc
    )
    if cung_sao_tp_moi == 5:
        cung_sao_tp_moi = 2

    # Trị Sứ tùy năm chi + Âm nghịch hành → bố 8 môn
    chi_tuan_thu_str = ten_tuan.split()[1]
    bat_mon = an_bat_mon_theo_chi(cung_tp_goc, chi_nam, chi_tuan_thu_str, am_duong)

    # Bố 8 thần Âm nghịch
    bat_than = an_bat_than(cung_sao_tp_moi, am_duong)

    return {
        "LoaiCuc": "Niên Gia Kỳ Môn",
        "Nam": year,
        "CanChiNam": f"{can_nam} {chi_nam}",
        "TamNguyen": nguyen,
        "ThongTinCuc": f"Âm {cuc_so} Cục - {nguyen} Nguyên",
        "TuanThu": f"{ten_tuan} ({can_tuan_thu})",
        "TrucPhuSu": f"Trực Phù: {sao_tp} | Trực Sử: {cua_ts}",
        "Data9Cung": build_data9cung(dia_ban, thien_ban, bat_mon, bat_than),
    }


# ================================================================
# 2. NGUYỆT GIA KỲ MÔN
# ================================================================

TIET_KHI_TO_CHI_THANG = {
    "Lập Xuân": "Dần", "Vũ Thủy": "Dần",
    "Kinh Trập": "Mão", "Xuân Phân": "Mão",
    "Thanh Minh": "Thìn", "Cốc Vũ": "Thìn",
    "Lập Hạ": "Tỵ", "Tiểu Mãn": "Tỵ",
    "Mang Chủng": "Ngọ", "Hạ Chí": "Ngọ",
    "Tiểu Thử": "Mùi", "Đại Thử": "Mùi",
    "Lập Thu": "Thân", "Xử Thử": "Thân",
    "Bạch Lộ": "Dậu", "Thu Phân": "Dậu",
    "Hàn Lộ": "Tuất", "Sương Giáng": "Tuất",
    "Lập Đông": "Hợi", "Tiểu Tuyết": "Hợi",
    "Đại Tuyết": "Tý", "Đông Chí": "Tý",
    "Tiểu Hàn": "Sửu", "Đại Hàn": "Sửu",
}

# Chi năm Phù đầu → Nguyên + cục
_PHU_DAU_CHI_TO_NGUYEN = {
    "Tý": ("Thượng", 7), "Ngọ": ("Thượng", 7),
    "Mão": ("Thượng", 7), "Dậu": ("Thượng", 7),
    "Dần": ("Trung", 1), "Thân": ("Trung", 1),
    "Tỵ": ("Trung", 1), "Hợi": ("Trung", 1),
    "Thìn": ("Hạ", 4), "Tuất": ("Hạ", 4),
    "Sửu": ("Hạ", 4), "Mùi": ("Hạ", 4),
}


def tim_nam_phu_dau(year: int) -> int:
    """Tìm năm Phù đầu gần nhất (năm Giáp hoặc Kỷ) không vượt quá year."""
    can_nam, _ = can_chi_from_year(year)
    # Giáp=0, Kỷ=5 trong THIEN_CAN
    idx = THIEN_CAN.index(can_nam)
    # số năm cần lùi để về Giáp hoặc Kỷ
    lui = idx % 5
    return year - lui


def xac_dinh_cuc_nguyet_gia(year: int) -> tuple[str, int]:
    nam_phu_dau = tim_nam_phu_dau(year)
    _, chi_phu_dau = can_chi_from_year(nam_phu_dau)
    return _PHU_DAU_CHI_TO_NGUYEN[chi_phu_dau]


def tinh_can_thang_ngu_ho_don(can_nam: str, chi_thang: str) -> str:
    idx_can_nam = THIEN_CAN.index(can_nam)
    start_idx = (idx_can_nam % 5) * 2 + 2
    seq = ["Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]
    offset = seq.index(chi_thang)
    return THIEN_CAN[(start_idx + offset) % 10]


def lap_nguyet_gia(year: int, month: int, day: int,
                   lich: CachedCalendarProvider | None = None) -> dict:
    """
    Lập bàn Nguyệt Gia Kỳ Môn cho tháng chứa ngày year/month/day.
    - Chỉ dùng Âm độn.
    - Cục dựa trên năm Phù đầu.
    - Trị Phù tùy nguyệt can, Trị Sứ tùy nguyệt chi.
    """
    lich = lich or CachedCalendarProvider()
    am_duong = -1

    # Can chi năm tiết khí chứa ngày hỏi
    solar_yr = solar_year_of_date(year, month, day, lich)
    nguyen, cuc_so = xac_dinh_cuc_nguyet_gia(solar_yr)
    can_nam, _ = tinh_can_chi_nam_tiet_khi(solar_yr)

    # Tiết khí hiện tại → chi tháng tiết khí
    ten_tiet = lich.tim_tiet_khi(year, month, day, 12, 0)
    chi_thang = TIET_KHI_TO_CHI_THANG.get(ten_tiet, "Dần")
    can_thang = tinh_can_thang_ngu_ho_don(can_nam, chi_thang)

    dia_ban = an_dia_ban(cuc_so, am_duong)
    can_tuan_thu, ten_tuan = tim_tuan_thu(can_thang, chi_thang)
    sao_tp, cua_ts, cung_tp_goc = tim_truc_phu_truc_su(dia_ban, can_tuan_thu)

    thien_ban = an_thien_ban_theo_can(dia_ban, cung_tp_goc, can_tuan_thu)

    cung_sao_tp_moi = next(
        (c for c in VONG_TRON_8_CUNG if thien_ban[c]["Sao"] == sao_tp), cung_tp_goc
    )
    if cung_sao_tp_moi == 5:
        cung_sao_tp_moi = 2

    chi_tuan_thu_str = ten_tuan.split()[1]
    bat_mon = an_bat_mon_theo_chi(cung_tp_goc, chi_thang, chi_tuan_thu_str, am_duong)
    bat_than = an_bat_than(cung_sao_tp_moi, am_duong)

    return {
        "LoaiCuc": "Nguyệt Gia Kỳ Môn",
        "NgayHoi": f"{day}/{month}/{year}",
        "TietKhi": ten_tiet,
        "CanChiThang": f"{can_thang} {chi_thang}",
        "TamNguyen": nguyen,
        "ThongTinCuc": f"Âm {cuc_so} Cục - {nguyen} Nguyên",
        "TuanThu": f"{ten_tuan} ({can_tuan_thu})",
        "TrucPhuSu": f"Trực Phù: {sao_tp} | Trực Sử: {cua_ts}",
        "Data9Cung": build_data9cung(dia_ban, thien_ban, bat_mon, bat_than),
    }


# ================================================================
# 3. NHẬT GIA KỲ MÔN — Triệt Bổ Pháp
# ================================================================

MAP_CUC_TIET_KHI = {
    "Đông Chí": ([1, 7, 4], 1), "Tiểu Hàn": ([2, 8, 5], 1), "Đại Hàn": ([3, 9, 6], 1),
    "Lập Xuân": ([8, 5, 2], 1), "Vũ Thủy": ([9, 6, 3], 1), "Kinh Trập": ([8, 5, 2], 1),
    "Xuân Phân": ([3, 9, 6], 1), "Thanh Minh": ([4, 1, 7], 1), "Cốc Vũ": ([5, 2, 8], 1),
    "Lập Hạ": ([4, 1, 7], 1), "Tiểu Mãn": ([5, 2, 8], 1), "Mang Chủng": ([6, 3, 9], 1),
    "Hạ Chí": ([9, 3, 6], -1), "Tiểu Thử": ([8, 2, 5], -1), "Đại Thử": ([7, 1, 4], -1),
    "Lập Thu": ([2, 5, 8], -1), "Xử Thử": ([1, 4, 7], -1), "Bạch Lộ": ([9, 3, 6], -1),
    "Thu Phân": ([7, 1, 4], -1), "Hàn Lộ": ([6, 9, 3], -1), "Sương Giáng": ([5, 8, 2], -1),
    "Lập Đông": ([6, 9, 3], -1), "Tiểu Tuyết": ([5, 8, 2], -1), "Đại Tuyết": ([4, 7, 1], -1),
}


def xac_dinh_cuc_nhat_triet_bo(
    can_ngay: str, chi_ngay: str, ten_tiet_khi: str
) -> tuple[int, int, str]:
    """
    Triệt bổ pháp: từ can-chi ngày xác định Thượng/Trung/Hạ nguyên,
    rồi tra MAP_CUC_TIET_KHI để lấy cục số và âm/dương.
    """
    c_idx = THIEN_CAN.index(can_ngay)
    z_idx = DIA_CHI.index(chi_ngay)
    delta = c_idx % 5
    chi_phu_dau_idx = (z_idx - delta) % 12
    # 0=Tý,6=Ngọ,3=Mão,9=Dậu → Thượng; 2=Dần,8=Thân,5=Tỵ,11=Hợi → Trung; còn lại → Hạ
    if chi_phu_dau_idx in (0, 6, 3, 9):
        nguyen_idx = 0
    elif chi_phu_dau_idx in (2, 8, 5, 11):
        nguyen_idx = 1
    else:
        nguyen_idx = 2
    info = MAP_CUC_TIET_KHI.get(ten_tiet_khi, ([1, 7, 4], 1))
    cuc_so = info[0][nguyen_idx]
    am_duong = info[1]
    nguyen_ten = ["Thượng", "Trung", "Hạ"][nguyen_idx]
    return cuc_so, am_duong, nguyen_ten


def tinh_can_chi_ngay(dd: int, mm: int, yy: int) -> tuple[str, str]:
    a = (14 - mm) // 12
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jdn = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return THIEN_CAN[(jdn + 9) % 10], DIA_CHI[(jdn + 1) % 12]


def lap_nhat_gia(year: int, month: int, day: int,
                 lich: CachedCalendarProvider | None = None) -> dict:
    """
    Lập bàn Nhật Gia Kỳ Môn cho ngày year/month/day dùng Triệt Bổ Pháp.
    Dương độn hoặc Âm độn tuỳ tiết khí.
    Trị Phù tùy nhật can, Trị Sứ tùy nhật chi.
    """
    lich = lich or CachedCalendarProvider()

    ten_tiet = lich.tim_tiet_khi(year, month, day, 12, 0)
    can_ngay, chi_ngay = tinh_can_chi_ngay(day, month, year)
    cuc_so, am_duong, nguyen = xac_dinh_cuc_nhat_triet_bo(can_ngay, chi_ngay, ten_tiet)

    dia_ban = an_dia_ban(cuc_so, am_duong)
    can_tuan_thu, ten_tuan = tim_tuan_thu(can_ngay, chi_ngay)
    sao_tp, cua_ts, cung_tp_goc = tim_truc_phu_truc_su(dia_ban, can_tuan_thu)

    # Trị Phù tùy nhật can → xoay Thiên bàn
    thien_ban = an_thien_ban_theo_can(dia_ban, cung_tp_goc, can_tuan_thu)

    cung_sao_tp_moi = next(
        (c for c in VONG_TRON_8_CUNG if thien_ban[c]["Sao"] == sao_tp), cung_tp_goc
    )
    if cung_sao_tp_moi == 5:
        cung_sao_tp_moi = 2

    # Trị Sứ tùy nhật chi
    chi_tuan_thu_str = ten_tuan.split()[1]
    bat_mon = an_bat_mon_theo_chi(cung_tp_goc, chi_ngay, chi_tuan_thu_str, am_duong)
    bat_than = an_bat_than(cung_sao_tp_moi, am_duong)

    return {
        "LoaiCuc": "Nhật Gia Kỳ Môn",
        "Ngay": f"{day}/{month}/{year}",
        "TietKhi": ten_tiet,
        "CanChiNgay": f"{can_ngay} {chi_ngay}",
        "AmDuong": "Dương độn" if am_duong == 1 else "Âm độn",
        "ThongTinCuc": f"{'Dương' if am_duong == 1 else 'Âm'} {cuc_so} Cục - {nguyen} Nguyên",
        "TuanThu": f"{ten_tuan} ({can_tuan_thu})",
        "TrucPhuSu": f"Trực Phù: {sao_tp} | Trực Sử: {cua_ts}",
        "Data9Cung": build_data9cung(dia_ban, thien_ban, bat_mon, bat_than),
    }
