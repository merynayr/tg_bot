import pandas as pd
import os
from _00_config import config
from _02_etl import etl_processor  # Импортируем ETL для обновления данных
 
class DatasetManager:
    def __init__(self, symbol, timeframe):
        """
        Инициализация менеджера датасетов с указанием торговой пары и таймфрейма.
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.file_path = f"{config.DATA_PATH}{symbol}_{timeframe}.csv"
        self.data = None  # Здесь будет храниться DataFrame с данными
 
    def load_data(self):
        """
        Загружаем датасет из CSV-файла.
        Если файл отсутствует — запускаем ETL для его создания.
        """
        if not os.path.exists(self.file_path):
            print("Датасет не найден. Запуск ETL для получения данных...")
            etl_processor.run_etl()
 
        # Чтение данных из CSV в DataFrame
        self.data = pd.read_csv(self.file_path, parse_dates=['timestamp'])
        print(f"Данные успешно загружены: {self.file_path}")
 
    def get_latest_data(self, n=50):
        """
        Возвращает последние n свечей из датасета.
        """
        if self.data is None:
            self.load_data()
        return self.data.tail(n).copy()
 
    def refresh_data(self):
        """
        Обновление датасета (перезапуск ETL).
        """
        print("Обновляем данные...")
        etl_processor.run_etl()
        self.load_data()
 
# Пример использования
if __name__ == "__main__":
    dm = DatasetManager(config.TRADING_PAIR, config.TIMEFRAME)
    dm.load_data()  # Загружаем данные
    print(dm.get_latest_data(5))  # Показываем последние 5 свечей