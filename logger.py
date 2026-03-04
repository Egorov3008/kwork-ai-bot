from pathlib import Path

# Путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent

# Путь к логам
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
