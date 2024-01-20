from aiogram import F, Bot, Dispatcher, types
from aiogram.enums import ContentType

import asyncio
from datetime import datetime, timedelta
import pytz

from handlers import start, profile, minemenu, mines, leaderboard, nickname, donate, inventory, stats, all_sale, \
    newsletter, eval, shop, clans, cases, referal, tournaments, quests
from utils.default_menu import set_default_commands
import logging
import motor.motor_asyncio
from handlers.tournaments import check_and_manage_tournament

from scheduler import Scheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config_reader import config

client = motor.motor_asyncio.AsyncIOMotorClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
miners = db["mines"]
stats_bd = db["stats"]

logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO, filename='bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

dp.include_routers(start.router,
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
                   clans.router,
                   cases.router,
                   referal.router,
                   tournaments.router,
                   )


async def update_data():
    async for document in miners.find({}):
        max_resources = document["max_resources"]
        miners.update_many({}, {"$set": {"date": datetime.now(), "resources": max_resources}})


async def update_health():
    async for document in users.find({}):
        hp = document['health']
        health_now = hp["now"]
        health_max = hp["max"]
        if health_now < health_max:
            users.update_one({'_id': document['_id']}, {'$inc': {'health.now': 1}})


def calculate_next_update_time():
    now = datetime.now()
    next_update_time = now.replace(second=0, microsecond=0)
    if now.minute % 10 != 0:
        next_update_time += timedelta(minutes=10 - (now.minute % 10))
    return next_update_time


# Schedule the update_data() function to run at specific times
async def schedule_updates():
    await set_default_commands()
    next_update_time = calculate_next_update_time()
    await asyncio.sleep((next_update_time - datetime.now()).total_seconds())
    await update_data()
    await update_health()

async def main():
    await send_message_pls_next()
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_updates())
    await dp.start_polling(bot)

async def send_message_pls():
    await bot.send_message(chat_id=815087430, text=f'понедельник типа')

async def send_message_pls_next():
    jobs = scheduler.get_jobs()
    for job in jobs:
        # Получаем текущее время с тем же часовым поясом, что и next_run_time
        now_with_timezone = datetime.now(pytz.timezone("Asia/Almaty"))

        # Вычисляем время до следующего запуска
        time_until_next_run = job.next_run_time - now_with_timezone
        print(f"{job}")

        await bot.send_message(chat_id=815087430, text=f'Time until next run: {time_until_next_run}')

# Вместо "Asia/Almaty" используйте нужный вам часовой пояс


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(check_and_manage_tournament, 'cron', day_of_week='sun', hour='23', minute='59')
    scheduler.start()

    try:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown()
