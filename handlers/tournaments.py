from aiogram import F, Bot, Router, types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from config_reader import config
from pymongo import MongoClient
import pymongo
from aiogram.enums import ParseMode
from utils.time import get_end_of_week
from datetime import datetime, timedelta
import pytz

bot = Bot(token=config.bot_token.get_secret_value())

client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
clans = db["clans"]
tournaments = db["tournaments"]

async def distribute_prizes(tournament_id):
    # Получение информации о турнире
    tournament_info = tournaments.find_one({"tournament_id": tournament_id})
    
    if not tournament_info:
        await bot.send_message(chat_id=815087430, text=f"Турнир с ID {tournament_id} не найден.")
        return
    # Получение топ-10 участников
    top_participants = list(users.find().sort("tournament_points", -1).limit(10))
    response = ""
    # Раздача призов участникам
    for idx, user in enumerate(top_participants, start=1):
        prize_amount = 1  # Замените на свою функцию расчета приза
        users.update_one({"_id": user["_id"]}, {"$inc": {"balance": prize_amount}})
        await bot.send_message(chat_id=user["_id"], text=f"Пользователь {user['_id']} получил приз в размере {prize_amount}.")
        response += "Пользователь {user['_id']} получил приз в размере {prize_amount}."
    
    await bot.send_message(chat_id=815087430, text=f"{response}")
    users.update_many({}, {"$set": {"tournament_points": 0}})
    clans.update_many({}, {"$set": {"tournament_points": 0}})

#    # Получение топ-3 кланов
#    top_clans = list(users_collection.aggregate([
#        {"$match": {"tournament_points": {"$gt": 0}}},
#        {"$group": {"_id": "$clan_id", "total_points": {"$sum": "$tournament_points"}}},
#        {"$sort": {"total_points": -1}},
#        {"$limit": 3}
#    ]))
#
#    # Раздача призов кланам
#    for idx, clan in enumerate(top_clans, start=1):
#        clan_prize_amount = 1  # Замените на свою функцию расчета приза для клана
#        # Обновление баланса клана (здесь предполагается, что у клана есть уникальный _id в коллекции)
#        users_collection.update_one({"_id": clan["_id"]}, {"$inc": {"donate_balance": clan_prize_amount}})
#        print(f"Клан {clan['_id']} получил приз в размере {clan_prize_amount}.")
all_tournament_types = ["block_mining", "block_selling", "invite_users"]

async def check_and_manage_tournament():
    # Проверка наличия активного турнира
    active_tournament = tournaments.find_one({"end_date": {"$gte": datetime.now()}})
    
    if active_tournament:
        await distribute_prizes(active_tournament["tournament_id"])
        # Определение следующего типа турнира в циклической последовательности
        current_tournament_type = active_tournament["type"]
        next_tournament_type_index = (all_tournament_types.index(current_tournament_type) + 1) % len(all_tournament_types)
        next_tournament_type = all_tournament_types[next_tournament_type_index]


        new_tournament_id = tournaments.count_documents({}) + 1 
        new_tournament = {
            "tournament_id": new_tournament_id,
            "start_date": datetime.now(),
            "end_date": get_end_of_week(),  
            "type": next_tournament_type,
            "total_participants": 0,  
            "total_points_earned": 0, 
        }
        tournaments.insert_one(new_tournament)
        await bot.send_message(chat_id=815087430, text=f"Новый турнир создан. Тип: {next_tournament_type}, ID: {new_tournament_id}")
    else:
        # Если нет активного турнира, создаётся турнир с первым типом
        new_tournament_id = tournaments.count_documents({}) + 1  
        new_tournament = {
            "tournament_id": new_tournament_id,
            "start_date": datetime.now(),
            "end_date": get_end_of_week(), 
            "type": all_tournament_types[0],
            "total_participants": 0, 
            "total_points_earned": 0,
        }
        tournaments.insert_one(new_tournament)
        await bot.send_message(chat_id=815087430, text=f"Новый турнир создан. Тип: {all_tournament_types[0]}, ID: {new_tournament_id}")

router = Router()

@router.message(Command("tourn"))
async def profilebutton(message: Message, bot: Bot):
    current_time = datetime.utcnow()
    active_tournament = tournaments.find_one({"end_date": {"$gte": datetime.now()}})
    end_date = active_tournament["end_date"]
    time_until_end = end_date - current_time
    all_users = list(users.find({"tournament_points": {"$gt": 0}}).sort([("tournament_points", pymongo.DESCENDING)]))
    top_users = all_users[:10]

    all_clans = list(clans.find({"tournament_points": {"$gt": 0}}).sort([("tournament_points", pymongo.DESCENDING)]))
    top_clans = all_clans[:10]

    user_data = users.find_one({'_id': message.from_user.id})

    user_position = None

    response = "Топ-10 пользователей по турнирным очкам:\n"
    for idx, user in enumerate(top_users, start=1):
        if user_data["_id"] == user["_id"]:
            response += f"<u>{idx}. {user['nickname']} - {user['tournament_points']} 🏆</u>\n"
            user_position = idx
        else:
            response += f"{idx}. {user['nickname']} - {user['tournament_points']} 🏆\n"

    if user_position is None:
        # If the user is not in the top 10, find their position
        user_position = next((i + 1 for i, u in enumerate(all_users) if u['_id'] == user_data['_id']), None)
        if user_position:
            response += f"\nВы занимаете {user_position}-е место с {user_data['tournament_points']} 🏆\n"
    
    response += "\nТоп-10 кланов по турнирным очкам:\n"
    for idx, clan in enumerate(top_clans, start=1):
        response += f"{idx}. [{clan['tag']}] {clan['title']} - {clan['tournament_points']} 🏆\n\n"
    response += f"🕰 До конца турнира {time_until_end}"
    await message.reply(response, parse_mode=ParseMode.HTML)


@router.message(Command("tourna"))  
async def end_tournament(message: Message):
    all_users = list(users.find({"tournament_points": {"$gt": 0}}).sort([("tournament_points", pymongo.DESCENDING)]))
    top_users = all_users[:10]
    await message.answer(f'{len(all_users)}')


