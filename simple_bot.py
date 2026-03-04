from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.bot import dp
from bot.handlers import (
    start_command,
    orders_command,
    stats_command,
    stop_command
)
from database.db import init_db
import asyncio


async def on_startup():
    """Инициализация при запуске"""
    await init_db()
    print("✅ База данных инициализирована")


async def on_shutdown():
    """Очистка при остановке"""
    print("🛑 Остановка бота...")


async def main():
    """Точка входа"""
    # Инициализация бота
    bot_instance = Bot(token="YOUR_BOT_TOKEN_HERE")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрация хендлеров
    dp.message.register(start_command, commands=["start"])
    dp.message.register(orders_command, commands=["orders"])
    dp.message.register(stats_command, commands=["stats"])
    dp.message.register(stop_command, commands=["stop"])
    
    # Запуск
    print("🤖 Telegram Kwork AI Bot запущен!")
    print("Команды:")
    print("  /start - Запустить бота")
    print("  /orders - Список заказов")
    print("  /stats - Статистика")
    print("  /stop - Остановить")
    
    await dp.start_polling(bot_instance)


if __name__ == "__main__":
    asyncio.run(main())
