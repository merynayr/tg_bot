import math
from _00_config import config

def calculate_atr(df, period=14):
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    return df['TR'].rolling(window=period).mean()

def calculate_position_size_by_risk(balance, atr, price, risk_percent):
    risk_dollars = balance * risk_percent / 100
    sl_distance = atr
    if sl_distance == 0:
        return 0
    return round(risk_dollars / sl_distance, 3)
