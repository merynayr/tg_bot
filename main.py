import signal
import threading
from _09_dashboard.dash_dashboard import app
from _10_trading.trading_bot import run_trading_bot
from werkzeug.serving import make_server

# Класс-поток для дашборда
class DashThread(threading.Thread):
    def __init__(self, app):
        super().__init__()
        self.server = make_server("127.0.0.1", 8050, app)
        self.ctx = app.server.app_context()
        self.ctx.push()

    def run(self):
        print("▶️  Дашборд: http://127.0.0.1:8050")
        self.server.serve_forever()

    def shutdown(self):
        print("🛑 Остановка дашборда...")
        self.server.shutdown()

# Поток для бота
bot_thread = threading.Thread(target=run_trading_bot)
bot_thread.daemon = True  # Чтобы завершался при выходе из main

dashboard = DashThread(app)

def shutdown(signum, frame):
    print("\n🔌 Получен сигнал остановки...")
    dashboard.shutdown()
    print("⌛ Ожидание завершения потоков...")
    # Бот — daemon, завершится сам
    dashboard.join()
    print("✅ Завершено.")
    exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

if __name__ == "__main__":
    dashboard.start()
    bot_thread.start()
    bot_thread.join()
