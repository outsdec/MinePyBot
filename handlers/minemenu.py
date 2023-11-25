from aiogram import F
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.mine import mine
from datetime import datetime
from base.diggers import add_user, find_user
from base.mines import add_mines

router = Router()  # [1]

@router.message(Command("mine"))
@router.message(F.text == '⛏ Шахта')  # [2]
async def minebutton(message: Message):
    user_id = message.from_user.id
    await add_user(user_id)
    user = await find_user(user_id)
    await message.answer(
        "⛏ Шахта",
        reply_markup=mine()
    )


@router.callback_query(F.data == "mine")
async def start_mine(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await find_user(user_id)
    result = ""
    result += f"⛏ Шахта"
    await callback.message.edit_text(str(result), reply_markup=mine())