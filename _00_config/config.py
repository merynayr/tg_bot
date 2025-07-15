# === API ===
BYBIT_API_KEY = "AeGsfCeKwx0AQyVsmH"
BYBIT_API_SECRET = "D2ZmO0nyxJnvg0fCdiP7HJIDqP5zZd2znnOn"

# === Общие параметры ===
TRADING_PAIR = "BTCUSDT"
TIMEFRAME = "15m"
MODE = "paper"  # "paper" или "live"

# === Пути ===
DATA_PATH = "./_03_datasets/"
LOG_PATH = "./logs/"

# === Индикаторы ===
EMA_PERIOD = 200
ATR_PERIOD = 14

# === Риск и мани-менеджмент ===
RISK_PERCENT = 1.0                 # Риск на сделку (%)
MARTINGALE_FACTOR = 1.3            # Множитель мартингейла
MAX_DRAWDOWN_PERCENT = 10.0        # Максимальная просадка (%)
MAX_TRADES_PER_DAY = 3             # Максимум сделок в день

# === Уровни выхода ===
TAKE_PROFIT_PERCENT = 1.5          # Тейк-профит (%)
TRAILING_START = 1.0               # Старт трейлинга (%)
TRAILING_STOP = 0.5                # Отступ трейлинга (%)
