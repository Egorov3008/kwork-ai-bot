from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from bot.bot import bot, dp
from bot.handlers import start_command, orders_command, stats_command, stop_command, get_response_keyboard
from database.db import init_db, get_pending_orders, get_stats, increment_stats, get_order, update_order_status, mark_sent
from kwork.client import KworkClient
from config import Config
import asyncio


# Состояния для машины состояний
class EditingState(StatesGroup):
    editing = State()


async def check_new_orders():
    """Проверка новых заказов каждые 30 минут"""
    try:
        client = KworkClient(
            username=Config.KWORK_USERNAME,
            password=Config.KWORK_PASSWORD
        )
        await client.connect()
        
        # Получаем заказы
        orders = await client.get_filtered_orders(Config.KEYWORDS)
        
        print(f"🔍 Проверено {len(orders)} новых заказов")
        
        if orders:
            for order in orders:
                # Проверяем есть ли уже в базе
                existing = await get_order(order.order_id)
                
                if not existing:
                    # Добавляем в базу
                    await db.add_order({
                        'order_id': order.order_id,
                        'title': order.title,
                        'budget': order.budget,
                        'description': order.description,
                        'deadline': order.deadline,
                        'category': order.category,
                        'client_username': order.client_username
                    })
                    
                    # Отправляем уведомление пользователю
                    # TODO: Реализовать отправку уведомления
                    
                    print(f"✅ Добавлен заказ: {order.title}")
        
        await client.disconnect()
        await increment_stats()
        
    except Exception as e:
        print(f"❌ Ошибка проверки заказов: {e}")


# Глобальная переменная для клиента
db = None


async def on_startup():
    """Запуск при старте"""
    global db
    from database.db import Database
    
    db = Database(Config.DB_PATH)
    await db.connect()
    
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
    
    # Начало проверки заказов
    asyncio.create_task(check_new_orders())
    
    # Запуск периодической проверки
    asyncio.create_task(periodic_check())


async def periodic_check():
    """Периодическая проверка каждые 30 минут"""
    while True:
        await asyncio.sleep(Config.CHECK_INTERVAL)
        await check_new_orders()


async def on_shutdown():
    """Очистка при остановке"""
    global db
    if db:
        await db.disconnect()
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
