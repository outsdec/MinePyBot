from aiogram import F, Bot, Router, types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from config_reader import config
from pymongo import MongoClient
from aiogram.enums import ParseMode

bot = Bot(token=config.bot_token.get_secret_value())

client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
clans = db["clans"]

router = Router()

@router.message(Command("tourn"))
async def profilebutton(message: Message, bot: Bot):
    top_users = list(users.find().sort('tournament_points', -1).limit(10))
    all_users = list(users.find().sort('tournament_points', -1))
    user_data = users.find_one({'_id': message.from_user.id})
    
    user_position = None
    
    response = "Топ пользователей по турнирным очкам:\n"
    for idx, user in enumerate(top_users, start=1):
        if user_data["_id"] == user["_id"]:
            response += f"<u>{idx}. {user['nickname']} - {user['tournament_points']} очков</u>\n"
            user_position = idx
        else:
            response += f"{idx}. {user['nickname']} - {user['tournament_points']} очков\n"

    if user_position is None:
        # If the user is not in the top 10, find their position
        user_position = all_users.index(user_data) + 1
        response += f"\nВы занимаете {user_position}-е место с {user_data['tournament_points']} очками\n"

    await message.reply(response, parse_mode=ParseMode.HTML)
