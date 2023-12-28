from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.deep_linking import create_start_link, decode_payload

from keyboards.start import start
from keyboards.mine import mine

from base.diggers import add_user, find_user

from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

router = Router()  # [1]
photo = FSInputFile("prison.jpg")

#@router.message(CommandStart(deep_link=True))
#async def handler(message: Message, command: CommandObject):
#    args = command.args
#    payload = decode_payload(args)
#    await message.answer(f"Your payload: {payload}")

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    username = message.from_user.username
    user_id = message.from_user.id
    args = command.args
    print(args)
    if not args:
        await find_user(user_id)
        await message.answer_photo(photo, caption=
    f'🤘 Добро пожаловать в Mine Prison!',
                               reply_markup=start())
    else:
        payload = decode_payload(args)
        refer = await find_user(payload)
        referall = await find_user(user_id)
        await find_user(user_id)
        await message.answer_photo(photo, caption=
        f'🤘 Добро пожаловать в Mine Prison!',
                               reply_markup=start())
        await message.answer(f'Вас пригласил {(refer["nickname"])}')
        
    


@router.callback_query(F.data == "start")
async def start_mine(callback: types.CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    await find_user(user_id)
    await callback.message.answer_photo(photo, caption=
    f'🤘 Добро пожаловать в Mine Prison!',
                                        reply_markup=start())
    await callback.answer()
