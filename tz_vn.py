# tz_vn.py
"""
Múi giờ Asia/Ho_Chi_Minh thuần Python — thay pytz cho engine.
pytz bị treo khi nạp trên app Android (Flet), nên engine dùng module này.
Bảng mốc đổi giờ lấy nguyên từ pytz (tzdata); localize() theo đúng thuật toán pytz (is_dst=False).
"""
from bisect import bisect_right
from datetime import datetime, timedelta, timezone

# (thời điểm UTC bắt đầu, độ lệch giây so với UTC)
_TRANSITIONS = [
    (datetime(1, 1, 1), 25620),             # LMT
    (datetime(1906, 6, 30, 16, 53, 30), 25620),
    (datetime(1911, 4, 30, 16, 53, 30), 25200),
    (datetime(1942, 12, 31, 16, 0), 28800),
    (datetime(1945, 3, 14, 15, 0), 32400),
    (datetime(1945, 9, 1, 15, 0), 25200),
    (datetime(1947, 3, 31, 17, 0), 28800),
    (datetime(1955, 6, 30, 17, 0), 25200),
    (datetime(1959, 12, 31, 16, 0), 28800),
    (datetime(1975, 6, 12, 16, 0), 25200),
]
_UTC_TIMES = [t for t, _ in _TRANSITIONS]
_TZS = {off: timezone(timedelta(seconds=off)) for _, off in _TRANSITIONS}


def _offset_at_utc(utc_naive):
    return _TRANSITIONS[bisect_right(_UTC_TIMES, utc_naive) - 1][1]


class _VietNam:
    zone = "Asia/Ho_Chi_Minh"

    def localize(self, dt):
        """Gắn múi giờ VN cho datetime naive (giờ địa phương), như pytz.timezone(...).localize(dt)."""
        if dt.tzinfo is not None:
            raise ValueError("Not naive datetime (tzinfo is already set)")
        # Thử độ lệch của mốc gần (dt ± 1 ngày), giữ độ lệch nào cho lại đúng giờ địa phương
        hop_le = set()
        for delta in (timedelta(days=-1), timedelta(days=1)):
            off = _offset_at_utc(dt + delta)
            utc = dt - timedelta(seconds=off)
            if utc + timedelta(seconds=_offset_at_utc(utc)) == dt:
                hop_le.add((utc, off))
        if not hop_le:
            # giờ rơi vào khoảng bị nhảy qua: như pytz, lùi 6 tiếng rồi cộng lại (giữ độ lệch cũ)
            return self.localize(dt - timedelta(hours=6)) + timedelta(hours=6)
        # giờ bị lặp: pytz (is_dst=False) chọn thời điểm UTC muộn nhất
        _, off = max(hop_le)
        return dt.replace(tzinfo=_TZS[off])

    def fromutc_aware(self, dt):
        """Đổi datetime có múi giờ bất kỳ sang giờ VN, như dt.astimezone(pytz_tz)."""
        utc = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt.astimezone(_TZS[_offset_at_utc(utc)])


TZ_VN = _VietNam()


def now():
    """Giờ hiện tại theo giờ Việt Nam."""
    return TZ_VN.fromutc_aware(datetime.now(timezone.utc))
