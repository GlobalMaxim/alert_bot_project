

from telegram_redis.redisPreparation import Redis_Preparation
from config import NOTIFICATION_CHANEL_ID
from aiogram.types import ParseMode

from telegram_redis.redis_for_notification import get_updated_regions

async def send_notification_to_chanel(bot):
    regions = get_updated_regions()
    if len(regions) > 0:
        for region in regions:
            if region['alert'] == True:
                await bot.send_message(int(NOTIFICATION_CHANEL_ID), f'🔴 <b>Повітряна тривога у "{region["name"]}"</b>\nПочаток тривоги у {region["changed"]}\n@Air_alarm_ukr', parse_mode=ParseMode.HTML)
            elif region['alert'] == False:
                await bot.send_message(int(NOTIFICATION_CHANEL_ID), f'🟢 <b>Відбій повітряної тривоги у "{region["name"]}"</b>\nОновлено у {region["changed"]}\n@Air_alarm_ukr', parse_mode=ParseMode.HTML)