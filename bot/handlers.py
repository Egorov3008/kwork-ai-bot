from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.bot import dp
from database.db import update_order_status, get_order, get_pending_orders, get_stats
from ai.generator import generate_ai_response
import asyncio

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
    )

async def orders_command(message: Message):
    """Команда /orders"""
    pending = await get_pending_orders(limit=5)
    
    if not pending:
        await message.answer("📭 Нет активных заказов")
        return
    
    text = "📋 Активные заказы:\n\n"
    for order in pending:
        text += f"🔹 {order['title']}\n"
        text += f"💰 {order['budget']}₽\n"
        text += f"📝 {order['description'][:100]}...\n\n"
    
    await message.answer(text[:4096])

async def stats_command(message: Message):
    """Команда /stats"""
    stats = await get_stats()
    
    text = "📊 Статистика:\n\n"
    text += f"✅ Всего заказов обработано: {stats['total_processed']}\n"
    text += f"✅ Ответов отправлено: {stats['total_sent']}\n"
    if stats['last_updated']:
        text += f"🕐 Последнее обновление: {stats['last_updated']}\n"
    
    await message.answer(text)

async def stop_command(message: Message):
    """Команда /stop"""
    await message.answer("🛑 Мониторинг остановлен")

def get_response_keyboard(order_id: str):
    """Клавиатура для ответа"""
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
