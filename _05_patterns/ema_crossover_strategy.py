import pandas as pd
 
def detect_ema_crossover_signals(df, short_period=9, long_period=21):
    """
    Функция для обнаружения сигналов на основе пересечения EMA.
 
    :param df: DataFrame с рассчитанными EMA (должны быть колонки EMA_short_period и EMA_long_period)
    :param short_period: Период короткой EMA
    :param long_period: Период длинной EMA
    :return: DataFrame с добавленной колонкой 'signal'
    """
    # Названия колонок с EMA
    short_ema_col = f'EMA_{short_period}'
    long_ema_col = f'EMA_{long_period}'
 
    # Инициализация новой колонки 'signal' значениями 0 (нет сигнала)
    df['signal'] = 0
 
    # Логика пересечения EMA:
    # Если короткая EMA была ниже длинной и стала выше — это сигнал на покупку (1)
    # Если короткая EMA была выше длинной и стала ниже — это сигнал на продажу (-1)
 
    for i in range(1, len(df)):
        if df[short_ema_col].iloc[i-1] < df[long_ema_col].iloc[i-1] and df[short_ema_col].iloc[i] > df[long_ema_col].iloc[i]:
            df.iloc[i, df.columns.get_loc("signal")] = 1   # Buy signal
        elif df[short_ema_col].iloc[i-1] > df[long_ema_col].iloc[i-1] and df[short_ema_col].iloc[i] < df[long_ema_col].iloc[i]:
            df.iloc[i, df.columns.get_loc("signal")] = -1
 
    return df
def detect_ema_crossover_signals(df, short_period=9, long_period=21):
    """
    Функция для обнаружения сигналов на основе пересечения EMA.
 
    :param df: DataFrame с рассчитанными EMA (должны быть колонки EMA_short_period и EMA_long_period)
    :param short_period: Период короткой EMA
    :param long_period: Период длинной EMA
    :return: DataFrame с добавленной колонкой 'signal'
    """
    # Названия колонок с EMA
    short_ema_col = f'EMA_{short_period}'
    long_ema_col = f'EMA_{long_period}'

    # Инициализация новой колонки 'signal' значениями 0 (нет сигнала)
    df['signal'] = 0
 
    # Логика пересечения EMA:
    # Если короткая EMA была ниже длинной и стала выше — это сигнал на покупку (1)
    # Если короткая EMA была выше длинной и стала ниже — это сигнал на продажу (-1)
 
    for i in range(1, len(df)):
        if (
            df[short_ema_col].iloc[i - 1] < df[long_ema_col].iloc[i - 1]
            and df[short_ema_col].iloc[i] > df[long_ema_col].iloc[i]
        ):
            df.loc[df.index[i], 'signal'] = 1 # Buy signal
        elif (
            df[short_ema_col].iloc[i - 1] > df[long_ema_col].iloc[i - 1]
            and df[short_ema_col].iloc[i] < df[long_ema_col].iloc[i]
        ):
            df.loc[df.index[i], 'signal'] = -1 # Sell signal

    return df

# Пример использования
if __name__ == "__main__":
    # Загружаем датасет с рассчитанными EMA (см. предыдущий модуль)
    df = pd.read_csv('./_03_datasets/BTCUSDT_15.csv', parse_dates=['timestamp'])
 
    # Предполагаем, что EMA уже добавлены (либо добавить расчёт здесь)
    df = detect_ema_crossover_signals(df, short_period=9, long_period=21)
 
    # Показываем строки, где есть сигналы
    signals = df[df['signal'] != 0]
    print(signals[['timestamp', 'close', 'EMA_9', 'EMA_21', 'signal']])