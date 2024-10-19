from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from calendar import monthrange
import config

from date_base.db_func import DataBaseBot


WEEK = ('пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс')
MONTH = {
    1: "Январь", 2: "Февраль", 3: "Март",
    4: "Апрель", 5: "Май", 6: "Июнь",
    7: "Июль", 8: "Август", 9: "Сентябрь",
    10: "Октябрь", 11: "Ноябрь", 12: "Декабрь",
}


def add_inline_keyboard_price():
    """ Создание клавиатуры для прайса. """
    db = DataBaseBot()
    list_price = db.get_menu_price_keyboard()

    builder = InlineKeyboardBuilder()  # Строитель кнопок

    for service in list_price:
        builder.add(InlineKeyboardButton(text=service[1],
                                         callback_data=str(service[0])))

    builder.adjust(1)  # Размерность сетки кнопок
    return builder


def add_inline_keyboard_date():
    """ Создание клавиатуры с календарем для выбора даты бронирования. """
    now_date = datetime.now()  # Текущая дата
    month, year = now_date.month, now_date.year
    day_in_month = monthrange(year, month)[1]  # Кол-во дней в месяце
    first_day_week = datetime.weekday(datetime(year, month, 1))  # Первый день недели месяца
    last_day_week = datetime.weekday(datetime(year, month, day_in_month))  # Последний день недели месяца
    name_month = MONTH.get(month)  # Название месяца по-русски
    builder = InlineKeyboardBuilder()  # Строитель кнопок

    builder.add(InlineKeyboardButton(text=f'{name_month} {year}г.',
                                     callback_data='_'))  # Первая не активная кнопка (Месяц 202_г.)
    for week_day in WEEK:
        builder.add(InlineKeyboardButton(text=week_day,
                                         callback_data='_'))  # Ряд не активных кнопок с днем недели

    list_date = [' ' for _ in range(first_day_week)]  # Первые пустые ячейки до 1 дня
    list_date += [i for i in range(1, day_in_month+1)]  # Все даты месяца
    list_date += [' ' for _ in range(6-last_day_week)]  # Пустые ячейки последние оставшейся недели

    for i in list_date:
        if i != ' ':
            builder.add(InlineKeyboardButton(text=f'{i}',
                                             callback_data=f'{i}.{month}.{year}'))  # Кнопки с числом в месяце
        else:
            builder.add(InlineKeyboardButton(text=f'{i}',
                                             callback_data=f'_'))  # Пустые кнопки

    builder.add(InlineKeyboardButton(text='<<',
                                     callback_data='back'))
    builder.add(InlineKeyboardButton(text='_',
                                     callback_data='_'))
    builder.add(InlineKeyboardButton(text='>>',
                                     callback_data='next'))

    if len(list_date) // 7 == 5:  # Собираем клавиатуру по кол-ву недель в месяце
        builder.adjust(1, 7, 7, 7, 7, 7, 7, 3)
    else:
        builder.adjust(1, 7, 7, 7, 7, 7, 7, 7, 3)
    return builder
    

# ---------------------------------------------------------------------------------------------------------
# def add_inline_keyboard_general(*name_button):
#     """ Создает клавиатуру из 3 кнопок, по принятым названиям.
#     row 1: 1; row 2: 2; row 3: ..."""
#     buttons = json_read.get_text_button_general()
#     builder = InlineKeyboardBuilder()  # Строитель кнопок
#     for name in name_button:  # Добавляем все кнопки
#         builder.add(InlineKeyboardButton(text="{name}".format(name=name),
#                                          callback_data=buttons.get(name)))
#     builder.adjust(1, 2)  # Размерность сетки кнопок
#     return builder
#
#
# def add_inline_keyboard_menu(*name_button):
#     """Создание кнопок раздела меню."""
#     json_read = JsonReader(config.JSON_FILE)
#     buttons = json_read.get_text_button_menu()
#     builder = InlineKeyboardBuilder()
#     for name in name_button:
#         builder.add(InlineKeyboardButton(text="{name}".format(name=name),
#                                          callback_data=buttons.get(name)))
#     builder.adjust(2)
#     return builder
#
#
# def add_inline_keyboard_answer(*name_button):
#     """ Создает клавиатуру из 5 кнопок, по принятым названиям."""
#     json_read = JsonReader(config.JSON_FILE)
#     buttons = json_read.get_text_button_dialog()
#     builder = InlineKeyboardBuilder()  # Строитель кнопок
#     for name in name_button:  # Добавляем все кнопки
#         builder.add(InlineKeyboardButton(text="{name}".format(name=name),
#                                          callback_data=buttons.get(name)))
#     builder.adjust(3, 1)  # Размерность сетки кнопок
#     return builder
#
#
# def add_inline_keyboard_question(*name_button):
#     """ Создает клавиатуру из 5 кнопок, по принятым названиям."""
#     json_read = JsonReader(config.JSON_FILE)
#     buttons = json_read.get_text_button_dialog()
#     builder = InlineKeyboardBuilder()  # Строитель кнопок
#     for name in name_button:  # Добавляем все кнопки
#         builder.add(InlineKeyboardButton(text="{name}".format(name=name),
#                                          callback_data=buttons.get(name)))
#     builder.adjust(1, 3)  # Размерность сетки кнопок
#     return builder
#
#
# def add_inline_keyboard_question_wait():
#     """Создание кнопок со всеми отвечающими и кнопкой обновить."""
#     builder = InlineKeyboardBuilder()
#     builder.add(InlineKeyboardButton(text="🔄",
#                                      callback_data='update'))