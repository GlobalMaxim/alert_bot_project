from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatJoinRequest

bot = Bot(token='5496059121:AAH3c5eNCqFSTctn_w9crkcnKSW1SZ4dPbM')
dp = Dispatcher(bot)

chat = '1648627950'

async def check(chanel_id, user_id):
    chat_member = await bot.get_chat_member(chanel_id, user_id)
    if chat_member ['status'] != 'left':
        print('True')
        return True
    else:
        print('True')
        return False

@dp.chat_join_request_handler()
async def register(message: ChatJoinRequest):
    print('Check registration')
    if type(message) == ChatJoinRequest:
        
        await message.approve()
        print(f'User', message.from_user.id, 'upproved')
        
    if await check(chat, message.from_user.id):

        print('ok')
        await bot.send_message(chat_id=message.from_user.id, text="текст")

async def on_startup(dp):
    await bot.send_message(389837052, 'Бот запущен')
    print('Hi')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)