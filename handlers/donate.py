from aiogram import Bot
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery
from yookassa import Configuration

router = Router()  # [1]

@router.message(Command("donate"))  # [2]
async def buy(message: types.Message, bot: Bot):
    print("donate")
