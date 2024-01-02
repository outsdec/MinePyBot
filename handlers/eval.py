from aiogram import F, Bot, Router, types
from aiogram.filters import Command, CommandObject

from base.nickname import update_nickname
from base.mines import add_mines

from config_reader import config

from pymongo import MongoClient
client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
router = Router()  # [1]

@router.message(Command("eval"))
async def eval_handler(message: types.Message):
    code = message.text[6:]
    print(code)
    try:
        result = eval(code)
        await message.answer(f'Команда выполнена {(result)}')
        print(result)
    except Exception as e:
        print(f"An error occurred while evaluating the command: {e}")
       