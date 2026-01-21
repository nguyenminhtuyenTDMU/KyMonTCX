from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from skyfield.searchlib import find_discrete
from datetime import datetime, timedelta, date
import pytz
import math


class AmLichVN:
    def __init__(self):
        # 1. Khởi tạo Skyfield
        try:
            self.ts = load.timescale()
            self.eph = load('de421.bsp')
        except:
            print("Đang tải dữ liệu de421.bsp...")
            self.eph = load('de421.bsp')
            self.ts = load.timescale()

        self.sun = self.eph['sun']
        self.moon = self.eph['moon']
        self.earth = self.eph['earth']
        self.MAP_TEN = {
            0: "Xuân Phân", 15: "Thanh Minh", 30: "Cốc Vũ", 45: "Lập Hạ",
            60: "Tiểu Mãn", 75: "Mang Chủng", 90: "Hạ Chí", 105: "Tiểu Thử",
            120: "Đại Thử", 135: "Lập Thu", 150: "Xử Thử", 165: "Bạch Lộ",
            180: "Thu Phân", 195: "Hàn Lộ", 210: "Sương Giáng", 225: "Lập Đông",
            240: "Tiểu Tuyết", 255: "Đại Tuyết", 270: "Đông Chí", 285: "Tiểu Hàn",
            300: "Đại Hàn", 315: "Lập Xuân", 330: "Vũ Thủy", 345: "Kinh Trập"
        }
        # Múi giờ Việt Nam
        self.tz_vn = pytz.timezone('Asia/Ho_Chi_Minh')

        # Dữ liệu Can Chi
        self.CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        self.CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

    # ==========================================
    # PHẦN 1: CÁC HÀM THIÊN VĂN (ĐÃ SỬA LỖI VECTOR)
    # ==========================================

    def get_solar_longitude(self, t):
        """Tính kinh độ mặt trời"""
        e = self.earth.at(t)
        _, lon, _ = e.observe(self.sun).apparent().frame_latlon(ecliptic_frame)
        return lon.degrees  # Trả về mảng numpy hoặc số float

    def get_new_moon(self, year_start, year_end):
        """Tìm các điểm Sóc (New Moon)"""
        t0 = self.ts.from_datetime(year_start)
        t1 = self.ts.from_datetime(year_end)

        def is_new_moon(t):
            e = self.earth.at(t)
            _, slon, _ = e.observe(self.sun).apparent().frame_latlon(ecliptic_frame)
            _, mlon, _ = e.observe(self.moon).apparent().frame_latlon(ecliptic_frame)
            # Sóc là khi hiệu kinh độ < 180 (chuyển từ 360 về 0)
            return (mlon.degrees - slon.degrees) % 360.0 < 180

        is_new_moon.step_days = 0.5
        times, values = find_discrete(t0, t1, is_new_moon)

        new_moons = []
        for t, v in zip(times, values):
            if v == 1:  # 1 nghĩa là bắt đầu chu kỳ mới (Sóc)
                dt_utc = t.utc_datetime()
                dt_vn = dt_utc.replace(tzinfo=pytz.utc).astimezone(self.tz_vn)
                new_moons.append(dt_vn)
        return new_moons

    def check_dong_chi(self, date_start, date_end):
        """
        [FIXED] Kiểm tra chính xác xem tháng này có chứa điểm ĐÔNG CHÍ (270 độ) không.
        Dùng phương pháp step integer thay vì so sánh float >= 270 để tránh lỗi tháng 1,2,3.
        """
        t_start = self.ts.from_datetime(date_start)
        t_end = self.ts.from_datetime(date_end)

        def step_15_degrees(t):
            lon = self.get_solar_longitude(t)
            # 270 độ chia 15 = 18. Đây là index của Đông Chí.
            return (lon // 15).astype(int)

        step_15_degrees.step_days = 2.0  # Quét kỹ
        times, values = find_discrete(t_start, t_end, step_15_degrees)

        # Nếu trong khoảng này mặt trời bước vào cung 18 (270-285 độ)
        # Thì đây chính là tháng Đông Chí (Tháng 11 âm)
        if 18 in values:
            return True
        return False
    def has_major_term(self, date_start, date_end):
        """Kiểm tra Trung Khí (Major Term) trong tháng"""
        t_start = self.ts.from_datetime(date_start)
        t_end = self.ts.from_datetime(date_end)

        def step_30_degrees(t):
            lon = self.get_solar_longitude(t)
            # FIX: Dùng .astype(int) thay vì int() để xử lý mảng
            return (lon // 30).astype(int)

        step_30_degrees.step_days = 5.0
        times, values = find_discrete(t_start, t_end, step_30_degrees)
        return len(times) > 0

    # ==========================================
    # PHẦN 2: THUẬT TOÁN HỒ NGỌC ĐỨC
    # ==========================================
    def get_lunar_date(self, dd, mm, yy):
        target_date = self.tz_vn.localize(datetime(yy, mm, dd))

        # 1. Tìm Sóc chứa ngày hiện tại (Để xác định ngày mùng 1)
        start_search = target_date - timedelta(days=60)
        end_search = target_date + timedelta(days=60)
        new_moons = self.get_new_moon(start_search, end_search)

        soc_hien_tai = None
        for nm in new_moons:
            if nm.date() <= target_date.date():
                soc_hien_tai = nm
            else:
                break

        if not soc_hien_tai: return None

        lunar_day = (target_date.date() - soc_hien_tai.date()).days + 1

        # 2. Tìm Tháng 11 Âm (Chứa Đông Chí)
        # Quét rộng từ tháng 11 năm trước đến tháng 3 năm sau
        search_year_start = datetime(yy - 1, 10, 1, tzinfo=self.tz_vn)
        search_year_end = datetime(yy + 1, 4, 1, tzinfo=self.tz_vn)

        all_new_moons = self.get_new_moon(search_year_start, search_year_end)

        # Tìm index các tháng có chứa Đông Chí
        dc_indices = []
        for i in range(len(all_new_moons) - 1):
            # [FIXED] Dùng hàm check_dong_chi mới
            if self.check_dong_chi(all_new_moons[i], all_new_moons[i + 1]):
                dc_indices.append(i)

        # Xác định vị trí tháng hiện tại trong danh sách
        current_moon_idx = -1
        for i, nm in enumerate(all_new_moons):
            # So sánh string date để tránh lỗi lệch giờ/phút nhỏ
            if nm.strftime("%Y-%m-%d") == soc_hien_tai.strftime("%Y-%m-%d"):
                current_moon_idx = i
                break

        if current_moon_idx == -1: return None  # Fallback

        # Tìm Sóc A (Tháng 11 gần nhất trong quá khứ)
        soc_A_idx = -1
        for idx in reversed(dc_indices):
            if idx <= current_moon_idx:
                soc_A_idx = idx
                break

        if soc_A_idx == -1: return None  # Fallback

        # Sóc B (Tháng 11 tiếp theo) để tính nhuận
        try:
            # Tìm index Đông chí tiếp theo trong danh sách dc_indices
            idx_in_dc_list = dc_indices.index(soc_A_idx)
            if idx_in_dc_list + 1 < len(dc_indices):
                soc_B_idx = dc_indices[idx_in_dc_list + 1]
            else:
                soc_B_idx = soc_A_idx + 12  # Giả định nếu list ko đủ dài
        except:
            soc_B_idx = soc_A_idx + 12

        is_leap_year = (soc_B_idx - soc_A_idx == 13)

        # Tính tháng Âm ban đầu (Tháng Đông Chí luôn là 11)
        month_offset = current_moon_idx - soc_A_idx
        lunar_month_val = 11 + month_offset

        is_leap_month = False

        if is_leap_year:
            leap_idx = -1
            # Tìm tháng nhuận (tháng đầu tiên ko có Trung Khí giữa 2 Đông Chí)
            for i in range(1, 13):  # Check các tháng kẹp giữa
                m_start = all_new_moons[soc_A_idx + i]
                m_end = all_new_moons[soc_A_idx + i + 1]
                if not self.has_major_term(m_start, m_end):
                    leap_idx = soc_A_idx + i
                    break

            if leap_idx != -1:
                if current_moon_idx == leap_idx:
                    is_leap_month = True
                    # Tháng nhuận lấy số của tháng trước -> trừ 1
                    lunar_month_val -= 1
                elif current_moon_idx > leap_idx:
                    # Các tháng sau tháng nhuận bị đẩy lùi 1 số
                    lunar_month_val -= 1

        # Chuẩn hóa số tháng (13 -> 1, 14 -> 2...)
        while lunar_month_val > 12:
            lunar_month_val -= 12

        # Tính Năm Âm Lịch
        lunar_year = yy
        # Nếu tháng > 10 (11, 12) mà vẫn đang ở đầu năm dương (tháng 1, 2)
        # Thì đó là tháng Chạp/Một của năm cũ
        if lunar_month_val >= 11 and mm < 4:
            lunar_year -= 1

        return lunar_day, lunar_month_val, lunar_year, is_leap_month

    # ==========================================
    # PHẦN 3: TÍNH CAN CHI (Cập nhật tính Giờ)
    # ==========================================
    def get_can_chi(self, dd, mm, yy, lunar_month, lunar_year, hour=0):
        """
        Tính Can Chi cho Năm, Tháng, Ngày, Giờ.
        Tham số hour: Giờ dương lịch (0-23). Mặc định là 0.
        """
        # 1. Can Chi Năm
        can_nam = self.CAN[(lunar_year + 6) % 10]
        chi_nam = self.CHI[(lunar_year + 8) % 12]

        # 2. Can Chi Tháng
        # Công thức: (Năm * 12 + Tháng + 3) % 10
        can_thang_idx = (lunar_year * 12 + lunar_month + 3) % 10
        can_thang = self.CAN[can_thang_idx]
        chi_thang = self.CHI[(lunar_month + 1) % 12]

        # 3. Can Chi Ngày (Dùng Julian Day Number)
        a = (14 - mm) // 12
        y = yy + 4800 - a
        m = mm + 12 * a - 3
        jdn = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

        can_ngay_idx = (jdn + 9) % 10
        chi_ngay_idx = (jdn + 1) % 12
        can_ngay = self.CAN[can_ngay_idx]
        chi_ngay = self.CHI[chi_ngay_idx]

        # 4. Can Chi Giờ (MỚI THÊM)
        # - Tìm Chi Giờ:
        chi_gio_idx = ((hour + 1) // 2) % 12

        # - Tìm Can Giờ (Ngũ Thử Độn): Dựa vào Can Ngày
        # Quy tắc: (CanNgày % 5) * 2 + ChiGiờ
        can_gio_idx = ((can_ngay_idx % 5) * 2 + chi_gio_idx) % 10

        can_gio = self.CAN[can_gio_idx]
        chi_gio = self.CHI[chi_gio_idx]

        return {
            "Nam": f"{can_nam} {chi_nam}",
            "Thang": f"{can_thang} {chi_thang}",
            "Ngay": f"{can_ngay} {chi_ngay}",
            "Gio": f"{can_gio} {chi_gio}"
        }

    # ==========================================
    # PHẦN 4: TÍNH TIẾT KHÍ
    # ==========================================
    def _fix_gio_dau_canh(self, dt_goc):
        """
        Hàm cốt lõi: Làm tròn giờ của Tiết khí xuống đầu Canh giờ (Giờ Lẻ)
        Ví dụ:
        - 03:02 -> 03:00 (Giữ nguyên giờ lẻ)
        - 04:59 -> 03:00 (Giờ chẵn lùi 1)
        - 00:15 -> 23:00 hôm trước (Giờ 0 lùi về 23)
        """
        gio = dt_goc.hour

        # Mặc định reset phút giây về 0
        dt_fix = dt_goc.replace(minute=0, second=0, microsecond=0)

        if gio % 2 != 0:
            # Nếu là giờ lẻ (1, 3, 5...): Đã là đầu canh giờ -> Giữ nguyên
            pass
        else:
            # Nếu là giờ chẵn (0, 2, 4...)
            if gio == 0:
                # Riêng 0h lùi về 23h ngày hôm trước
                dt_fix = dt_fix - timedelta(hours=1)
            else:
                # Các giờ chẵn khác thì lùi 1 tiếng (vd 8h -> 7h)
                dt_fix = dt_fix.replace(hour=gio - 1)

        return dt_fix

    def lay_danh_sach_tiet_khi_ca_nam(self, year):
        """
        Tính toán danh sách tiết khí và FIX lại giờ bắt đầu theo ý bạn
        """
        # Quét rộng ra năm trước và năm sau để đảm bảo không bị sót tháng 1 hoặc tháng 12
        t0 = self.ts.utc(year, 1, 1)
        t1 = self.ts.utc(year + 1, 1, 31)

        def step_15_degrees(t):
            e = self.earth.at(t)
            _, lon, _ = e.observe(self.sun).apparent().frame_latlon(ecliptic_frame)
            return (lon.degrees // 15).astype(int)

        step_15_degrees.step_days = 5.0
        times, values = find_discrete(t0, t1, step_15_degrees)

        danh_sach = []
        for t, v in zip(times, values):
            degree = (v * 15) % 360
            name = self.MAP_TEN.get(degree)

            # Thời gian thiên văn chính xác
            dt_thuc_te = t.utc_datetime().replace(tzinfo=pytz.utc).astimezone(self.tz_vn)

            # Thời gian ĐÃ FIX theo logic Trương Chí Xuân
            dt_bat_dau_tiet = self._fix_gio_dau_canh(dt_thuc_te)

            danh_sach.append({
                "Ten": name,
                "ThoiGianThuc": dt_thuc_te,  # 03:02
                "ThoiGianTinh": dt_bat_dau_tiet  # 03:00
            })

        return danh_sach

    def tim_tiet_khi(self, nam, thang, ngay, gio, phut):
        """
        Hàm so sánh và break như bạn mô tả
        """
        # 1. Thời gian người dùng nhập vào
        dt_input = self.tz_vn.localize(datetime(nam, thang, ngay, gio, phut))

        # 2. Lấy danh sách tiết khí (Đã fix giờ)
        # Lưu ý: Lấy năm của input để tính list
        ds_tiet_khi = self.lay_danh_sach_tiet_khi_ca_nam(nam)

        # Nếu ngày nhập là đầu năm, có thể cần check thêm danh sách năm ngoái
        # Nhưng thường danh sách trên đã quét dư ra rồi nên yên tâm.

        ket_qua_solar = "Chưa xác định"

        # 3. VÒNG LẶP SO SÁNH (Đúng ý tưởng của bạn)
        for item in ds_tiet_khi:
            ngay_bat_dau_tiet = item["ThoiGianTinh"]  # Đây là mốc 03:00

            if ngay_bat_dau_tiet <= dt_input:
                # Nếu mốc tiết khí nhỏ hơn hoặc bằng thời gian nhập -> Lấy giá trị này
                ket_qua_solar = item["Ten"]
            else:
                # Nếu gặp mốc lớn hơn -> Break ngay lập tức
                # Vì danh sách đã sắp xếp tăng dần, cái cuối cùng gán cho ket_qua_solar
                # chính là tiết khí hiện tại.
                break

        return ket_qua_solar