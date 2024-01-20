from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.top import top_keyboards

from base.diggers import find_user
from base.top import sort_users_balance, sort_users_by_total_sum

router = Router()  # [1]


@router.message(F.text == '🤴 Таблица лидеров')
@router.message(Command("top"))  # [2]
async def top_command(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await find_user(user_id)
    await message.answer(f'⏏ По какому параметру ты хочешь увидеть топ?', reply_markup = top_keyboards())


@router.callback_query(F.data == "top")
async def top_command(callback: types.CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    await find_user(user_id)
    await callback.message.answer(f'⏏ По какому параметру ты хочешь увидеть топ?', reply_markup = top_keyboards())

@router.callback_query(F.data == "top_balance")
async def top_command(callback: types.CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    await find_user(user_id)
    await callback.message.answer(f'{await sort_users_balance()} ')

@router.callback_query(F.data == "top_digs")
async def top_command(callback: types.CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    await find_user(user_id)
    await callback.message.answer(f'{await sort_users_by_total_sum()} ')
