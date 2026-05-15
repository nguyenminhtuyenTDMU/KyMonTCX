# kymon_logic.py
from calendar_provider import CachedCalendarProvider
from datetime import timedelta, datetime

class KyMonLapTran:
    def __init__(self, lich_provider=None):
        self.lich = lich_provider or CachedCalendarProvider()

        self.THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        self.DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

        # Mapping Cung -> Địa Chi
        self.CUNG_TO_CHI = {
            1: ["Tý"], 8: ["Sửu", "Dần"], 3: ["Mão"], 4: ["Thìn", "Tỵ"],
            9: ["Ngọ"], 2: ["Mùi", "Thân"], 7: ["Dậu"], 6: ["Tuất", "Hợi"]
        }

        # Mapping Tiết Khí -> Chi Tháng (Lịch Tiết Khí)
        self.TIET_KHI_TO_CHI_THANG = {
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
            "Tiểu Hàn": "Sửu", "Đại Hàn": "Sửu"
        }

        # Dữ liệu Cửu Tinh, Bát Môn, Bát Thần...
        self.CUU_TINH = {1: "Bồng", 2: "Nhuế", 3: "Xung", 4: "Phụ", 5: "Cầm", 6: "Tâm", 7: "Trụ", 8: "Nhậm", 9: "Anh"}
        self.BAT_MON = {1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 5: "", 6: "Khai", 7: "Kinh", 8: "Sinh", 9: "Cảnh"}
        self.THU_TU_BAT_MON = ["Hưu", "Sinh", "Thương", "Đỗ", "Cảnh", "Tử", "Kinh", "Khai"]
        self.BAT_THAN = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]
        self.VONG_TRON_8_CUNG = [1, 8, 3, 4, 9, 2, 7, 6]

        # DỮ LIỆU CỤC SỐ
        self.MAP_CUC_SO = {
            "Đông Chí": ([1, 7, 4], 1), "Tiểu Hàn": ([2, 8, 5], 1), "Đại Hàn": ([3, 9, 6], 1),
            "Lập Xuân": ([8, 5, 2], 1), "Vũ Thủy": ([9, 6, 3], 1), "Kinh Trập": ([1, 7, 4], 1),
            "Xuân Phân": ([3, 9, 6], 1), "Thanh Minh": ([4, 1, 7], 1), "Cốc Vũ": ([5, 2, 8], 1),
            "Lập Hạ": ([4, 1, 7], 1), "Tiểu Mãn": ([5, 2, 8], 1), "Mang Chủng": ([6, 3, 9], 1),
            "Hạ Chí": ([9, 3, 6], -1), "Tiểu Thử": ([8, 2, 5], -1), "Đại Thử": ([7, 1, 4], -1),
            "Lập Thu": ([2, 5, 8], -1), "Xử Thử": ([1, 4, 7], -1), "Bạch Lộ": ([9, 3, 6], -1),
            "Thu Phân": ([7, 1, 4], -1), "Hàn Lộ": ([6, 9, 3], -1), "Sương Giáng": ([5, 8, 2], -1),
            "Lập Đông": ([6, 9, 3], -1), "Tiểu Tuyết": ([5, 8, 2], -1), "Đại Tuyết": ([4, 7, 1], -1)
        }

        # Data Ngũ Hành & Trường Sinh
        self.NGU_HANH_SAO = {"Bồng": "Thủy", "Nhuế": "Thổ", "Xung": "Mộc", "Phụ": "Mộc", "Cầm": "Thổ", "Tâm": "Kim",
                             "Trụ": "Kim", "Nhậm": "Thổ", "Anh": "Hỏa"}
        self.NGU_HANH_CHI = {"Hợi": "Thủy", "Tý": "Thủy", "Dần": "Mộc", "Mão": "Mộc", "Tỵ": "Hỏa", "Ngọ": "Hỏa",
                             "Thân": "Kim", "Dậu": "Kim", "Thìn": "Thổ", "Tuất": "Thổ", "Sửu": "Thổ", "Mùi": "Thổ"}
        self.NGU_HANH_CUNG = {
            1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ",
            6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"
        }
        self.QUY_TAC_NGU_HANH = {
            "Kim": {"Sinh": "Thủy", "Khắc": "Mộc"}, "Mộc": {"Sinh": "Hỏa", "Khắc": "Thổ"},
            "Thủy": {"Sinh": "Mộc", "Khắc": "Hỏa"},
            "Hỏa": {"Sinh": "Thổ", "Khắc": "Kim"}, "Thổ": {"Sinh": "Kim", "Khắc": "Thủy"}
        }
        self.STEM_POLARITY = {"Giáp": 0, "Ất": 1, "Bính": 0, "Đinh": 1, "Mậu": 0, "Kỷ": 1, "Canh": 0, "Tân": 1,
                              "Nhâm": 0, "Quý": 1}
        self.BRANCH_POLARITY = {"Tý": 0, "Dần": 0, "Thìn": 0, "Ngọ": 0, "Thân": 0, "Tuất": 0, "Sửu": 1, "Mão": 1,
                                "Tỵ": 1, "Mùi": 1, "Dậu": 1, "Hợi": 1}
        self.BANG_TRUONG_SINH = {
            "Giáp": {"Hợi": 0, "Tý": 1, "Sửu": 2, "Dần": 3, "Mão": 4, "Thìn": 5, "Tỵ": 6, "Ngọ": 7, "Mùi": 8, "Thân": 9,
                     "Dậu": 10, "Tuất": 11},
            "Bính": {"Dần": 0, "Mão": 1, "Thìn": 2, "Tỵ": 3, "Ngọ": 4, "Mùi": 5, "Thân": 6, "Dậu": 7, "Tuất": 8,
                     "Hợi": 9, "Tý": 10, "Sửu": 11},
            "Mậu": {"Dần": 0, "Mão": 1, "Thìn": 2, "Tỵ": 3, "Ngọ": 4, "Mùi": 5, "Thân": 6, "Dậu": 7, "Tuất": 8,
                    "Hợi": 9, "Tý": 10, "Sửu": 11},
            "Canh": {"Tỵ": 0, "Ngọ": 1, "Mùi": 2, "Thân": 3, "Dậu": 4, "Tuất": 5, "Hợi": 6, "Tý": 7, "Sửu": 8, "Dần": 9,
                     "Mão": 10, "Thìn": 11},
            "Nhâm": {"Thân": 0, "Dậu": 1, "Tuất": 2, "Hợi": 3, "Tý": 4, "Sửu": 5, "Dần": 6, "Mão": 7, "Thìn": 8,
                     "Tỵ": 9, "Ngọ": 10, "Mùi": 11},
            "Ất": {"Ngọ": 0, "Tỵ": 1, "Thìn": 2, "Mão": 3, "Dần": 4, "Sửu": 5, "Tý": 6, "Hợi": 7, "Tuất": 8, "Dậu": 9,
                   "Thân": 10, "Mùi": 11},
            "Đinh": {"Dậu": 0, "Thân": 1, "Mùi": 2, "Ngọ": 3, "Tỵ": 4, "Thìn": 5, "Mão": 6, "Dần": 7, "Sửu": 8, "Tý": 9,
                     "Hợi": 10, "Tuất": 11},
            "Kỷ": {"Dậu": 0, "Thân": 1, "Mùi": 2, "Ngọ": 3, "Tỵ": 4, "Thìn": 5, "Mão": 6, "Dần": 7, "Sửu": 8, "Tý": 9,
                   "Hợi": 10, "Tuất": 11},
            "Tân": {"Tý": 0, "Hợi": 1, "Tuất": 2, "Dậu": 3, "Thân": 4, "Mùi": 5, "Ngọ": 6, "Tỵ": 7, "Thìn": 8, "Mão": 9,
                    "Dần": 10, "Sửu": 11},
            "Quý": {"Mão": 0, "Dần": 1, "Sửu": 2, "Tý": 3, "Hợi": 4, "Tuất": 5, "Dậu": 6, "Thân": 7, "Mùi": 8, "Ngọ": 9,
                    "Tỵ": 10, "Thìn": 11}
        }
        self.TEN_12_GIAI_DOAN = ["Trường Sinh", "Mộc Dục", "Quan Đới", "Lâm Quan", "Đế Vượng", "Suy", "Bệnh", "Tử",
                                 "Mộ", "Tuyệt", "Thai", "Dưỡng"]

    # ========================================================
    # XỬ LÝ NGÀY GIỜ & LỊCH TIẾT KHÍ
    # ========================================================
    def lay_thoi_diem_lap_xuan(self, year):
        ds_tiet = self.lich.lay_danh_sach_tiet_khi_ca_nam(year)
        for t in ds_tiet:
            if t["Ten"] == "Lập Xuân":
                return t["ThoiGianTinh"]
        return None

    def tinh_can_chi_nam_tiet_khi(self, dt_input):
        year = dt_input.year
        lap_xuan_hien_tai = self.lay_thoi_diem_lap_xuan(year)

        if not lap_xuan_hien_tai:
            return self.lich.get_can_chi(dt_input.day, dt_input.month, dt_input.year, 1, 1)['Nam']

        if dt_input < lap_xuan_hien_tai:
            nam_tinh = year - 1
        else:
            nam_tinh = year

        can_idx = (nam_tinh - 4) % 10
        chi_idx = (nam_tinh - 4) % 12
        return f"{self.THIEN_CAN[can_idx]} {self.DIA_CHI[chi_idx]}"

    def tinh_can_thang_ngu_ho_don(self, can_nam, chi_thang_tiet_khi):
        can_nam_short = can_nam.split()[0]
        idx_can_nam = self.THIEN_CAN.index(can_nam_short)
        start_idx = (idx_can_nam % 5) * 2 + 2

        seq_month = ["Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]
        offset = seq_month.index(chi_thang_tiet_khi)

        final_can_idx = (start_idx + offset) % 10
        return self.THIEN_CAN[final_can_idx]

    def xu_ly_gio_ty(self, year, month, day, hour, minute):
        dt = datetime(year, month, day, hour, minute)
        if hour >= 23:
            dt = dt + timedelta(days=1)
            return dt, 0
        return dt, hour

    def tinh_thang_tiet_khi(self, can_nam, chi_thang_tiet_khi):
        idx_can_nam = self.THIEN_CAN.index(can_nam)
        idx_khoi_dau = (idx_can_nam % 5) * 2 + 2

        idx_chi_thang = self.DIA_CHI.index(chi_thang_tiet_khi)
        idx_dan = self.DIA_CHI.index("Dần")
        offset = (idx_chi_thang - idx_dan) % 12

        idx_can_thang = (idx_khoi_dau + offset) % 10
        return self.THIEN_CAN[idx_can_thang]

    def xac_dinh_cuc_so(self, can_ngay_str, chi_ngay_str, ten_tiet_khi):
        c_idx = self.THIEN_CAN.index(can_ngay_str)
        z_idx = self.DIA_CHI.index(chi_ngay_str)
        delta = c_idx % 5
        chi_phu_dau_idx = (z_idx - delta) % 12
        if chi_phu_dau_idx in [0, 6, 3, 9]: nguyen = 0
        elif chi_phu_dau_idx in [2, 8, 5, 11]: nguyen = 1
        else: nguyen = 2
        info_cuc = self.MAP_CUC_SO.get(ten_tiet_khi, ([1, 7, 4], 1))
        return info_cuc[0][nguyen], info_cuc[1], ["Thượng", "Trung", "Hạ"][nguyen]

    def an_dia_ban(self, cuc_so, am_duong):
        thu_tu = ["Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý", "Đinh", "Bính", "Ất"]
        dia_ban = {}
        curr = cuc_so
        for can in thu_tu:
            dia_ban[curr] = can
            if am_duong == 1: curr = (curr % 9) + 1
            else: curr = (curr - 2) % 9 + 1
        return dia_ban

    def tim_tuan_thu(self, can_gio_str, chi_gio_str):
        c_idx = self.THIEN_CAN.index(can_gio_str)
        z_idx = self.DIA_CHI.index(chi_gio_str)
        diff = (z_idx - c_idx) % 12
        mapping = {0: "Mậu", 10: "Kỷ", 8: "Canh", 6: "Tân", 4: "Nhâm", 2: "Quý"}
        ten_tuan = {0: "Giáp Tý", 10: "Giáp Tuất", 8: "Giáp Thân", 6: "Giáp Ngọ", 4: "Giáp Thìn", 2: "Giáp Dần"}.get(diff)
        return mapping.get(diff, "Mậu"), ten_tuan

    def tim_truc_phu_truc_su(self, dia_ban, can_tuan_thu):
        cung_vi = 0
        for c, can in dia_ban.items():
            if can == can_tuan_thu:
                cung_vi = c
                break
        sao_tp = self.CUU_TINH.get(cung_vi)
        cua_ts = self.BAT_MON.get(cung_vi)
        if cung_vi == 5:
            sao_tp = "Cầm"
            cua_ts = "Tử"
        return sao_tp, cua_ts, cung_vi

    def an_thien_ban(self, dia_ban, cung_truc_phu, can_gio_str, can_tuan_thu):
        target_can = can_gio_str
        if "Giáp" in target_can: target_can = can_tuan_thu
        cung_can_gio = 0
        for c, can in dia_ban.items():
            if can == target_can:
                cung_can_gio = c
                break
        start_node = cung_truc_phu if cung_truc_phu != 5 else 2
        end_node = cung_can_gio if cung_can_gio != 5 else 2
        try:
            idx_start = self.VONG_TRON_8_CUNG.index(start_node)
            idx_end = self.VONG_TRON_8_CUNG.index(end_node)
            shift = idx_end - idx_start
        except ValueError:
            shift = 0
        thien_ban = {}
        for cung_hien_tai in self.VONG_TRON_8_CUNG:
            idx_current = self.VONG_TRON_8_CUNG.index(cung_hien_tai)
            idx_goc = (idx_current - shift) % 8
            cung_goc = self.VONG_TRON_8_CUNG[idx_goc]
            ten_sao = self.CUU_TINH.get(cung_goc)
            can_bay = dia_ban.get(cung_goc)
            if cung_goc == 2:
                can_5 = dia_ban.get(5)
                can_bay = f"{can_bay}/{can_5}"
            thien_ban[cung_hien_tai] = {"Sao": ten_sao, "Can": can_bay}
        thien_ban[5] = {"Sao": "", "Can": ""}
        return thien_ban

    def an_bat_mon(self, cung_truc_su_goc, chi_gio_str, ten_tuan_thu, am_duong):
        chi_tuan_thu_str = ten_tuan_thu.split()[1]
        idx_chi_tuan = self.DIA_CHI.index(chi_tuan_thu_str)
        idx_chi_gio = self.DIA_CHI.index(chi_gio_str)
        so_buoc = (idx_chi_gio - idx_chi_tuan) % 12
        curr = cung_truc_su_goc
        if am_duong == 1: curr = (curr - 1 + so_buoc) % 9 + 1
        else:
            curr = (curr - 1 - so_buoc) % 9 + 1
            if curr <= 0: curr += 9
        cung_truc_su_dich = curr
        if cung_truc_su_dich == 5: cung_truc_su_dich = 2
        bat_mon_result = {}
        cung_lay_ten = cung_truc_su_goc if cung_truc_su_goc != 5 else 2
        ten_cua_truc_su = self.BAT_MON.get(cung_lay_ten)
        idx_cua_start = self.THU_TU_BAT_MON.index(ten_cua_truc_su)
        idx_cung_start = self.VONG_TRON_8_CUNG.index(cung_truc_su_dich)
        for i in range(8):
            cua = self.THU_TU_BAT_MON[(idx_cua_start + i) % 8]
            cung = self.VONG_TRON_8_CUNG[(idx_cung_start + i) % 8]
            bat_mon_result[cung] = cua
        bat_mon_result[5] = ""
        return bat_mon_result

    def an_bat_than(self, cung_sao_truc_phu_thien_ban, am_duong):
        ds_than = self.BAT_THAN
        bat_than_result = {}
        start_node = cung_sao_truc_phu_thien_ban if cung_sao_truc_phu_thien_ban != 5 else 2
        try:
            idx_start = self.VONG_TRON_8_CUNG.index(start_node)
        except ValueError:
            idx_start = 0
        for i in range(8):
            ten_than = ds_than[i]
            if am_duong == 1: idx_dest = (idx_start + i) % 8
            else: idx_dest = (idx_start - i) % 8
            cung_dest = self.VONG_TRON_8_CUNG[idx_dest]
            bat_than_result[cung_dest] = ten_than
        bat_than_result[5] = ""
        return bat_than_result

    # ========================================================
    # LOGIC MỚI: TÍNH NHẬP MỘ CỤ THỂ
    # ========================================================
    def tinh_truong_sinh_theo_cung(self, thien_can, cung_id):
        if not thien_can or cung_id == 5: return ""
        can_chinh = thien_can.split("/")[0]

        # 1. KIỂM TRA LUẬT NHẬP MỘ (THIÊN CAN) ĐỘC QUYỀN
        # - Giáp, Ất lạc Cung Khôn (2) là nhập mộ
        # - Bính, Mậu nhập cung Càn (6) là nhập mộ
        # - Đinh lạc cung Cấn (8) là nhập mộ
        is_mo = False
        if can_chinh in ["Giáp", "Ất"] and cung_id == 2:
            is_mo = True
        elif can_chinh in ["Bính", "Mậu"] and cung_id == 6:
            is_mo = True
        elif can_chinh == "Đinh" and cung_id == 8:
            is_mo = True

        if is_mo:
            return "Mộ"

        # 2. TÍNH 12 VÒNG TRƯỜNG SINH CHO CÁC TRƯỜNG HỢP KHÁC
        if can_chinh not in self.STEM_POLARITY: return ""
        list_chi = self.CUNG_TO_CHI.get(cung_id)
        if not list_chi: return ""

        # Ưu tiên tính trường sinh theo Chi có cùng thuộc tính Âm/Dương với Can
        pol_can = self.STEM_POLARITY.get(can_chinh)
        chi_selected = list_chi[0]
        for chi in list_chi:
            if self.BRANCH_POLARITY.get(chi) == pol_can:
                chi_selected = chi
                break

        idx_final = self.BANG_TRUONG_SINH[can_chinh][chi_selected]
        ten_stage = self.TEN_12_GIAI_DOAN[idx_final]

        # QUAN TRỌNG: "Những cái còn lại không gọi nhập mộ"
        # Nên nếu theo 12 vòng trường sinh mà vô tình rơi vào "Mộ" (VD: Canh tại Cấn)
        # Thì ta chặn lại, trả về rỗng để không in chữ "Mộ" ra ngoài.
        if ten_stage == "Mộ":
            return ""

        return ten_stage

    def tinh_vuong_suy_sao(self, ten_sao, cung_id):
        if not ten_sao or not cung_id: return ""
        hanh_sao = self.NGU_HANH_SAO.get(ten_sao)
        hanh_cung = self.NGU_HANH_CUNG.get(cung_id)
        if not hanh_sao or not hanh_cung: return ""
        if hanh_sao == hanh_cung: return "Tướng"
        if self.QUY_TAC_NGU_HANH[hanh_sao]["Sinh"] == hanh_cung: return "Vượng"
        if self.QUY_TAC_NGU_HANH[hanh_cung]["Sinh"] == hanh_sao: return "Phế"
        if self.QUY_TAC_NGU_HANH[hanh_cung]["Khắc"] == hanh_sao: return "Tù"
        if self.QUY_TAC_NGU_HANH[hanh_sao]["Khắc"] == hanh_cung: return "Hưu"
        return ""

    def tim_dich_ma(self, chi_gio):
        if chi_gio in ["Thân", "Tý", "Thìn"]: return "Dần"
        if chi_gio in ["Dần", "Ngọ", "Tuất"]: return "Thân"
        if chi_gio in ["Tỵ", "Dậu", "Sửu"]: return "Hợi"
        if chi_gio in ["Hợi", "Mão", "Mùi"]: return "Tỵ"
        return ""

    def tim_tuan_khong_tuyet_doi(self, can, chi):
        idx_can = self.THIEN_CAN.index(can)
        idx_chi = self.DIA_CHI.index(chi)
        diff = (idx_chi - idx_can) % 12
        idx_kk1 = (diff - 1) % 12
        idx_kk2 = (diff - 2) % 12
        return [self.DIA_CHI[idx_kk2], self.DIA_CHI[idx_kk1]]
    
    def doi_giap_sang_nghi_an(self, can, can_tuan_thu):
        # Trong Kỳ Môn, thời can Giáp không hiện trực tiếp trên bàn mà ẩn dưới lục nghi.
        if can == "Giáp":
            return can_tuan_thu
        return can

    def tim_cung_theo_can(self, data9cung, can_tim):
        if not can_tim:
            return None
        for cid, data in data9cung.items():
            thien = data.get("Thien", "") or ""
            dia = data.get("Dia", "") or ""
            ds_thien = [x.strip() for x in thien.split("/") if x.strip()]
            if can_tim in ds_thien or can_tim == dia:
                return cid
        return None

    def tim_cung_theo_cua(self, data9cung, cua_tim):
        if not cua_tim:
            return None
        for cid, data in data9cung.items():
            if data.get("Cua") == cua_tim:
                return cid
        return None

    def cung_co_chi_trong_ds(self, cung_id, ds_chi):
        if cung_id is None:
            return False
        return any(chi in ds_chi for chi in self.CUNG_TO_CHI.get(cung_id, []))

    def lap_que(self, nam, thang, ngay, gio, phut):
        dt_tinh, gio_tinh = self.xu_ly_gio_ty(nam, thang, ngay, gio, phut)

        import pytz
        tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')
        dt_input_tz = tz_vn.localize(datetime(nam, thang, ngay, gio, phut))

        can_chi_nam_chuan = self.tinh_can_chi_nam_tiet_khi(dt_input_tz)

        ten_tiet_khi = self.lich.tim_tiet_khi(nam, thang, ngay, gio, phut)
        chi_thang_tk = self.TIET_KHI_TO_CHI_THANG.get(ten_tiet_khi, "Dần")
        can_thang_tk = self.tinh_can_thang_ngu_ho_don(can_chi_nam_chuan.split()[0], chi_thang_tk)
        can_chi_thang_chuan = f"{can_thang_tk} {chi_thang_tk}"

        info_lich = self.lich.get_lunar_date(dt_tinh.day, dt_tinh.month, dt_tinh.year)
        cc_tmp = self.lich.get_can_chi(dt_tinh.day, dt_tinh.month, dt_tinh.year, info_lich[1], info_lich[2], hour=gio_tinh)

        cc_final = {
            "Nam": can_chi_nam_chuan,
            "Thang": can_chi_thang_chuan,
            "Ngay": cc_tmp["Ngay"],
            "Gio": cc_tmp["Gio"]
        }

        can_ngay, chi_ngay = cc_final['Ngay'].split()
        can_gio, chi_gio = cc_final['Gio'].split()

        cuc, am_duong, nguyen = self.xac_dinh_cuc_so(can_ngay, chi_ngay, ten_tiet_khi)
        dia_ban = self.an_dia_ban(cuc, am_duong)
        can_tuan_thu, ten_tuan = self.tim_tuan_thu(can_gio, chi_gio)
        sao_tp_goc, cua_ts_goc, cung_tp_goc = self.tim_truc_phu_truc_su(dia_ban, can_tuan_thu)

        can_gio_don = cc_final['Gio'].split()[0]
        thien_ban = self.an_thien_ban(dia_ban, cung_tp_goc, can_gio_don, can_tuan_thu)

        target_can = can_gio_don
        if "Giáp" in target_can: target_can = can_tuan_thu
        cung_sao_tp_moi = 0
        for c, can in dia_ban.items():
            if can == target_can: cung_sao_tp_moi = c; break
        if cung_sao_tp_moi == 5: cung_sao_tp_moi = 2

        chi_gio_don = cc_final['Gio'].split()[1]
        bat_mon = self.an_bat_mon(cung_tp_goc, chi_gio_don, ten_tuan, am_duong)
        bat_than = self.an_bat_than(cung_sao_tp_moi, am_duong)

        tk_nhat = self.tim_tuan_khong_tuyet_doi(can_ngay, chi_ngay)
        tk_thoi = self.tim_tuan_khong_tuyet_doi(can_gio, chi_gio)

        ket_qua = {
            "ThoiGian": f"{gio}h{phut} {ngay}/{thang}/{nam}",
            "CanChi": f"Giờ {cc_final['Gio']} | Ngày {cc_final['Ngay']} | Tiết {ten_tiet_khi}",
            "TuTru": cc_final,
            "ThongTinCuc": f"{'Dương' if am_duong == 1 else 'Âm'} {cuc} Cục - {nguyen} Nguyên",
            "TuanThu": f"{ten_tuan} ({can_tuan_thu})",
            "TrucPhuSu": f"Trực Phù: {sao_tp_goc} | Trực Sử: {cua_ts_goc}",
            "InfoTuanKhong": {"Nhat": tk_nhat, "Thoi": tk_thoi},
            "Data9Cung": {
                c: {
                    "Dia": dia_ban.get(c, ""),
                    "Thien": thien_ban[c]["Can"],
                    "Sao": thien_ban[c]["Sao"],
                    "Cua": bat_mon.get(c, ""),
                    "Than": bat_than.get(c, "")
                } for c in range(1, 10)
            }
        }

        ket_qua_full = self.phan_tich_bo_sung(ket_qua)
        data9 = ket_qua_full["Data9Cung"]
        thoi_can_hien = self.doi_giap_sang_nghi_an(can_gio, can_tuan_thu)

        ket_qua_full["Maps"] = {
            "NhatCan": can_ngay,
            "NhatChi": chi_ngay,
            "ThoiCan": can_gio,
            "ThoiChi": chi_gio,
            "ThoiCanHien": thoi_can_hien,
            "TuanThu": ten_tuan,
            "GiapAnNghi": can_tuan_thu if can_gio == "Giáp" else None,
            "NhatCanCung": self.tim_cung_theo_can(data9, can_ngay),
            "ThoiCanCung": self.tim_cung_theo_can(data9, thoi_can_hien),
            "KhaiMonCung": self.tim_cung_theo_cua(data9, "Khai"),
            "SinhMonCung": self.tim_cung_theo_cua(data9, "Sinh"),
            "HuuMonCung": self.tim_cung_theo_cua(data9, "Hưu"),
        }

        ket_qua_full["HiddenStems"] = {
            "Giáp Tý": "Mậu",
            "Giáp Tuất": "Kỷ",
            "Giáp Thân": "Canh",
            "Giáp Ngọ": "Tân",
            "Giáp Thìn": "Nhâm",
            "Giáp Dần": "Quý",
            "Current": {
                "Tuan": ten_tuan,
                "Nghi": can_tuan_thu
            }
        }

        maps = ket_qua_full["Maps"]
        ket_qua_full["Flags"] = {
            "NhatCanCungNhatKhong": self.cung_co_chi_trong_ds(maps["NhatCanCung"], tk_nhat),
            "NhatCanCungThoiKhong": self.cung_co_chi_trong_ds(maps["NhatCanCung"], tk_thoi),
            "ThoiCanCungNhatKhong": self.cung_co_chi_trong_ds(maps["ThoiCanCung"], tk_nhat),
            "ThoiCanCungThoiKhong": self.cung_co_chi_trong_ds(maps["ThoiCanCung"], tk_thoi),
            "KhaiMonCungNhatKhong": self.cung_co_chi_trong_ds(maps["KhaiMonCung"], tk_nhat),
            "KhaiMonCungThoiKhong": self.cung_co_chi_trong_ds(maps["KhaiMonCung"], tk_thoi),
            "SinhMonCungNhatKhong": self.cung_co_chi_trong_ds(maps["SinhMonCung"], tk_nhat),
            "SinhMonCungThoiKhong": self.cung_co_chi_trong_ds(maps["SinhMonCung"], tk_thoi),
        }

        return ket_qua_full

    def phan_tich_bo_sung(self, ket_qua_lap_que):
        data_9_cung = ket_qua_lap_que["Data9Cung"]
        can_chi_gio_full = ket_qua_lap_que["CanChi"].split("|")[0].strip()
        chi_gio = can_chi_gio_full.split()[-1]
        dich_ma = self.tim_dich_ma(chi_gio)

        for cung_id in range(1, 10):
            if cung_id == 5: continue
            info = data_9_cung[cung_id]
            chi_tai_cung_list = self.CUNG_TO_CHI.get(cung_id, [])

            is_dich_ma = (dich_ma in chi_tai_cung_list)
            can_thien = info["Thien"]
            ts_thien_ban = self.tinh_truong_sinh_theo_cung(can_thien, cung_id)
            ten_sao = info["Sao"]
            trang_thai_sao = self.tinh_vuong_suy_sao(ten_sao, cung_id)

            mon = info["Cua"]
            is_mon_nhap_mo = False
            map_mo_cua = {"Hưu": ["Thìn"], "Thương": ["Mùi"], "Đỗ": ["Mùi"], "Cảnh": ["Tuất"], "Kinh": ["Sửu"],
                          "Khai": ["Sửu"], "Sinh": ["Thìn"], "Tử": ["Thìn"]}
            mo_chi = map_mo_cua.get(mon, [])
            for chi in chi_tai_cung_list:
                if chi in mo_chi: is_mon_nhap_mo = True

            info["PhanTich"] = {
                "DichMa": is_dich_ma,
                "TruongSinh": ts_thien_ban,
                "VuongSuyCung": trang_thai_sao,
                "VuongSuyThang": trang_thai_sao,
                "MonNhapMo": is_mon_nhap_mo
            }
        return ket_qua_lap_que
