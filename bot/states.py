from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup


class BotStates(StatesGroup):
    """Состояния бота"""
    waiting_for_order_id = StatesGroup.State()
    editing_response = StatesGroup.State()
    waiting_for_text = StatesGroup.State()


async def start_bot(bot: Bot):
    """Запуск бота"""
    # Регистрация команд
    commands = [
        {"command": "start", "description": "Запустить бота"},
        {"command": "orders", "description": "Список заказов"},
        {"command": "stats", "description": "Статистика"},
        {"command": "stop", "description": "Остановить мониторинг"},
    ]
    
    await bot.set_my_commands(commands)


async def send_message(bot: Bot, chat_id: int, text: str, reply_markup=None):
    """Отправка сообщения"""
    await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup
    )


async def send_media(bot: Bot, chat_id: int, media_url: str, caption: str = None):
    """Отправка медиа"""
    if caption:
        await bot.send_document(
            chat_id=chat_id,
            document=media_url,
            caption=caption
        )
    else:
        await bot.send_document(
            chat_id=chat_id,
            document=media_url
        )
