from datetime import datetime
from aiogram.types import ParseMode, ChatJoinRequest
from mailing.mailing import Mailing
from telebot import dp, bot
from aiogram.types import Message, ReplyKeyboardRemove
from config import admin_id, CHANEL_ID, ANSWER_TEXT
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from keyboards.default.menu import menu, menu_2, show_chanels
from keyboards.mailing.regionsMarkup import regions_markup
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from telegram_redis.redisPreparation import Redis_Preparation
from utils.misc.throttling import rate_limit
import logging

logging.basicConfig(level=logging.WARNING, filename='log/user_handlers-log.txt')

async def check_sub_chanel(chanel_id, user_id):
    chat_member = await bot.get_chat_member(chanel_id, user_id)
    if chat_member['status'] != 'left':
        return True
    else:
        return False

@dp.chat_join_request_handler()
async def start_user(message: Message | ChatJoinRequest):
    try:
        print('New invite user')
        # if type(message) == ChatJoinRequest:
        #     await message.approve()
        chat_id = message.from_user.id
        # if await check_sub_chanel(CHANEL_ID[0], chat_id):
        r = Redis_Preparation()
        r.create_new_user_to_redis(message)
        
        name = message.from_user.first_name
        mail = Mailing()
        is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
        if is_user_uses_alert == True:
            markup = menu_2
        else:
            markup = menu
        await bot.send_message(chat_id=chat_id, text=f'✅ Привіт, {name}! Це офіційний бот, що інформує про повітряну тривогу в будь-якій області України.\n\n⚡️Командою /region обери свою область', reply_markup=markup)
        # else:
        #     msg = await bot.send_message(chat_id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
        #     await bot.delete_message(chat_id, msg['message_id'])
        #     await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
    except:
        logging.exception('\n'+'Start User log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

@rate_limit(limit=10)
# @dp.chat_join_request_handler()
@dp.message_handler(CommandStart())
async def start_user(message: Message | ChatJoinRequest):
    try:
        # if type(message) == ChatJoinRequest:
        #     await message.approve()
        chat_id = message.from_user.id
        if await check_sub_chanel(CHANEL_ID[0], chat_id):
            r = Redis_Preparation()
            r.create_new_user_to_redis(message)
            
            name = message.from_user.first_name
            mail = Mailing()
            is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
            if is_user_uses_alert == True:
                markup = menu_2
            else:
                markup = menu
            await bot.send_message(chat_id=chat_id, text=f'✅ Привіт, {name}! Це офіційний бот, що інформує про повітряну тривогу в будь-якій області України.\n\n⚡️Командою /region обери свою область', reply_markup=markup)
        else:
            msg = await bot.send_message(chat_id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id, msg['message_id'])
            await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
    except:
        logging.exception('\n'+'Start User log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

@dp.message_handler(Text(equals=["🗺Отримати карту повітряних тривог"]))
@rate_limit(limit=10)
async def run(message: Message):
    try:
        chat_id = message.from_user.id
        if await check_sub_chanel(CHANEL_ID[0], chat_id):
            mail = Mailing()
            is_user_uses_alert = mail.is_user_alert_active(chat_id)
            if is_user_uses_alert == True:
                markup = menu_2
            else:
                markup = menu
            # if chat_id not in admin_id:
            #     notify_admin=f"Пользователь с ником @{message.from_user.username}, {message.from_user.first_name}, {message.from_user.id} воспользовался ботом"
            #     await bot.send_message(admin_id[0], text=notify_admin, disable_notification=True)
            # await message.answer('Зачекайте...')
            r = Redis_Preparation()
            res = r.get_regions_from_redis()
            current_date = str(datetime.now().strftime('%H:%M %d-%m-%Y'))
            if len(res['regions']) > 0:
                await message.answer('Тривоги працюють в наступних областях:')
                for i in res['regions']:
                    await message.answer(f"🛑 <b>{i['name']}</b>\nПочаток тривоги у {i['changed']}\n@Official_alarm_bot", parse_mode=ParseMode.HTML)
                # await message.answer('Зачекайте, завантажується фото...')
                await message.answer_photo(photo=open('screenshot.png', 'rb'), caption=f"<b>❗️Карта повітряних тривог станом на {current_date}</b>\n\n@Official_alarm_bot", parse_mode=ParseMode.HTML, reply_markup=markup)
           
                # await message.answer(f"<b>❗️Карта повітряних тривог станом на {res['regions'][0]['last_update']}</b>\n\n@Official_alarm_bot", parse_mode=ParseMode.HTML, reply_markup=markup)
            else:
                
                await message.answer('Тривог зараз немає!')
            r.create_user_updates_to_redis(message)
        else:
            msg = await bot.send_message(chat_id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id, msg['message_id'])
            await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
    except:
        logging.exception('\n'+'Get Alert Map log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

@dp.callback_query_handler(text='subchanneldone')
async def channeldone(message: Message):
    try:
        chat_id = message.from_user.id
        await bot.delete_message(chat_id, message.message.message_id)
        if await check_sub_chanel(CHANEL_ID[0], chat_id):
            mail = Mailing()
            is_user_uses_alert = mail.is_user_alert_active(chat_id)
            if is_user_uses_alert == True:
                markup = menu_2
            else:
                markup = menu
            await bot.send_message(chat_id=chat_id, text=f'Доступ разблоковано!', reply_markup=markup)
        else:
            await bot.send_message(chat_id, ANSWER_TEXT, reply_markup=show_chanels())
    except:
        logging.exception('\n'+'Callback subchaneldone log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        

\
@dp.message_handler(commands=['region'])
@rate_limit(limit=5)
@dp.message_handler(Text(equals=["📢Увімкнути повідомлення про тривогу"]))
async def send_mail(message: Message):
    try:
        chat_id = message.from_user.id
        if await check_sub_chanel(CHANEL_ID[0], message.from_user.id):
            await message.answer(text='📍Оберіть місце, де ви знаходитесь:', reply_markup=regions_markup)
        else:
            msg = await bot.send_message(chat_id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id, msg['message_id'])
            await bot.send_message(message.from_user.id, ANSWER_TEXT, reply_markup=show_chanels())
    except:
        logging.exception('\n'+'Turn On alert log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')

@dp.callback_query_handler()
async def save_user_region(call: CallbackQuery):
    mail = Mailing()
    try:
        if call.data == 'cancel':
            await call.message.edit_reply_markup()
            await call.message.delete()
            await bot.send_message(chat_id=call.from_user.id, text= f'❗️Ви не обрали регіон')
            mail.stop_mailing(call)
        else:
            await bot.answer_callback_query(callback_query_id=call.id, text= f'{call.data}', cache_time=1)
            await call.message.edit_reply_markup()
            await mail.save_user_mailing(call)
            await bot.send_message(chat_id=call.from_user.id, text= f'✅Вітаю, ви будете отримумати сповіщення при повітряній тривозі у <b>"{call.data}"</b>', parse_mode=ParseMode.HTML, reply_markup=menu_2)
            await mail.check_is_active_user_region(bot, call)
        # await call.answer()
        # print('Answered')
    except:
        logging.exception('\n'+'Save User Region log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')
        

@dp.message_handler(Text(equals=["❌Вимкнути сповіщення про тривогу"]))
async def send_mail(message: Message):
    try:
        if await check_sub_chanel(CHANEL_ID[0], message.from_user.id):
            mail = Mailing()
            mail.stop_mailing(message)
            await message.answer(text='❗️Ви не будете отримувати сповіщення про тривоги', reply_markup=menu)
        else:
            msg = await bot.send_message(message.from_user.id, "Доступ заблоковано!", reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(message.from_user.id, msg['message_id'])
            await bot.send_message(message.from_user.id, ANSWER_TEXT, reply_markup=show_chanels())
    except:
        logging.exception('\n'+'Turn Off Alert log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


@dp.message_handler(CommandHelp())
async def bot_help(message: Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку',
        '/restart - Перезапустить'
    ]
    await message.answer('\n'.join(text))

@dp.message_handler(Text('Слава Україні!🇺🇦'))
async def register_user(message: Message):
    await message.answer('Героям Слава!🇺🇦')

@rate_limit(limit=5)
@dp.message_handler()
async def register_user(message: Message):
    mail = Mailing()
    is_user_uses_alert = mail.is_user_alert_active(message.from_user.id)
    if is_user_uses_alert == True:
        markup = menu_2
    else:
        markup = menu
    chat_id = message.from_user.id
    name = message.from_user.first_name
    await bot.send_message(chat_id=chat_id, text=f'{name}, спробуйте ще раз', reply_markup=markup)


