from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.delete_message import DeleteMessage

from sqlalchemy.ext.asyncio import AsyncSession

import handlers.keyboards as kb
from database.orm_query import orm_user_request, orm_add_user

for_user_router = Router()


@for_user_router.message(CommandStart())
async def cmd_start(message: Message):
    await orm_add_user(message.from_user.username)
    file = FSInputFile("./mediafile_for_bot/1_zapchasti.jpg")
    string = (f"❗️ Для поиска нужных вам запчастей загрузите 3 фотографии:\n"
              f"\n<b><u>Фото №1</u></b> - Общий вид коляски (для понимания модели и типа коляски)\n"
              f"\n<b><u>Фото №2</u></b> - Фото поломанной (не рабочей) детали или какого либо элемента коляски\n"
              f"\n<b><u>Фото №3</u></b> - Фото той же детали (узла, элемента коляски), но с любого другого ракурса "
              f"для полноты картины\n"
              f"\n\n*фотографии можно сделать сразу из бота (заранее подготавливать их не нужно)")
    await message.answer_photo(photo=file, caption=string,
                               reply_markup=kb.start_photo)


# команды для кнопки МЕНЮ
@for_user_router.message(Command("policy"))
async def policy_cmd(message: Message):
    await message.answer("Политика конфиденциальности")


@for_user_router.message(Command("info"))
async def info_cmd(message: Message):
    info_text = (f"Бот отправляет запрос в 87 организаций. Оплата производится через приложение и все происходит "
                 f"как надо. Ваш запрос за Ваши деньги. Все предельно понятно и ясно")
    await message.answer(text=info_text)


@for_user_router.message(Command("offer"))
async def offer_cmd(message: Message):
    await message.answer("Оферта")


@for_user_router.message(Command("disclaimer"))
async def disclaimer_cmd(message: Message):
    await message.answer("Отказ от ответственности")


@for_user_router.message(Command("company"))
async def company_cmd(message: Message):
    await message.answer("Регистрация мастерской")


# для машины состояния (FSM)
class UserRequest(StatesGroup):
    get_photo1 = State()
    get_photo2 = State()
    get_photo3 = State()
    get_comments = State()


# фильтры для загрузки фото клиента №1-3 и комментария

photo_dict = []

@for_user_router.callback_query(StateFilter(None), F.data == "start_photo")
async def cmd_get_photo(callback: CallbackQuery, state: FSMContext):
    file = FSInputFile("./mediafile_for_bot/1_zapchasti.jpg")
    string = (f"Загрузите в БОТ фото общего вида коляски\n"
              f"\nДля этого нажмите на скрепку 📎 внизу экрана, сделайте снимок и отправьте его в БОТ")
    await callback.answer()
    await callback.message.answer_photo(photo=file, caption=string)
    await state.set_state(UserRequest.get_photo1)


@for_user_router.message(StateFilter(None))
async def cmd_get_photo(message: Message, state: FSMContext):
    await message.answer(text="Нужно нажать на кнопку ⤴️")


@for_user_router.message(UserRequest.get_photo1, F.photo)
async def get_photo1(message: Message, state: FSMContext):
    file = FSInputFile("./mediafile_for_bot/1_zapchasti.jpg")
    string = (f"Отлично 👌\n"
              f"\nТеперь сделайте и загрузите фото сломанной детали. Или нерабочего узла (если явных дефектов не видно)\n"
              f"\nПри необходимости отодвиньте текстиль, который может перекрывать вид на деталь")
    await state.update_data(get_photo1=message.photo[-1].file_id)
    await message.answer_photo(photo=file, caption=string)
    await state.set_state(UserRequest.get_photo2)
    photo_data_1 = message.photo[-1]
    photo_dict.append(photo_data_1.file_id)


@for_user_router.message(UserRequest.get_photo1)
async def get_photo1(message: Message, state: FSMContext):
    await message.answer(text="Это не то что нужно. Пришлите фото внешнего вида коляски")


@for_user_router.message(UserRequest.get_photo2, F.photo)
async def get_photo2(message: Message, state: FSMContext):
    file = FSInputFile("./mediafile_for_bot/1_zapchasti.jpg")
    string = (f"👍\n"
              f"\nПожалуйста сделайте и загрузите ещё одно фото этойже детали или узла, но с любого другого ракурса")
    await state.update_data(get_photo2=message.photo[-1].file_id)
    await message.answer_photo(photo=file, caption=string)
    await state.set_state(UserRequest.get_photo3)
    photo_data_2 = message.photo[-1]
    photo_dict.append(photo_data_2.file_id)


@for_user_router.message(UserRequest.get_photo3, F.photo)
async def get_photo3(message: Message, state: FSMContext):
    file = FSInputFile("./mediafile_for_bot/1_zapchasti.jpg")
    string = (f"Фото сохранены. Остался последний шаг\n"
              f"\nНапишите короткий комментарий-пояснение к вашему запросу, если это необходимо "
              f"или нажмите кнопку ниже")
    await state.update_data(get_photo3=message.photo[-1].file_id)
    await message.answer_photo(photo=file, caption=string,
                               reply_markup=kb.no_commens)
    await state.set_state(UserRequest.get_comments)
    photo_data_3 = message.photo[-1]
    photo_dict.append(photo_data_3.file_id)


@for_user_router.message(UserRequest.get_comments, F.text)
async def get_comments(message: Message, state: FSMContext):
    string = (f"<b><u>Дополнительная информация:</u></b>\n"
              f"\n{message.text}")
    await state.update_data(get_comments=message.text)

    album = []

    album.append(InputMediaPhoto(media=photo_dict[0]))
    album.append(InputMediaPhoto(media=photo_dict[1]))
    album.append(InputMediaPhoto(media=photo_dict[-1], caption=string))

    await message.answer_media_group(media=album)
    await message.answer(text=(f"👆 Ваш запрос сформирован и готов к отправке в 87 организаций\n"
              f"\nЭто официальные дистребьюторы, сервисные центры, частные мастерские и интернет-магазины "
              f"запчастей для детских колясок"), reply_markup=kb.finish)




@for_user_router.callback_query(UserRequest.get_comments, F.data == "no_commens")
async def keyboards_no_commens(callback: CallbackQuery, state: FSMContext, session: AsyncSession()):
    string = (f"<b><u>Дополнительная информация:</u></b>\n"
              f"\n(<i>комментарий отсутствует</i>)")
    await state.update_data(get_comments="Комментарий отсутствует")
    await callback.answer()

    album = []

    album.append(InputMediaPhoto(media=photo_dict[0]))
    album.append(InputMediaPhoto(media=photo_dict[1]))
    album.append(InputMediaPhoto(media=photo_dict[-1], caption=string))

    await callback.message.answer_media_group(media=album)
    await callback.message.answer(text=(f"👆 Ваш запрос сформирован и готов к отправке в 87 организаций\n"
              f"\nЭто официальные дистребьюторы, сервисные центры, частные мастерские и интернет-магазины "
              f"запчастей для детских колясок"), reply_markup=kb.finish)




# Сброс состояний - обработчик отмены запроса
@for_user_router.callback_query(StateFilter("*"), F.data == "clear")
async def clear_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await callback.message.answer(text=f"Ваш запрос удален ❌\n"
                                       f"\nЧто бы создать новый нажмите кнопку \n"
                                       f"МЕНЮ -> НАЙТИ ЗАПЧАСТЬ")


# Начать поиск
@for_user_router.callback_query(StateFilter("*"), F.data == "get_search")
async def clear_handler(callback: CallbackQuery, state: FSMContext, session: AsyncSession()):
    data = await state.get_data()
    await orm_user_request(session, data)
    await callback.answer()
    await callback.message.answer(text=f"Ваш запрос отправлен\n"
                                       f"\nПоиск может занять 24 часа")
    await state.clear()