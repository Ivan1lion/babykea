import os
import json
from aiogram.types import LabeledPrice, Message, CallbackQuery
from aiogram import Bot
# import yookassa
# from yookassa import Payment, Configuration
# import uuid




############## Создание платежа ##############
PROVIDER_DATA_WO_EMAIL = {
    "receipt":{
        "items":[
                {
                "description": "Рассылка запроса на необходимые комплектующие для коляски",
                "amount": {"value": "99.00", "currency": "RUB"},
                "vat_code": 1,
                "quantity": "1.00",
                }
        ]
    }
}


async def order(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        payload="payment form",
        title="Поиск запчастей для детских колясок",
        description=f"Согласно закону об оказании услуг при оплате укажите ваш телефон\n"
                    f"\nНа указанный номер поступит чек об оплате услуги "
                    f"\"Рассылка запроса на необходимые комплектующие для коляски\"",
        provider_token=os.getenv("API_TOKEN_TEST"),
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
        provider_data=json.dumps(PROVIDER_DATA_WO_EMAIL),
        need_phone_number=True,
        send_phone_number_to_provider=True,
        photo_url="https://cache3.youla.io/files/images/780_780/5e/57/5e57f744de8854cf032b63d6.jpg",
        photo_width=150,
        photo_height=100
    )
