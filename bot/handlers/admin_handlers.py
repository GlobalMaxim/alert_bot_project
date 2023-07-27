import asyncio
from aiogram.types import ParseMode
from aiogram.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeDefault,CallbackQuery, BotCommandScopeChatMember
from aiogram.dispatcher.filters import Command, Text
from typing import Union

from telebot import dp, bot
from bot.config import ADMIN_ID, CHANEL_ID
from bot.keyboards.default.menu import menu, menu_2
from bot.db.database import Database
from bot.crone.crone import scheduler
from bot.telegram_redis.redisPreparation import Redis_Preparation 
from bot.keyboards.mailing.regionsMarkup import regions_markup
from bot.mailing.mailing import Mailing
from bot.test import  parse_photo, api_parse_info
from bot.mailing.send_private_mailing import send_message_to_users, update_active_users_in_db, get_size_active_users


async def send_to_admin(dp):
    asyncio.create_task(scheduler(bot))
    # import middlewares
    # middlewares.setup(dp)
    
    
    await bot.set_my_commands([
        BotCommand('region', 'Обрати регіон')
    ])

    for admin in ADMIN_ID:
        try:
            await bot.set_my_commands([
                BotCommand('region', 'Обрати регіон'),
                BotCommand('show_all_data', 'Показати статистику'),
                BotCommand('parse', 'Оновити фото'),
                # BotCommand('show_mails_count', 'Кількість активних розсилок'),
                BotCommand('save', 'Зберегти дані у БД'),
                # BotCommand('clear_mails_log', "Cкинути кеш розсилок"),
                # BotCommand('post', "Надіслати пповідомлення користувачу"),

                # BotCommand('convert_redis', "Перенести редис")

            ], scope=BotCommandScopeChat(chat_id=admin), )
        except:
            pass

    await bot.send_message(ADMIN_ID[0], 'Бот запущен', reply_markup=menu)

@dp.message_handler(commands=['show_users_count'])
async def count_user(message: Message):
    if message.from_user.id in ADMIN_ID:
        db = Database()
        count = db.count_users()
        db.close_connection()
        await message.answer(text=f'Всього {count} користувача', reply_markup=menu)

# @dp.message_handler(commands=['convert_redis'])
async def convert_redis(message: Message):
    if message.from_user.id in ADMIN_ID:
        mail = Mailing()
        mail.reload_redis_instances()
        await message.answer('Обновлено')

@dp.message_handler(commands=['convert_redis'])
async def users_redis_update(message: Message):
    if message.from_user.id in ADMIN_ID:
        redis = Redis_Preparation()
        count = redis.replace_redis_new_users_to_new_redis_db()
        await message.answer(f'Обновлено {count}')
        redis.replace_new_users_redis_db()
        await message.answer(f'finished')

@dp.message_handler(commands=['show_mails_count'])
async def count_mails(message: Message):
    if message.from_user.id in ADMIN_ID:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        mails_count = mail.get_number_mails()
        await message.answer(text=f'Всього {mails_count} розсилок', reply_markup=markup)

@dp.message_handler(commands=['clear_mails_log'])
async def count_mails(message: Message):
    if message.from_user.id in ADMIN_ID:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        mail = Mailing()
        mail.clear_redis_statuses()
        await message.answer(text=f'Редис сброшен', reply_markup=markup)

@dp.message_handler(commands=['save'])
async def save(message: Message):
    if message.from_user.id in ADMIN_ID:
        db = Database()
        values = db.save_data_to_db()
        db.close_connection()
        await message.answer(f'Додано {values[0]} нових користувача та оновлено {values[1]} ', reply_markup=menu)

@dp.message_handler(commands=['post'])
async def send_private_message(message: Message):
    if message.from_user.id in ADMIN_ID:
        msg = message.text[message.text.find(' '):]
        await send_message_to_users(msg, bot)

@dp.message_handler(content_types=['photo'])
async def send_private_message_with_photo(message: Message):
    if message.from_user.id in ADMIN_ID and '/post_photo' in message.caption:
        msg = message.caption[message.caption.find(' '):]
        photo = message.photo[0].file_id
        await send_message_to_users(msg, bot, photo)

# @dp.message_handler(commands=['update'])
# async def update_users_status(message: Message):
#     if message.from_user.id in ADMIN_ID:
#         db = Database()
#         db.update_user_statuses()
#         db.close_connection()

@dp.message_handler(commands=['parse'])
async def save(message: Message):
    print('parse')
    if message.from_user.id in ADMIN_ID:
        mail = Mailing()
        await parse_photo()
        await message.answer('Фото оновлено', reply_markup=menu)

# @dp.message_handler(commands=['delete'])
# async def reset(message: Message):
#     if message.from_user.id in ADMIN_ID:
#         db = Database()
#         db.clear_redis()
#         db.close_connection()
#         await message.answer('Redis cleared')


@dp.message_handler(commands=['show_all_data'])
async def show_all_info(message: Message):
    if message.from_user.id in ADMIN_ID:
        # mail = Mailing()
        r = Redis_Preparation()
        new_users =  r.get_count_new_users()
        # mails_count = mail.get_number_mails()
        # await message.answer(text=f'Всього {mails_count} активних розсилок')
        db = Database()
        await message.answer(text=f'За сьогодні {new_users} нових користувача')
        updated_users = r.get_count_user_updates()
        await message.answer(text=f'За сьогодні {updated_users} нових запитів')
        count = db.count_users()
        if not count:
            count = 0
        await message.answer(text=f'Всього {count} користувача')
        count = db.count_requests()
        if not count:
            count = 0
        await message.answer(text=f'Всього {count} запитів')
        db.close_connection()
        count_active = get_size_active_users()
        await message.answer(text=f'Всього {count_active} активних користувачів', reply_markup=menu)
        
@dp.message_handler(commands=['show_all_requests_count'])
async def count_user(message: Message):
    if message.from_user.id in ADMIN_ID:
        db = Database()
        count = db.count_requests()
        await message.answer(text=f'Всего {count} Запросов')
        db.close_connection()

@dp.message_handler(commands=['get_updated_regions'])
async def count_user(message: Message):
    if message.from_user.id in ADMIN_ID:
        db = Redis_Preparation()
        db.get_updated_regions()