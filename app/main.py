from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.modules.data_module.historical import fetch_historical_candles
from app.modules.data_module.config import ALLOWED_INTERVALS

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# IMPORTANT FIX: rutas absolutas
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/klines")
def klines(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 500):
    if interval not in ALLOWED_INTERVALS:
        return {"error": "invalid interval"}

    data = fetch_historical_candles(symbol, interval, limit)
    return data.model_dump()
