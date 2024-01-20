from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def top_keyboards():
    menu = [
        [
            InlineKeyboardButton(text="Топ-10 по балансу 💰", callback_data="top_balance")
        ],
        [
            InlineKeyboardButton(text="Топ-10 по выкопанным блокам ⛏", callback_data="top_digs"),
        ],
        [
            InlineKeyboardButton(text="🔎 Вернуться в меню", callback_data="start")
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu