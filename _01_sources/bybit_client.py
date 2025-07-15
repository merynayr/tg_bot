import time
import requests
from pybit.unified_trading import HTTP
from _00_config import config

session = HTTP(
    api_key=config.BYBIT_API_KEY,
    api_secret=config.BYBIT_API_SECRET,
    demo=(config.MODE == "paper")
)

# === Получение исторических свечей ===
def get_ohlcv(symbol, interval, limit=200, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            response = session.get_kline(
                category="linear",
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            return response['result']['list']
        except requests.exceptions.ReadTimeout:
            print(f"[!] Попытка {attempt}/{retries}: таймаут при запросе к API Bybit.")
        except requests.exceptions.RequestException as e:
            print(f"[!] Попытка {attempt}/{retries}: ошибка подключения — {e}")

        if attempt < retries:
            print(f"⏳ Ждем {delay} секунд перед повтором...")
            time.sleep(delay)
        else:
            raise Exception(f"❌ Не удалось получить OHLCV данные после {retries} попыток.")

# === Получение баланса ===
def get_balance(coin="USDT"):
    result = session.get_wallet_balance(accountType="UNIFIED", coin=coin)
    if isinstance(result, tuple):
        result = result[0]
    result_data = result.get('result', {})
    lists = result_data.get('list', [])
    if not lists:
        return 0.0
    coins = lists[0].get('coin', [])
    for c in coins:
        if c.get('coin') == coin:
            return float(c.get('walletBalance', 0.0))
    return 0.0

# === Получение последнего результата сделки ===
def get_last_closed_pnl(symbol: str = config.TRADING_PAIR):
    if config.MODE == "paper":
        print("[Paper] Симулируем результат последней сделки: win")
        return 10.0  # Можно рандомизировать или задавать вручную
    history = session.get_closed_pnl(
        category="linear",
        symbol=symbol,
        limit=1
    )
    if not history["result"]["list"]:
        return None
    last = history["result"]["list"][0]
    pnl = float(last["closedPnl"])
    return pnl

# === Эмуляция или исполнение ордера ===
def place_order(side, size):
    if config.MODE == "paper":
        print(f"[Paper] Псевдо-открытие позиции: {side} x{size}")
        return
    side_str = "Buy" if side == "Long" else "Sell"
    session.place_order(
        category="linear",
        symbol=config.TRADING_PAIR,
        side=side_str,
        order_type="Market",
        qty=size,
        time_in_force="GoodTillCancel"
    )

def close_position():
    if config.MODE == "paper":
        print("[Paper] Псевдо-закрытие позиции")
        return
    session.set_trading_stop(
        category="linear",
        symbol=config.TRADING_PAIR,
        stop_loss=None,
        take_profit=None,
        trailing_stop=None
    )
    session.place_order(
        category="linear",
        symbol=config.TRADING_PAIR,
        side="Sell",  # по умолчанию закрытие long
        order_type="Market",
        qty=1,  # TODO: можно передавать точный объём позиции
        reduce_only=True,
        time_in_force="GoodTillCancel"
    )

# === Пример использования ===
if __name__ == "__main__":
    data = get_ohlcv(config.TRADING_PAIR, config.TIMEFRAME)
    print(data[:2])
