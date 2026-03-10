# kymon_logic.py
from am_lich_vn import AmLichVN
from datetime import timedelta, datetime


class KyMonLapTran:
    def __init__(self):
        self.lich = AmLichVN()

        self.THIEN_CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        self.DIA_CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

        # Mapping Cung -> Địa Chi
        self.CUNG_TO_CHI = {
            1: ["Tý"], 8: ["Sửu", "Dần"], 3: ["Mão"], 4: ["Thìn", "Tỵ"],
            9: ["Ngọ"], 2: ["Mùi", "Thân"], 7: ["Dậu"], 6: ["Tuất", "Hợi"]
        }

        # Mapping Tiết Khí -> Chi Tháng (Lịch Tiết Khí)
        # Tháng Dần bắt đầu từ Lập Xuân, Tháng Mão từ Kinh Trập...
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

        # Dữ liệu Cửu Tinh, Bát Môn, Bát Thần... (GIỮ NGUYÊN)
        self.CUU_TINH = {1: "Bồng", 2: "Nhuế", 3: "Xung", 4: "Phụ", 5: "Cầm", 6: "Tâm", 7: "Trụ", 8: "Nhậm", 9: "Anh"}
        self.BAT_MON = {1: "Hưu", 2: "Tử", 3: "Thương", 4: "Đỗ", 5: "", 6: "Khai", 7: "Kinh", 8: "Sinh", 9: "Cảnh"}
        self.THU_TU_BAT_MON = ["Hưu", "Sinh", "Thương", "Đỗ", "Cảnh", "Tử", "Kinh", "Khai"]
        self.BAT_THAN = ["Trực Phù", "Đằng Xà", "Thái Âm", "Lục Hợp", "Bạch Hổ", "Huyền Vũ", "Cửu Địa", "Cửu Thiên"]
        self.VONG_TRON_8_CUNG = [1, 8, 3, 4, 9, 2, 7, 6]

        # DỮ LIỆU CỤC SỐ (GIỮ NGUYÊN)
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

        # Data Ngũ Hành & Trường Sinh (GIỮ NGUYÊN)
        self.NGU_HANH_SAO = {"Bồng": "Thủy", "Nhuế": "Thổ", "Xung": "Mộc", "Phụ": "Mộc", "Cầm": "Thổ", "Tâm": "Kim",
                             "Trụ": "Kim", "Nhậm": "Thổ", "Anh": "Hỏa"}
        self.NGU_HANH_CHI = {"Hợi": "Thủy", "Tý": "Thủy", "Dần": "Mộc", "Mão": "Mộc", "Tỵ": "Hỏa", "Ngọ": "Hỏa",
                             "Thân": "Kim", "Dậu": "Kim", "Thìn": "Thổ", "Tuất": "Thổ", "Sửu": "Thổ", "Mùi": "Thổ"}
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
        """Tìm thời điểm Lập Xuân chính xác của năm dương lịch"""
        ds_tiet = self.lich.lay_danh_sach_tiet_khi_ca_nam(year)
        for t in ds_tiet:
            if t["Ten"] == "Lập Xuân":
                return t["ThoiGianTinh"]  # Trả về datetime object
        return None

    def tinh_can_chi_nam_tiet_khi(self, dt_input):
        """
        Xác định Can Chi Năm dựa trên điểm Lập Xuân.
        - Nếu thời gian nhập < Lập Xuân năm đó -> Tính là Năm trước.
        - Nếu thời gian nhập >= Lập Xuân năm đó -> Tính là Năm nay.
        """
        year = dt_input.year
        lap_xuan_hien_tai = self.lay_thoi_diem_lap_xuan(year)

        # Nếu không tìm thấy (hiếm), fallback về logic cũ
        if not lap_xuan_hien_tai:
            return self.lich.get_can_chi(dt_input.day, dt_input.month, dt_input.year, 1, 1)['Nam']

        # So sánh với Lập Xuân
        # Lưu ý: dt_input cần có timezone giống lap_xuan_hien_tai (Asia/Ho_Chi_Minh)
        if dt_input < lap_xuan_hien_tai:
            nam_tinh = year - 1
        else:
            nam_tinh = year

        # Tính Can Chi cho năm đã xác định
        # Công thức tính Can Năm: (Năm dương - 3) % 10. 4 -> Giáp (0)
        can_idx = (nam_tinh - 4) % 10
        # Công thức tính Chi Năm: (Năm dương - 4) % 12. 4 -> Tý (0)
        chi_idx = (nam_tinh - 4) % 12

        return f"{self.THIEN_CAN[can_idx]} {self.DIA_CHI[chi_idx]}"

    def tinh_can_thang_ngu_ho_don(self, can_nam, chi_thang_tiet_khi):
        """
        Ngũ Hổ Độn: Tìm Can Tháng từ Can Năm và Chi Tháng (Dần, Mão...)
        """
        # Giáp/Kỷ khởi Bính Dần (Bính=2)
        # Ất/Canh khởi Mậu Dần (Mậu=4)
        # Bính/Tân khởi Canh Dần (Canh=6)
        # Đinh/Nhâm khởi Nhâm Dần (Nhâm=8)
        # Mậu/Quý khởi Giáp Dần (Giáp=0)

        can_nam_short = can_nam.split()[0]
        idx_can_nam = self.THIEN_CAN.index(can_nam_short)

        # Công thức tìm can tháng Dần (Tháng khởi đầu)
        start_idx = (idx_can_nam % 5) * 2 + 2

        # Khoảng cách từ Dần đến Chi tháng hiện tại
        idx_dan = self.DIA_CHI.index("Dần")
        idx_chi_ht = self.DIA_CHI.index(chi_thang_tiet_khi)

        # Xử lý vòng tròn: Tý Sửu nằm sau Hợi
        # Trong danh sách DIA_CHI: Tý=0, Sửu=1, Dần=2...
        # Nếu tháng là Tý (idx 0), Dần là 2 -> Offset phải tính theo vòng
        # Cách dễ nhất: Map lại thứ tự tháng tiết khí: Dần=0, Mão=1 ... Sửu=11

        seq_month = ["Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"]
        offset = seq_month.index(chi_thang_tiet_khi)

        final_can_idx = (start_idx + offset) % 10
        return self.THIEN_CAN[final_can_idx]
    def xu_ly_gio_ty(self, year, month, day, hour, minute):
        """
        Nếu giờ >= 23h, chuyển sang ngày hôm sau (Giờ Tý Đầu).
        Trả về datetime object đã điều chỉnh.
        """
        dt = datetime(year, month, day, hour, minute)
        if hour >= 23:
            # Cộng thêm 1 ngày
            dt = dt + timedelta(days=1)
            # Giờ dùng để tính Can Chi sẽ là 0 (Tý)
            # Lưu ý: Ta trả về ngày mới, nhưng giờ hiển thị vẫn là 23h
            # Tuy nhiên để tính Can Chi, ta dùng giờ 0
            return dt, 0
        return dt, hour

    def tinh_thang_tiet_khi(self, can_nam, chi_thang_tiet_khi):
        """
        Tính Can Tháng theo Ngũ Hổ Độn (Giáp Kỷ khởi Bính Dần...)
        """
        # Mapping Can Năm -> Can tháng Dần (Tháng 1 tiết khí)
        # Giáp/Kỷ (0/5) -> Bính (2)
        # Ất/Canh (1/6) -> Mậu (4)
        # Bính/Tân (2/7) -> Canh (6)
        # Đinh/Nhâm (3/8) -> Nhâm (8)
        # Mậu/Quý (4/9) -> Giáp (0)

        idx_can_nam = self.THIEN_CAN.index(can_nam)
        idx_khoi_dau = (idx_can_nam % 5) * 2 + 2  # Công thức Ngũ Hổ Độn

        # Tìm offset của chi tháng so với Dần (Dần là 0)
        # Dần=0, Mão=1... Sửu=11
        idx_chi_thang = self.DIA_CHI.index(chi_thang_tiet_khi)
        idx_dan = self.DIA_CHI.index("Dần")

        offset = (idx_chi_thang - idx_dan) % 12

        idx_can_thang = (idx_khoi_dau + offset) % 10
        return self.THIEN_CAN[idx_can_thang]

    # ... (Các hàm xac_dinh_cuc_so, an_dia_ban, tim_tuan_thu... GIỮ NGUYÊN) ...
    # Để code gọn, tôi chỉ viết lại các phần thay đổi.
    # Bạn hãy giữ lại các hàm logic cốt lõi từ bài trước:
    # xac_dinh_cuc_so, an_dia_ban, tim_tuan_thu, tim_truc_phu_truc_su, an_thien_ban, an_bat_mon, an_bat_than

    # [COPY LẠI CÁC HÀM CŨ VÀO ĐÂY]
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

    # ... (Hàm tính trường sinh, vượng suy sao, dịch mã giữ nguyên) ...
    def tinh_truong_sinh_theo_cung(self, thien_can, cung_id):
        if not thien_can or cung_id == 5: return ""
        can_chinh = thien_can.split("/")[0]
        if can_chinh not in self.STEM_POLARITY: return ""
        list_chi = self.CUNG_TO_CHI.get(cung_id)
        if not list_chi: return ""
        if len(list_chi) == 1:
            chi = list_chi[0]
            idx_stage = self.BANG_TRUONG_SINH[can_chinh][chi]
            return self.TEN_12_GIAI_DOAN[idx_stage]
        for chi in list_chi:
            idx_stage = self.BANG_TRUONG_SINH[can_chinh][chi]
            ten_stage = self.TEN_12_GIAI_DOAN[idx_stage]
            if ten_stage == "Mộ": return "Mộ"
        pol_can = self.STEM_POLARITY.get(can_chinh)
        chi_selected = None
        for chi in list_chi:
            pol_chi = self.BRANCH_POLARITY.get(chi)
            if pol_can == pol_chi:
                chi_selected = chi
                break
        if not chi_selected: chi_selected = list_chi[0]
        idx_final = self.BANG_TRUONG_SINH[can_chinh][chi_selected]
        return self.TEN_12_GIAI_DOAN[idx_final]

    def tinh_vuong_suy_sao(self, ten_sao, chi_thang):
        if not ten_sao or not chi_thang: return ""
        hanh_sao = self.NGU_HANH_SAO.get(ten_sao)
        hanh_thang = self.NGU_HANH_CHI.get(chi_thang)
        if not hanh_sao or not hanh_thang: return ""
        if hanh_sao == hanh_thang: return "Tướng"
        if self.QUY_TAC_NGU_HANH[hanh_sao]["Sinh"] == hanh_thang: return "Vượng"
        if self.QUY_TAC_NGU_HANH[hanh_thang]["Sinh"] == hanh_sao: return "Tử"
        if self.QUY_TAC_NGU_HANH[hanh_thang]["Khắc"] == hanh_sao: return "Tù"
        if self.QUY_TAC_NGU_HANH[hanh_sao]["Khắc"] == hanh_thang: return "Hưu"
        return ""

    def tim_dich_ma(self, chi_gio):
        if chi_gio in ["Thân", "Tý", "Thìn"]: return "Dần"
        if chi_gio in ["Dần", "Ngọ", "Tuất"]: return "Thân"
        if chi_gio in ["Tỵ", "Dậu", "Sửu"]: return "Hợi"
        if chi_gio in ["Hợi", "Mão", "Mùi"]: return "Tỵ"
        return ""

    # ========================================================
    # LOGIC MỚI: TÍNH 2 LOẠI TUẦN KHÔNG (NHẬT & THỜI)
    # ========================================================
    def tim_tuan_khong_tuyet_doi(self, can, chi):
        """Trả về 2 Chi bị Tuần Không của cặp Can Chi bất kỳ"""
        idx_can = self.THIEN_CAN.index(can)
        idx_chi = self.DIA_CHI.index(chi)

        # Tìm Tuần Thủ (Can Giáp nằm ở đâu)
        # Công thức: (Chi - Can) % 12
        diff = (idx_chi - idx_can) % 12

        # Tuần Không là 2 chi nằm ngay trước Tuần Thủ
        # Tuần Thủ tại Tý (0) -> TK tại Tuất, Hợi
        idx_kk1 = (diff - 1) % 12
        idx_kk2 = (diff - 2) % 12

        return [self.DIA_CHI[idx_kk2], self.DIA_CHI[idx_kk1]]

    # ========================================================
    # MAIN LOGIC (CẬP NHẬT)
    # ========================================================
    # ========================================================
    # HÀM LAP QUE (SỬA LẠI ĐỂ DÙNG NĂM TIẾT KHÍ)
    # ========================================================
    def lap_que(self, nam, thang, ngay, gio, phut):
        # 1. Xử lý Giờ Tý (Dạ Tý)
        dt_tinh, gio_tinh = self.xu_ly_gio_ty(nam, thang, ngay, gio, phut)

        # Tạo object datetime có múi giờ để so sánh với Lập Xuân
        import pytz
        tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')
        dt_input_tz = tz_vn.localize(datetime(nam, thang, ngay, gio, phut))

        # 2. TÍNH NĂM TIẾT KHÍ (QUAN TRỌNG)
        # Không dùng năm của AmLichVN nữa, mà tự tính
        can_chi_nam_chuan = self.tinh_can_chi_nam_tiet_khi(dt_input_tz)

        # 3. TÍNH THÁNG TIẾT KHÍ
        # Lấy tên tiết khí
        ten_tiet_khi = self.lich.tim_tiet_khi(nam, thang, ngay, gio, phut)
        # Lấy Chi tháng (Dần/Mão...) từ tiết khí
        chi_thang_tk = self.TIET_KHI_TO_CHI_THANG.get(ten_tiet_khi, "Dần")
        # Tính Can tháng theo Ngũ Hổ Độn (dựa vào Can Năm Chuẩn vừa tính)
        can_thang_tk = self.tinh_can_thang_ngu_ho_don(can_chi_nam_chuan.split()[0], chi_thang_tk)

        can_chi_thang_chuan = f"{can_thang_tk} {chi_thang_tk}"

        # 4. TÍNH NGÀY GIỜ (Dùng AmLichVN là ok, chỉ cần sửa Năm/Tháng)
        # Vẫn cần gọi AmLichVN để lấy Can Chi Ngày/Giờ (vì ngày giờ ko phụ thuộc Lập Xuân)
        info_lich = self.lich.get_lunar_date(dt_tinh.day, dt_tinh.month, dt_tinh.year)
        cc_tmp = self.lich.get_can_chi(dt_tinh.day, dt_tinh.month, dt_tinh.year, info_lich[1], info_lich[2],
                                       hour=gio_tinh)

        # GỘP LẠI THÀNH BỘ TỨ TRỤ CHUẨN
        cc_final = {
            "Nam": can_chi_nam_chuan,  # Đã fix theo Lập Xuân
            "Thang": can_chi_thang_chuan,  # Đã fix theo Ngũ Hổ Độn + Tiết Khí
            "Ngay": cc_tmp["Ngay"],  # Giữ nguyên
            "Gio": cc_tmp["Gio"]  # Giữ nguyên
        }

        # 5. TIẾP TỤC CÁC BƯỚC LẬP CỤC NHƯ CŨ
        # Lưu ý: Các bước sau dùng cc_final thay vì cc cũ
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
            "TuTru": cc_final,  # Trả về Tứ Trụ chuẩn để hiển thị
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

        # Pass Chi Tháng chuẩn vào phân tích để tính Vượng Suy Sao
        ket_qua_full = self.phan_tich_bo_sung(ket_qua, chi_thang_tk)
        return ket_qua_full
    def phan_tich_bo_sung(self, ket_qua_lap_que, chi_thang):
        data_9_cung = ket_qua_lap_que["Data9Cung"]

        # Lấy Can Chi Giờ để tính Mã
        can_chi_gio_full = ket_qua_lap_que["CanChi"].split("|")[0].strip()
        chi_gio = can_chi_gio_full.split()[-1]
        dich_ma = self.tim_dich_ma(chi_gio)

        for cung_id in range(1, 10):
            if cung_id == 5: continue
            info = data_9_cung[cung_id]
            chi_tai_cung_list = self.CUNG_TO_CHI.get(cung_id, [])

            # --- Dịch Mã ---
            is_dich_ma = (dich_ma in chi_tai_cung_list)

            # --- Trường Sinh ---
            can_thien = info["Thien"]
            ts_thien_ban = self.tinh_truong_sinh_theo_cung(can_thien, cung_id)

            # --- Vượng Suy Sao ---
            ten_sao = info["Sao"]
            trang_thai_sao = self.tinh_vuong_suy_sao(ten_sao, chi_thang)

            # --- Cửa Nhập Mộ ---
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
                "VuongSuyThang": trang_thai_sao,
                "MonNhapMo": is_mon_nhap_mo
            }
        return ket_qua_lap_que
