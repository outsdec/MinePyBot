from aiogram import F, Router, types

from base.diggers import find_user
from base.stats import botstat
from base.bonus import calculate_sale_price

from utils.number_format import spaces, spaces_mine

from config_reader import config

from datetime import datetime, timedelta

from pymongo import MongoClient
client = MongoClient(config.base_token.get_secret_value())
db = client["Mineprison"]
users = db["users"]
bonuses = db["bonuses"]
router = Router()


@router.callback_query(F.data == "all_sale")
async def all_sale_items(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user = await find_user(user_id)
    current_time = datetime.now()
    blocks = user['blocks']
    stat = await botstat()
    stat_price= stat['prices']
    block_names = ['sand', 'silicon', 'overgrown_stone', 'smooth_stone', 'resin', 'amber']
    resource_rusification = {
        'sand': 'песка','silicon': 'кремния','overgrown_stone': 'заросшего камня',
        'smooth_stone': 'гладкого камня','resin': 'смолы','amber': 'янтаря',  
        }
    if user["clan_id"] != 0: 
        user_clan_id = user["clan_id"]
    else: 
        user_clan_id = 0
    user_bonuses = bonuses.find({
        "$or": [
            {"user_id": user_id, "is_personal": True, "start_time": {"$lt": current_time}, "end_time": {"$gt": current_time}},
            {"clan_id": user_clan_id, "is_personal": False, "start_time": {"$lt": current_time}, "end_time": {"$gt": current_time}}
        ]
    })
    response_lines = []
    sand_sale = blocks['sand'] * stat_price['sand']
    silicon_sale = blocks['silicon'] * stat_price['silicon']
    overgrown_stone_sale = blocks['overgrown_stone'] * stat_price['overgrown_stone']
    smooth_stone_sale = blocks['smooth_stone'] * stat_price['smooth_stone']
    resin_sale = blocks['resin'] * stat_price['resin']
    amber_sale = blocks['amber'] * stat_price['amber']
    sell_sum = round(sand_sale + silicon_sale + overgrown_stone_sale + smooth_stone_sale + resin_sale + amber_sale, 4)
    bonus_sum = await calculate_sale_price(user_id, sell_sum)
    all_sum = round(sell_sum + bonus_sum, 4)
    response = "💱 Продажа блоков:\n\n"
    for block_name in block_names:
        block_count = blocks[block_name]
        block_sale = block_count * stat_price[block_name]
        if block_sale > 0:
            response_lines.append(
                f"💲 Вы успешно продали {spaces_mine(block_count)} шт. {resource_rusification.get(block_name)} на сумму {spaces(block_sale)} монет."
            )
    response += "\n".join(response_lines)
    response += f"\n\n🌟 С учётом всех бонусов ({sum(bonus['percentage'] for bonus in user_bonuses)}%) к сумме добавлено {spaces(bonus_sum)} монеток\n"
    response += f"\n💰 За продажу блоков вы заработали {spaces(all_sum)} монеток"
    users.update_one(
    {'_id': user_id},
    {
        "$set": {
            f"blocks.{block_name}": 0 for block_name in block_names
        },
        "$inc": {"balance": all_sum}
    }
)
    await callback.answer()
    return callback.message.answer(text= response)
