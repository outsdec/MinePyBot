from pymongo import MongoClient
from datetime import datetime
from utils.number_format import spaces
from base.diggers import find_user, add_user

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]

async def update_nickname(_id, nickname):
    if await find_user(_id) is None:
        await add_user(_id)
    else:
        users.update_one({'_id': _id}, {'$set': {'nickname': str(nickname)}})
