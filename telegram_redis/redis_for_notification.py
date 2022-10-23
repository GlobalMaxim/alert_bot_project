from datetime import datetime
import redis
import json
from telegram_redis.redisPreparation import Redis_Preparation
from test import api_parse_info
import logging
def get_updated_regions():
    logging.basicConfig(level=logging.WARNING, filename='log/notification-redis-log.txt')
    try:
        regionsRedis = Redis_Preparation()

        with redis.Redis(db=6) as redis_client:
            try:
                regions_from_redis = json.loads(redis_client.get('updated_regs'))
            except:
                regions_from_redis = None

            if regions_from_redis == None:
                default = regionsRedis.get_regions_from_redis()
                redis_client.set('updated_regs', json.dumps(default['regions']))
                return default['regions']
            else:
                api_data = api_parse_info()
                is_correct = True
                if api_data == False:
                    is_correct = False
                regions_from_api = regionsRedis.get_and_update_regions_from_redis_notification(api_data, is_correct)
                regs_redis = regions_from_redis
                changed_regs = []
                # regions_from_redis = data.copy()
                if len(regions_from_redis) > 0:
                    for region_api in regions_from_api['regions']:
                        for key, reg_redis in enumerate(regs_redis.copy()):
                            if region_api['alert'] == True and region_api not in regs_redis:
                                changed_regs.append(region_api)
                                regs_redis.append(region_api)
                            elif region_api['alert'] == False and region_api['name'] == reg_redis['name']:
                                
                                del regs_redis[key]
                                changed_regs.append(region_api)
                redis_client.set('updated_regs', json.dumps(regs_redis))
                return changed_regs

    except:
        logging.exception('\n'+'Get updated regions error! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
