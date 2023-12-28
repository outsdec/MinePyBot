from aiogram import F, Bot, Router, types
from aiogram.filters import Command, CommandObject

from base.nickname import update_nickname

router = Router()  # [1]


@router.message(Command("nick"))
async def cmd_name(message: types.Message, command: CommandObject):
    if command.args:
        print(len(command.args))
        if len(command.args) > 20:
            return message.answer('Ник должен быть меньше 20 символов!')
        else:
            userid = message.from_user.id
            await update_nickname(userid, command.args)
            await message.answer(f"Хороший выбор, <b>{command.args}</b>", parse_mode="HTML")
    else:
        await message.answer("Пожалуйста, укажи своё ник после команды /nick!")
