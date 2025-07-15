import logging
import os
from datetime import datetime

# Создание папки logs, если её нет
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Имя лог-файла по дате
log_filename = datetime.now().strftime("trading_%Y-%m-%d.log")
log_path = os.path.join(LOG_DIR, log_filename)

# Настройка логгера
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Общий логгер для всего проекта
log = logging.getLogger("trading_bot")
