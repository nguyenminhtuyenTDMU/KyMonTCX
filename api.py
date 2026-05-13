# api.py

from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from kymon_logic import KyMonLapTran

app = FastAPI(title="KyMonTCX API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

km = KyMonLapTran()


@app.get("/")
def root():
    return {
        "name": "KyMonTCX API",
        "usage": "/qimen?y=2026&m=6&d=17&h=8&mi=1"
    }


@app.get("/qimen")
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
    try:
        datetime(y, m, d, h, mi)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Ngày giờ không hợp lệ: {exc}")

    try:
        return km.lap_que(y, m, d, h, mi)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Dữ liệu ngày giờ không hợp lệ: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
