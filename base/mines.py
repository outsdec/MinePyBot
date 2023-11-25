from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]
mines = db["mines"]

async def add_mines():
        datereg = datetime.now()
        mines.insert_one({
            "_id": 3,
            "name": "Янтарный путь",
            "resources": 10000,
            "max_resources": 10000,
            "date": str(datereg)
    })


async def find_mines(mines_id):
        mine = mines.find_one({"_id": mines_id})
        return mine

async def find_item(user_id, item_id):
        user = users.find_one({"_id": user_id})
        items = user['inventory']
        if items:
                for item in items:
                        if item['id'] == item_id:
                                return item