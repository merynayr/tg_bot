import pandas as pd
 
def calculate_ema(df, period, column='close'):
    """
    Функция для расчета экспоненциальной скользящей средней (EMA).
 
    :param df: DataFrame с рыночными данными (должен содержать колонку 'close')
    :param period: Период для расчета EMA (например, 9 или 21)
    :param column: Колонка, по которой рассчитывается EMA (по умолчанию 'close')
    :return: DataFrame с добавленной колонкой EMA_{period}
    """
    ema_column_name = f'EMA_{period}'  # Имя новой колонки для хранения значений EMA
 
    # Используем встроенную функцию pandas для расчета EMA
    df[ema_column_name] = df[column].ewm(span=period, adjust=False).mean()
 
    return df
 
# Пример использования
if __name__ == "__main__":
    # Загружаем тестовый датасет (предполагаем, что он уже есть после работы DatasetManager)
    df = pd.read_csv('./_03_datasets/BTCUSDT_15.csv', parse_dates=['timestamp'])

    # Рассчитываем две EMA с разными периодами (например, для стратегии пересечения EMA)
    df = calculate_ema(df, period=9)
    df = calculate_ema(df, period=21)
 
    # Выводим последние 5 строк для проверки результата
    print(df[['timestamp', 'close', 'EMA_9', 'EMA_21']].tail(5))
