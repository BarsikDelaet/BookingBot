""" Отработка кнопок для прайс-листа. """


from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext


from date_base.db_func import DataBaseBot
from fsm import Order
from keyboards import add_inline_keyboard_date as keyboard_date


router = Router()


def callback_button_masters():
    """ Список call-ов кнопок мастер """
    db = DataBaseBot()
    return db.get_id_masters()


def callback_button_price():
    """ Список call-ов кнопок прайс-лист """
    db = DataBaseBot()
    return db.get_id_service()


@router.callback_query(F.data.in_(callback_button_masters()))
@router.callback_query(F.data.in_(callback_button_price()))
async def main_cb(call: types.CallbackQuery, state: FSMContext):
    """ Отработка кнопок Прайс листа. """
    db = DataBaseBot()
    msg_choice_date = db.get_msg('choice_date')[0]  # Сообщение которому нужно передать name_service

    await state.update_data(choice_service=call.data)  # Сохраняем номер услуги
    await state.set_state(Order.choice_date)

    id_service = await state.get_data()
    name_service = db.get_name_service(id_service['choice_service'])
    print(msg_choice_date)
    await call.message.edit_text(text=msg_choice_date.format(service=name_service),
                                 reply_markup=keyboard_date().as_markup())
