# kymon_logic.py
from am_lich_vn import AmLichVN


class KyMonLapTran:
    def __init__(self):
        self.lich = AmLichVN()

        # 1. HẰNG SỐ CƠ BẢN
        self.THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        self.DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

        # Cửu Tinh & Bát Môn & Bát Thần
        self.CUU_TINH = {1: "Bồng", 2: "Nhuế", 3: "Xung", 4: "Phụ", 5: "Cầm", 6: "Tâm", 7: "Trụ", 8: "Nhậm", 9: "Anh"}
        self.BAT_MON = {1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 5: "", 6: "Khai", 7: "Kinh", 8: "Sinh", 9: "Cảnh"}
        self.THU_TU_BAT_MON = ["Hưu", "Sinh", "Thương", "Đỗ", "Cảnh", "Tử", "Kinh", "Khai"]
        self.BAT_THAN = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]

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

        # Vòng tròn 8 cung (Bỏ 5)
        self.VONG_TRON_8_CUNG = [1, 8, 3, 4, 9, 2, 7, 6]

        # Ngũ hành
        self.NGU_HANH_CUNG = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 5: "Thổ", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
        self.NGU_HANH_MON = {
            "Hưu": "Thủy", "Sinh": "Thổ", "Thương": "Mộc", "Đỗ": "Mộc",
            "Cảnh": "Hỏa", "Tử": "Thổ", "Kinh": "Kim", "Khai": "Kim"
        }

        # Mapping Cung -> Địa Chi
        self.CUNG_TO_CHI = {
            1: ["Tý"], 8: ["Sửu", "Dần"], 3: ["Mão"], 4: ["Thìn", "Tỵ"],
            9: ["Ngọ"], 2: ["Mùi", "Thân"], 7: ["Dậu"], 6: ["Tuất", "Hợi"]
        }

        # --- [MỚI] DỮ LIỆU ĐỂ TÍNH TRƯỜNG SINH ƯU TIÊN ---

        # 1. Âm Dương Thiên Can (0: Dương, 1: Âm)
        self.STEM_POLARITY = {
            "Giáp": 0, "Ất": 1, "Bính": 0, "Đinh": 1, "Mậu": 0,
            "Kỷ": 1, "Canh": 0, "Tân": 1, "Nhâm": 0, "Quý": 1
        }

        # 2. Âm Dương Địa Chi (0: Dương, 1: Âm)
        # Tý(1)=Dương, Sửu(2)=Âm... (Lẻ là Dương, Chẵn là Âm)
        self.BRANCH_POLARITY = {
            "Tý": 0, "Dần": 0, "Thìn": 0, "Ngọ": 0, "Thân": 0, "Tuất": 0,  # Dương
            "Sửu": 1, "Mão": 1, "Tỵ": 1, "Mùi": 1, "Dậu": 1, "Hợi": 1  # Âm
        }

        # 3. Bảng Vòng Trường Sinh Full
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
            # Âm Can
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
        # Ngũ hành của Cửu Tinh (Cố định theo cung gốc)
        # Bồng(1-Thủy), Nhuế(2-Thổ), Xung(3-Mộc), Phụ(4-Mộc), Cầm(5-Thổ)
        # Tâm(6-Kim), Trụ(7-Kim), Nhậm(8-Thổ), Anh(9-Hỏa)
        self.NGU_HANH_SAO = {
            "Bồng": "Thủy", "Nhuế": "Thổ", "Xung": "Mộc", "Phụ": "Mộc", "Cầm": "Thổ",
            "Tâm": "Kim", "Trụ": "Kim", "Nhậm": "Thổ", "Anh": "Hỏa"
        }

        # Ngũ hành của 12 Địa Chi (Để so sánh với Tháng)
        self.NGU_HANH_CHI = {
            "Hợi": "Thủy", "Tý": "Thủy",
            "Dần": "Mộc", "Mão": "Mộc",
            "Tỵ": "Hỏa", "Ngọ": "Hỏa",
            "Thân": "Kim", "Dậu": "Kim",
            "Thìn": "Thổ", "Tuất": "Thổ", "Sửu": "Thổ", "Mùi": "Thổ"
        }

        # Quy tắc sinh khắc (A sinh/khắc B)
        self.QUY_TAC_NGU_HANH = {
            "Kim": {"Sinh": "Thủy", "Khắc": "Mộc"},
            "Mộc": {"Sinh": "Hỏa", "Khắc": "Thổ"},
            "Thủy": {"Sinh": "Mộc", "Khắc": "Hỏa"},
            "Hỏa": {"Sinh": "Thổ", "Khắc": "Kim"},
            "Thổ": {"Sinh": "Kim", "Khắc": "Thủy"}
        }
    # ... [GIỮ NGUYÊN CÁC HÀM: xac_dinh_cuc_so, an_dia_ban, tim_tuan_thu, tim_truc_phu_truc_su, an_thien_ban, an_bat_mon, an_bat_than] ...
    # (Tôi rút gọn đoạn này để code đỡ dài, bạn giữ nguyên logic của các hàm trên trong file cũ nhé)
    def xac_dinh_cuc_so(self, can_ngay_str, chi_ngay_str, ten_tiet_khi):
        c_idx = self.THIEN_CAN.index(can_ngay_str)
        z_idx = self.DIA_CHI.index(chi_ngay_str)
        delta = c_idx % 5
        chi_phu_dau_idx = (z_idx - delta) % 12
        if chi_phu_dau_idx in [0, 6, 3, 9]:
            nguyen = 0
        elif chi_phu_dau_idx in [2, 8, 5, 11]:
            nguyen = 1
        else:
            nguyen = 2
        info_cuc = self.MAP_CUC_SO.get(ten_tiet_khi, ([1, 7, 4], 1))
        return info_cuc[0][nguyen], info_cuc[1], ["Thượng", "Trung", "Hạ"][nguyen]

    def an_dia_ban(self, cuc_so, am_duong):
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

    def tim_tuan_thu(self, can_gio_str, chi_gio_str):
        c_idx = self.THIEN_CAN.index(can_gio_str)
        z_idx = self.DIA_CHI.index(chi_gio_str)
        diff = (z_idx - c_idx) % 12
        mapping = {0: "Mậu", 10: "Kỷ", 8: "Canh", 6: "Tân", 4: "Nhâm", 2: "Quý"}
        ten_tuan = {0: "Giáp Tý", 10: "Giáp Tuất", 8: "Giáp Thân", 6: "Giáp Ngọ", 4: "Giáp Thìn", 2: "Giáp Dần"}.get(
            diff)
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
        if am_duong == 1:
            curr = (curr - 1 + so_buoc) % 9 + 1
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
            if am_duong == 1:
                idx_dest = (idx_start + i) % 8
            else:
                idx_dest = (idx_start - i) % 8
            cung_dest = self.VONG_TRON_8_CUNG[idx_dest]
            bat_than_result[cung_dest] = ten_than
        bat_than_result[5] = ""
        return bat_than_result

    # ========================================================
    # HÀM LOGIC MỚI: TÍNH TRƯỜNG SINH (PRIORITY LOGIC)
    # ========================================================
    def tinh_truong_sinh_theo_cung(self, thien_can, cung_id):
        """
        Tính giai đoạn trường sinh của Thiên Can tại một Cung cụ thể.
        Xử lý cung có 2 chi (Cấn, Tốn, Khôn, Càn) theo quy tắc ưu tiên:
        1. Ưu tiên "Mộ" (Grave).
        2. Nếu không có Mộ, chọn Chi cùng tính Âm/Dương (Đồng Khí).
        """
        if not thien_can or cung_id == 5: return ""

        # Xử lý Can ghép "Ất/Canh" -> Lấy can đầu
        can_chinh = thien_can.split("/")[0]
        if can_chinh not in self.STEM_POLARITY: return ""

        list_chi = self.CUNG_TO_CHI.get(cung_id)
        if not list_chi: return ""

        # Trường hợp 1: Cung Tí, Ngọ, Mão, Dậu (Chỉ có 1 chi)
        if len(list_chi) == 1:
            chi = list_chi[0]
            idx_stage = self.BANG_TRUONG_SINH[can_chinh][chi]
            return self.TEN_12_GIAI_DOAN[idx_stage]

        # Trường hợp 2: Cung Góc (Có 2 chi) -> Xử lý ưu tiên
        # --- ƯU TIÊN 1: Tìm xem có chi nào là "Mộ" không? ---
        for chi in list_chi:
            idx_stage = self.BANG_TRUONG_SINH[can_chinh][chi]
            ten_stage = self.TEN_12_GIAI_DOAN[idx_stage]
            if ten_stage == "Mộ":
                return "Mộ"

        # --- ƯU TIÊN 2: Chọn Chi Đồng Khí (Âm theo Âm, Dương theo Dương) ---
        pol_can = self.STEM_POLARITY.get(can_chinh)
        chi_selected = None

        for chi in list_chi:
            pol_chi = self.BRANCH_POLARITY.get(chi)
            if pol_can == pol_chi:
                chi_selected = chi
                break

        # Fallback (phòng hờ, thực tế cung góc luôn có 1 âm 1 dương)
        if not chi_selected: chi_selected = list_chi[0]

        idx_final = self.BANG_TRUONG_SINH[can_chinh][chi_selected]
        return self.TEN_12_GIAI_DOAN[idx_final]

    # ========================================================
    # HÀM PHÂN TÍCH BỔ SUNG
    # ========================================================\
    def tinh_vuong_suy_sao(self, ten_sao, chi_thang):
        """
        Tính Vượng Suy của Cửu Tinh so với Tháng (Trương Chí Xuân).
        Quy tắc Đèn Dầu:
        - Vượng: Ta sinh Tháng (Đèn tỏa sáng).
        - Tướng: Ta hòa Tháng.
        - Tử:    Tháng sinh Ta (Đèn bị đổ ngập dầu -> tắt).
        - Tù:    Tháng khắc Ta.
        - Hưu:   Ta khắc Tháng.
        """
        if not ten_sao or not chi_thang: return ""

        hanh_sao = self.NGU_HANH_SAO.get(ten_sao)
        hanh_thang = self.NGU_HANH_CHI.get(chi_thang)

        if not hanh_sao or not hanh_thang: return ""

        # 1. Tướng (Hòa)
        if hanh_sao == hanh_thang:
            return "Tướng"

        # 2. Vượng (Sao sinh Tháng)
        # Check xem HanhSao có sinh HanhThang không
        if self.QUY_TAC_NGU_HANH[hanh_sao]["Sinh"] == hanh_thang:
            return "Vượng"

        # 3. Tử (Tháng sinh Sao)
        if self.QUY_TAC_NGU_HANH[hanh_thang]["Sinh"] == hanh_sao:
            return "Phế"

        # 4. Tù (Tháng khắc Sao)
        if self.QUY_TAC_NGU_HANH[hanh_thang]["Khắc"] == hanh_sao:
            return "Tù"

        # 5. Hưu (Sao khắc Tháng) - Còn lại
        # Check cho chắc: Sao khắc Tháng
        if self.QUY_TAC_NGU_HANH[hanh_sao]["Khắc"] == hanh_thang:
            return "Hưu"

        return ""
    def tim_tuan_khong(self, ten_tuan_thu):
        chi_tuan = ten_tuan_thu.split()[1]
        idx = self.DIA_CHI.index(chi_tuan)
        idx_kk1 = (idx - 1) % 12
        idx_kk2 = (idx - 2) % 12
        return [self.DIA_CHI[idx_kk2], self.DIA_CHI[idx_kk1]]

    def tim_dich_ma(self, chi_gio):
        if chi_gio in ["Thân", "Tý", "Thìn"]: return "Dần"
        if chi_gio in ["Dần", "Ngọ", "Tuất"]: return "Thân"
        if chi_gio in ["Tỵ", "Dậu", "Sửu"]: return "Hợi"
        if chi_gio in ["Hợi", "Mão", "Mùi"]: return "Tỵ"
        return ""

    def check_mon_nhap_mo(self, ten_cua, list_chi_cung):
        map_mo_cua = {
            "Hưu": ["Thìn"], "Thương": ["Mùi"], "Đỗ": ["Mùi"],
            "Cảnh": ["Tuất"], "Kinh": ["Sửu"], "Khai": ["Sửu"],
            "Sinh": ["Thìn"], "Tử": ["Thìn"]
        }
        mo_chi = map_mo_cua.get(ten_cua, [])
        for chi in list_chi_cung:
            if chi in mo_chi: return True
        return False

    def phan_tich_bo_sung(self, ket_qua_lap_que, chi_thang):
        """
        Gắn nhãn: Tuần Không, Dịch Mã, Nhập Mộ, Trường Sinh Thiên Bàn.
        """
        data_9_cung = ket_qua_lap_que["Data9Cung"]

        tuan_thu_str = ket_qua_lap_que["TuanThu"]
        ten_tuan = tuan_thu_str.split(" (")[0]
        can_chi_gio_full = ket_qua_lap_que["CanChi"].split("|")[0].strip()
        chi_gio = can_chi_gio_full.split()[-1]

        tuan_khong_list = self.tim_tuan_khong(ten_tuan)
        dich_ma = self.tim_dich_ma(chi_gio)

        for cung_id in range(1, 10):
            if cung_id == 5: continue

            info = data_9_cung[cung_id]
            chi_tai_cung_list = self.CUNG_TO_CHI.get(cung_id, [])

            # 1. Tuần Không / Dịch Mã
            is_tuan_khong = any(chi in tuan_khong_list for chi in chi_tai_cung_list)
            is_dich_ma = (dich_ma in chi_tai_cung_list)

            # 2. Vòng Trường Sinh (Thiên Bàn vs Cung) - Dùng Logic Mới
            can_thien = info["Thien"]
            ts_thien_ban = self.tinh_truong_sinh_theo_cung(can_thien, cung_id)

            # Gắn cờ Nhập Mộ nếu trạng thái là "Mộ"
            can_nhap_mo_text = []
            if ts_thien_ban == "Mộ":
                can_nhap_mo_text.append(f"Can {can_thien} Nhập Mộ")

            # 3. Tính vượng tướng hưu tù phế của 9 tinh
            ten_sao = info["Sao"]
            trang_thai_sao = self.tinh_vuong_suy_sao(ten_sao, chi_thang)

            # 4. Cửa Nhập Mộ
            mon = info["Cua"]
            is_mon_nhap_mo = self.check_mon_nhap_mo(mon, chi_tai_cung_list)

            # Cập nhật Data
            info["PhanTich"] = {
                "TuanKhong": is_tuan_khong,
                "DichMa": is_dich_ma,
                "TruongSinh": ts_thien_ban,  # Kết quả ưu tiên (vd: Quan Đới)
                "CanNhapMo": can_nhap_mo_text,
                "VuongSuyThang": trang_thai_sao,
                "MonNhapMo": is_mon_nhap_mo
            }

        return ket_qua_lap_que

    # ========================================================
    # MAIN LAP QUE
    # ========================================================
    def lap_que(self, nam, thang, ngay, gio, phut):
        # 1. Lấy Lịch & Can Chi
        info_lich = self.lich.get_lunar_date(ngay, thang, nam)
        if not info_lich: return "Lỗi tính lịch"
        lday, lmonth, lyear, _ = info_lich
        cc = self.lich.get_can_chi(ngay, thang, nam, lmonth, lyear, hour=gio)

        # Lấy Chi Tháng để dùng cho Phân Tích sau này
        chi_thang_hien_tai = cc['Thang'].split()[1]

        ten_tiet_khi = self.lich.tim_tiet_khi(nam, thang, ngay, gio, phut)

        # 2. Tính toán Cục, Địa, Thiên, Môn, Thần
        can_ngay, chi_ngay = cc['Ngay'].split()
        can_gio, chi_gio = cc['Gio'].split()
        cuc, am_duong, nguyen = self.xac_dinh_cuc_so(can_ngay, chi_ngay, ten_tiet_khi)
        dia_ban = self.an_dia_ban(cuc, am_duong)
        can_tuan_thu, ten_tuan = self.tim_tuan_thu(can_gio, chi_gio)
        sao_tp_goc, cua_ts_goc, cung_tp_goc = self.tim_truc_phu_truc_su(dia_ban, can_tuan_thu)

        can_gio_don = cc['Gio'].split()[0]
        thien_ban = self.an_thien_ban(dia_ban, cung_tp_goc, can_gio_don, can_tuan_thu)

        target_can = can_gio_don
        if "Giáp" in target_can: target_can = can_tuan_thu
        cung_sao_tp_moi = 0
        for c, can in dia_ban.items():
            if can == target_can:
                cung_sao_tp_moi = c
                break
        if cung_sao_tp_moi == 5: cung_sao_tp_moi = 2

        chi_gio_don = cc['Gio'].split()[1]
        bat_mon = self.an_bat_mon(cung_tp_goc, chi_gio_don, ten_tuan, am_duong)
        bat_than = self.an_bat_than(cung_sao_tp_moi, am_duong)

        # 3. Đóng gói dữ liệu thô
        ket_qua = {
            "ThoiGian": f"{gio}h{phut} {ngay}/{thang}/{nam}",
            "CanChi": f"Giờ {cc['Gio']} | Ngày {cc['Ngay']} | Tiết {ten_tiet_khi}",
            "ThongTinCuc": f"{'Dương' if am_duong == 1 else 'Âm'} {cuc} Cục - {nguyen} Nguyên",
            "TuanThu": f"{ten_tuan} ({can_tuan_thu})",
            "TrucPhuSu": f"Trực Phù: {sao_tp_goc} | Trực Sử: {cua_ts_goc}",
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

        # 4. GỌI PHÂN TÍCH BỔ SUNG (Quan trọng!)
        # Vì bạn muốn dùng logic phân tích (Mộ, Tuần Không) nhưng không muốn viết lẫn lộn
        # Ta gọi hàm này ở bước cuối cùng để "gắn nhãn" cho dữ liệu
        ket_qua_full = self.phan_tich_bo_sung(ket_qua, chi_thang_hien_tai)

        return ket_qua_full


# --- TEST ---
if __name__ == "__main__":
    km = KyMonLapTran()

    # Test ngày: 16/3/2003 11:30
    kq = km.lap_que(2003, 3, 16, 11, 30)

    print("-" * 40)
    print("KẾT QUẢ LẬP TRẬN")
    print("-" * 40)
    print(kq["ThoiGian"])
    print(kq["CanChi"])
    print(kq["ThongTinCuc"])
    print(kq["TuanThu"])
    print(kq["TrucPhuSu"])
    print("-" * 40)
    print(kq["Data9Cung"])
    # In thử Cung 6 (Càn) và Cung 4 (Tốn) để xem logic Trường Sinh
    # Ví dụ Can Ất ở cung Càn (Tuất/Hợi) -> Sẽ ưu tiên Mộ (Tuất) thay vì Dưỡng/Thai
    # for c in [4, 6]:
    #     data = kq["Data9Cung"][c]
    #     print(f"CUNG {c}: Thiên={data['Thien']} | Trường Sinh={data['PhanTich']['TruongSinh']}")