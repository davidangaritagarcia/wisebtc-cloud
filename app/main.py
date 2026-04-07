from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.modules.data_module.historical import fetch_historical_candles
from app.modules.data_module.config import ALLOWED_INTERVALS

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="WiseBTC Cloud")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/api/health")
def health():
    return {"ok": True, "service": "wisebtc-cloud"}


@app.get("/api/klines")
def get_klines(
    symbol: str = Query(default="BTCUSDT"),
    interval: str = Query(default="1m"),
    limit: int = Query(default=500, ge=1, le=1000),
):
    try:
        if interval not in ALLOWED_INTERVALS:
            raise HTTPException(
                status_code=400,
                detail=f"Intervalo no permitido. Usa uno de: {sorted(ALLOWED_INTERVALS)}",
            )

        data = fetch_historical_candles(
            symbol=symbol,
            interval=interval,
            limit=limit,
        )

        return data.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
