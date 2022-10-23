from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


regions_markup = InlineKeyboardMarkup(row_width=1, one_time_keyboard=True, inline_keyboard=
        [
            [InlineKeyboardButton(text="Вінницька область",url="https://t.me/alarm_vinnytsa")],
            [InlineKeyboardButton(text="Волинська область", url="https://t.me/alarm_volyn")],
            [InlineKeyboardButton(text="Дніпропетровська область", url="https://t.me/alarm_dnipr")],
            # [InlineKeyboardButton(text="Донецька область", callback_data="Донецька область")],
            [InlineKeyboardButton(text="Житомирська область", url="https://t.me/alarm_zhitomi")],
            # [InlineKeyboardButton(text="Закарпатська область", callback_data="Закарпатська область")],
            # [InlineKeyboardButton(text="Запорізька область", callback_data="Запорізька область")],
            [InlineKeyboardButton(text="Івано-Франківська область", url="https://t.me/alarm_frank")],
            # [InlineKeyboardButton(text="Київська область", callback_data="Київська область")],
            # [InlineKeyboardButton(text="Кіровоградська область", callback_data="Кіровоградська область")],
            # [InlineKeyboardButton(text="Луганська область", callback_data="Луганська область")],
            [InlineKeyboardButton(text="Львівська область", url="https://t.me/alarm_liviv")],
            [InlineKeyboardButton(text="Миколаївська область", url="https://t.me/alarm_mykolaiv")],
            [InlineKeyboardButton(text="Одеська область", url="https://t.me/alarm_odesa")],
            [InlineKeyboardButton(text="Полтавська область", url="https://t.me/alarm_poltava")],
            [InlineKeyboardButton(text="Рівненська область", url="https://t.me/alarm_rivne")],
            [InlineKeyboardButton(text="Сумська область", url="https://t.me/alarm_sumy")],
            [InlineKeyboardButton(text="Тернопільська область", url="https://t.me/alarm_ternopil")],
            [InlineKeyboardButton(text="Харківська область", url="https://t.me/alarm_harkiv")],
            # [InlineKeyboardButton(text="Херсонська область", callback_data="Херсонська область")],
            [InlineKeyboardButton(text="Хмельницька область", url="https://t.me/alarm_khmlv")],
            [InlineKeyboardButton(text="Черкаська область", url="https://t.me/alarm_cherkassy")],
            # [InlineKeyboardButton(text="Черкаська область", callback_data='Черкаська областьhttps://t.me/+OswDcsqmIkNlNzJi')],
            [InlineKeyboardButton(text="Чернівецька область", url="https://t.me/alarm_chernivts")],
            [InlineKeyboardButton(text="Чернігівська область", url="https://t.me/alarm_chernihiv")],
            [InlineKeyboardButton(text="м. Київ", url="https://t.me/alarm_kyiv")],
            [InlineKeyboardButton(text="⬅️Відмінити", callback_data="cancel")]
        ]
    )