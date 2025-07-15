import pandas as pd
from _01_sources.bybit_client import get_ohlcv  # Импорт функции для получения данных с ByBit
from _00_config import config  # Импорт конфигурационных параметров
 
def run_etl():
    # Шаг 1: Извлечение данных с биржи (получаем "сырые" данные в виде списка)
    raw_data = get_ohlcv(config.TRADING_PAIR, config.TIMEFRAME)

    # Шаг 2: Преобразование данных в DataFrame для удобной работы
    df = pd.DataFrame(raw_data, columns=[
        'timestamp',  # Время открытия свечи (в миллисекундах)
        'open',       # Цена открытия
        'high',       # Максимальная цена
        'low',        # Минимальная цена
        'close',      # Цена закрытия
        'volume',     # Объём торгов
        'turnover'    # Дополнительные данные (оборот)
    ])
     
    # Шаг 3: Преобразуем timestamp в читаемый формат даты и времени
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype('int64'), unit='ms')

    # Шаг 4: Приводим числовые данные к типу float для корректных вычислений
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
     
    # Шаг 5: Сортируем данные по времени (на случай, если биржа вернула их неупорядоченными)
    df = df.sort_values('timestamp')
     
    # Шаг 6: Сохраняем итоговый датасет в формате CSV для дальнейшего использования
    df.to_csv(f"{config.DATA_PATH}{config.TRADING_PAIR}_{config.TIMEFRAME}.csv", index=False)
     
    # Сообщаем пользователю о завершении процесса
    print(f"Данные сохранены: {config.DATA_PATH}{config.TRADING_PAIR}_{config.TIMEFRAME}.csv")
 
# Запускаем процесс ETL, если файл выполняется напрямую
if __name__ == "__main__":
    run_etl()