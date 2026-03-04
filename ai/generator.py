from openai import OpenAI
from config import Config
from typing import Optional


class AIResponseGenerator:
    """Генератор ответов через AI (Qwen3.5)"""
    
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = model
    
    async def generate(self, order_title: str, order_desc: str, budget: int) -> str:
        """Генерация ответа"""
        
        prompt = f"""Ты - опытный Python-разработчик с 3+ годами опыта.
Напиши ответ на заказ фрилансера в дружелюбном, профессиональном стиле.

Заказ:
Название: {order_title}
Описание: {order_desc}
Бюджет: {budget}₽

Твои данные:
- Опыт: Python, FastAPI, AIogram, Pyrogram
- Портфолио: github.com/egorov3008
- Цены: разумные,低于 рыночных
- Сроки: всегда соблюдаю

Требования к ответу:
1. Дружелюбное приветствие
2. Упоминание релевантного опыта
3. Предложение цены (на 5-10% ниже рыночной)
4. Упоминание портфолио
5. Призыв к действию ("готов обсудить детали")
6. Коротко и по делу (максимум 150 слов)
7. Без маркдауна, только текст
8. Естественный, человеческий язык

Ответ:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты - опытный Python-разработчик."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Ошибка AI: {e}")
            return self._fallback_response(order_title)
    
    def _fallback_response(self, order_title: str) -> str:
        """Запасной ответ если AI не сработал"""
        return f"""Привет! Вижу ваш заказ на "{order_title}".
Готов выполнить с гарантией качества.
Мои работы: github.com/egorov3008
Цена: договорная.
Готов обсудить детали!"""


async def generate_ai_response(order) -> str:
    """Генерация ответа через AI"""
    generator = AIResponseGenerator(
        api_key=Config.AI_API_KEY,
        model=Config.AI_MODEL
    )
    
    return await generator.generate(
        order_title=order['title'],
        order_desc=order['description'],
        budget=order['budget']
    )
