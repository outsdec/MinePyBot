from aiogram import F, Bot, Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from base.diggers import find_user

from config_reader import config

from pymongo import MongoClient
client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
bonuses = db["bonuses"]

from datetime import datetime, timedelta

class Bonus:
    def __init__(self, bonus_id, user_id, clan_id, amount, is_personal, percentage, clan_bonus_id, start_time, duration_minutes):
        self.bonus_id = bonus_id
        self.user_id = user_id
        self.clan_id = clan_id
        self.amount = amount
        self.is_personal = is_personal
        self.percentage = percentage
        self.clan_bonus_id = clan_bonus_id
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=duration_minutes)

async def award_personal_bonus(user_id, amount, percentage, clan_bonus_id=None, duration_minutes=30):
    # Логика выдачи личного бонуса
    start_time = datetime.now()
    bonus = Bonus(bonus_id=None, user_id=user_id, clan_id=None, amount=amount, is_personal=True, percentage=percentage,
                  clan_bonus_id=clan_bonus_id, start_time=start_time, duration_minutes=duration_minutes)
    bonuses.insert_one(bonus.__dict__)

async def award_clan_bonus(clan_id, amount, percentage, duration_minutes=30):
    # Логика выдачи кланового бонуса
    start_time = datetime.now()
    clan_bonus_id = "example_clan_bonus_id"
    bonus = Bonus(bonus_id=None, user_id=None, clan_id=clan_id, amount=amount, is_personal=False, percentage=percentage,
                  clan_bonus_id=clan_bonus_id, start_time=start_time, duration_minutes=duration_minutes)
    bonuses.insert_one(bonus.__dict__)

async def calculate_sale_price(user_id, block_price):
    # Рассчет цены с учетом личных и клановых бонусов пользователя
    current_time = datetime.now()
    user = await find_user(user_id)
    if user["clan_id"] != 0: 
        user_clan_id = user["clan_id"]
    else: 
        user_clan_id = 0
    user_bonuses = bonuses.find({
        "$or": [
            {"user_id": user_id, "is_personal": True, "start_time": {"$lt": current_time}, "end_time": {"$gt": current_time}},
            {"clan_id": user_clan_id, "is_personal": False, "start_time": {"$lt": current_time}, "end_time": {"$gt": current_time}}
        ]
    })
    total_percentage = sum(bonus["percentage"] for bonus in user_bonuses)
    total_bonus = total_percentage / 100 * block_price
    sale_price = block_price - total_bonus
    return sale_price

# Пример использования
async def process_sale(message: types.Message):
    user_id = message.from_user.id
    user_clan_id = "example_clan_id"
    block_price = 100  # Цена блока

    # Предположим, что у пользователя есть личный бонус 5% на 30 минут
    await award_personal_bonus(user_id, amount=0, percentage=5, duration_minutes=30)

    # Предположим, что у клана есть клановый бонус 10% на 1 час
    await award_clan_bonus(user_clan_id, amount=0, percentage=10, duration_minutes=60)

    # Рассчитываем цену с учетом бонусов при продаже блока
    sale_price = await calculate_sale_price(user_id, block_price)

    await message.answer(f"Цена блока с учетом бонусов: {sale_price} монет")