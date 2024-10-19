""" Управление Базой Данных. """


import psycopg2
from date_base.config import *
from datetime import datetime


class DataBaseBot:

    def __init__(self):
        self.connect = psycopg2.connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )

# Функции client -------------------------------------------------------------------------------------------------------

    def add_user(self, chat_id: int, first_name: str, last_name: str) -> None:
        """ Создание нового пользователя.
        При условии, что его нет в базе."""
        cursor = self.connect.cursor()
        cursor.execute(f"""
        select id_client from clients
        where id_chat = {chat_id}""")
        check_id = cursor.fetchone()
        if check_id:  # Пользователь уже добавлен
            pass
        else:
            now_date = datetime.today().strftime('%Y.%m.%d')  # TODO: попробовать обратную запись %d.%m.%Y
            cursor.execute(f"""
            insert into clients (id_chat, name_client, first_date)
            values ({chat_id}, '{first_name+' '+last_name}', '{now_date}')""")

# Функции Msg ----------------------------------------------------------------------------------------------------------

    def get_msg(self, name_msg: str) -> str:
        """ Получает сообщение по спец. имени name_msg. """
        cursor = self.connect.cursor()
        cursor.execute(f"""
        Select text_msg
        From msg
        Where name_msg = '{name_msg}'
        """)
        return cursor.fetchone()

# Функции Service ------------------------------------------------------------------------------------------------------

    def get_menu_price(self) -> list:
        """ Получение списка всех услуг.
        [(name_service: str,
        price: int,
        duration: datetime.time()), (...), (...)]"""
        cursor = self.connect.cursor()
        cursor.execute("""
        select name_service, price, duration  from service""")
        return cursor.fetchall()

    def get_menu_price_keyboard(self) -> list:
        """ Получение списка прайс с id и name. """
        cursor = self.connect.cursor()
        cursor.execute("""
                select id_service, name_service  from service""")
        return cursor.fetchall()

    def get_id_service(self) -> list:
        """ Получение id услуг """
        cursor = self.connect.cursor()
        cursor.execute("""
                select id_service from service""")
        list_id = [str(i[0]) for i in cursor.fetchall()]
        return list_id

    def get_name_service(self, id_service: int) -> str:
        """ Получение названия услуги по id_service """
        cursor = self.connect.cursor()
        cursor.execute(f"""
        select name_service from service
        where id_service = {id_service}""")
        return cursor.fetchone()[0]

# Функции Masters ------------------------------------------------------------------------------------------------------

    def availability_masters(self) -> bool:
        """ Возвращает True если мастера есть, иначе False """
        cursor = self.connect.cursor()
        cursor.execute("""
        select * from masters""")
        if cursor.fetchone():
            return True
        else:
            return False

    def get_id_masters(self) -> list:
        """ Получение id мастеров """
        cursor = self.connect.cursor()
        cursor.execute("""
                   select id_master from masters""")
        list_id = [str(i[0]) for i in cursor.fetchall()]
        return list_id

    def __del__(self):
        self.connect.commit()
        self.connect.close()
# ---------------------------   ----------------------------------------------------------------------------------
#     def add_user(self, chat_id: int):
#         """ Ищет пользователя в Базе данных если нет -
#         создает пользователя заполняя основную информацию;
#         если есть - pass. """
#         cursor = self.connect.cursor()
#         cursor.execute(f"""
#         select id
#         from bot_user
#         where chat_id = {chat_id}""")
#         check_id = cursor.fetchone()
#         if check_id:
#             pass
#         else:
#             cursor.execute(f"""
#             insert into bot_user (chat_id, nickname, age, reputation)
#             values ('{chat_id}', 'None', 'None', 'Нейтральная')""")
#
#
#     def update_nickname(self, chat_id: int, nickname: str):
#         """ Обновление никнейма. """
#         cursor = self.connect.cursor()
#         cursor.execute(f"""
#         update bot_user
#         set nickname='{nickname}'
#         where chat_id = '{chat_id}'""")
#
#     def update_age(self, chat_id: int, age: str):
#         """ Обновление возраста. """
#         cursor = self.connect.cursor()
#         cursor.execute(f"""
#         update bot_user
#         set age='{age}'
#         where chat_id = '{chat_id}'""")
#
#     def put_user_data(self, chat_id: int):
#         """ Получение Никнейма, возраста, репутации
#         По chat_id. """
#         cursor = self.connect.cursor()
#         cursor.execute(f"""
#         select nickname, age, reputation
#         from bot_user
#         where chat_id = {chat_id}""")
#         return cursor.fetchone()
#

