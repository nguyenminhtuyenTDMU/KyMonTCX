# api.py

from copy import deepcopy
from datetime import datetime, timedelta
from functools import lru_cache
from os import getenv
from time import perf_counter

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from kymon_logic import KyMonLapTran

api_base_url = getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

app = FastAPI(
    title="KyMonTCX API",
    version="1.0.0",
    servers=[{"url": api_base_url}],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

km = KyMonLapTran()


@lru_cache(maxsize=2048)
def cached_lap_que(y: int, m: int, d: int, h: int, mi: int):
    return km.lap_que(y, m, d, h, mi)


def validate_datetime(y: int, m: int, d: int, h: int, mi: int):
    try:
        return datetime(y, m, d, h, mi)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Ngày giờ không hợp lệ: {exc}")


def parse_iso_datetime(value: str, name: str):
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"{name} không phải ISO datetime hợp lệ: {exc}")


@app.get("/")
def root():
    return {
        "name": "KyMonTCX API",
        "usage": "/qimen?y=2026&m=6&d=17&h=8&mi=1"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/qimen", operation_id="lapTranKyMon")
def qimen(
    y: int = Query(..., ge=1900, le=2100),
    m: int = Query(..., ge=1, le=12),
    d: int = Query(..., ge=1, le=31),
    h: int = Query(..., ge=0, le=23),
    mi: int = Query(0, ge=0, le=59),
):
    """
    Ví dụ:
    /qimen?y=2026&m=6&d=17&h=8&mi=1
    """
    validate_datetime(y, m, d, h, mi)

    start_time = perf_counter()
    try:
        result = deepcopy(cached_lap_que(y, m, d, h, mi))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Dữ liệu ngày giờ không hợp lệ: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    result["_meta"] = {"elapsed_seconds": perf_counter() - start_time}
    return result


@app.get("/qimen/range", operation_id="lapTranKyMonRange")
def qimen_range(
    start: str = Query(..., description="ISO datetime, ví dụ 2026-06-17T07:00"),
    end: str = Query(..., description="ISO datetime, ví dụ 2026-06-17T19:00"),
    step_hours: int = Query(2, ge=1, le=12),
):
    start_dt = parse_iso_datetime(start, "start")
    end_dt = parse_iso_datetime(end, "end")

    if start_dt > end_dt:
        raise HTTPException(status_code=400, detail="start phải nhỏ hơn hoặc bằng end")

    items = []
    current = start_dt
    step = timedelta(hours=step_hours)

    try:
        while current <= end_dt:
            validate_datetime(current.year, current.month, current.day, current.hour, current.minute)
            data = deepcopy(cached_lap_que(current.year, current.month, current.day, current.hour, current.minute))
            items.append({
                "input": current.isoformat(timespec="minutes"),
                "data": data,
            })
            current += step
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Dữ liệu ngày giờ không hợp lệ: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {
        "count": len(items),
        "items": items,
    }
