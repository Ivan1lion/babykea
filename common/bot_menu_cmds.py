from aiogram.types import BotCommand


bot_menu = [
    BotCommand(command="start", description="Найти запчасть"),
    BotCommand(command="info", description="Как работает бот"),
    BotCommand(command="help", description="Инф-я для пользователя"),
    BotCommand(command="company", description="❗️ Инф-я для продавцов запчастей"),
    BotCommand(command="policy", description="Политика конфиденциальности"),
    BotCommand(command="offer", description="Оферта"),
    BotCommand(command="disclaimer", description="Отказ от ответственности"),
]