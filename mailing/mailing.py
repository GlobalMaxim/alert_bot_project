from datetime import datetime
import logging
import redis
import json
from test import  api_parse_info
from aiogram.utils.exceptions import BotBlocked,CantInitiateConversation, ChatNotFound
from aiogram.types import ParseMode
from aioredis.exceptions import ConnectionError
"""
1. При сохраненении региона пользователем, он получает уведомление о тревоге по крону (каждые 30 сек проверка).
Если тревога активна сейчас, пользователь получает уведомление, если у него is_sent_start_message = False
После получения сообщения у пользователя в "mail" меняется поле is_sent_start_message на True

"""

class Mailing():
    logging.basicConfig(level=logging.WARNING, filename='log/mailing-log.txt')

    def __init__(self):
        redis_pull = redis.ConnectionPool(db=4)
        self.redis_client = redis.Redis(connection_pull=redis_pull, db=2, max_connections=2 * 31)
        # self.mail_data = self.redis_client.get('mail')


    async def save_user_mailing(self, callback):
        try:
            user_id = callback.from_user.id
            user_region = callback.data
            user_data = {
                'user_id': user_id, 
                'user_region': user_region,
                'is_active': True,
                'is_sent_start_message': False,
                'is_sent_stop_message': False
            }
            self.redis_client.set(str(user_id), json.dumps(user_data))
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

    async def send_mailing(self, bot):
        regions = api_parse_info()
        for region in regions:
            if self.redis_client.dbsize() > 0:
                for user in self.redis_client.keys("*"):
                    user_clear = user.decode("utf-8")
                    user_data = json.loads(self.redis_client.get(user_clear))
                    try:
                        if region['name'] == user_data['user_region'] and user_data['is_sent_start_message'] == False and region['alert'] == True:
                            await bot.send_message(int(user_clear),f'🔴<b>Повітряна тривога у "{region["name"]}"</b>\nПочаток тривоги у {region["changed"]}\n\n@Official_alarm_bot', parse_mode=ParseMode.HTML)
                            user_data['is_sent_start_message'] = True
                            user_data['is_sent_stop_message'] = False
                            # print(f'Need to send message to user {key}')
                        
                        elif region['name'] == user_data['user_region'] and user_data['is_sent_start_message'] == True and user_data['is_sent_stop_message'] == False and region['alert'] == False:
                            await bot.send_message(int(user_clear), f'🟢<b>Відбій повітряної тривоги у "{region["name"]}"</b>\nОновлено у {region["changed"]}\n\n@Official_alarm_bot', parse_mode=ParseMode.HTML)
                            user_data['is_sent_stop_message'] = True
                            user_data['is_sent_start_message'] = False

                        self.redis_client.set(user_clear, json.dumps(user_data))
                    # except:
                    #     logging.exception('\n\n'+'Send mailing log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
                                
                    except (BotBlocked, CantInitiateConversation, ChatNotFound):
                        self.redis_client.delete(user_clear)
                        logging.exception('\n\n'+'Send mailing log! '  + '\n'+ f'User ID: {user_clear}' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
                    except:
                        # user_data['is_sent_stop_message'] = False
                        # user_data['is_sent_start_message'] = False
                        logging.exception('\n\n'+'Send mailing log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
                        
                
                # try:
                #     with open('mailing/mails.json', 'r', encoding='utf-8') as f:
                #         data = json.loads(f)
                #         # print(data)
                # except:
                #     data = {}
                # if user not in data.keys():
                #     data[user] = user_data
                # # print(data)
                # with open('mailing/mails.json', 'w') as f:
                #         json.dump(data, f, ensure_ascii=False)

    def reload_redis_instances(self):
        old_client = redis.Redis()
        user_mails = json.loads(old_client.get('mail'))
        # print(user_mails)
        for key, value in user_mails.items():
            self.redis_client.set(key, json.dumps(value))
    
    def get_number_mails(self):
        return self.redis_client.dbsize()

    def clear_redis_statuses(self):
        if self.redis_client.dbsize() > 0:
            for user in self.redis_client.keys("*"):
                user = user.decode("utf-8")
                user_data = json.loads(self.redis_client.get(user))
                user_data['is_sent_stop_message'] = False
                user_data['is_sent_start_message'] = False
                self.redis_client.set(user, json.dumps(user_data))
        # with redis.Redis() as redis_client:
        #     users_from_redis = json.loads(redis_client.get('mail'))
        #     if users_from_redis != None:
        #         for key, values in users_from_redis.items():
        #             values['is_sent_stop_message'] = False
        #             values['is_sent_start_message'] = False
        #     redis_client.set('mail', json.dumps(users_from_redis))
        
    def stop_mailing(self, callback):
        try:
            user_id = str(callback.from_user.id)
            del self.redis_client[user_id]
            # self.redis_client.delete(str(user_id))
            # with redis.Redis() as redis_client:
            #     if redis_client.get('mail') != None:
            #         users_from_redis = json.loads(redis_client.get('mail'))
            #         if user_id in users_from_redis.keys():
            #             users_from_redis.pop(user_id)
            #         redis_client.set('mail', json.dumps(users_from_redis))
        except Exception as ex:
            logging.exception('\n'+'Stop mailing log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    
    def is_user_alert_active(self, user_id):
        if self.redis_client.exists(str(user_id)):
            return True
        else:
            return False

        # with redis.Redis() as redis_client:
        #     if redis_client.get('mail') != None:
        #         users_from_redis = json.loads(redis_client.get('mail'))
        #         if str(user_id) in users_from_redis.keys():
        #             return True
        #         else:
        #             return False