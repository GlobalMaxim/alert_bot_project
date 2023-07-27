import redis 
import json
from datetime import datetime
from aiogram.types import Message, ParseMode
from aiogram.utils.exceptions import BotBlocked,CantInitiateConversation, ChatNotFound, UserDeactivated
import logging
from aiogram import Bot
from bot.telegram_redis.redisPreparation import Redis_Preparation
# from region_telebot import region_data

def save_user_mailing(message: Message, region_data):
        try:
            with redis.Redis(db=2) as redis_client:
                user_id = message.from_user.id
                user_data = {
                    'user_id': user_id, 
                    'user_region': region_data['name'],
                    'region_id': region_data['id'],
                    'is_active': True,
                    'is_sent_start_message': False,
                    'is_sent_stop_message': False
                }
                redis_client.set(f"{region_data['id']}:{str(user_id)}", json.dumps(user_data))
            # if self.mail_data == None:
            #     data = {}
            #     data[str(user_id)] = user_data
            #     self.redis_client.set('mail', json.dumps(data))
            # else:
            #     users_from_redis = json.loads(self.mail_data)
            #     users_from_redis[str(user_id)] = user_data
            #     self.redis_client.set('mail', json.dumps(users_from_redis))
        except Exception as ex:
            logging.exception('\n'+'Save user mailing log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

def get_info_from_updated_region(region_id):
        try:
            with redis.Redis(db=3) as redis_client:
                active_region_keys = redis_client.keys(f'{region_id}:*')
                if len(active_region_keys) > 0:
                    region_data = json.loads(redis_client.get(active_region_keys[0]))
                    del redis_client[active_region_keys[0]]
                    return region_data
                else:
                    return
        except:
            return
# async def send_mailing_schedule(bot: Bot, region_data):
#     _region = get_info_from_updated_region(region_data['id'])
#     start = datetime.now()
#     # regions = api_parse_info()
#     if region:
#         with redis.Redis(db=2) as redis_client:
#             if redis_client.dbsize() > 0:
#                 print('Start mailing time now: ', datetime.now())
#                 redis_keys = []
#                 for user in redis_client.scan_iter(f"{region_data['id']}:*"):
#                     redis_keys.append(user)
#                 users = redis_client.mget(redis_keys)
#                 for user in users:
#                     user_data = json.loads(user)
#                     try:
#                         if region['id'] == user_data['region_id'] and user_data['is_sent_start_message'] == False and region['alert'] == True:
#                             await bot.send_message(int(user_data['user_id']),f'🔴<b>Повітряна тривога у "{region["name"]}"</b>\nПочаток тривоги у {region["changed"]}\n\n@Official_alarm_bot', parse_mode=ParseMode.HTML)
#                             user_data['is_sent_start_message'] = True
#                             user_data['is_sent_stop_message'] = False
#                             # print(f'Need to send message to user {key}')
                    
#                         elif region['id'] == user_data['region_id'] and user_data['is_sent_start_message'] == True and user_data['is_sent_stop_message'] == False and region['alert'] == False:
#                             await bot.send_message(int(user_data['user_id']), f'🟢<b>Відбій повітряної тривоги у "{region["name"]}"</b>\nОновлено у {region["changed"]}\n\n@Official_alarm_bot', parse_mode=ParseMode.HTML)
#                             user_data['is_sent_stop_message'] = True
#                             user_data['is_sent_start_message'] = False

#                         redis_client.set(f"{region_data['id']}:{user_data['user_id']}", json.dumps(user_data))
#                     # except:
#                     #     logging.exception('\n\n'+'Send mailing log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
                            
#                     except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
#                         redis_client.delete(f"{region_data['id']}:{user_data['user_id']}")
#                         # logging.exception('\n\n'+'Send mailing log! '   + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
#                     except:
#                         # user_data['is_sent_stop_message'] = False
#                         # user_data['is_sent_start_message'] = False
#                         logging.exception('\n\n'+'Send mailing log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
#             end = datetime.now()
#             print('End mailing time: ', datetime.now())
#             print('Mail sent with: ' + str(end - start))

def stop_mailing(message: Message, region_data):
        try:
            with redis.Redis(db=2) as redis_client:
                del redis_client[f"{region_data['id']}:{message.from_user.id}"]
        except Exception as ex:
            logging.exception('\n'+'Stop mailing log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    
async def check_is_active_user_region(bot: Bot, message: Message, region_data):
    user_id = message.from_user.id
    regions = Redis_Preparation().get_regions_from_redis()
    # alert_regions = []
    for region in regions['regions']:
        if region['name'] == region_data['name']:
            await bot.send_message(user_id,f'🔴<b>Повітряна тривога у "{region["name"]}"</b>\nПочаток тривоги у {region["changed"]}\n\n@Official_alarm_bot', parse_mode=ParseMode.HTML)
            with redis.Redis(db=2) as redis_client:
                user = json.loads(redis_client.get(f"{region_data['id']}:{user_id}"))
                user['is_sent_start_message'] = True
                redis_client.set(f"{region_data['id']}:{user_id}", json.dumps(user))
            break

def is_user_alert_active(user_id, region_data):
        with redis.Redis(db=3) as redis_client:
            if redis_client.exists(f"{region_data['id']}:{user_id}"):
                return True
            else:
                return False