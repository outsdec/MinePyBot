import re

from aiogram import F
from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from base.nickname import update_nickname
from base.mines import add_mines
from pymongo import MongoClient
from config_reader import config

client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
router = Router()  # [1]

@router.message(Command("eval"))
async def eval_handler(message: types.Message):
    code = message.text[6:]
    try:
        result = await eval(code)
        print(result)
    except Exception as e:
        print(f"An error occurred while evaluating the command: {e}")
       