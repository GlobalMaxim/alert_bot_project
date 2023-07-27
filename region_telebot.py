import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from bot.config import TOKEN, ADMIN_ID
from bot.middlewares.throttling import ThrottlingMiddleware
from region_bot.utils.crone import send_mailing_schedule
from region_bot.utils.regions import get_region_data

import sys

storage = MemoryStorage()

region_data = get_region_data(sys.argv[1])

bot = Bot(region_data['token'])
dp = Dispatcher(bot, storage=storage)


async def on_startup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    asyncio.create_task(send_mailing_schedule(bot, region_data))
    await bot.send_message(ADMIN_ID[0], 'Бот запущен')

async def on_shutdown(dp):
    pass

if __name__ == '__main__':
    # from bot.handlers.admin_handlers import send_to_admin, dp
    from region_bot.handlers.user_handlers import dp
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)