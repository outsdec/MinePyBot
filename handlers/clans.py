from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.clans import clans_list, clan_menu_list
from base.diggers import find_user
from base.stats import botstat
from pymongo import MongoClient
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import math

client = MongoClient("mongodb+srv://Outsdec:Mama1980@cluster0.brpqv.mongodb.net/?retryWrites=true&w=majority")
db = client["Mineprison"]
users = db["users"]
miners = db["mines"]
clans = db["clans"]


class Form(StatesGroup):
    title = State()
    tag = State()


router = Router()  # [1]


# СОЗДАНИЕ КЛАНА #########################################
@router.message(Command("clan_create"))  # [2]
async def create_clan(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Form.title)
    await message.reply("Введите название (От 5 до 20 символов):")


@router.message(Form.title)
async def process_name(message: types.Message, state: FSMContext) -> None:
    if len(message.text) > 20 or len(message.text) < 5:
        await message.reply("Название превышает 20 символов! Введите заново:")
        return
    await state.update_data(title=message.text)
    await state.set_state(Form.tag)
    await message.reply("Введите тэг (до 4 символов):")


@router.message(Form.tag)
async def process_tag(message: types.Message, state: FSMContext) -> None:
    if len(message.text) > 4 or len(message.text) < 2:
        await message.reply("Тэг превышает 4 символа! Введите заново:")
        return
    await state.update_data(tag=message.text)
    data = await state.get_data()
    stat = await botstat()
    user_id = message.from_user.id
    clans.insert_one({
        "id": int(stat["clans"]) + 1,
        "title": data['title'],
        "tag": data['tag'],
        "tokens": 0,
        "level": 1,
        "members": [{
            "id": message.from_user.id,
            "right": 3
        }]
    })
    users.update_one({"_id": int(user_id)}, {"$set": {"clan_id": int(stat["clans"]) + 1}})
    await state.clear()
    await message.reply("Клан успешно создан!")


@router.callback_query(F.data.startswith('clanjoins_'))
async def get_clan(callback: types.CallbackQuery):
    if callback.data and callback.data.startswith('clanjoins_'):
        code = callback.data.split("_")[1]
        print(code)
        clan = clans.find_one({"id": int(code)})
        print(clan)
        user_id = callback.from_user.id
        user = await find_user(user_id)
        if user["clan_id"] != 0:
            return callback.message.answer('Вы уже находитесь в клане!')
        if clan:
            if callback.from_user.id not in clan["members"]:
                clans.update_one({"id": int(code)}, {"$push": {"members": {"id": callback.from_user.id, "right": 0}}})
                users.update_one({"_id": int(user_id)}, {"$set": {"clan_id": int(code)}})
                await callback.message.answer(f"Вы присоединились к клану [{clan['tag']}] {clan['title']}!")
            else:
                await callback.message.reply("Вы уже состоите в этом клане!")
        else:
            await callback.message.reply("Такого клана не существует!")


@router.message(F.text == 'кланвыйти')
@router.message(Command("clan_leave"))
async def leave_clans(message: Message):
    user = await find_user(message.from_user.id)
    clan = clans.find_one({"id": user["clan_id"]})
    if user["clan_id"] == 0:
        await message.answer("Вы не состоите в клане!")
    if clan:
        users.update_one({"_id": int(user["_id"])}, {"$set": {"clan_id": 0}})
        clans.update_one({"id": user["clan_id"]}, {"pull": {"members": {"id": user["_id"]}}})
        await message.answer("Вы успешно вышли из клана!")

@router.callback_query(F.data == "clans_leave")
async def leave_clans(callback: types.CallbackQuery):
    user = await find_user(callback.from_user.id)
    clan = clans.find_one({"id": user["clan_id"]})
    if user["clan_id"] == 0:
        await callback.message.answer("Вы не состоите в клане!")
    if clan:
        users.update_one({"_id": int(user["_id"])}, {"$set": {"clan_id": 0}})
        clans.update_one({"id": user["clan_id"]}, {"pull": {"members": {"id": user["_id"]}}})
        await callback.message.answer("Вы успешно вышли из клана!")


# ИНФОРМАЦИЯ О КЛАНЕ #########################################
@router.message(F.text == '🏛 Клан')
async def profilebutton(message: Message):
    user_id = message.from_user.id
    user = await find_user(user_id)
    if user["clan_id"] != 0:
        clan = clans.find_one({"id": int(user["clan_id"])})
        leader_clan = "Глава клана: \n"
        zam = "Заместители клана: \n"
        stareishn = "Старейшины клана: \n"
        members = "Участники клана: \n"
        for leader in clan['members']:
            print(leader)
            if leader['right'] == 3:
                user = await find_user(leader["id"])
                leader_clan += f"[{clan['tag']}] {user['nickname']} \n"
            elif leader['right'] == 2:
                user = await find_user(leader["id"])
                zam += f"[{clan['tag']}] {user['nickname']} \n"
            elif leader['right'] == 1:
                user = await find_user(leader["id"])
                stareishn += f"[{clan['tag']}] {user['nickname']} \n"
            elif leader['right'] == 0:
                user = await find_user(leader["id"])
                members += f"[{clan['tag']}] {user['nickname']} \n"

        text = (
            f"🤖 [{clan['tag']}] {clan['title']}\n\n"
            f"💰 Жетоны: {(clan['tokens'])} шт.\n"
            f"💰 Развитие: {(clan['level'])} уровень\n\n"
        )
        if leader_clan != "Глава клана: \n":
            text += f"{leader_clan}\n"
        if zam != "Заместители клана: \n":
            text += f"{zam}\n"
        if stareishn != "Старейшины клана: \n":
            text += f"{stareishn}\n"
        if members != "Участники клана: \n":
            text += f"{members}\n"
        await message.reply(f"{text}")
    else:
        await message.reply("У вас не создан клан!", reply_markup=clans_list())
    ##########################################################


# СПИСОК КЛАНОВ (ПАГИНАЦИЯ) #########################################

PAGE_SIZE = 10


@router.callback_query(F.data == "clans_list")
async def get_clans(callback: types.CallbackQuery):
    page = 1
    keyboard = get_keyboard(page)
    total_count = clans.count_documents({})
    pages = math.ceil(total_count / PAGE_SIZE)
    text = f"Страница {page}/{pages}\nВыберите клан:"
    await callback.message.answer(text, reply_markup=keyboard)


@router.message(Command("clans"))
async def get_clans(message: types.Message):
    page = 1
    keyboard = get_keyboard(page)
    total_count = clans.count_documents({})
    pages = math.ceil(total_count / PAGE_SIZE)
    text = f"Страница {page}/{pages}\nВыберите клан:"
    await message.answer(text, reply_markup=keyboard)


def get_keyboard(page):
    keyboard = InlineKeyboardBuilder()
    total_count = clans.count_documents({})
    pages = math.ceil(total_count / PAGE_SIZE)
    clanss = clans.find({}).sort("title") \
        .skip((page - 1) * PAGE_SIZE).limit(PAGE_SIZE)

    for clan in clanss:
        callback_data = f"clan_id:{clan['id']}"
        keyboard.button(text=clan['title'], callback_data=callback_data)
    if page > 1:
        keyboard.add(InlineKeyboardButton(text="⬅️", callback_data=f"page:{page - 1}"))

    if page < pages:
        keyboard.add(InlineKeyboardButton(text="➡️", callback_data=f"page:{page + 1}"))
    keyboard.adjust(2)
    return keyboard.as_markup()


async def list_clans(message, page, pages, keyboard):
    text = f"Страница {page}/{pages}\nВыберите клан:"
    await message.edit_text(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith('clan_id:'))
async def clan_info(call: types.CallbackQuery):
    clan_id = call.data.split(":")[1]
    clan = clans.find_one({"id": int(clan_id)})
    print(clan)
    text = f"Название: {clan['title']}\nЖетоны: {clan['tokens']}"
    await call.message.answer(text, reply_markup=clan_menu_list(clan_id))


@router.callback_query(F.data.startswith('page:'))
async def page_switch(call: types.CallbackQuery):
    page = int(call.data.split(":")[1])
    keyboard = get_keyboard(page)
    total_count = clans.count_documents({})
    pages = math.ceil(total_count / PAGE_SIZE)
    await list_clans(call.message, page, pages, keyboard)

##########################################################
