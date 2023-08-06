from datetime import datetime, timezone, timedelta
import re
import logging


from aiogram.utils.exceptions import BotBlocked,CantInitiateConversation, ChatNotFound, UserDeactivated, CantTalkWithBots
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ParseMode, ChatJoinRequest
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Text

from telebot import dp, bot
from bot.mailing.mailing import Mailing
from bot.config import ADMIN_ID, CHANEL_ID, ANSWER_TEXT
from bot.keyboards.default.menu import menu, menu_2, show_chanels
from bot.keyboards.mailing.regionsMarkup import regions_markup
from bot.telegram_redis.redisPreparation import Redis_Preparation
from bot.utils.misc.throttling import rate_limit

logging.basicConfig(level=logging.WARNING, filename='bot/log/user_handlers-log.txt')

async def check_sub_chanel(chanel_id, user_id):
    try:
        chat_member = await bot.get_chat_member(chanel_id, user_id)
        if chat_member['status'] != 'left':
            return True
        else:
            return False
    except:
        logging.exception('\n'+'check_sub_chanel log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


@dp.chat_join_request_handler()
async def start_user(message: Message | ChatJoinRequest):
    try:
        chat_id = message.from_user.id
        r = Redis_Preparation()
        r.create_new_user_to_redis(message)
        
        name = message.from_user.first_name
        await bot.send_message(chat_id=chat_id, text=f'✅ Привіт, {name}! Це офіційний бот, що інформує про повітряну тривогу в будь-якій області України.\n\n⚡️Командою /region обери свою область', reply_markup=menu)
    except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
        pass
    except:
        logging.exception('\n'+'Start User log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

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
            await bot.send_message(chat_id=chat_id, text=f'✅ Привіт, {name}! Це офіційний бот, що інформує про повітряну тривогу в будь-якій області України.\n\n⚡️Командою /region обери свою область', reply_markup=menu)
        else:
            await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
    except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
        pass
    except:
        logging.exception('\n'+'Start User log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

@dp.message_handler(Text(equals=["🗺Отримати карту повітряних тривог"]))
@rate_limit(limit=7)
async def run(message: Message):
    try:
        chat_id = message.from_user.id
        if await check_sub_chanel(CHANEL_ID[0], chat_id):
            r = Redis_Preparation()
            res = r.get_regions_from_redis()
            current_datetime = datetime.now() + timedelta(hours=1)
            current_date = current_datetime.strftime('%H:%M %d-%m-%Y')
            if len(res['regions']) > 0:
                await message.answer('Тривоги працюють в наступних областях:')
                for i in res['regions']:
                    await message.answer(f"🛑 <b>{i['name']}</b>\nПочаток тривоги у {i['changed']}\n@Official_alarm_bot", parse_mode=ParseMode.HTML)
                await message.answer_photo(photo=open('bot/screenshot.png', 'rb'), caption=f"<b>❗️Карта повітряних тривог станом на {current_date}</b>\n\n@Official_alarm_bot", parse_mode=ParseMode.HTML)
            else:
                
                await message.answer('Тривог зараз немає!')
            r.create_user_updates_to_redis(message)
        else:
            msg = await bot.send_message(chat_id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id, msg['message_id'])
            await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
    except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
        pass
    except:
        logging.exception('\n'+'Get Alert Map log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

@dp.message_handler(commands=['region'])
@rate_limit(limit=5)
@dp.message_handler(Text(equals=["Обрати регіон"]))
async def send_mail(message: Message):
    try:
        chat_id = message.from_user.id
        if await check_sub_chanel(CHANEL_ID[0], message.from_user.id):
            await message.answer(text='📍Оберіть місце, де ви знаходитесь:', reply_markup=regions_markup)
        else:
            msg = await bot.send_message(chat_id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id, msg['message_id'])
            await bot.send_message(message.from_user.id, ANSWER_TEXT, reply_markup=show_chanels())
    except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
        pass
    except:
        logging.exception('\n'+'Turn On alert log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


@dp.callback_query_handler()
async def save_user_region(call: CallbackQuery):
    
    if call.data == 'subchanneldone':
        try:
            chat_id = call.from_user.id
            # await bot.delete_message(chat_id, message.message.message_id)
            await bot.delete_message(chat_id, call.message.message_id)
            # await call.message.delete()
            if await check_sub_chanel(CHANEL_ID[0], chat_id):
                await bot.send_message(chat_id=chat_id, text=f'Доступ разблоковано!', reply_markup=menu)
            else:
                await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
            await call.answer()
        except:
            logging.exception('\n'+'Callback subchaneldone log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

    elif call.data == 'cancel':
        try:
            await call.message.edit_reply_markup()
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            await bot.send_message(chat_id=call.from_user.id, text= f'❗️Ви не обрали регіон', reply_markup=menu)
            await call.answer()
        except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated):
            pass
        except:
            logging.exception('\n'+'Save User Region log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
 
@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/restart - Перезапустить'
    ]
    await message.answer('\n'.join(text))

@rate_limit(limit=10)
@dp.message_handler()
async def register_user(message: Message):
    try:
        chat_id = message.from_user.id
        name = message.from_user.first_name
        await bot.send_message(chat_id=chat_id, text=f'{name}, спробуйте ще раз', reply_markup=menu)
    except (BotBlocked, CantInitiateConversation, ChatNotFound, UserDeactivated, CantTalkWithBots):
        pass

