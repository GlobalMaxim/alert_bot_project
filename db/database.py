from datetime import datetime
import json
import mysql.connector
from config import DATABASE_HOST, DATABASE_PASS, MYSQL_DATABASE, MYSQL_USER
import redis
import logging
import os
from mailing.send_private_mailing import update_active_users_in_db

from telegram_redis.redisPreparation import Redis_Preparation

class Database():
    logging.basicConfig(filename='log/database-log.txt', level=logging.WARNING)
    def __init__(self):
        self.connection = mysql.connector.connect(user=MYSQL_USER, password=DATABASE_PASS, port='43306', host=DATABASE_HOST, database=MYSQL_DATABASE)
        

    def get_user(self, user_id):
        try:
            query = 'SELECT user_id, username, first_name, last_name, language_code, count_exec_script FROM users WHERE user_id=%s'
            atr = (user_id,)
            cursor = self.connection.cursor()
            cursor.execute(query, atr)
            user_data = cursor.fetchall()
            return(user_data)
        except :
            logging.exception('\n'+'Get User Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        finally:
            cursor.close()
    """
    def add_new_user(message):
        # user_id = message
        try:
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name
            language_code = message.from_user.language_code

            if len(get_user(user_id)) > 0:
                query = 'UPDATE users SET count_exec_script = count_exec_script + 1 WHERE user_id=%s'
                apt=(user_id,)
                connection = connect()
                cursor = connection.cursor()
                cursor.execute(query, apt)
                connection.commit()
            else:
                query = 'INSERT IGNORE INTO users (user_id, first_name, last_name, username, language_code, count_exec_script) VALUES (%s, %s, %s, %s, %s, 1)'
                atr = (user_id,first_name, last_name, username, language_code)
                connection = connect()
                cursor = connection.cursor()
                cursor.execute(query, atr)
                connection.commit()
        except Exception :
                logging.exception('\n'+'Add New User Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        finally:
            cursor.close()
            connection.close()
    """

    def count_users(self):
        try:
            query = 'SELECT COUNT(DISTINCT user_id) from users'
            
            cursor = self.connection.cursor()
            cursor.execute(query)
            users_count = cursor.fetchall()
            return(users_count[0][0])
        except:
            logging.exception('\n'+'Count All Users Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        finally:
            if self.connection.is_connected():
                cursor.close()

    def count_requests(self):
        try:
            query = 'SELECT SUM(count_exec_script) from users where user_id not in (389837052, 2121074781)'
            cursor = self.connection.cursor()
            cursor.execute(query)
            count_requests = cursor.fetchall()
            return(count_requests[0][0])
        except:
            logging.exception('\n'+'Count Requests Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        finally:
            if self.connection.is_connected():
                cursor.close()

    def add_new_users_from_redis_to_db(self):
        try:
            r = Redis_Preparation()
            users = r.get_new_users_from_redis()

            # print(users)
            if users != None:
                print(len(users))
                users_arr = []
                for val in users:
                    values = json.loads(val)
                    # print(values)
                    if isinstance(values, dict):
                        try:
                            user_id = int(values['user_id'])
                            first_name = values['first_name']
                            last_name = values['last_name']
                            username = values['username']
                            language_code = values['language_code']
                            count_exec_script = values['count_exec_script']
                            created_at = values['created_at']
                            modified_at = values['modified_at']
                            users_arr.append((user_id, first_name, last_name, username, language_code, count_exec_script, created_at, modified_at))
                        except:
                            pass
                cursor = self.connection.cursor()
                query = 'INSERT INTO users (user_id, first_name, last_name, username, language_code, count_exec_script, created_at, modified_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE user_id = user_id;'
                cursor.executemany(query, users_arr)
                self.connection.commit()
                count = cursor.rowcount
                cursor.close()
                return str(count)
            else:
                return str(0)
        except Exception as ex:
            print(ex)
            logging.exception('\n'+'Add New Users Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
            raise
        # finally:
        #     self.save_data_to_file(users, 'new_users')

    def update_user_statuses(self):
        try:
            user_updates = update_active_users_in_db()
            # print(user_updates)
            cursor = self.connection.cursor()
            query = 'UPDATE users set is_active = %s where user_id = %s;'
            cursor.executemany(query, user_updates)
            self.connection.commit()
            count = cursor.rowcount
            print(count)
            cursor.close()
        except Exception as ex:
            print(ex)

    def add_user_updates_from_redis_to_db(self):
        try:
            r = Redis_Preparation()
            users = r.get_new_updates_from_redis()
            if users is not None:
                users_arr = []
                for val in users:
                    values = json.loads(val)
                    count_exec_script = values['count_exec_script']
                    modified_at = values['modified_at']
                    user_id = int(values['user_id'])
                    users_arr.append((count_exec_script, modified_at,user_id))
                cursor = self.connection.cursor()

                query = "INSERT INTO users (count_exec_script, modified_at, user_id) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE count_exec_script = count_exec_script + VALUES(count_exec_script), modified_at = VALUES(modified_at);"
                # query = 'UPDATE users set count_exec_script = count_exec_script + %s, modified_at = %s where user_id = %s'
                cursor.executemany(query, users_arr)
                self.connection.commit()
                count = cursor.rowcount
                cursor.close()
                return str(count)
            else:
                return str(0)
        except:
            logging.exception('\n'+'Add New Users Exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
            raise
        # finally:
        #     self.save_data_to_file(users, 'user_updates')
            
    
    def close_connection(self):
        self.connection.close()

    def save_data_to_db(self):
        try:
            new_users =  self.add_new_users_from_redis_to_db()
            print(f'Saved {new_users} new users')
            updated_users =  self.add_user_updates_from_redis_to_db()
            print(f'Saved {updated_users} user updates')
            client_users = redis.Redis(db=1)
            client_user_updates = redis.Redis(db=4)
            client_users.flushdb()
            client_user_updates.flushdb()
            print('Cache deleted')
            return [new_users, updated_users]
        except Exception as ex:
            print(ex)
            logging.exception('\n'+'Save data to db exception!!! ' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
    
    def clear_redis(self):
        r = redis.Redis(db=1)
        r.delete('updates')
        r.delete('users')
        print('Cache deleted')
    
    def save_data_to_file(self, data, type):
        folder_date = str(datetime.now().strftime("%d-%m-%y"))
        file_date = str(datetime.now().strftime("%H-%M_%d-%m-%y"))
        if not os.path.exists(f'data/{folder_date}'):
            os.mkdir(f'data/{folder_date}')
        file_name = type + '_' + file_date
        with open(f'data/{folder_date}/{file_name}.json', 'w') as f:
            json.dump(data, f)
    
# new_users = {'389837052': {'user_id': 389837052, 'first_name': 'Maxim', 'last_name': None, 'username': 'GlobalMaxim', 'language_code': 'ru', 'count_exec_scripts': 1, 'created_at': '19-05-2022 02:12', 'modified_at': '19-05-2022 02:12'}, '2121074781': {'user_id': 2121074781, 'first_name': 'Игорь', 'last_name': None, 'username': None, 'language_code': 'ru', 'count_exec_scripts': 1, 'created_at': '19-05-2022 02:12', 'modified_at': '19-05-2022 02:12'}}