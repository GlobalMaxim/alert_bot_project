from datetime import datetime, timezone, timedelta
import re
import logging

from aiogram.types import ParseMode, ChatJoinRequest
from aiogram.utils.exceptions import BotBlocked,CantInitiateConversation, ChatNotFound, UserDeactivated
from aiogram.types import Message, CallbackQuery
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from region_telebot import dp, bot, region_data
from bot.telegram_redis.redisPreparation import Redis_Preparation
from bot.utils.misc.throttling import rate_limit
from bot.config import ADMIN_ID, CHANEL_ID, ANSWER_TEXT
from bot.keyboards.default.menu import show_chanels
from region_bot.keyboard.user_keyboard import menu, menu_2
from region_bot.utils.mailing import is_user_alert_active, save_user_mailing , stop_mailing, check_is_active_user_region

async def check_sub_chanel(chanel_id, user_id):
    try:
        chat_member = await bot.get_chat_member(int(chanel_id), user_id)
        if chat_member['status'] != 'left':
            return True
        else:
            return False
    except:
        logging.exception('\n'+'check_sub_chanel log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


@rate_limit(limit=10)
# @dp.chat_join_request_handler()
@dp.message_handler(CommandStart())
async def start_user(message: Message | ChatJoinRequest):
    try:
        chat_id = message.from_user.id
        r = Redis_Preparation()
        r.create_new_user_to_redis(message)
        if await check_sub_chanel(CHANEL_ID[0], chat_id):
            name = message.from_user.first_name
            await bot.send_message(chat_id=chat_id, text=f'✅ Привіт, {name}! Це офіційний бот, що інформує про повітряну тривогу в обраній області України.', reply_markup=menu)
        else:
            await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
    except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
        pass
    except:
        logging.exception('\n'+'Start User log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


@rate_limit(limit=10)
# @dp.chat_join_request_handler()
@dp.message_handler(Text(equals="Увімкнути сповіщення про тривогу"))
async def start_user(message: Message):
    try:
        if await check_sub_chanel(CHANEL_ID[0], message.from_user.id):
            save_user_mailing(message, region_data)
            await bot.send_message(chat_id=message.from_user.id, text= f'✅Вітаю, ви будете отримумати сповіщення при повітряній тривозі у <b>\"{region_data["name"]}\"</b>', parse_mode=ParseMode.HTML, reply_markup=menu_2)
            await check_is_active_user_region(bot, message, region_data)
        else:
            msg = await bot.send_message(message.from_user.id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(message.from_user.id, msg['message_id'])
            await bot.send_message(message.from_user.id, ANSWER_TEXT, reply_markup=show_chanels())
    
    except:
        logging.exception('\n'+'Save User Region log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


@dp.message_handler(Text(equals=["❌Вимкнути сповіщення про тривогу"]))
async def send_mail(message: Message):
    try:
        if await check_sub_chanel(CHANEL_ID[0], message.from_user.id):
            stop_mailing(message, region_data)
            await message.answer(text='❗️Ви не будете отримувати сповіщення про тривоги', reply_markup=menu)
        else:
            msg = await bot.send_message(message.from_user.id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(message.from_user.id, msg['message_id'])
            await bot.send_message(message.from_user.id, ANSWER_TEXT, reply_markup=show_chanels())
    except:
        logging.exception('\n'+'Turn Off Alert log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

@dp.callback_query_handler(lambda x: x.data and x.data == "subchanneldone")
async def save_user_region(call: CallbackQuery):
        try:
            chat_id = call.from_user.id
            # await bot.delete_message(chat_id, message.message.message_id)
            await call.message.delete()
            if await check_sub_chanel(CHANEL_ID[0], chat_id):
                is_active_alert = is_user_alert_active(chat_id, region_data)
                await bot.send_message(chat_id=chat_id, text=f'Доступ разблоковано!', reply_markup=menu_2 if is_active_alert else menu)
            else:
                await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
        except:
            logging.exception('\n'+'Callback subchaneldone log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        finally:
            await call.answer()
