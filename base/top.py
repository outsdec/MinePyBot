from pymongo import MongoClient
from datetime import datetime
from utils.number_format import spaces, spaces_mine

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users_collection = db["users"]

async def sort_users_balance():
    doc = list(users_collection.find().sort("balance", -1))
    text = ''
    text += '💰 Топ пользователей по балансу: \n\n'
    i = 1
    for user in doc:
        text += f'{i}. {user["nickname"]} [ID: {user["_id"]}] - {spaces(user["balance"])} монеток 💰' + "\n" 
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
    top_users = users_sorted[:5]
    response = '\n\n⛏ Топ пользователей по добытым блокам: \n'
    i = 1
    for user, user_array, total_sum in top_users:
        response += f'{i}. {user["nickname"]} [ID: {user["_id"]}] - {spaces_mine(total_sum)} шт.\n'
        i += 1
    return response



