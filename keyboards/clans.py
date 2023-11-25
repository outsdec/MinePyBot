from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
def clans_list():
    menu = [
        [   
            InlineKeyboardButton(text="🔍Список кланов", callback_data="clans_list"),
        ],
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu