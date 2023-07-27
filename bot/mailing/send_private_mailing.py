from datetime import datetime
import json
import mysql.connector
import redis
import logging
from aiogram import Bot
from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked,CantInitiateConversation, ChatNotFound, UserDeactivated

from bot.config import DATABASE_HOST, DATABASE_PASS, MYSQL_DATABASE, MYSQL_USER

def get_users_from_db():
    connection = mysql.connector.connect(user=MYSQL_USER, password=DATABASE_PASS, port='43306', host=DATABASE_HOST, database=MYSQL_DATABASE)
    query = 'SELECT DISTINCT user_id FROM users WHERE is_active = True or is_active is NULL;'
    cursor = connection.cursor()
    cursor.execute(query)
    user_data = cursor.fetchall()
    user_data = [i[0] for i in user_data]
    print(len(user_data))
    return(user_data)

def update_active_users_in_db():
    with redis.Redis(db=5) as client:
        keys = []
        for user in client.scan_iter("*"):
            status = json.loads(client.get(user))
            user = json.loads(user).split(":")[0]
            keys.append((status, user))
        return keys
        # print(users)

def get_size_active_users():
    with redis.Redis(db=5) as client:
        count = len(client.keys("*:1"))
        return count

# def rename_user_in_redis():
#     with redis.Redis(db=5) as client:
#         for user_key in client.keys():
            
#             new_username = str(user_key).replace("\"","").replace("'","").replace("b","")
#             client.rename(user_key, new_username)
        
async def send_message_to_users(message,bot: Bot,photo = None):
    logging.basicConfig(level=logging.WARNING, filename='bot/log/private-message-log.txt')
    users = get_users_from_db()
    print("Started private mailing ", datetime.now())
    # users = [389837052, 2121074781, 2147483647, 2133124028]
    count = 0
    with redis.Redis(db=5) as client:
        for user in users:
            try:
                if photo is not None:
                    await bot.send_photo(chat_id = int(user),photo = photo, caption = message, parse_mode=ParseMode.HTML)
                else:
                    await bot.send_message(int(user), message, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                client.set(f"{user}:1", int(1))
                count += 1
            except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
                client.set(f"{user}:0", int(0))
            except Exception as ex:
                print(ex)
                logging.exception('\n\n'+'Send private message log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    await bot.send_message(5327208068, message=f"Рассылка завершена. Уведомление получиди {count} пользователей.")
    print("Finished private mailing ", datetime.now())
# rename_user_in_redis()
# print(get_size_active_users())