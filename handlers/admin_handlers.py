import asyncio
from aiogram.types import ParseMode
from typing import Union
from telebot import dp, bot
from aiogram.types import Message, BotCommand, BotCommandScopeChat, BotCommandScopeDefault,CallbackQuery
from config import admin_id, OS
from keyboards.default.menu import menu, menu_2
from aiogram.dispatcher.filters import Command, Text
from db.database import Database
from telegram_redis.redisPreparation import Redis_Preparation 
from crone.crone import scheduler
from keyboards.mailing.regionsMarkup import regions_markup
from mailing.mailing import Mailing
from test import  parse_photo, api_parse_info


async def send_to_admin(dp):
    asyncio.create_task(scheduler(bot))
    import middlewares
    middlewares.setup(dp)
    
    
    await bot.set_my_commands([
        BotCommand('restart', 'Перезапустити'),
        BotCommand('set', 'Выбрать регион')
    ])

    for admin in admin_id:
        await bot.set_my_commands([
            BotCommand('set', 'Выбрать регион'),
            BotCommand('show_all_data', 'Показать статистику'),
            BotCommand('parse', 'Обновить фото'),
            BotCommand('show_mails_count', 'Количество рассылок'),
            BotCommand('save', 'Сохранить данные')
        ], scope=BotCommandScopeChat(chat_id=admin), )

    await bot.send_message(admin_id[0], 'Бот запущен', reply_markup=menu)

@dp.message_handler(commands=['show_users_count'])
async def count_user(message: Message):
    if message.from_user.id in admin_id:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        db = Database()
        count = db.count_users()
        db.close_connection()
        await message.answer(text=f'Всего {count} пользователей', reply_markup=markup)

@dp.message_handler(commands=['show_mails_count'])
async def count_mails(message: Message):
    if message.from_user.id in admin_id:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        mail = Mailing()
        mails_count = mail.get_number_mails()
        await message.answer(text=f'Всего {mails_count} рассылок', reply_markup=markup)

@dp.message_handler(commands=['clear_mails_log'])
async def count_mails(message: Message):
    if message.from_user.id in admin_id:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        mail = Mailing()
        mail.clear_redis_statuses()
        await message.answer(text=f'Редис очищен', reply_markup=markup)

@dp.message_handler(commands=['save'])
async def save(message: Message):
    if message.from_user.id in admin_id:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        db = Database()
        values = db.save_data_to_db()
        db.close_connection()
        await message.answer(f'Добавлено {values[0]} новых пользователей и обновлено {values[1]} пользователя', reply_markup=markup)

@dp.message_handler(commands=['parse'])
async def save(message: Message):
    if message.from_user.id in admin_id:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        await parse_photo()
        await message.answer('Фото обновлено', reply_markup=markup)

# @dp.message_handler(commands=['delete'])
# async def reset(message: Message):
#     if message.from_user.id in admin_id:
#         db = Database()
#         db.clear_redis()
#         db.close_connection()
#         await message.answer('Redis cleared')


@dp.message_handler(commands=['show_all_data'])
async def show_all_info(message: Message):
    if message.from_user.id in admin_id:
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        r = Redis_Preparation()
        new_users =  r.get_count_new_users()
        db = Database()
        await message.answer(text=f'За сегодня {new_users} новых пользователей')
        updated_users = r.get_count_user_updates()
        await message.answer(text=f'За сегодня {updated_users} новых запросов')
        count = db.count_users()
        if not count:
            count = 0
        await message.answer(text=f'Всего {count} пользователей')
        count = db.count_requests()
        if not count:
            count = 0
        await message.answer(text=f'Всего {count} Запросов', reply_markup=markup)
        db.close_connection()

@dp.message_handler(commands=['show_all_requests_count'])
async def count_user(message: Message):
    if message.from_user.id in admin_id:
        db = Database()
        count = db.count_requests()
        await message.answer(text=f'Всего {count} Запросов')
        db.close_connection()