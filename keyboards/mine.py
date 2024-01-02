from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove


def mine(level):
    menu = [
        [
            InlineKeyboardButton(text="Песчаный карьер", callback_data="mine_1"),
        ],
        [
            InlineKeyboardButton(text=f"{'🔒 Каменный лабиринт (2 уровень.)' if level < 2 else 'Каменный лабиринт'}", callback_data="mine_2"),

        ],
        [
            InlineKeyboardButton(text=f"{'🔒 Янтарный путь (3 уровень.)' if level < 2 else 'Янтарный путь'}", callback_data="mine_3"),
        ],
        [
            InlineKeyboardButton(text="💰 Продать добытое", callback_data="all_sale")
        ],
        [
            InlineKeyboardButton(text="🔎 Меню", callback_data="start")
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu


def dig():
    menu = [
        [
            InlineKeyboardButton(text="💰 Продать добытое", callback_data="all_sale")
        ],
        [
            InlineKeyboardButton(text="⛏ Шахта", callback_data="mine"),
            InlineKeyboardButton(text="🔎 Меню", callback_data="start"),
            InlineKeyboardButton(text="🏛 Инвентарь", callback_data="inventory"),
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu


def items(code):
    menu = [
        [
            InlineKeyboardButton(text="Взять в руки", callback_data=f"takeitem_{code}")
        ],
        [
            InlineKeyboardButton(text="⛏ Шахта", callback_data="mine"),
            InlineKeyboardButton(text="🔎 Меню", callback_data="start"),
            InlineKeyboardButton(text="🏛 Инвентарь", callback_data="inventory"),
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu
