from pymongo import MongoClient
from datetime import datetime
from utils.number_format import spaces, spaces_mine
from config_reader import config

client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users_collection = db["users"]

async def sort_users_balance():
    doc = list(users_collection.find().sort("balance", -1))
    doc = doc[:10]
    text = ''
    text += '💰 Топ-10 пользователей по балансу: \n\n'
    i = 1
    for user in doc:
        text += f'{i}. {user["nickname"]} - {spaces(user["balance"])} монеток 💰' + "\n" 
        i += 1
    return text

async def get_users_arrays():
    users = list(users_collection.find())
    users_arrays = []
    for user in users:
        stats_blocks = user.get('stats_blocks', {})
        user_array = list(stats_blocks.values())
        total_sum = sum(user_array)
        users_arrays.append((user, user_array, total_sum))
    return users_arrays

async def sort_users_by_total_sum():
    users_arrays = await get_users_arrays()
    users_sorted = sorted(users_arrays, key=lambda x: x[2], reverse=True)
    top_users = users_sorted[:10]
    response = '\n\n⛏ Топ-10 пользователей по добытым блокам: \n'
    i = 1
    for user, user_array, total_sum in top_users:
        response += f'{i}. {user["nickname"]} - {spaces_mine(total_sum)} шт.\n'
        i += 1
    return response



