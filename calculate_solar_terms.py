from skyfield.api import load
from skyfield.framelib import ecliptic_frame
from skyfield.searchlib import find_discrete
import pytz


def calculate_solar_terms(year):
    # 1. Tải dữ liệu thiên văn (Ephemeris)
    ts = load.timescale()
    try:
        planets = load('de421.bsp')
    except Exception as e:
        print("Đang tải dữ liệu de421.bsp từ NASA (chỉ mất lần đầu)...")
        planets = load('de421.bsp')

    sun = planets['sun']
    earth = planets['earth']

    # 2. Định nghĩa danh sách 24 tiết khí
    solar_terms_map = {
        0: "Xuân Phân", 15: "Thanh Minh", 30: "Cốc Vũ", 45: "Lập Hạ",
        60: "Tiểu Mãn", 75: "Mang Chủng", 90: "Hạ Chí", 105: "Tiểu Thử",
        120: "Đại Thử", 135: "Lập Thu", 150: "Xử Thử", 165: "Bạch Lộ",
        180: "Thu Phân", 195: "Hàn Lộ", 210: "Sương Giáng", 225: "Lập Đông",
        240: "Tiểu Tuyết", 255: "Đại Tuyết", 270: "Đông Chí", 285: "Tiểu Hàn",
        300: "Đại Hàn", 315: "Lập Xuân", 330: "Vũ Thủy", 345: "Kinh Trập"
    }

    # 3. Hàm xác định bước nhảy (Discrete Function)
    # Skyfield sẽ dùng hàm này để dò tìm thời điểm chuyển giao
    def step_15_degrees(t):
        # Tính vị trí biểu kiến (Apparent position) của Mặt trời từ Trái đất
        position = earth.at(t).observe(sun).apparent()
        lat, lon, distance = position.frame_latlon(ecliptic_frame)

        # Trả về số nguyên đại diện cho mỗi "bậc" 15 độ
        return (lon.degrees // 15).astype(int)

    # Thiết lập bước nhảy thời gian ban đầu để dò tìm (giúp chạy nhanh hơn)
    step_15_degrees.step_days = 5.0

    # 4. Thiết lập khoảng thời gian tìm kiếm
    t0 = ts.utc(year, 1, 1)
    t1 = ts.utc(year + 1, 1, 1)

    # 5. Tìm kiếm thời điểm thay đổi tiết khí
    print(f"Đang tính toán tiết khí cho năm {year}...")
    times, values = find_discrete(t0, t1, step_15_degrees)

    # 6. Hiển thị kết quả
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')

    print(f"\n--- LỊCH TIẾT KHÍ NĂM {year} (Múi giờ Việt Nam UTC+7) ---")
    print(f"{'Tiết Khí':<15} | {'Thời gian (Ngày - Giờ : Phút : Giây)':<30} | {'Kinh độ':<10}")
    print("-" * 65)

    for t, v in zip(times, values):
        # v là index của khoảng 15 độ. Nhân 15 để ra độ chính xác của mốc đó.
        # Lưu ý: Do phép chia lấy dư, đôi khi nó trả về mốc bắt đầu của cung tiếp theo
        degree = (v * 15) % 360

        # Chuyển đổi sang giờ Việt Nam
        dt_utc = t.utc_datetime()
        dt_vn = dt_utc.replace(tzinfo=pytz.utc).astimezone(vn_tz)

        name = solar_terms_map.get(degree, f"Góc {degree}°")

        # Format thời gian
        time_str = dt_vn.strftime("%d/%m/%Y - %H:%M:%S")

        print(f"{name:<15} | {time_str:<30} | {degree}°")


# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    calculate_solar_terms(2026)