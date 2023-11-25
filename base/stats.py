from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
stats = db["stats"]

async def add_stats():
        datereg = datetime.now()
        stats.insert_one({
            "users": 3,
            "resources": 10000,
            "items": 3,
            "clans": 0,
            "prices": {
                "sand": 0.0005,
                "silicon": 0.0008
            }
    })

async def botstat():
        stat = stats.find_one({"id": 1})
        return stat