""" Состояния для линейного перехода. """


from aiogram.fsm.state import StatesGroup, State


class Order(StatesGroup):
    """ Выбор услуги из раздела меню. """
    choice_masters = State()
    choice_service = State()
    choice_date = State()
