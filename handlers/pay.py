import os
import yookassa
from yookassa import Payment, Configuration
import uuid
# from aiogram import Bot
# from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

async def get_search_comand(message: Message):
    Configuration.account_id = os.getenv("ACCOUNT_ID")
    Configuration.secret_key = os.getenv("SECRET_KEY")

    payment = Payment.create({
        "amount": {
            "value": "99.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/Babykea_Bot"
        },
        "capture": True,
        "description": "Заказ №37",
        "metadata": {
            "order_id": "37"
        }
    })










# async def order(message: Message, bot: Bot):
#     await bot.send_invoice(
#         chat_id=message.chat.id,
#         title="Поиск запчастей для детских колясок",
#         description="Рассылка запроса на подбор комплектующих для детской коляски",
#         provider_token=os.getenv("PROVIDER_TOKEN"),
#         currency="RUB",
#         prices=[
#             LabeledPrice(
#                 label="Оплата услуги",
#                 amount=250
#             ),
#             LabeledPrice(
#                 label="Скидка",
#                 amount=-151
#             )
#         ],
#         need_shipping_address=False,
#         is_flexible=False,
#         request_timeout=15
#     )




