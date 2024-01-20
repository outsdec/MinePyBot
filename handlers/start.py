from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.deep_linking import create_start_link, decode_payload

from keyboards.start import start
from keyboards.mine import mine

from base.diggers import add_user, find_user

from datetime import datetime
import logging
from config_reader import config

bot = Bot(config.bot_token.get_secret_value())
logging.basicConfig(level=logging.INFO)

router = Router()  # [1]
photo = FSInputFile("prison.jpg")


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    username = message.from_user.username
    user_id = message.from_user.id
    args = command.args
    await message.answer_photo(photo, caption=
        f'🤘 Добро пожаловать в Mine Prison!',
                               reply_markup=start())
    if args:
        payload = decode_payload(args)
        refer = await find_user(payload)
        referall = await find_user(user_id)
        if(refer == referall):
            return
        await find_user(user_id)
        await message.answer(f'Вас пригласил {(refer["nickname"])}')
        await bot.send_message(chat_id=refer["_id"], text=f'Вы успешно пригласили {referall["nickname"]}')