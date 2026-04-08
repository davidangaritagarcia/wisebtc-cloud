from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.modules.data_module.historical import fetch_historical_candles
from app.modules.data_module.config import ALLOWED_INTERVALS

from pathlib import Path
import os

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# App init
app = FastAPI()

# Templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Static (SAFE FOR RENDER)
static_path = BASE_DIR / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# =========================
# ROUTES
# =========================

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/klines")
def get_klines(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 100):
    if interval not in ALLOWED_INTERVALS:
        return {"error": "Invalid interval"}

    data = fetch_historical_candles(symbol=symbol, interval=interval, limit=limit)
    return data

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})