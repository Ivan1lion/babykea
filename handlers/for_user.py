from aiogram import F, Router, types, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto, PreCheckoutQuery, ContentType, SuccessfulPayment
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.delete_message import DeleteMessage

from sqlalchemy.ext.asyncio import AsyncSession

import handlers.keyboards as kb
from handlers.pay import order
from database.orm_query import orm_user_request, orm_add_user

for_user_router = Router()


# команды для кнопки МЕНЮ
@for_user_router.message(Command("policy"))
async def policy_cmd(message: Message):
    await message.answer("Политика конфиденциальности")


@for_user_router.message(Command("help"))
async def policy_cmd(message: Message):
    await message.answer(f"Если при подборе запчастей в переписке с вами продавец или представитель официального "
                         f"дистребьютора вели диалог неподобающим образом (хамили, игнорировали ваши вопросы), "
                         f"обязательно сообщите нам о этом через специальную форму на сайте\n"
                         f"\n<a href='http://www.Babykea.ru/'>Babykea.ru</a>\n"
                         f"\nМы поможем вам. Разберемся в ситуации и в случае подтверждения грубого общения "
                         f"заблокируем данного продавца на нашем сервисе")


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


@for_user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    check_state = await state.get_state()
    if check_state:
        await state.clear()

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


# фильтры для загрузки фото клиента №1-3 и комментария

photo_dict = []

@for_user_router.callback_query(StateFilter(None), F.data == "start_photo")
async def cmd_get_photo(callback: CallbackQuery, state: FSMContext):
    file = FSInputFile("./mediafile_for_bot/1_zapchasti.jpg")
    string = (f"Загрузите в БОТ фото общего вида коляски\n"
              f"\nДля этого нажмите на скрепку 📎 внизу экрана, сделайте ОДИН снимок и отправьте его")
    await callback.answer()
    await callback.message.answer_photo(photo=file, caption=string)
    await state.set_state(UserRequest.get_photo1)


@for_user_router.message(StateFilter(None))
async def cmd_get_photo(message: Message, state: FSMContext):
    if message.from_user.is_bot:
        return
    await message.delete()
    await message.answer(text="Нужно нажать на кнопку ⤴️")


@for_user_router.message(UserRequest.get_photo1, F.photo)
async def get_photo1(message: Message, state: FSMContext):
    if message.media_group_id is not None:
        await message.delete()
        return

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
    await message.delete()


@for_user_router.message(UserRequest.get_photo2, F.photo)
async def get_photo2(message: Message, state: FSMContext):
    if message.media_group_id is not None:
        await message.delete()
        return

    file = FSInputFile("./mediafile_for_bot/1_zapchasti.jpg")
    string = (f"👍\n"
              f"\nПожалуйста сделайте и загрузите ещё одно фото этойже детали или узла, но с любого другого ракурса")
    await state.update_data(get_photo2=message.photo[-1].file_id)
    await message.answer_photo(photo=file, caption=string)
    await state.set_state(UserRequest.get_photo3)
    photo_data_2 = message.photo[-1]
    photo_dict.append(photo_data_2.file_id)


@for_user_router.message(UserRequest.get_photo2)
async def get_photo1(message: Message, state: FSMContext):
    await message.delete()


@for_user_router.message(UserRequest.get_photo3, F.photo)
async def get_photo3(message: Message, state: FSMContext):
    if message.media_group_id is not None:
        await message.delete()
        return

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


@for_user_router.message(UserRequest.get_photo3)
async def get_photo1(message: Message, state: FSMContext):
    await message.delete()


@for_user_router.message(UserRequest.get_comments, F.text)
async def get_comments(message: Message, state: FSMContext):
    string = (f"<b><u>Дополнительная информация:</u></b>\n"
              f"\n<blockquote>{message.text}</blockquote>")
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


@for_user_router.message(UserRequest.get_comments)
async def get_photo1(message: Message, state: FSMContext):
    await message.delete()


# Сброс состояний - обработчик отмены запроса
@for_user_router.callback_query(StateFilter("*"), F.data == "clear")
async def clear_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await callback.message.answer(text=f"Ваш запрос удален ❌\n"
                                       f"\nЧто бы создать новый нажмите кнопку \n"
                                       f"МЕНЮ -> НАЙТИ ЗАПЧАСТЬ")



@for_user_router.message(StateFilter("*"))
async def get_photo1(message: Message, state: FSMContext):
    await message.delete()


############# Оплата #############
@for_user_router.callback_query(StateFilter("*"), F.data == "get_search")
async def get_search_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    await order(callback.message, bot)


@for_user_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@for_user_router.message(F.content_types == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await bot.send_message(message.chat.id, f"Thanks! Payment was successful, id: {message.successful_payment.provider_payment_charge_id}")
    data = await state.get_data()
    user_name = message.from_user.username
    await orm_user_request(session,user_name, data)
    await message.answer(text=f"Ваш запрос отправлен\n"
                                       f"\nПоиск может занять 24 часа")
    await state.clear()




# @for_user_router.callback_query(StateFilter("*"), F.data == "get_search")
# async def clear_handler(callback: CallbackQuery, state: FSMContext, session: AsyncSession()):
#     data = await state.get_data()
#     user_name = callback.from_user.username
#     await orm_user_request(session,user_name, data)
#     await callback.answer()
#     await callback.message.answer(text=f"Ваш запрос отправлен\n"
#                                        f"\nПоиск может занять 24 часа")
#     await state.clear()





