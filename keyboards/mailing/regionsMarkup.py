from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


regions_markup = InlineKeyboardMarkup(row_width=1, one_time_keyboard=True, inline_keyboard=
        [
            [InlineKeyboardButton(text="Вінницька область",callback_data='Вінницька область')],
            [InlineKeyboardButton(text="Волинська область", callback_data="Волинська область")],
            [InlineKeyboardButton(text="Дніпропетровська область", callback_data="Дніпропетровська область")],
            [InlineKeyboardButton(text="Донецька область", callback_data="Донецька область")],
            [InlineKeyboardButton(text="Житомирська область", callback_data="Житомирська область")],
            [InlineKeyboardButton(text="Закарпатська область", callback_data="Закарпатська область")],
            [InlineKeyboardButton(text="Запорізька область", callback_data="Запорізька область")],
            [InlineKeyboardButton(text="Івано-Франківська область", callback_data="Івано-Франківська область")],
            [InlineKeyboardButton(text="Київська область", callback_data="Київська область")],
            [InlineKeyboardButton(text="Кіровоградська область", callback_data="Кіровоградська область")],
            [InlineKeyboardButton(text="Луганська область", callback_data="Луганська область")],
            [InlineKeyboardButton(text="Львівська область", callback_data="Львівська область")],
            [InlineKeyboardButton(text="Миколаївська область", callback_data="Миколаївська область")],
            [InlineKeyboardButton(text="Одеська область", callback_data="Одеська область")],
            [InlineKeyboardButton(text="Полтавська область", callback_data="Полтавська область")],
            [InlineKeyboardButton(text="Рівненська область", callback_data="Рівненська область")],
            [InlineKeyboardButton(text="Сумська область", callback_data="Сумська область")],
            [InlineKeyboardButton(text="Тернопільська область", callback_data="Тернопільська область")],
            [InlineKeyboardButton(text="Харківська область", callback_data="Харківська область")],
            [InlineKeyboardButton(text="Херсонська область", callback_data="Херсонська область")],
            [InlineKeyboardButton(text="Хмельницька область", callback_data="Хмельницька область")],
            [InlineKeyboardButton(text="Черкаська область", callback_data="Черкаська область")],
            [InlineKeyboardButton(text="Чернівецька область", callback_data="Чернівецька область")],
            [InlineKeyboardButton(text="Чернігівська область", callback_data="Чернігівська область")],
            [InlineKeyboardButton(text="м. Київ", callback_data="м. Київ")],
            [InlineKeyboardButton(text="⬅️Відмінити", callback_data="cancel")]
        ]
    )