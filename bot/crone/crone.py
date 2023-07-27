import aioschedule
import asyncio

from bot.db.database import Database
from bot.mailing.mailing import Mailing
from bot.mailing.send_notification_to_chanel import send_notification_to_chanel
from bot.telegram_redis.redisPreparation import Redis_Preparation
from bot.test import  parse_photo, api_parse_info
from bot.config import ADMIN_ID
from telebot import bot

values = []

async def execute_script():
    global values
    db = Database()
    values = db.save_data_to_db()

async def update_api_data():
    api_data = api_parse_info()
    r = Redis_Preparation()
    if api_data is not None:
        res = r.get_and_update_regions_from_redis(api_data)
        if res['is_updated'] == True:
            mail = Mailing()
            r.set_updated_regions_to_redis_db()
            # await mail.send_mailing_to_chanels(bot)
            await parse_photo()
            # print('waiting for 20 sec sleep')
            await asyncio.sleep(20)
            # print('start parsing 2')
            await parse_photo() 
            # print('updated in 20 sec')
    

async def send_message_to_admin(bot):
    for admin in ADMIN_ID:
        await bot.send_message(admin, f'Сохранено {values[0]} новых пользователей и обновлено {values[1]} старых пользователя')

async def update_api_data_notification():
    api_data = api_parse_info()
    is_correct = True
    if api_data == False:
        is_correct = False
    r = Redis_Preparation()
    res = r.get_and_update_regions_from_redis_notification(api_data,is_correct)
    if res['is_updated'] == True:
        await send_notification_to_chanel(bot)

async def scheduler(bot):
    aioschedule.every().day.at('01:59').do(execute_script)
    aioschedule.every().day.at('02:00').do(send_message_to_admin, bot=bot)
    aioschedule.every(10).seconds.do(update_api_data)
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def notification_scheduler(bot):
    aioschedule.every(15).seconds.do(update_api_data_notification)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

