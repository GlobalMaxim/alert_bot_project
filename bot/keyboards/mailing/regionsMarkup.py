from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


regions_markup = InlineKeyboardMarkup(row_width=1, one_time_keyboard=True, inline_keyboard=
        [
            [InlineKeyboardButton(text="Вінницька область",url="https://t.me/Vinnytsia_alarm_bot")],
            [InlineKeyboardButton(text="Волинська область", url="https://t.me/Volyn_alarm_bot")],
            [InlineKeyboardButton(text="Дніпропетровська область", url="https://t.me/Dnipro_alarm_bot")],
            # [InlineKeyboardButton(text="Дніпропетровська область", url="https://t.me/Dnipro_alarm_bot")],
            # [InlineKeyboardButton(text="Донецька область", callback_data="Донецька область")],
            [InlineKeyboardButton(text="Житомирська область", url="https://t.me/Zhytomyr_alarm_bot")],
            [InlineKeyboardButton(text="Запорізька область", url="https://t.me/Zp_alarm_bot")],
            [InlineKeyboardButton(text="Івано-Франківська область", url="https://t.me/Frank_alarm_bot")],
            # [InlineKeyboardButton(text="Київська область", callback_data="Київська область")],
            # [InlineKeyboardButton(text="Кіровоградська область", callback_data="Кіровоградська область")],
            # [InlineKeyboardButton(text="Луганська область", callback_data="Луганська область")],
            [InlineKeyboardButton(text="Львівська область", url="https://t.me/Liviv_alarm_bot")],
            [InlineKeyboardButton(text="Миколаївська область", url="https://t.me/Mykolaiv_alarm_bot")],
            [InlineKeyboardButton(text="Одеська область", url="https://t.me/Odes_alarm_bot")],
            [InlineKeyboardButton(text="Полтавська область", url="https://t.me/Poltava_alarm_bot")],
            [InlineKeyboardButton(text="Рівненська область", url="https://t.me/Rivn_alarm_bot")],
            [InlineKeyboardButton(text="Сумська область", url="https://t.me/Summy_alarm_bot")],
            [InlineKeyboardButton(text="Тернопільська область", url="https://t.me/Ternopil_alarm_bot")],
            [InlineKeyboardButton(text="Харківська область", url="https://t.me/Harkiv_alarm_bot")],
            # [InlineKeyboardButton(text="Херсонська область", callback_data="Херсонська область")],
            [InlineKeyboardButton(text="Хмельницька область", url="https://t.me/Khmlv_alarm_bot")],
            [InlineKeyboardButton(text="Черкаська область", url="https://t.me/Cherkasy_alarm_bot")],
            [InlineKeyboardButton(text="Чернівецька область", url="https://t.me/Chernivtsi_alarm_bot")],
            [InlineKeyboardButton(text="Чернігівська область", url="https://t.me/Chernihiv_alarm_bot")],
            [InlineKeyboardButton(text="Київська область", url="https://t.me/Kyiv_alarm_bot")],
            [InlineKeyboardButton(text="⬅️Відмінити", callback_data="cancel")]
        ]
    )