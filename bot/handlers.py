from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.bot import dp
from database.db import update_order_status, get_order
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
    pending = await get_order("pending")
    
    if not pending:
        await message.answer("📭 Нет активных заказов")
        return
    
    text = "📋 Активные заказы:\n\n"
    for order in pending[:5]:
        text += f"🔹 {order['title']}\n"
        text += f"💰 {order['budget']}₽\n"
        text += f"📝 {order['description'][:100]}...\n\n"
    
    await message.answer(text[:4096])

async def stats_command(message: Message):
    """Команда /stats"""
    text = "📊 Статистика:\n\n"
    text += "✅ Всего заказов обработано: 0\n"
    text += "✅ Ответов отправлено: 0\n"
    text += "⏰ Среднее время ответа: 0 мин\n"
    
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
