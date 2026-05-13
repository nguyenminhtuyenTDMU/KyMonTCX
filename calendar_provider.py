from datetime import datetime
from functools import lru_cache
from pathlib import Path
import json

import pytz

from am_lich_vn import AmLichVN


class CachedCalendarProvider:
    def __init__(self, cache_path=None):
        self.cache_path = Path(cache_path or Path(__file__).parent / "data" / "tiet_khi_cache.json")
        self.tz_vn = pytz.timezone("Asia/Ho_Chi_Minh")
        self.CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        self.CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]
        self._cache = self._load_cache()
        self._dynamic = None

    def _load_cache(self):
        if not self.cache_path.exists():
            return {"years": {}, "dates": {}}
        with self.cache_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "years": data.get("years", {}),
            "dates": data.get("dates", {}),
        }

    @property
    def dynamic(self):
        if self._dynamic is None:
            self._dynamic = AmLichVN()
        return self._dynamic

    def _parse_dt(self, value):
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            return self.tz_vn.localize(dt)
        return dt.astimezone(self.tz_vn)

    def _parse_tiet_item(self, item):
        return {
            "Ten": item["Ten"],
            "ThoiGianThuc": self._parse_dt(item["ThoiGianThuc"]),
            "ThoiGianTinh": self._parse_dt(item["ThoiGianTinh"]),
        }

    @lru_cache(maxsize=256)
    def lay_danh_sach_tiet_khi_ca_nam(self, year):
        year_key = str(year)
        year_data = self._cache.get("years", {}).get(year_key)
        if year_data and year_data.get("tiet_khi"):
            return [self._parse_tiet_item(item) for item in year_data["tiet_khi"]]
        return self.dynamic.lay_danh_sach_tiet_khi_ca_nam(year)

    @lru_cache(maxsize=200000)
    def tim_tiet_khi(self, nam, thang, ngay, gio, phut):
        dt_input = self.tz_vn.localize(datetime(nam, thang, ngay, gio, phut))
        ds_tiet_khi = self.lay_danh_sach_tiet_khi_ca_nam(nam)
        ket_qua_solar = "Chưa xác định"

        for item in ds_tiet_khi:
            if item["ThoiGianTinh"] <= dt_input:
                ket_qua_solar = item["Ten"]
            else:
                break

        return ket_qua_solar

    @lru_cache(maxsize=200000)
    def get_lunar_date(self, dd, mm, yy):
        date_key = f"{yy:04d}-{mm:02d}-{dd:02d}"
        date_data = self._cache.get("dates", {}).get(date_key)
        if date_data:
            return (
                date_data["lunar_day"],
                date_data["lunar_month"],
                date_data["lunar_year"],
                date_data["is_leap_month"],
            )
        return self.dynamic.get_lunar_date(dd, mm, yy)

    def get_can_chi(self, dd, mm, yy, lunar_month, lunar_year, hour=0):
        can_nam = self.CAN[(lunar_year + 6) % 10]
        chi_nam = self.CHI[(lunar_year + 8) % 12]

        can_thang_idx = (lunar_year * 12 + lunar_month + 3) % 10
        can_thang = self.CAN[can_thang_idx]
        chi_thang = self.CHI[(lunar_month + 1) % 12]

        a = (14 - mm) // 12
        y = yy + 4800 - a
        m = mm + 12 * a - 3
        jdn = dd + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045

        can_ngay_idx = (jdn + 9) % 10
        chi_ngay_idx = (jdn + 1) % 12
        can_ngay = self.CAN[can_ngay_idx]
        chi_ngay = self.CHI[chi_ngay_idx]

        chi_gio_idx = ((hour + 1) // 2) % 12
        can_gio_idx = ((can_ngay_idx % 5) * 2 + chi_gio_idx) % 10

        return {
            "Nam": f"{can_nam} {chi_nam}",
            "Thang": f"{can_thang} {chi_thang}",
            "Ngay": f"{can_ngay} {chi_ngay}",
            "Gio": f"{self.CAN[can_gio_idx]} {self.CHI[chi_gio_idx]}",
        }
