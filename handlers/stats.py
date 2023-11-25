from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from keyboards.start import start
from keyboards.mine import mine
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from datetime import datetime
from base.diggers import add_user, find_user
from base.stats import add_stats
import random
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

router = Router()  # [1]


@router.message(Command("/stats"))
async def addstats(message: types.Message, bot: Bot):
    message.answer("Статистика добавлена")