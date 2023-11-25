from aiogram import F, Bot
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.shop import shop, shop_mines, shop_mines_pickaxe_buy
from datetime import datetime
from base.diggers import add_user, find_user
from base.stats import botstat

bot = Bot(token="6380980028:AAF80OnPKPfoPdoo_HE9mUcxs0s1ddnY-w0")
from pymongo import MongoClient
client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]
stats = db["stats"]

router = Router()  # [1]

@router.message(Command("shop")) 
async def profilebutton(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    user = await find_user(user_id)
    result = "Добро пожаловать в магазин! \n\n Какой раздел вас интересует?"
    await message.answer(str(result), reply_markup=shop())

@router.message(F.text == '🏪 Магазин')
async def profilebutton(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    user = await find_user(user_id)
    result = "Добро пожаловать в магазин! \n\n Какой раздел вас интересует?"
    await message.answer(str(result), reply_markup=shop())

@router.callback_query(F.data == "shop_mines")
async def shop_mine(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await add_user(user_id)
    user = await find_user(user_id)
    result = "Раздел Шахта"
    await callback.message.answer(str(result), reply_markup= shop_mines())

@router.callback_query(F.data == "shop_mines_pickaxe")
async def shop_mines_pickaxe(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await add_user(user_id)
    user = await find_user(user_id)
    result = "⛏ Деревянная кирка \n Стоимость: 1 монета \n Для покупки нажмите кнопку ниже"
    await callback.message.edit_text(str(result), reply_markup= shop_mines_pickaxe_buy())
    
@router.callback_query(F.data == "shop_mines_pickaxe_buy")
async def shop_mines_pickaxe_buys(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await add_user(user_id)
    user = await find_user(user_id)
    items = user['inventory']
    if check_pickaxe(user_id):
        print(1)
        return callback.message.edit_text(f'У вас уже есть кирка!')
    else:
        if(user["balance"] < 1):
            print(2)
            return callback.message.edit_text(f'Вам не хватает {1 - user["balance"]}')
        print(3)
        stat = await botstat()
        users.update_one({'_id': user_id}, # Условие поиска
            {"$push": {"inventory": { # Объект, который нужно добавить в массив
            "id": int(stat["items"]) + 1,
            "name": "Деревянная кирка",
            "level": 1,
            "type": "pickaxe",
            "status": False
            }}}
            )
        users.update_one({'_id': user_id}, {"$inc": {"balance": -1}})
        result = "⛏ Успешная покупка!"
        await callback.message.edit_text(str(result))

def check_pickaxe(user_id):
    user = users.find_one({"_id": user_id})
    if user is not None:
        if "inventory" in user:
            for item in user["inventory"]:
                if item["type"] == "pickaxe":
                    return True
    return False