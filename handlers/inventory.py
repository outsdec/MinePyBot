from aiogram import F
from aiogram import Bot, Router, types
from aiogram.filters import Command, CommandObject
from base.nickname import update_nickname
from base.mines import find_item
from keyboards.mine import items
import html
from pymongo import MongoClient
from datetime import datetime
from utils.number_format import spaces
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]


router = Router()  # [1]
@router.message(Command("add_item"))
async def add_item_command(message: types.Message, bot: Bot):
    user_id = message.from_user.id 
    # Получение данных об игровом предмете от пользователя
    name = "Деревянная лопата"
    level = int(1)
    item_type = "shovel"
    status = False

    # Добавление игрового предмета в базу данных
    item = {
        "name": name,
        "level": level,
        "type": item_type,
        "status": status
    }
    users.update_one({"_id": user_id}, {"$push": {"inventory": item}})

    # Отправка сообщения об успешном добавлении игрового предмета
    response = f"Игровой предмет {name} успешно добавлен в базу данных."
    await bot.send_message(chat_id=message.chat.id, text=response)
    
@router.message(Command("inventory"))
async def inventory_commad(message: types.Message, bot: Bot):
    user_id = message.from_user.id 
    user = users.find_one({"_id": int(user_id)})
    items = user['inventory']
    keyboard = InlineKeyboardBuilder()
    response = "Ваш инвентарь:\n\n"
    # Отправка сообщения с клавиатурой пользователю
    if items:
        for item in items:
            response += f"<b>{item['name']} (ID: {item['id']})</b>\n"
            response += f"Уровень: {item['level']}\n"
            response += f"Тип: {item['type']}\n\n"
            button_text = f"{item['name']} ({item['level']})"
            button_callback = f"item_{item['id']}"
            keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_callback))
        await message.answer(response, reply_markup=keyboard.as_markup(), parse_mode= "HTML")
    else:
        response += "Ваш инвентарь пуст"
        await message.answer(response)

@router.message(F.text == '🏛 Инвентарь')
async def inventory_commad(message: types.Message, bot: Bot):
    user_id = message.from_user.id 
    user = users.find_one({"_id": int(user_id)})
    items = user['inventory']
    keyboard = InlineKeyboardBuilder()
    response = "Ваш инвентарь:\n\n"
    # Отправка сообщения с клавиатурой пользователю
    if items:
        for item in items:
            response += f"<b>{item['name']} (ID: {item['id']})</b>\n"
            response += f"Уровень: {item['level']}\n"
            response += f"Тип: {item['type']}\n\n"
            button_text = f"{item['name']} ({item['level']})"
            button_callback = f"item_{item['id']}"
            keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_callback))
        await message.answer(response, reply_markup=keyboard.as_markup(), parse_mode= "HTML")

@router.callback_query(F.data == "inventory")
async def inventory_commad(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id 
    user = users.find_one({"_id": int(user_id)})
    items = user['inventory']
    keyboard = InlineKeyboardBuilder()
    response = "Ваш инвентарь:\n\n"
    # Отправка сообщения с клавиатурой пользователю
    if items:
        for item in items:
            response += f"<b>{item['name']} (ID: {item['id']})</b>\n"
            response += f"Уровень: {item['level']}\n"
            response += f"Тип: {item['type']}\n\n"
            button_text = f"{item['name']} ({item['level']})"
            button_callback = f"item_{item['id']}"
            keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_callback))
    await callback.message.answer(response, reply_markup=keyboard.as_markup(), parse_mode= "HTML")

@router.callback_query(F.data.startswith('item_'))
async def minemenu(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = users.find_one({"_id": user_id})
    blocks = user['stats_blocks']
    if callback.data and callback.data.startswith("item_"):
        code = callback.data.split("_")[1]
    print(code)
    if code.isdigit():
        code = int(code)
    if await find_item(user_id, code) is None:
         return callback.answer(text="Ошибка!", show_alert= True)
    else:
        item = await find_item(user_id, code)
        conditions = upgrade_shovel_conditions.get(item['level'])
        if blocks['sand'] < conditions['sand']:
            smile_sand = "❌"
        else:
            smile_sand = "✔️"
        
        if blocks['silicon'] < conditions['silicon']:
            smile_silicon = "❌"
        else:
            smile_silicon = "✔️"
        await callback.message.edit_text(f"{item['name']} (ID: {item['id']})\n Уровень: {item['level']} \n\n ⛓ Для улучшения требуется: \n📌 Песок: {blocks['sand']}/{conditions['sand']} шт. {smile_sand}\n📌 Кремний: {blocks['silicon']}/{conditions['silicon']} шт. {smile_silicon}", reply_markup=await item_keyboard(code))
        await callback.answer()

@router.callback_query(F.data.startswith('takeitem_'))
async def minemenu(callback: types.CallbackQuery):
    user_id = callback.from_user.id 
    user = users.find_one({"_id": user_id})
    if callback.data and callback.data.startswith("takeitem_"):
        code = callback.data.split("_")[1]
        if code.isdigit():
            code = int(code)
        if await find_item(user_id, code) is None:
            await callback.answer(text="Ошибка!", show_alert= True)
        else:
            item = await find_item(user_id, code)
            for item in user['inventory']:
                if item['id'] == code:
                    if item["status"] == False:
                        print(item['id'])
                        item['status'] = True
                        users.update_one({"_id": user_id}, {"$set": user})
                        await callback.message.edit_text(f"Успешно взяли предмет! {item['name']} (ID: {item['id']})\n Уровень: {item['level']} \nТип: {item['type']}", reply_markup=await item_keyboard(code))
                        await callback.answer()
                    else:
                        for item in user['inventory']:
                            if item['id'] == code:
                                print(item['id'])
                                item['status'] = False
                                users.update_one({"_id": user_id}, {"$set": user})
                                await callback.message.edit_text(f"Успешно убрали предмет! {item['name']} (ID: {item['id']})\n Уровень: {item['level']} \nТип: {item['type']}", reply_markup=await item_keyboard(code))
                                await callback.answer()

upgrade_shovel_conditions = {
            1: {"sand": 600,
                "silicon": 400},
            2: {"sand": 1200,
                "silicon": 800},
            3: {"sand": 2400,
                "silicon": 1600},
            4: {"sand": 4800,
                "silicon": 3200},
            5: {"sand": 9600,
                "silicon": 6400},
            6: {"sand": 19200,
                "silicon": 12800},
    # Добавьте дополнительные условия для других уровней предмета
}

@router.callback_query(F.data.startswith('upgradeitem_'))
async def minemenu(callback: types.CallbackQuery):
    user_id = callback.from_user.id 
    user = users.find_one({"_id": user_id})
    blocks = user['stats_blocks']
    if callback.data and callback.data.startswith("upgradeitem_"):
        code = callback.data[-1:]
        if code.isdigit():
            code = int(code)
        if await find_item(user_id, code) is None:
            await callback.answer(text="Ошибка!", show_alert= True)
        else:
            item = await find_item(user_id, code)
            for item in user['inventory']:
                if item['id'] == code:
                    current_level = item['level']
                   
                    # Получение условий для текущего уровня
                    conditions = upgrade_shovel_conditions.get(current_level)
                        
                    # Проверка условий для улучшения на основе текущего уровня
                    if conditions['sand'] <= blocks['sand'] and conditions['silicon'] <= blocks['silicon']:
                        item['level'] += 1
                        item['status'] = True
                        users.update_one({"_id": user_id}, {"$set": user})
                        await callback.message.answer("Предмет успешно улучшен!")
                        break
                    else:
                        await callback.message.answer("Не хватает блоков для улучшения", parse_mode= "HTML")

        
async def item_keyboard(code):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='🫳 Взять/Положить', callback_data=f'takeitem_{code}'))
    keyboard.add(InlineKeyboardButton(text='⚡️ Улучшить', callback_data=f'upgradeitem_{code}'))
    keyboard.add(InlineKeyboardButton(text='🏛 Инвентарь', callback_data='inventory'))
    keyboard.add(InlineKeyboardButton(text='⛏ Шахта', callback_data='mine'))
    keyboard.add(InlineKeyboardButton(text='🔎 Меню', callback_data='start'))
    keyboard.adjust(2)
    return keyboard.as_markup()  


