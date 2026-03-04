import random
import string


def generate_random_id(length: int = 10) -> str:
    """Генерация случайного ID"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def truncate(text: str, max_length: int = 500) -> str:
    """Обрезка текста"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_budget(budget: int) -> str:
    """Форматирование бюджета"""
    if budget >= 1000000:
        return f"{budget / 1000000:.1f}M₽"
    elif budget >= 1000:
        return f"{budget / 1000:.1f}K₽"
    return f"{budget}₽"
