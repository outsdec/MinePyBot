from aiogram import F, Bot, Router, types
from aiogram.filters import Command, CommandObject

from config_reader import config

from pymongo import MongoClient
client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]

router = Router()  

def get_subscribers():
    subscribers = users.find()
    return subscribers


async def send_newsletter(message):
    subscribers = get_subscribers()
    for subscriber in subscribers:
        user_id = subscriber['_id']
        await send_message(user_id, message, Bot)


async def send_message(user_id, message, bot: Bot):
    await bot.send_message(chat_id=user_id, text=f'{message}')


@router.message(Command("sendall"))
async def start_newsletter(message: types.Message, bot: Bot):
    if message.from_user.id == 815087430:
        text = message.text[9:]
        subscribers = users.find()
        good = 0
        bad = 0
        for subscriber in subscribers:
            user_id = subscriber['_id']
            try:
                await bot.send_message(user_id, text)
                good += 1
            except:
                bad += 1
                print('Неудачная рассылка')
        await message.answer("Рассылка завершена")
