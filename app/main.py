from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.modules.data_module.config import ALLOWED_INTERVALS
from app.modules.data_module.historical import fetch_historical_candles

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(title="WiseBTC Cloud")

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR)) if TEMPLATES_DIR.exists() else None


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/klines")
def get_klines(symbol: str = "BTCUSDT", interval: str = "1m", limit: int = 100):
    try:
        if interval not in ALLOWED_INTERVALS:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "invalid_interval",
                    "allowed": ALLOWED_INTERVALS,
                },
            )

        data = fetch_historical_candles(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

        return {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "data": data,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "klines_failed",
                "detail": str(e),
            },
        )


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    if templates is None:
        return HTMLResponse("<h1>WiseBTC Cloud is running</h1>")
    return templates.TemplateResponse(request, "index.html")
