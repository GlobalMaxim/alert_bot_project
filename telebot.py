from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from config import TOKEN

storage = RedisStorage2(db=3,pool_size=10)

bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    # bot.session.close()

if __name__ == '__main__':
    from handlers.admin_handlers import send_to_admin
    from handlers.user_handlers import dp
    executor.start_polling(dp, on_startup=send_to_admin, on_shutdown=on_shutdown)