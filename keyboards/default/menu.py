from re import L
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardRemove
from config import CHANEL_ID
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗺Отримати карту повітряних тривог"),
        ],
        [
            KeyboardButton(text="📢Увімкнути повідомлення про тривогу"),
        ]
    ],
    resize_keyboard=True
)

menu_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗺Отримати карту повітряних тривог"),
        ],
        [
            KeyboardButton(text="❌Вимкнути сповіщення про тривогу"),
        ]
    ],
    resize_keyboard=True
)
def show_chanels():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn = InlineKeyboardButton(text = "✍🏻Підписатися", url = CHANEL_ID[1])
    keyboard.insert(btn)
    btnDone = InlineKeyboardButton(text="✅ Готово", callback_data='subchanneldone')
    keyboard.insert(btnDone)
    return keyboard