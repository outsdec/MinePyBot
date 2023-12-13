import random
from aiogram import F, Router, types
from aiogram.filters import Command
from pymongo import MongoClient
from config_reader import config

client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
cases_collection = db["cases"]

router = Router()

async def open_case(user_id, case_id):
    # Получение кейса из базы данных
    case = cases_collection.find_one({"_id": case_id})
    if not case:
        return "Кейс не найден в базе данных"

    # Проверка стоимости кейса и доступности для пользователя
    # Здесь вы должны реализовать логику проверки доступности кейса для пользователя

    # Шансы для каждого предмета в кейсе
    item_chances = {item["type"]: item["chance"] for item in case["items"]}

    # Открытие кейса
    opened_item = random.choices(list(item_chances.keys()), weights=item_chances.values(), k=1)[0]

    # Добавление монеток или предмета в инвентарь пользователя
    if opened_item == "coins":
        # Здесь вы должны реализовать добавление монеток в инвентарь пользователя
        pass
    else:
        # Здесь вы должны реализовать добавление предмета в инвентарь пользователя
        pass

    return f"Открыт кейс! Вы получили: {opened_item}"

# Пример использования в aiogram
@router.message(F.text == '👤 Персонаж')
@router.message(Command("profile"))
async def open_case_command(message: types.Message):
    user_id = message.from_user.id
    case_id = 1  # Замените на ID кейса, который вы хотите открыть
    result = await open_case(user_id, case_id)
    await message.answer(result)