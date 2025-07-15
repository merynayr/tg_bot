import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from _00_config import config
from _04_indicators.ema_calculator import calculate_ema
from _07_management.risk_manager import calculate_atr, calculate_sl_tp

def generate_signals(df):
    df = calculate_ema(df, period=200)
    df['ATR'] = calculate_atr(df, config.ATR_PERIOD)

    df['bullish'] = df['close'] > df['EMA_200']
    df['bearish'] = df['close'] < df['EMA_200']

    df['support'] = df['close'].rolling(window=20).min()
    df['resistance'] = df['close'].rolling(window=20).max()

    df['signal'] = 0
    df.loc[(df['bullish']) & (df['close'] <= df['support']), 'signal'] = 1
    df.loc[(df['bearish']) & (df['close'] >= df['resistance']), 'signal'] = -1

    return df


def run_backtest(df, initial_balance=1000):
    """
    Простой бэктестинг стратегии на основе сигналов (1 = long, -1 = short).
    DataFrame должен содержать колонки: ['timestamp', 'close', 'signal'].
    """
    df = generate_signals(df)
    balance = initial_balance
    position = 0               # 0 = нет позиции, 1 = LONG, -1 = SHORT
    entry_price = 0
    sl = tp = 0                # Уровни стоп-лосса и тейк-профита
    trade_log = []

    for index, row in df.iterrows():
        timestamp = row.get('timestamp', index)  # индекс или поле 'timestamp'
        signal = row['signal']
        price = row['close']

        # --- Открытие позиции ---
        if position == 0 and signal != 0:
            entry_price = price
            sl, tp = calculate_sl_tp(entry_price)
            position = signal
            trade_log.append(f"[{timestamp}] Открыта {'LONG' if signal == 1 else 'SHORT'} по {price:.2f} | SL: {sl:.2f}, TP: {tp:.2f}")

        # --- Проверка закрытия позиции ---
        elif position == 1:
            if price <= sl or price >= tp:
                result = (tp - entry_price) if price >= tp else (sl - entry_price)
                balance += result
                trade_log.append(f"[{timestamp}] Закрыт LONG по {price:.2f} | {'TP' if price >= tp else 'SL'} | Результат: {result:.2f} USDT")
                position = 0

        elif position == -1:
            if price >= sl or price <= tp:
                result = (entry_price - tp) if price <= tp else (entry_price - sl)
                balance += result
                trade_log.append(f"[{timestamp}] Закрыт SHORT по {price:.2f} | {'TP' if price <= tp else 'SL'} | Результат: {result:.2f} USDT")
                position = 0

    trade_log.append(f"\n📊 Финальный баланс: {balance:.2f} USDT")
    return trade_log


if __name__ == "__main__":
    df = pd.read_csv('_08_baktesting/BTCUSDT_60_2024-11-01_2024-11-30.csv', parse_dates=['timestamp'])
    logs = run_backtest(df)
    for line in logs:
        print(line)
