import os
import yookassa
from yookassa import Payment, Configuration
import uuid
# from aiogram import Bot
# from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

async def get_search_comand(message: Message):
    Configuration.account_id = os.getenv("ACCOUNT_ID")
    Configuration.secret_key = os.getenv("SECRET_KEY")
    idempotence_key = str(uuid.uuid4())

    payment = Payment.create({
        "amount": {
            "value": "99.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "embedded",
        },
        "capture": True,
        "description": "Заказ №37",
        "metadata": {
            "order_id": "37"
        }
    }, idempotence_key)










# async def order(message: Message, bot: Bot):
#     await bot.send_invoice(
#         chat_id=message.chat.id,
#         title="Поиск запчастей для детских колясок",
#         description="Рассылка запроса на подбор комплектующих для детской коляски",
#         provider_token=os.getenv("API_TOKEN"),
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




