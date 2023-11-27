import os

from aiogram import F, Bot
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.start import start
from datetime import datetime
from base.diggers import add_user, find_user, level_up_exp
from utils.number_format import spaces
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import InputFile, FSInputFile

bot = Bot(token="6380980028:AAF80OnPKPfoPdoo_HE9mUcxs0s1ddnY-w0")

router = Router()  # [1]


@router.message(F.text == '👤 Персонаж')
@router.message(Command("profile"))
async def profilebutton(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await add_user(user_id)
    user = await find_user(user_id)
    hp = user['health']
    blocks = user['stats_blocks']
    text = (
        f"🤖 Ваш персонаж:\n\n"
        f"👀 Игровой ник: {(user['nickname'])}\n"
        f"❤️ Количество жизней: [{(hp['now'])}/{(hp['max'])}]\n"
        f"💰 Баланс: {spaces(user['balance'])} монет\n"
        f"Уровень {(user['level'])} ({user['exp']} EXP/{level_up_exp(user['level'] + 1)} EXP)\n\n"
        f"⛏ Выкопано блоков:\n"
        f"  📍 Песок {(blocks['sand'])} шт.\n"
        f"  📍 Кремний {(blocks['silicon'])} шт.\n"
        f"  📍 Заросший камень {(blocks['overgrown_stone'])} шт.\n"
        f"  📍 Гладкий камень {(blocks['smooth_stone'])} шт.\n"
        f"  📍 Смола {(blocks['resin'])} шт.\n"
        f"  📍 Янтарь {(blocks['amber'])} шт.\n"
        f"\n📅 Дата регистрации: {(user['date'])}\n"
    )
    img = Image.open('black.png')
    draw = ImageDraw.Draw(img)
    line1 = ImageFont.truetype("profile.ttf", size=30)
    sz = 1500
    x, y = 90, -80
    # img = img.resize((sz, sz), Image.Resampling.LANCZOS)
    draw.text((100, 170), f'{user["nickname"]}', font=line1, fill=(0, 0, 0, 255))
    draw.text((300, 230), f'Баланс - {user["balance"]} 💰', font=line1, fill=(0, 0, 0, 255))
    draw.text((100, 800), f'Дата регистрации - {user["date"]}', font=line1, fill=(0, 0, 0, 255))
    # отправляем изображение пользователю
    img.save(f'temp/profile_{user_id}.png')
    image_from_pc = FSInputFile(f'temp/profile_{user_id}.png')
    result = await message.answer_photo(
        image_from_pc,
        caption=f'{str(text)}',
        reply_markup=start()
    )
