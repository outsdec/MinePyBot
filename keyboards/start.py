from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="⛏ Шахта")
    kb.button(text="👤 Персонаж")
    kb.button(text="🏛 Инвентарь")
    kb.button(text="🏪 Магазин")
    kb.button(text="🛍 Аукцион")
    kb.button(text="🤴 Таблица лидеров")
    kb.button(text="🔖 Квесты")
    kb.button(text="Сундуки")
    kb.button(text="🏛 Клан")
    kb.button(text="Донат")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
