from datetime import datetime
import redis
import json
import logging

from test import api_parse_info

class Redis_Preparation():

    logging.basicConfig(level=logging.WARNING, filename='log/redis-log.txt')
    
    def get_and_update_regions_from_redis(self, data):
        try:
            with redis.Redis(host="127.0.0.1", port=6379) as redis_client:
                try:
                    reg_from_redis = redis_client.get('reg')
                except:
                    reg_from_redis = None
                regs = []
                if data:
                    for i in data:
                        res = {}
                        res['name'] = i['name']
                        res['changed'] = i['changed']
                        res['alert'] = i['alert']
                        regs.append(res)
                    result = {}
                # Если данные из апи отличаются от данных из Redis или Redis пустой, то сохраняем данные с АПИ в редис
                if reg_from_redis is None or json.loads(reg_from_redis) != regs:
                    redis_client.set('reg', json.dumps(regs))
                    result['regions'] = regs
                    result['is_updated'] = True
                    print('Regions updated')
                # Иначе возвращаем данные с редиса
                else:
                    not_updated = json.loads(reg_from_redis)
                    result['regions'] = not_updated
                    result['is_updated'] = False
                return result
        except:
            logging.exception('\n'+'Get and update regions from redis error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

    def get_and_update_regions_from_redis_notification(self, data, is_correct=True):
        try:
            with redis.Redis(db=6) as redis_client:
                try:
                    reg_from_redis = redis_client.get('reg')
                except:
                    reg_from_redis = None
                regs = []
                if data:
                    for i in data:
                        res = {}
                        res['name'] = i['name']
                        res['changed'] = i['changed']
                        res['alert'] = i['alert']
                        regs.append(res)
                result = {}
                # Если данные из апи отличаются от данных из Redis или Redis пустой, то сохраняем данные с АПИ в редис
                if (reg_from_redis is None or json.loads(reg_from_redis) != regs) and is_correct == True:
                    redis_client.set('reg', json.dumps(regs))
                    result['regions'] = regs
                    result['is_updated'] = True
                    print('Regions updated')
                # Иначе возвращаем данные с редиса
                else:
                    not_updated = json.loads(reg_from_redis)
                    result['regions'] = not_updated
                    result['is_updated'] = False
                return result
        except:
            logging.exception('\n'+'Get and update regions from redis error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

    def get_updated_regions(self):
        try:
            with redis.Redis() as redis_client:
                try:
                    regions_from_redis = json.loads(redis_client.get('updated_regs'))

                except:
                    regions_from_redis = None
                if regions_from_redis == None:
                    default = self.get_regions_from_redis()
                    redis_client.set('updated_regs', json.dumps(default['regions']))
                    
                    # print(regions)
                    # for region in regs.copy():
                    #     if region['name'] == 'Луганська область':
                    #         regs.remove(region)
                    # print('Default regions:')
                    # print('Default:')
                    return default['regions']
                else:
                    # print('Start not empty regions')
                    api_data = api_parse_info()
                    regions_from_api = self.get_and_update_regions_from_redis(api_data)
                    # print(regions_from_api)
                    # print('\n')
                    # print('Regions from redis default')
                    # print(regions_from_redis)
                    regs_redis = regions_from_redis
                    # print(regions_from_redis)
                    # print(regions_from_api)
                    changed_regs = []
                    if len(regions_from_redis) > 0:
                        for region_api in regions_from_api['regions']:
                            for key, reg_redis in enumerate(regs_redis.copy()):
                                # if reg_redis in regs_redis:
                                #     print('Is in regs')
                                #     print(reg_redis)
                                if region_api['alert'] == True and region_api not in regs_redis:
                                    changed_regs.append(region_api)
                                    regs_redis.append(region_api)
                                elif region_api['alert'] == False and region_api['name'] == reg_redis['name']:
                                    
                                    del regs_redis[key]
                                    changed_regs.append(region_api)
                                # if reg_redis['name'] == region_api['name'] and reg_redis['alert'] != region_api['alert']:
                                #     changed_regs.append(region_api)
                    # print('\n')
                    # print('regs_redis')
                    # print(regs_redis)
                    redis_client.set('updated_regs', json.dumps(regs_redis))
                    # print('\n')
                    # print('Changed regions')
                    # print(changed_regs)
                    # if len(changed_regs) > 0:
                    # redis_client.set('updated_regs', json.dumps(changed_regs))

                    return changed_regs

        except:
            logging.exception('\n'+'Get updated regions error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

    def get_regions_from_redis(self):
        try:
            with redis.Redis() as redis_client:
                try:
                    data = json.loads(redis_client.get('reg'))
                except:
                    data = None
                active_regions = {}
                regs = []
                for i in data:
                    if i['alert'] == True:
                        regs.append(i)
                active_regions['regions'] = regs
                return active_regions
        except Exception as ex:
            logging.exception('\n'+'Get regions from redis error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    """
    ШАГ №1 
    Берем Апдейты пользователей и добавляем их в JSON файл users
    """
    def replace_redis_new_users_to_new_redis_db(self):
        with redis.Redis(db=1) as client:
            user_updates_from_redis = json.loads(client.get('updates'))
            new_users_from_redis = json.loads(client.get('users'))
            count = 0
            for key, value in user_updates_from_redis.items():
                data = {
                    'user_id': value['user_id'], 
                    'first_name': '', 
                    'last_name': '', 
                    'username': '', 
                    'language_code': 'ru', 
                    'count_exec_script': 0,
                    'created_at':str(datetime.now().strftime("%d-%m-%Y %H:%M")), 
                    'modified_at': value['modified_at']
                }
                if key not in new_users_from_redis.keys():
                    new_users_from_redis[key] = data
                    count +=1

            return str(count)
    """
    ШАГ №2 Переносим данные из JSON формата в ключ - значение базы редис 
    !!! Нужно потом удалить ключ users
    """
    def replace_new_users_redis_db(self):
        with redis.Redis(db=1) as redis_client:
            user_mails = json.loads(redis_client.get('users'))
            for key, value in user_mails.items():
                redis_client.set(key, json.dumps(value))
    """
    ШАГ №4 Меням расположение апдейтов на db=4 и делаем их ключ-значение 
    """
    def replace_user_updates_location(self):
        client = redis.Redis(db=1)
        new_db = redis.Redis(db=4)
        user_mails = json.loads(client.get('updates'))
        for key, value in user_mails:
            new_db.set(str(key), json.dumps(value))

            

    def create_new_user_to_redis(self,message):
        try:
            with redis.Redis(db=1) as redis_client:
                user_id = message.from_user.id
                username = message.from_user.username
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name
                language_code = message.from_user.language_code
                user_data = {
                    'user_id':user_id, 
                    'first_name': first_name, 
                    'last_name': last_name, 
                    'username': username, 
                    'language_code': language_code, 
                    'count_exec_script': 0,
                    'created_at':str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 
                    'modified_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    'is_active': 1
                }

                if redis_client.get(str(user_id)) is None:
                    # data = {}
                    # data[user_id] = user_data
                    redis_client.set(str(user_id), json.dumps(user_data))
                # else:
                #     users_from_redis = json.loads(redis_client.get('users'))
                #     if str(user_id) not in users_from_redis.keys():
                #         users_from_redis[user_id] = user_data
                #         redis_client.set('users', json.dumps(users_from_redis))

        except:
            logging.exception('\n'+'Create new user error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    
    def create_user_updates_to_redis(self, message):
        try:
            with redis.Redis(db=4) as redis_client:
                user_id = message.from_user.id
                user_data = {
                    'user_id':user_id,
                    'count_exec_script': 1, 
                    'modified_at': str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                }
                user_from_redis = redis_client.get(str(user_id))
                if user_from_redis is None:
                    # data = {}
                    # data[user_id] = user_data
                    redis_client.set(user_id, json.dumps(user_data))
                elif user_from_redis is not None:
                    user_update_redis = json.loads(user_from_redis)
                    
                    user_update_redis['count_exec_script'] += 1
                    user_update_redis['modified_at'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    redis_client.set(str(user_id), json.dumps(user_update_redis))
                    # else:
                    #     updates_from_redis[user_id] = user_data
                    #     redis_client.set('updates', json.dumps(updates_from_redis))
        except:
            logging.exception('\n'+'Create user updates error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        
    def get_new_users_from_redis(self):
        try:
            with redis.Redis(db=1) as redis_client:
                if redis_client.dbsize() > 0:
                    redis_keys = []
                    for user in redis_client.scan_iter("*"):
                        redis_keys.append(user)
                    new_users = redis_client.mget(redis_keys)
                    return new_users
                else:
                    return None
        except Exception as ex:
            print(ex)
            logging.exception('\n'+'Create user updates error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        # with redis.Redis(db=1) as redis_client:
        #     if (redis_client.get('users')) != None:
        #         users = json.loads(redis_client.get('users'))
        #         return users
    
    def get_new_updates_from_redis(self):
        try:
            with redis.Redis(db=4) as redis_client:
                if redis_client.dbsize() > 0:
                    redis_keys = []
                    for user in redis_client.scan_iter("*"):
                        redis_keys.append(user)
                    user_updates = redis_client.mget(redis_keys)
                    return user_updates
                else:
                    return None
        except Exception as ex:
            print(ex)
            logging.exception('\n'+'get_new_updates_from_redis error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
            # if (redis_client.get('updates')) != None:
            #     users = json.loads(redis_client.get('updates'))
            #     return users

    def get_count_new_users(self):
        try:
            redis_client = redis.Redis(db=1)
            return redis_client.dbsize()
        except:
            logging.exception('\n'+'get_count_new_users error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        
    
    def get_count_user_updates(self):
        try:
            with redis.Redis(db=4) as redis_client:
                if redis_client.dbsize() > 0:
                    redis_keys = []
                    count = 0
                    for user in redis_client.scan_iter("*"):
                        redis_keys.append(user)
                    user_updates = redis_client.mget(redis_keys)
                    for update in user_updates:
                        update_data = json.loads(update)
                        count += int(update_data['count_exec_script'])
                    return count
                else:
                    return 0
        except:
            logging.exception('\n'+'get_count_user_updates error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        # users = self.get_new_updates_from_redis()
        # if users is not None:
        #     count = 0
        #     for key, values in users.items():
        #         count += int(values['count_exec_script'])
        #     return count
        # else:
        #     return 0