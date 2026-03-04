from kwork.client import Kwork
from typing import List, Optional
from pydantic import BaseModel
import asyncio


class Order(BaseModel):
    """Модель заказа"""
    order_id: str
    title: str
    budget: int
    description: str
    deadline: str
    category: str
    client_username: str


class KworkClient:
    """Клиент для работы с Kwork API"""
    
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.api: Optional[Kwork] = None
    
    async def connect(self):
        """Подключение к Kwork"""
        self.api = Kwork(
            email=self.email,
            password=self.password,
            timeout=30.0,
            retry_max_attempts=3
        )
        await self.api.connect()
    
    async def disconnect(self):
        """Отключение от Kwork"""
        if self.api:
            await self.api.close()
    
    async def get_recent_orders(self, hours: int = 24) -> List[Order]:
        """Получение новых заказов за последние N часов"""
        if not self.api:
            await self.connect()
        
        # Получаем заказы через API
        try:
            # Получаем все заказы
            orders_data = await self.api.get_orders()
            
            orders = []
            for order in orders_data:
                orders.append(Order(
                    order_id=str(order.get('id', '')),
                    title=order.get('title', ''),
                    budget=order.get('price', 0),
                    description=order.get('description', ''),
                    deadline=order.get('deadline', ''),
                    category=order.get('category', ''),
                    client_username=order.get('author', {}).get('username', '')
                ))
            
            return orders
            
        except Exception as e:
            print(f"Ошибка получения заказов: {e}")
            return []
    
    async def get_filtered_orders(self, keywords: List[str]) -> List[Order]:
        """Фильтрация заказов по ключевым словам"""
        all_orders = await self.get_recent_orders()
        
        filtered = []
        for order in all_orders:
            # Проверяем соответствие ключевым словам
            text = f"{order.title} {order.description}".lower()
            if any(keyword.lower() in text for keyword in keywords):
                filtered.append(order)
        
        return filtered
    
    async def send_response(self, order_id: str, response: str):
        """Отправка ответа на заказ"""
        if not self.api:
            await self.connect()
        
        try:
            # Отправка ответа
            await self.api.send_response(order_id, response)
        except Exception as e:
            print(f"Ошибка отправки: {e}")
