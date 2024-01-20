from aiogram import F, Bot,Router, types
from aiogram.filters import Command


router = Router()  # [1]


@router.message(Command("/stats"))
async def stats(message: types.Message, bot: Bot):
    message.answer("Статистика добавлена")