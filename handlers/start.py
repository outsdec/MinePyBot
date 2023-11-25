from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from keyboards.start import start
from keyboards.mine import mine
from datetime import datetime
from base.diggers import add_user, find_user
import logging
logging.basicConfig(level=logging.INFO)

router = Router()  # [1]
photo = FSInputFile("prison.jpg")

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await find_user(user_id)
    await message.answer_photo(photo, caption=
        f'🤘 Добро пожаловать в Mine Prison!',
        reply_markup=start())


@router.callback_query(F.data == "start")
async def start_mine(callback: types.CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    await find_user(user_id)
    await callback.message.answer_photo(photo, caption=
        f'🤘 Добро пожаловать в Mine Prison!',
        reply_markup=start())
    await callback.answer()

