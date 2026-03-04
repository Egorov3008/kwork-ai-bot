from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.bot import dp
from bot.keyboards import get_main_keyboard, get_response_keyboard
from bot.handlers import handle_new_order, handle_edit_response, handle_send_response
from database.db import init_db, get_pending_orders
from ai.generator import generate_ai_response


class ResponseState(StatesGroup):
    editing = State()
    waiting_for_text = State()


async def start_command(message: Message):
    """Команда /start"""
    await message.answer(
        "🤖 Привет! Я бот для автоматической отправки ответов на заказы Kwork.\n\n"
        "📋 Я отслеживаю новые заказы и предлагаю ответы.\n"
        "✨ Ответы генерируются с помощью AI.\n\n"
        "Команды:\n"
        "/start - Запустить бота\n"
        "/orders - Список активных заказов\n"
        "/stats - Статистика\n"
        "/stop - Остановить мониторинг",
        reply_markup=get_main_keyboard()
    )


async def orders_command(message: Message):
    """Команда /orders"""
    pending = await get_pending_orders()
    
    if not pending:
        await message.answer("📭 Нет активных заказов")
        return
    
    text = "📋 Активные заказы:\n\n"
    for order in pending[:5]:  # Показываем первые 5
        text += f"🔹 {order['title']}\n"
        text += f"💰 {order['budget']}₽\n"
        text += f"📝 {order['description'][:100]}...\n\n"
    
    await message.answer(text[:4096])  # Ограничение длины сообщения Telegram


async def stats_command(message: Message):
    """Команда /stats"""
    from database.db import get_stats
    stats = await get_stats()
    
    text = "📊 Статистика:\n\n"
    text += f"✅ Всего заказов обработано: {stats['total_processed']}\n"
    text += f"✅ Ответов отправлено: {stats['sent_responses']}\n"
    text += f"⏰ Среднее время ответа: {stats['avg_time']} мин\n"
    
    await message.answer(text)


async def stop_command(message: Message):
    """Команда /stop"""
    # Остановить мониторинг (реализовать в future)
    await message.answer("🛑 Мониторинг остановлен")


async def on_startup():
    """Запуск бота"""
    await init_db()
    await dp.start_polling(bot)


async def on_shutdown():
    """Остановка бота"""
    await bot.delete_webhook()


def register_handlers():
    """Регистрация хендлеров"""
    # Основные команды
    dp.message.register(start_command, Command("start"))
    dp.message.register(orders_command, Command("orders"))
    dp.message.register(stats_command, Command("stats"))
    dp.message.register(stop_command, Command("stop"))
    
    # Callback кнопки
    dp.callback_query.register(handle_send_response, F.data == "send_response")
    dp.callback_query.register(handle_edit_response, F.data.startswith("edit_"))
    
    # Машина состояний
    dp.message.register(handle_edit_response, ResponseState.waiting_for_text)


def create_main_keyboard():
    """Создание клавиатуры"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои заказы"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )
    return kb


def get_main_keyboard():
    """Главная клавиатура"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Заказы"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )
    return kb


def get_response_keyboard(order_id: str):
    """Клавиатура для ответа на заказ"""
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✏️ Редактировать"),
                KeyboardButton(text="✅ Отправить")
            ],
            [
                KeyboardButton(text="❌ Пропустить"),
                KeyboardButton(text="⏰ Напомнить через 1ч")
            ],
            [
                KeyboardButton(text="⏰ Напомнить через 24ч")
            ]
        ],
        resize_keyboard=True
    )
    return kb
