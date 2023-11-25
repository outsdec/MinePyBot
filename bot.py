from aiogram import F, Bot, Dispatcher, types
from aiogram.enums import ContentType
import asyncio
import logging
from typing import Collection
from datetime import datetime, timedelta
from handlers import start, profile, minemenu, mines, leaderboard, nickname, donate, inventory, stats, all_sale, newsletter, eval, shop, clans
from handlers.donate import pre_checkout_query, successful_payment
import logging
from pymongo import MongoClient
import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]
miners = db["mines"]

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
bot = Bot(token="6380980028:AAF80OnPKPfoPdoo_HE9mUcxs0s1ddnY-w0")
dp = Dispatcher()

dp.include_routers( start.router, 
                    profile.router,
                    minemenu.router, 
                    mines.router, 
                    leaderboard.router, 
                    nickname.router,
                    inventory.router,
                    donate.router,
                    stats.router,
                    all_sale.router,
                    newsletter.router,
                    eval.router,
                    shop.router,
                    clans.router
                    )

dp.pre_checkout_query.register(pre_checkout_query)
dp.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)

async def update_data():
     async for document in miners.find({"_id": 1}):
        max_resources = document["max_resources"]
        miners.update_many({}, {"$set": {"date": datetime.now(), "resources": max_resources}})

async def update_health():
        async for document in users.find({}):
            hp = document['health']
            health_now = hp["now"]
            health_max = hp["max"]
            if(health_now < health_max):
                users.update_one({'_id': document['_id']}, {'$inc': {'health.now': 1}})
                            

def calculate_next_update_time():
    now = datetime.now()
    next_update_time = now.replace(second=0, microsecond=0)
    if now.minute % 10 != 0:
        next_update_time += timedelta(minutes=10 - (now.minute % 10))
    return next_update_time

# Schedule the update_data() function to run at specific times
async def schedule_updates():
        next_update_time = calculate_next_update_time()
        await asyncio.sleep((next_update_time - datetime.now()).total_seconds())
        await update_data()
        await update_health()
# Запуск процесса поллинга новых апдейтов
async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_updates())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())