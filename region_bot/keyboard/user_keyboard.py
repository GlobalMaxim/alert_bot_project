from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton, ReplyKeyboardRemove

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Увімкнути сповіщення про тривогу"),
        ]
    ],
    resize_keyboard=True
)

menu_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Вимкнути сповіщення про тривогу"),
        ]
    ],
    resize_keyboard=True
)