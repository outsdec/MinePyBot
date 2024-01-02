from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())

async def set_default_commands():
    menu = [
        BotCommand(command = "start", description = "Запустить/обновить бота"),
        BotCommand(command = "profile", description = "Профиль персонажа"),
        BotCommand(command = "nick", description = "Сменить никнейм"),
        BotCommand(command = "shop", description = "Магазин предметов"),
        BotCommand(command = "ref", description = "Реферальная система"),
        BotCommand(command = "top", description = "Топ пользователей"),
        BotCommand(command = "inventory", description = "Инвентарь"),
        BotCommand(command = "donate", description = "Магазин внутриигровых предметов"),
    ]
    await bot.set_my_commands(menu, BotCommandScopeDefault())
