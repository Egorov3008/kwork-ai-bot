import aiosqlite
from config import Config
from typing import List, Optional
from datetime import datetime


class Database:
    """База данных SQLite"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None
    
    async def connect(self):
        """Подключение к базе данных"""
        self.conn = await aiosqlite.connect(self.db_path)
        await self.conn.execute("PRAGMA journal_mode = WAL")
        await self.create_tables()
    
    async def disconnect(self):
        """Отключение от базы данных"""
        if self.conn:
            await self.conn.close()
    
    async def create_tables(self):
        """Создание таблиц"""
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                budget INTEGER NOT NULL,
                description TEXT,
                deadline TEXT,
                category TEXT,
                client_username TEXT,
                status TEXT DEFAULT 'pending',
                draft_response TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                processed_at DATETIME,
                sent_at DATETIME
            )
        """)
        
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_processed INTEGER DEFAULT 0,
                total_sent INTEGER DEFAULT 0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    async def add_order(self, order_data: dict):
        """Добавление заказа"""
        await self.conn.execute("""
            INSERT OR REPLACE INTO orders 
            (order_id, title, budget, description, deadline, category, client_username, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (
            order_data['order_id'],
            order_data['title'],
            order_data['budget'],
            order_data['description'],
            order_data['deadline'],
            order_data['category'],
            order_data['client_username']
        ))
        await self.conn.commit()
    
    async def get_order(self, order_id: str) -> Optional[dict]:
        """Получение заказа"""
        cursor = await self.conn.execute(
            "SELECT * FROM orders WHERE order_id = ?",
            (order_id,)
        )
        row = await cursor.fetchone()
        if row:
            # Преобразуем row в словарь с правильными ключами
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    async def get_pending_orders(self, limit: int = 10) -> List[dict]:
        """Получение ожидающих заказов"""
        cursor = await self.conn.execute(
            "SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = await cursor.fetchall()
        # Преобразуем rows в список словарей с правильными ключами
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    async def update_order_status(self, order_id: str, status: str, draft_response: str = None):
        """Обновление статуса заказа"""
        await self.conn.execute("""
            UPDATE orders 
            SET status = ?, draft_response = ?, processed_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
        """, (status, draft_response, order_id))
        await self.conn.commit()
    
    async def mark_sent(self, order_id: str):
        """Пометка отправленным"""
        await self.conn.execute("""
            UPDATE orders 
            SET status = 'sent', sent_at = CURRENT_TIMESTAMP
            WHERE order_id = ?
        """, (order_id,))
        await self.conn.commit()
    
    async def increment_stats(self):
        """Обновление статистики"""
        await self.conn.execute("""
            UPDATE stats SET 
                total_processed = total_processed + 1,
                last_updated = CURRENT_TIMESTAMP
        """)
        await self.conn.commit()
    
    async def increment_sent_stats(self):
        """Обновление статистики отправленных"""
        await self.conn.execute("""
            UPDATE stats SET 
                total_sent = total_sent + 1,
                last_updated = CURRENT_TIMESTAMP
        """)
        await self.conn.commit()
    
    async def get_stats(self) -> dict:
        """Получение статистики"""
        cursor = await self.conn.execute(
            "SELECT * FROM stats ORDER BY id DESC LIMIT 1"
        )
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return {
            'total_processed': 0,
            'total_sent': 0,
            'last_updated': None
        }
    
    async def get_unsent_orders(self) -> List[dict]:
        """Получение неотправленных заказов"""
        cursor = await self.conn.execute("""
            SELECT * FROM orders 
            WHERE status IN ('pending', 'draft') 
            ORDER BY created_at DESC
        """)
        rows = await cursor.fetchall()
        # Преобразуем rows в список словарей с правильными ключами
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]


# Глобальная база данных
db = Database(Config.DB_PATH)


async def init_db():
    """Инициализация базы данных"""
    await db.connect()


async def get_order(order_id: str) -> Optional[dict]:
    """Получение заказа"""
    return await db.get_order(order_id)


async def get_pending_orders(limit: int = 10) -> List[dict]:
    """Получение ожидающих заказов"""
    return await db.get_pending_orders(limit)


async def update_order_status(order_id: str, status: str, draft_response: str = None):
    """Обновление статуса"""
    await db.update_order_status(order_id, status, draft_response)


async def mark_sent(order_id: str):
    """Пометка отправленным"""
    await db.mark_sent(order_id)


async def get_stats() -> dict:
    """Получение статистики"""
    return await db.get_stats()


async def increment_stats():
    """Обновление статистики"""
    await db.increment_stats()


async def increment_sent_stats():
    """Обновление статистики отправленных"""
    await db.increment_sent_stats()
