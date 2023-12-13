from aiogram import F, Router, types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
from datetime import datetime
from base.diggers import find_user, user_exp
from base.mines import find_mines
from utils.number_format import spaces_mine
from pymongo import MongoClient
from random import randint
from config_reader import config

client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
miners = db["mines"]

router = Router()  # [1]


@router.callback_query(F.data.startswith('mine_'))
async def minemenu(callback: types.CallbackQuery):
    if callback.data and callback.data.startswith("mine_"):
        code = callback.data[-1:]
        if code.isdigit():
            code = int(code)
        if await find_mines(code) is None:
            await callback.answer(text="Данная шахта ещё в разработке!", show_alert=True)
        else:
            mines = await find_mines(code)
            await callback.message.edit_text(
                f"👀 Шахта: {(mines['name'])}\n\n🗿 Ресурсов в шахте: {spaces_mine(int(mines['resources']))} шт. \n\n🕰 Последнее обновление шахты: {(mines['date']).replace(microsecond=0)}",
                reply_markup=await keyboard(code))
            await callback.answer()


@router.callback_query(F.data.startswith('dig_'))
async def minemenu(callback: types.CallbackQuery):
    if callback.data and callback.data.startswith("dig_"):
        print(callback.data)
        code = callback.data[-1:]
        if code.isdigit():
            code = int(code)
        user_id = callback.from_user.id
        user = await find_user(user_id)
        items = user['inventory']
        chance_attack = randint(1, 100)
        num = randint(1, 100)
        if not items:
            await callback.answer(text="У вас нет предметов в инвентаре!", show_alert=True)
            return callback.answer()
        if (code == 1):
            for item in items:
                if item["type"] == "shovel" and item["status"] == True:
                    mines = await find_mines(code)
                    resource = item["level"]
                    await user_exp(user_id, resource)
                    if chance_attack == 69:
                        await callback.answer(f'Вас пизданула ебанутая ящерица, минус 1 хп.', show_alert = True)
                        users.update_one({'_id': user_id}, {"$inc": {"health.now": -1}})
                    if num < 40:
                        answer = f'⚡️ Вы успешно выкопали {resource} шт. кремния!\n'
                        users.update_one({'_id': user_id},
                                         {"$inc": {"blocks.silicon": resource, "stats_blocks.silicon": resource}})
                    else:
                        answer = f'⚡️ Вы успешно выкопали {resource} шт. песка!\n'
                        users.update_one({'_id': user_id},
                                         {"$inc": {"blocks.sand": resource, "stats_blocks.sand": resource}})
                    miners.update_many({'_id': 1}, {"$inc": {"resources": -resource}})
                    await callback.message.edit_text(
                        f"⛏ Шахта: {mines['name']}\n\n {answer} \n🗿 Ресурсов в шахте {spaces_mine(mines['resources'] - resource)} шт.\n {datetime.now()}",
                        reply_markup=await keyboard(code))
                    await callback.answer()
                    break
            await callback.answer(text="У вас не выбрана лопата для выкапывания!", show_alert=True)

        if (code == 2):
            for item in items:
                if item["type"] == "pickaxe" and item["status"] == True:
                    mines = await find_mines(code)
                    resource = item["level"]
                    await user_exp(user_id, resource)
                    if chance_attack == 69:
                        await callback.answer(f'Вам на голову упал бешенный камень, минус 1 хп.', show_alert = True)
                        users.update_one({'_id': user_id}, {"$inc": {"health.now": -1}})
                    if num < 40:
                        answer = f'⚡️ Вы успешно выкопали {resource} шт. гладкого камня!\n'
                        users.update_one({'_id': user_id}, {
                            "$inc": {"blocks.smooth_stone": resource, "stats_blocks.smooth_stone": resource}})
                    else:
                        answer = f'⚡️ Вы успешно выкопали {resource} шт. заросшего камня!\n'
                        users.update_one({'_id': user_id}, {
                            "$inc": {"blocks.overgrown_stone": resource, "stats_blocks.overgrown_stone": resource}})
                    miners.update_many({'_id': 2}, {"$inc": {"resources": -resource}})
                    await callback.message.edit_text(
                        f"⛏ Шахта: {mines['name']}\n\n {answer} \n🗿 Ресурсов в шахте {spaces_mine(mines['resources'] - resource)} шт.\n {datetime.now()}",
                        reply_markup=await keyboard(code))
                    await callback.answer()
                    return
            await callback.answer(text="У вас не выбрана кирка для выкапывания!", show_alert=True)

        if (code == 3):
            for item in items:
                if item["type"] == "pickaxe" and item["status"] == True:
                    mines = await find_mines(code)
                    resource = item["level"]
                    await user_exp(user_id, resource)
                    if chance_attack == 69:
                        await callback.answer(f'Вы попали в смолу, минус 1 хп.', show_alert = True)
                        users.update_one({'_id': user_id}, {"$inc": {"health.now": -1}})
                    num = randint(1, 100)
                    resource = item["level"]
                    if num < 40:
                        answer = f'⚡️ Вы успешно выкопали {resource} шт. янтаря!\n'
                        users.update_one({'_id': user_id},
                                         {"$inc": {"blocks.amber": resource, "stats_blocks.amber": resource}})
                    else:
                        answer = f'⚡️ Вы успешно выкопали {resource} шт. смолы!\n'
                        users.update_one({'_id': user_id},
                                         {"$inc": {"blocks.resin": resource, "stats_blocks.resin": resource}})
                    miners.update_many({'_id': 3}, {"$inc": {"resources": -resource}})
                    await callback.message.edit_text(
                        f"⛏ Шахта: {mines['name']}\n\n {answer} \n🗿 Ресурсов в шахте {spaces_mine(mines['resources'] - resource)} шт.\n {datetime.now()}",
                        reply_markup=await keyboard(code))
                    await callback.answer()
                    return
            await callback.answer(text="У вас не выбрана кирка для выкапывания!", show_alert=True)


    
@router.callback_query(F.data.startswith('notification'))
async def notification(callback: types.CallbackQuery):
    await callback.answer(text="На данном участке нет ресурсов!", show_alert=True)
    await callback.answer()


async def keyboard(code):
    clickable_buttons = random.sample(range(1, 10), random.randint(1, 3))
    # Создайте клавиатуру с размером 3 на 3 кнопки
    keyboard = InlineKeyboardBuilder()
    # Добавьте все кнопки в клавиатуру
    for button_number in range(1, 10):
        if button_number in clickable_buttons:
            keyboard.add(InlineKeyboardButton(text="⛏", callback_data="dig_" + str(code)))
        else:
            keyboard.add(InlineKeyboardButton(text="📍", callback_data="notification"))
    keyboard.add(InlineKeyboardButton(text='🏛 Инвентарь', callback_data='inventory'))
    keyboard.add(InlineKeyboardButton(text='💰 Продать добытое', callback_data='all_sale'))
    keyboard.add(InlineKeyboardButton(text='⛏ Шахта', callback_data='mine'))
    keyboard.add(InlineKeyboardButton(text='🔎 Меню', callback_data='start'))
    keyboard.adjust(3)
    return keyboard.as_markup()
