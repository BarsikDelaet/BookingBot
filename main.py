""" Подключение и объединение всех функций. """

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from config import API_TOKEN
from handlers import common, menu


async def main():
    """Основное включение бота и его поддержка"""
    dp = Dispatcher()  # Диспетчер для управления
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))  # Конкретно бот

    dp.include_router(common.router)
    dp.include_router(menu.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
