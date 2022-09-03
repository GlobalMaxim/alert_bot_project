from datetime import datetime
import mysql.connector
from config import DATABASE_HOST, DATABASE_PASS, MYSQL_DATABASE, MYSQL_USER
import redis
import logging
from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked,CantInitiateConversation, ChatNotFound

def get_users_from_db():
    connection = mysql.connector.connect(user=MYSQL_USER, password=DATABASE_PASS, port='43306', host=DATABASE_HOST, database=MYSQL_DATABASE)
    query = 'SELECT DISTINCT user_id FROM users;'
    cursor = connection.cursor()
    cursor.execute(query)
    user_data = cursor.fetchall()
    user_data = [i[0] for i in user_data]
    print(len(user_data))
    return(user_data)

async def send_message_to_users(message, bot):
    logging.basicConfig(level=logging.WARNING, filename='log/private-message-log.txt')
    users = get_users_from_db()

    # users = [389837052, 2121074781, 2147483647, 2133124028]
    with redis.Redis(db=5) as client:
        for user in users:
            try:
                await bot.send_message(int(user), message, parse_mode=ParseMode.HTML,disable_web_page_preview=True)
                client.set(user, int(1))
            except (BotBlocked, CantInitiateConversation, ChatNotFound):
                client.set(user, int(0))
            except:
                logging.exception('\n\n'+'Send private message log! Some Strange Exception' + '\n\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    