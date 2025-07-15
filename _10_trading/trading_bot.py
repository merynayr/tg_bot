from datetime import datetime

from _03_datasets.dataset_manager import DatasetManager
from _04_indicators.ema_calculator import calculate_ema
from _07_management.risk_manager import calculate_atr, calculate_position_size_by_risk
from _01_sources.bybit_client import get_last_closed_pnl, session, get_balance, place_order, close_position
from _00_config import config
from _07_management.state_manager import load_state, save_state
from _07_management.logger import log

# === Глобальные переменные состояния ===
trades_today = 0
last_trade_day = None
initial_balance = None
martingale_multiplier = 1.0
last_trade_result = None
current_position = None
entry_price = None
max_price = 0
min_price = 1e10
trailing_active = False

# === Загрузка состояния из файла ===
state = load_state()
trades_today = state.get("trades_today", trades_today)
last_trade_day = state.get("last_trade_day", last_trade_day)
initial_balance = state.get("initial_balance", initial_balance)
martingale_multiplier = state.get("martingale_multiplier", martingale_multiplier)
last_trade_result = state.get("last_trade_result", last_trade_result)
current_position = state.get("current_position", current_position)
entry_price = state.get("entry_price", entry_price)
max_price = state.get("max_price", max_price)
min_price = state.get("min_price", min_price)
trailing_active = state.get("trailing_active", trailing_active)


def run_trading_bot():
    global trades_today, last_trade_day, initial_balance, martingale_multiplier
    global last_trade_result, current_position, entry_price
    global max_price, min_price, trailing_active

    now = datetime.now()
    if last_trade_day != now.date():
        trades_today = 0
        last_trade_day = now.date()

    if trades_today >= config.MAX_TRADES_PER_DAY:
        log.info("🚫 Превышен лимит сделок на день")
        return

    balance = get_balance(coin="USDT")
    if initial_balance is None:
        initial_balance = balance

    drawdown = 100 * (1 - balance / initial_balance)
    if drawdown >= config.MAX_DRAWDOWN_PERCENT:
        log.info(f"🚫 Максимальная просадка достигнута: {drawdown:.2f}%")
        return

    log.info(f"Баланс: {balance:.2f} USDT")

    dm = DatasetManager(config.TRADING_PAIR, config.TIMEFRAME)
    dm.refresh_data()
    df = dm.get_latest_data(100)

    df = calculate_ema(df, period=config.EMA_PERIOD)
    df["ATR"] = calculate_atr(df, config.ATR_PERIOD)

    ema_column = f"EMA_{config.EMA_PERIOD}"
    if ema_column not in df.columns or df[ema_column].isna().all():
        log.warning("❗ EMA колонка отсутствует или пуста")
        return

    ema = df[ema_column].iloc[-1]
    atr = df["ATR"].iloc[-1]
    close = df["close"].iloc[-1]

    bullish = close > ema
    bearish = close < ema
    support = df["close"].rolling(window=20).min().iloc[-1]
    resistance = df["close"].rolling(window=20).max().iloc[-1]

    long_condition = bullish and close <= support
    short_condition = bearish and close >= resistance

    # === Управление открытой позицией ===
    if current_position:
        handle_position(close, atr)
        return

    # === Вход в позицию ===
    if long_condition or short_condition:
        risk_amount = balance * (config.RISK_PERCENT / 100)
        position_size = calculate_position_size_by_risk(risk_amount, atr) * martingale_multiplier
        direction = "Long" if long_condition else "Short"
        entry_price = close
        current_position = {
            "side": direction,
            "size": position_size,
            "entry": entry_price
        }
        max_price = close
        min_price = close
        trailing_active = False
        trades_today += 1
        place_order(direction, position_size)
        log.info(f"📈 Открыта позиция: {direction} @ {entry_price:.2f}")
    
    # === Сохраняем состояние ===
    save_state({
        "trades_today": trades_today,
        "last_trade_day": last_trade_day,
        "initial_balance": initial_balance,
        "martingale_multiplier": martingale_multiplier,
        "last_trade_result": last_trade_result,
        "current_position": current_position,
        "entry_price": entry_price,
        "max_price": max_price,
        "min_price": min_price,
        "trailing_active": trailing_active
    })


def handle_position(price, atr):
    global current_position, martingale_multiplier, last_trade_result
    global trailing_active, max_price, min_price

    side = current_position["side"]
    entry = current_position["entry"]
    take_profit = entry * (1 + config.TAKE_PROFIT_PERCENT / 100) if side == "Long" else entry * (1 - config.TAKE_PROFIT_PERCENT / 100)
    trailing_trigger = entry * (1 + config.TRAILING_START / 100) if side == "Long" else entry * (1 - config.TRAILING_START / 100)
    trailing_offset = price * (config.TRAILING_STOP / 100)

    # Обновление max/min
    if side == "Long":
        max_price = max(max_price, price)
        if not trailing_active and price >= trailing_trigger:
            trailing_active = True
        if trailing_active and price <= max_price - trailing_offset:
            close_trade(price, "Trailing Stop Hit")
        elif price >= take_profit:
            close_trade(price, "Take Profit Hit")
    else:
        min_price = min(min_price, price)
        if not trailing_active and price <= trailing_trigger:
            trailing_active = True
        if trailing_active and price >= min_price + trailing_offset:
            close_trade(price, "Trailing Stop Hit")
        elif price <= take_profit:
            close_trade(price, "Take Profit Hit")

def close_trade(price, reason):
    global current_position, martingale_multiplier, last_trade_result

    log.info(f"📉 Закрытие позиции по причине: {reason}")
    close_position()
    result = get_last_closed_pnl()
    last_trade_result = result
    if result < 0:
        martingale_multiplier *= config.MARTINGALE_FACTOR
        log.info(f"❗ Убыток. Увеличение лота до x{martingale_multiplier:.2f}")
    else:
        martingale_multiplier = 1.0
        log.info("✅ Прибыль. Сброс множителя мартингейла.")
    current_position.clear()
