import os
from aiogram.types import LabeledPrice, Message
from aiogram import Bot
# import yookassa
# from yookassa import Payment, Configuration
# import uuid




############## Создание платежа ##############
async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Поиск запчастей для детских колясок",
        description="Рассылка запроса на подбор комплектующих для детской коляски",
        provider_token=os.getenv("API_TOKEN"),
        currency="RUB",
        prices=[
            LabeledPrice(
                label="Оплата услуги",
                amount=25000
            ),
            LabeledPrice(
                label="Скидка",
                amount=-15100
            )
        ],
        need_shipping_address=False,
        is_flexible=False,
        request_timeout=15,
        provider_data={
            "items":[
                {
                "description": "Рассылка запроса на необходимые комплектующие для коляски",
                "amount": {"value": "99.00", "currency": "RUB"},
                "vat_code": 1,
                "quantity": 1,
                }
            ]
        }
    )







# Configuration.account_id = os.getenv("ACCOUNT_ID")
# Configuration.secret_key = os.getenv("SECRET_KEY")



# async def get_search_comand():
#     idempotence_key = str(uuid.uuid4())
#     payment = Payment.create({
#         "amount": {
#             "value": "99.00",
#             "currency": "RUB"
#         },
#         "receipt": {
#             "items":[
#                 {
#                 "description":  "Рассылка запроса на необходимые комплектующие для коляски",
#                 "amount": {"value": "99.00", "currency": "RUB"},
#                 "vat_code": 1,
#                 "quantity": 1,
#                 }
#             ],
#         },
#         "confirmation": {
#             "type": "embedded"
#         },
#         "capture": True,
#         "description": "Быстрый поиск запчатей для колясок",
#     }, idempotence_key)
#
#     return payment




