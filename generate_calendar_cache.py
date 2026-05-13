from argparse import ArgumentParser
from datetime import date, timedelta
from pathlib import Path
import json

from am_lich_vn import AmLichVN


def serialize_dt(dt):
    return dt.isoformat()


def build_cache(start_year, end_year, include_lunar=False):
    lich = AmLichVN()
    cache = {
        "version": 1,
        "range": {"start_year": start_year, "end_year": end_year},
        "years": {},
        "dates": {},
    }

    for year in range(start_year, end_year + 1):
        ds_tiet = lich.lay_danh_sach_tiet_khi_ca_nam(year)
        cache["years"][str(year)] = {
            "tiet_khi": [
                {
                    "Ten": item["Ten"],
                    "ThoiGianThuc": serialize_dt(item["ThoiGianThuc"]),
                    "ThoiGianTinh": serialize_dt(item["ThoiGianTinh"]),
                }
                for item in ds_tiet
            ]
        }
        print(f"Generated solar terms for {year}")

    if include_lunar:
        current = date(start_year, 1, 1)
        end_date = date(end_year, 12, 31)
        while current <= end_date:
            lunar = lich.get_lunar_date(current.day, current.month, current.year)
            if lunar:
                lunar_day, lunar_month, lunar_year, is_leap_month = lunar
                cache["dates"][current.isoformat()] = {
                    "lunar_day": lunar_day,
                    "lunar_month": lunar_month,
                    "lunar_year": lunar_year,
                    "is_leap_month": is_leap_month,
                }
            if current.day == 1:
                print(f"Generated lunar dates through {current:%Y-%m}")
            current += timedelta(days=1)

    return cache


def main():
    parser = ArgumentParser(description="Generate calendar cache for KyMonTCX.")
    parser.add_argument("--start-year", type=int, default=1900)
    parser.add_argument("--end-year", type=int, default=2100)
    parser.add_argument("--output", default="data/tiet_khi_cache.json")
    parser.add_argument("--with-lunar", action="store_true", help="Also precompute lunar dates. This is much slower.")
    args = parser.parse_args()

    cache = build_cache(args.start_year, args.end_year, args.with_lunar)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
