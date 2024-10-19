""" Отработка команд:
                     /start """


from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


from date_base.db_func import DataBaseBot
from keyboards import add_inline_keyboard_price as keyboard_menu
from fsm import Order

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """ Записываем данные о пользователе: chat_id для дальнейшей связи, имя с тг, дату первого входа.
        1. Отправляет сообщение приветствия;
        2. Отправляет сообщение с меню услугами."""
    await message.delete()

    db = DataBaseBot()

    if db.availability_masters():
        await state.set_state(Order.choice_masters)
    else:
        await state.set_state(Order.choice_service)
    
    chat_id = message.chat.id  # Получение id_chat с пользователем
    first_name, last_name = message.from_user.first_name, message.from_user.last_name  # Получение данных имени из тг


    db.add_user(chat_id,
                first_name, last_name)  # Передаем полученные данные, дата первого входа формируется в запрос к бд

    msg_hello = db.get_msg('hello')[0]
    await message.answer(msg_hello)

    price = db.get_menu_price()  # Получение прайса цен списком
    menu_price = ''
    for i in price:  # Сообщение с прайсом цен
        menu_price += f'{i[0]} - {i[1]}p {i[2].strftime("%H:%M")}\n'

    await message.answer(  # Сообщение с прайсом и Inline-клавиатурой для выбора
        text=menu_price,
        reply_markup=keyboard_menu().as_markup()
    )
