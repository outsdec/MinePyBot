from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

def shop():
    menu = [
        [   
            InlineKeyboardButton(text="⛏ Шахта", callback_data="shop_mines"),
        ],
        [
            InlineKeyboardButton(text="🔎 Вернуться в меню", callback_data="start")
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu
def shop_mines():
    menu = [
        [   
            InlineKeyboardButton(text="⛏ Деревянная кирка", callback_data="shop_mines_pickaxe"),
        ],
        [
            InlineKeyboardButton(text="🔎 Вернуться в меню", callback_data="start")
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu

def shop_mines_pickaxe_buy():
    menu = [
        [   
            InlineKeyboardButton(text="Купить", callback_data="shop_mines_pickaxe_buy"),
        ],
        [
            InlineKeyboardButton(text="🔎 Вернуться в меню", callback_data="start")
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu