from datetime import datetime
import json
import logging
import aioschedule
import asyncio
from aiogram import Bot
import redis
from region_bot.utils.mailing import get_info_from_updated_region
from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated
# from region_telebot import region_data
# async def update_api_data():
#     api_data = api_parse_info()
#     r = Redis_Preparation()
#     if api_data is not None:
#         res = r.get_and_update_regions_from_redis(api_data)
#         if res['is_updated'] == True:
#             mail = Mailing()
#             await mail.send_mailing_to_chanels(bot)
#             await parse_photo()
#             # print('waiting for 20 sec sleep')
#             await asyncio.sleep(20)
#             # print('start parsing 2')
#             await parse_photo() 
            # print('updated in 20 sec')

async def send_mailing_schedule(bot, region_data):
    aioschedule.every(15).seconds.do(send_mailing, bot, region_data)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def send_mailing(bot: Bot, region_data):
        region = get_info_from_updated_region(region_data['id'])
        start = datetime.now()
        # regions = api_parse_info()
        if region:
            with redis.Redis(db=2) as redis_client:
                if redis_client.dbsize() > 0:
                    print('Start mailing time now: ', datetime.now())
                    redis_keys = []
                    for user in redis_client.scan_iter(f"{region_data['id']}:*"):
                        redis_keys.append(user)
                    users = redis_client.mget(redis_keys)
                    for user in users:
                        user_data = json.loads(user)
                        try:
                            if region['id'] == user_data['region_id'] and user_data['is_sent_start_message'] == False and region['alert'] == True:
                                await bot.send_message(int(user_data['user_id']),f'🔴<b>Повітряна тривога у "{region["name"]}"</b>\nПочаток тривоги у {region["changed"]}\n\n@Official_alarm_bot', parse_mode=ParseMode.HTML)
                                user_data['is_sent_start_message'] = True
                                user_data['is_sent_stop_message'] = False
                                # print(f'Need to send message to user {key}')
                            
                            elif region['id'] == user_data['region_id'] and user_data['is_sent_start_message'] == True and user_data['is_sent_stop_message'] == False and region['alert'] == False:
                                await bot.send_message(int(user_data['user_id']), f'🟢<b>Відбій повітряної тривоги у "{region["name"]}"</b>\nОновлено у {region["changed"]}\n\n@Official_alarm_bot', parse_mode=ParseMode.HTML)
                                user_data['is_sent_stop_message'] = True
                                user_data['is_sent_start_message'] = False

                            redis_client.set(f"{region_data['id']}:{user_data['user_id']}", json.dumps(user_data))
                        # except:
                        #     logging.exception('\n\n'+'Send mailing log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
                                    
                        except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
                            redis_client.delete(f"{region_data['id']}:{user_data['user_id']}")
                            # logging.exception('\n\n'+'Send mailing log! '   + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
                        except:
                            # user_data['is_sent_stop_message'] = False
                            # user_data['is_sent_start_message'] = False
                            logging.exception('\n\n'+'Send mailing log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
                end = datetime.now()
                print('End mailing time: ', datetime.now())
                print('Mail sent with: ' + str(end - start))
        else:
            pass




async def scheduler(bot: Bot):
    aioschedule.every(10).seconds.do(send_mailing_schedule, bot)
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)