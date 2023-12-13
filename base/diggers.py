from aiogram import F, Bot
from pymongo import MongoClient
from datetime import datetime
from base.stats import botstat
from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())

client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
stats = db["stats"]

async def add_user(user_id):
    if users.find_one({"_id": int(user_id)}) is None:
        stat = await botstat()
        datereg = datetime.now().date()
        users.insert_one({
            "_id": int(user_id),
            "nickname": "Копатель",
            "balance": 0,
            "level": 1,
            "exp": 0,
            "clan_id": 0,
            "health": {
                "now": 20,
                "max": 20,
            },
            "blocks": {
                "sand": 0,
                "silicon": 0,
                "overgrown_stone": 0,
                "smooth_stone": 0,
                "resin": 0,
                "amber": 0
            },
            "stats_blocks": {
                "sand": 0,
                "silicon": 0,
                "overgrown_stone": 0,
                "smooth_stone": 0,
                "resin": 0,
                "amber": 0,
            },
            "inventory": [{
                "id": int(stat["items"]) + 1,
                "name": "Деревянная лопата",
                "level": 1,
                "type": "shovel",
                "status": False
            }],
            "date": str(datereg)
        })
        stats.update_one({"id": 1}, {"$inc": {"users": 1, "items": 1}})
        await bot.send_message(user_id, 'Добро пожаловать! Держи лопату, положил тебе в инвентарь ⛏')

async def find_user(user_id):
    if users.find_one({"_id": int(user_id)}) is None:
        await add_user(user_id)
    else:
        user = users.find_one({"_id": user_id})
        return user

async def update_level(user_id, level, exp):
    """Обновляет уровень пользователя и возвращает оставшееся опыт."""
    users.update_one({"_id": int(user_id)}, {"$set": {"level": level}})
    return exp - level_up_exp(level)

def level_up_exp(level):
    """Вернет количество опыта, необходимое для повышения уровня."""
    return 500 * (level ** 2)

async def user_exp(user_id, exp):
    user = users.find_one({"_id": int(user_id)})
    if user is None:
        return "User not found"

    current_level = user["level"]
    exp_needed = level_up_exp(current_level + 1) - user["exp"]

    if exp_needed <= exp:
        # Если достаточно опыта для повышения уровня, обновляем уровень
        exp -= exp_needed
        await update_level(user_id, current_level + 1, exp)
    else:
        # Иначе просто добавляем опыт
        users.update_one({"_id": int(user_id)}, {"$inc": {"exp": exp}})

