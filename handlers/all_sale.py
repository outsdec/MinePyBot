from aiogram import Bot
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, FSInputFile, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.start import start
from base.diggers import add_user, find_user
from base.stats import botstat
from utils.number_format import spaces, spaces_mine
from aiogram.types.message import ContentType
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]

router = Router()

@router.callback_query(F.data == "all_sale")
async def all_sale_items(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = await find_user(user_id)
    blocks = user['blocks']
    stat = await botstat()
    stat_price= stat['prices']
    sand_sale = blocks['sand'] * stat_price['sand']
    silicon_sale = blocks['silicon'] * stat_price['silicon']
    overgrown_stone_sale = blocks['overgrown_stone'] * stat_price['overgrown_stone']
    smooth_stone_sale = blocks['smooth_stone'] * stat_price['smooth_stone']
    resin_sale = blocks['resin'] * stat_price['resin']
    amber_sale = blocks['amber'] * stat_price['amber']
    all_sum = round(sand_sale + silicon_sale + overgrown_stone_sale + smooth_stone_sale + resin_sale + amber_sale, 4)
    response = "💱 Продажа блоков:\n\n"
    if(sand_sale > 0): response += f"💲 Вы успешно продали {spaces_mine(blocks['sand'])} шт. песка на сумму {spaces(sand_sale)} монет.\n"
    if(silicon_sale > 0): response += f"💲 Вы успешно продали {spaces_mine(blocks['silicon'])} шт. кремния на сумму {spaces(silicon_sale)} монет.\n"
    if(overgrown_stone_sale > 0): response += f"💲 Вы успешно продали {spaces_mine(blocks['overgrown_stone'])} шт. заросшего камня на сумму {spaces(overgrown_stone_sale)} монет.\n"
    if(smooth_stone_sale > 0): response += f"💲 Вы успешно продали {spaces_mine(blocks['smooth_stone'])} шт. гладкого камня на сумму {spaces(smooth_stone_sale)} монет.\n"
    if(resin_sale > 0): response += f"💲 Вы успешно продали {spaces_mine(blocks['resin'])} шт. смолы на сумму {spaces(resin_sale)} монет.\n"
    if(amber_sale > 0): response += f"💲 Вы успешно продали {spaces_mine(blocks['amber'])} шт. янтаря на сумму {spaces(amber_sale)} монет.\n"
    response += f"\n💰 За продажу блоков вы заработали {spaces(all_sum)} монеток"
    users.update_one({'_id': user_id}, {"$set": {"blocks.sand": 0, "blocks.silicon": 0, "blocks.overgrown_stone": 0, "blocks.smooth_stone": 0, "blocks.resin": 0, "blocks.amber": 0}})
    users.update_one({'_id': user_id}, {"$inc": {"balance": all_sum}})
    await callback.answer()
    return callback.message.answer(text= response)
