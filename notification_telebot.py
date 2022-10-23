import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatJoinRequest

from crone.crone import notification_scheduler
from config import NOTIFICATION_TOKEN

bot = Bot(token=NOTIFICATION_TOKEN)
dp = Dispatcher(bot)

# chat = '1648627950'

async def on_startup(dp):
    asyncio.create_task(notification_scheduler(bot))
    await bot.send_message(389837052, 'Бот для канала запущен')
    print('Hi')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)