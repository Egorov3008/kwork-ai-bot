"""Сервис для обработки заказов Kwork"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import logging

from kwork.kwork_client import KworkClient, Order
from database.db import (
    add_order, get_order, get_pending_orders, update_order_status, 
    mark_sent, get_stats, increment_stats, increment_sent_stats,
    get_unsent_orders
)
from ai.generator import generate_ai_response
from config import Config


logger = logging.getLogger(__name__)


class OrderService:
    """Сервис для управления заказами Kwork"""
    
    def __init__(self, kwork_client: KworkClient):
        self.kwork_client = kwork_client
        
    async def fetch_and_store_orders(self) -> List[Dict]:
        """Получение и сохранение новых заказов"""
        logger.info("Получение новых заказов...")
        
        try:
            # Получаем заказы из Kwork
            orders = await self.kwork_client.get_recent_orders()
            
            stored_orders = []
            for order in orders:
                # Сохраняем заказ в базу данных
                order_data = {
                    'order_id': order.order_id,
                    'title': order.title,
                    'budget': order.budget,
                    'description': order.description,
                    'deadline': order.deadline,
                    'category': order.category,
                    'client_username': order.client_username
                }
                
                await add_order(order_data)
                stored_orders.append(order_data)
                
                logger.info(f"Заказ {order.order_id} сохранен: {order.title}")
            
            logger.info(f"Получено и сохранено {len(stored_orders)} заказов")
            return stored_orders
            
        except Exception as e:
            logger.error(f"Ошибка при получении заказов: {e}")
            return []
    
    async def filter_orders_by_keywords(self, keywords: List[str]) -> List[Dict]:
        """Фильтрация заказов по ключевым словам"""
        logger.info(f"Фильтрация заказов по ключевым словам: {keywords}")
        
        try:
            # Получаем все заказы из базы
            pending_orders = await get_pending_orders(limit=50)  # Увеличиваем лимит для фильтрации
            
            filtered_orders = []
            for order in pending_orders:
                # Проверяем соответствие ключевым словам
                text = f"{order['title']} {order['description']}".lower()
                if any(keyword.lower() in text for keyword in keywords):
                    filtered_orders.append(order)
                    
            logger.info(f"Найдено {len(filtered_orders)} подходящих заказов")
            return filtered_orders
            
        except Exception as e:
            logger.error(f"Ошибка при фильтрации заказов: {e}")
            return []
    
    async def generate_responses_for_orders(self, orders: List[Dict]) -> List[Dict]:
        """Генерация AI-ответов для заказов"""
        logger.info(f"Генерация ответов для {len(orders)} заказов")
        
        responses = []
        for order in orders:
            try:
                # Генерируем ответ с помощью AI
                prompt = f"""
                Заказ: {order['title']}
                Описание: {order['description']}
                Бюджет: {order['budget']} руб.
                
                Напиши профессиональный, дружелюбный и убедительный ответ для этого заказа.
                Ответ должен быть коротким, но информативным.
                """
                
                response_text = await generate_ai_response(prompt)
                
                response_data = {
                    'order_id': order['order_id'],
                    'response': response_text,
                    'generated_at': datetime.now().isoformat()
                }
                
                # Обновляем статус заказа в базе
                await update_order_status(
                    order['order_id'], 
                    'draft', 
                    response_text
                )
                
                # Обновляем статистику
                await increment_stats()
                
                responses.append(response_data)
                logger.info(f"Ответ сгенерирован для заказа {order['order_id']}")
                
            except Exception as e:
                logger.error(f"Ошибка при генерации ответа для заказа {order['order_id']}: {e}")
                
                # Отмечаем заказ как ошибочный
                await update_order_status(order['order_id'], 'error')
        
        return responses
    
    async def send_response_to_kwork(self, order_id: str, response: str) -> bool:
        """Отправка ответа на Kwork"""
        logger.info(f"Отправка ответа для заказа {order_id}")
        
        try:
            # Отправляем ответ через Kwork клиент
            await self.kwork_client.send_response(order_id, response)
            
            # Обновляем статус заказа в базе
            await mark_sent(order_id)
            
            # Обновляем статистику отправленных
            await increment_sent_stats()
            
            logger.info(f"Ответ успешно отправлен для заказа {order_id}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при отправке ответа для заказа {order_id}: {e}")
            return False
    
    async def process_new_orders(self) -> Dict[str, Any]:
        """Полный цикл обработки новых заказов"""
        logger.info("Начало полного цикла обработки новых заказов")
        
        # Шаг 1: Получаем новые заказы
        new_orders = await self.fetch_and_store_orders()
        
        if not new_orders:
            logger.info("Новых заказов нет")
            return {
                'fetched': 0,
                'filtered': 0,
                'responses_generated': 0,
                'responses_sent': 0
            }
        
        # Шаг 2: Фильтруем заказы по ключевым словам
        filtered_orders = await self.filter_orders_by_keywords(Config.KEYWORDS)
        
        # Шаг 3: Генерируем ответы для отфильтрованных заказов
        responses = await self.generate_responses_for_orders(filtered_orders)
        
        # Шаг 4: Отправляем ответы на Kwork
        sent_count = 0
        for response in responses:
            success = await self.send_response_to_kwork(
                response['order_id'], 
                response['response']
            )
            if success:
                sent_count += 1
        
        logger.info(f"Цикл обработки завершен: {len(new_orders)} получено, "
                   f"{len(filtered_orders)} отфильтровано, "
                   f"{len(responses)} ответов сгенерировано, "
                   f"{sent_count} отправлено")
        
        return {
            'fetched': len(new_orders),
            'filtered': len(filtered_orders),
            'responses_generated': len(responses),
            'responses_sent': sent_count
        }
    
    async def get_unsent_orders_list(self) -> List[Dict]:
        """Получение списка неотправленных заказов"""
        logger.info("Получение списка неотправленных заказов")
        
        try:
            unsent_orders = await get_unsent_orders()
            logger.info(f"Найдено {len(unsent_orders)} неотправленных заказов")
            return unsent_orders
        except Exception as e:
            logger.error(f"Ошибка при получении неотправленных заказов: {e}")
            return []
    
    async def resend_failed_orders(self) -> int:
        """Повторная отправка неотправленных заказов"""
        logger.info("Повторная отправка неотправленных заказов")
        
        unsent_orders = await self.get_unsent_orders_list()
        sent_count = 0
        
        for order in unsent_orders:
            if order['status'] in ['draft', 'pending']:
                try:
                    # Пробуем отправить ответ снова
                    success = await self.send_response_to_kwork(
                        order['order_id'],
                        order['draft_response']
                    )
                    if success:
                        sent_count += 1
                except Exception as e:
                    logger.error(f"Ошибка при повторной отправке заказа {order['order_id']}: {e}")
        
        logger.info(f"Повторно отправлено {sent_count} заказов")
        return sent_count