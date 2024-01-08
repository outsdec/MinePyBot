from aiogram import F, Bot, Router, types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link, decode_payload

router = Router()

@router.message(Command("ref"))
async def profilebutton(message: Message, bot: Bot):
    link = await create_start_link(bot, f'{message.from_user.id}', encode=True)
    await message.answer(f"⚡️ Держи ссылку для приглашения друзей: \n {link}\n\n 👌 Скоро будут добавлены награды за приглашение.")
    print(link)
