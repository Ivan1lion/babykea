from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Поиск запчастей для детских колясок",
        description="Рассылка запроса на подбор комплектующих для детской коляски",
        provider_token=os.getenv("PROVIDER_TOKEN"),
        currency="RUB",
        prices=[
            LabeledPrice(
                label="Оплата услуги",
                amount=250
            ),
            LabeledPrice(
                label="Скидка",
                amount=-151
            )
        ],
        need_shipping_address=False,
        is_flexible=False,
        request_timeout=15
    )


# async def su

