import pickle
import os

STATE_FILE = "bot_state.pkl"

def save_state(state: dict):
    try:
        with open(STATE_FILE, "wb") as f:
            pickle.dump(state, f)
    except Exception as e:
        print(f"Ошибка при сохранении состояния: {e}")

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке состояния: {e}")
            return {}
    return {}
