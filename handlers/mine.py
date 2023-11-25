from aiogram import F
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.start import start
from datetime import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]

async def add_user(user_id, username):
    if users.find_one({"_id": int(user_id)}) is None:
        datereg = datetime.now().date()
        users.insert_one({
            "_id": int(user_id),
            "nickname": str(username),
            "balance": 0,
            "date": str(datereg)
    })

router = Router()  # [1]

@router.message(Command("mine"))  # [2]
async def profilebutton(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await add_user(user_id, username)
    user = users.find_one({"_id": user_id})
    await message.answer(
        "🤖 Ваш персонаж:",
        f"👀 Игровой ник: {str(user['nickname'])}",
        f"💰 Баланс: {str(user['balance'])} монет",
        f"📅 Дата регистрации: {str(user['date'])}",
        reply_markup=start()
    )

@router.message(F.text == 'Шахта')
async def profilebutton(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    user = users.find_one({"_id": user_id})
    print(user)
    result = ""
    result += f"🤖 Ваш персонаж:\n\n"
    result += f"👀 Игровой ник: {(user['nickname'])}\n"
    result += f"💰 Баланс: {(user['balance'])} монет\n"
    result += f"\n📅 Дата регистрации: {(user['date'])}\n"
    print(result)
    await add_user(user_id, username)
    await message.answer(str(result), reply_markup=start())
