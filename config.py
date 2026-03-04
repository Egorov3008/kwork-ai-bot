from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация приложения"""
    
    # Telegram
    BOT_TOKEN = "8719309412:AAGC6ydpMdkaj-5KOmv8OunvqEuyA8W1r8I"
    
    # Kwork
    KWORK_USERNAME = "vla.egorow2018@yandex.ru"
    KWORK_PASSWORD = "7188924Ego"
    CHECK_INTERVAL = 1800  # 30 минут
    
    # AI
    AI_MODEL = "openrouter/qwen/qwen3.5-35b-a3b"
    AI_API_KEY = ""  # Заполни если есть API ключ OpenRouter
    AI_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Database
    DB_PATH = "kwork_bot.db"
    
    # Keywords for filtering
    KEYWORDS = [
        "python", "бот", "разработка", "сайт", "парсинг",
        "api", "telegram", "backend", "aiogram", "pyrogram"
    ]
    
    @classmethod
    def validate(cls):
        """Проверка обязательных настроек"""
        errors = []
        if not cls.BOT_TOKEN or cls.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            errors.append("BOT_TOKEN не настроен")
        if not cls.KWORK_USERNAME or cls.KWORK_USERNAME == "YOUR_KWORK_USERNAME":
            errors.append("KWORK_USERNAME не настроен")
        
        if errors:
            raise ValueError("Ошибки конфигурации: " + ", ".join(errors))
