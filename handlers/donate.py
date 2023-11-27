from aiogram import Bot
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message, PreCheckoutQuery
from yookassa import Configuration

Configuration.account_id = 237154
Configuration.secret_key = "390540012:LIVE:37752"

tok = "390540012:LIVE:37752"
amount = 1500

router = Router()  # [1]


@router.message(Command("donate"))  # [2]
async def buy(message: types.Message, bot: Bot):
    await message.answer("!!!Тестовый платеж!!!")
    await bot.send_invoice(
        chat_id=message.chat.id,
        title=f"Пополнение на {amount} монет",
        description=f"Вы пополняете баланс на {amount} монет",
        provider_token=tok,
        currency="rub",
        prices=[types.LabeledPrice(label=f"пополнить на {amount} руб", amount=int(amount) * 100)],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    msg = f'Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}'
    await message.answer(msg)
