from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from bot.bot import bot, dp
from bot.handlers import start_command, orders_command, stats_command, stop_command, get_response_keyboard
from database.db import init_db, get_pending_orders, get_stats, increment_stats, get_order, update_order_status, mark_sent
from kwork.kwork_client import KworkClient
from services.order_service import OrderService
from config import Config
import asyncio
import logging


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Состояния для машины состояний
class EditingState(StatesGroup):
    editing = State()


async def check_new_orders():
    """Проверка новых заказов каждые 30 минут"""
    try:
        # Создаем клиент Kwork
        kwork_client = KworkClient(
            email=Config.KWORK_USERNAME,
            password=Config.KWORK_PASSWORD
        )
        await kwork_client.connect()
        
        # Создаем сервис обработки заказов
        order_service = OrderService(kwork_client)
        
        # Выполняем полный цикл обработки заказов
        result = await order_service.process_new_orders()
        
        print(f"🔍 Проверка завершена:")
        print(f"  - Новых заказов получено: {result['fetched']}")
        print(f"  - Отфильтровано по ключевым словам: {result['filtered']}")
        print(f"  - Ответов сгенерировано: {result['responses_generated']}")
        print(f"  - Ответов отправлено: {result['responses_sent']}")
        
        await kwork_client.disconnect()
        
    except Exception as e:
        logger.error(f"❌ Ошибка проверки заказов: {e}")


async def periodic_check():
    """Периодическая проверка каждые 30 минут"""
    while True:
        await asyncio.sleep(Config.CHECK_INTERVAL)
        await check_new_orders()


async def on_startup():
    """Запуск при старте"""
    # Инициализация базы данных
    await init_db()
    print("✅ База данных подключена")
    
    # Регистрация команд
    commands = [
        {"command": "start", "description": "Запустить бота"},
        {"command": "orders", "description": "Список заказов"},
        {"command": "stats", "description": "Статистика"},
        {"command": "stop", "description": "Остановить мониторинг"},
    ]
    await bot.set_my_commands(commands)
    
    print("✅ Команды зарегистрированы")
    
    # Запуск периодической проверки
    asyncio.create_task(periodic_check())


async def on_shutdown():
    """Очистка при остановке"""
    print("🛑 Бот остановлен")


def register_handlers():
    """Регистрация обработчиков"""
    # Основные команды
    dp.message.register(start_command, Command("start"))
    dp.message.register(orders_command, Command("orders"))
    dp.message.register(stats_command, Command("stats"))
    dp.message.register(stop_command, Command("stop"))


async def main():
    """Основная функция"""
    try:
        await on_startup()
        register_handlers()
        
        print("🤖 Бот запущен!")
        print("Команды:")
        print("  /start - Запустить бота")
        print("  /orders - Список заказов")
        print("  /stats - Статистика")
        print("  /stop - Остановить мониторинг")
        print()
        print("Ожидание сообщений...")
        
        await dp.start_polling(bot)
        
    except KeyboardInterrupt:
        print("🛑 Остановлено пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Фатальная ошибка: {e}")
        import sys
        sys.exit(1)
