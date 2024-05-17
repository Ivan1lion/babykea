from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="Информация")],
#     [KeyboardButton(text="Оферта"), KeyboardButton(text="📎")]
# ],
#                             resize_keyboard=True,
#                             input_field_placeholder="Выберете пункт меню")

start_photo = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="👉 Создать запрос 👈",
                                                                         callback_data="start_photo")]])

no_commens = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🙅🏼‍♀️ Без пояснения",
                                                                       callback_data="no_commens")]])

finish = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отмена", callback_data="clear"),
     InlineKeyboardButton(text="✅ Начать поиск", callback_data="get_search")],
                                              ])




