from pathlib import Path

# Base del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[4]

# Carpeta donde guardaremos datos descargados
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
HISTORICAL_DIR = RAW_DIR / "historical"
LIVE_DIR = RAW_DIR / "live"

# Crear carpetas automáticamente
for folder in [DATA_DIR, RAW_DIR, HISTORICAL_DIR, LIVE_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Configuración por defecto
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_INTERVAL = "1m"
DEFAULT_LIMIT = 500

# Intervalos que aceptaremos al inicio
ALLOWED_INTERVALS = {
    "1m",
    "5m",
    "15m",
    "1h",
    "4h",
    "1d",
}

# Binance REST
BINANCE_REST_BASE = "https://api.binance.com"
KLINES_ENDPOINT = "/api/v3/klines"

# Binance WebSocket
BINANCE_WS_BASE = "wss://stream.binance.com:9443/ws"

def get_historical_file(symbol: str, interval: str) -> Path:
    symbol = symbol.upper()
    return HISTORICAL_DIR / f"{symbol}_{interval}.json"

def get_live_file(symbol: str, interval: str) -> Path:
    symbol = symbol.upper()
    return LIVE_DIR / f"{symbol}_{interval}_live.json"
