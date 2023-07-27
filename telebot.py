from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from bot.config import TOKEN
from bot.middlewares.throttling import ThrottlingMiddleware

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(ThrottlingMiddleware())

async def on_shutdown(dp):
    pass

if __name__ == '__main__':
    from bot.handlers.admin_handlers import send_to_admin, dp
    from bot.handlers.user_handlers import dp
    executor.start_polling(dp,skip_updates=True, on_startup=send_to_admin, on_shutdown=on_shutdown)