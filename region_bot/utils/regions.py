from bot.config import  TOKEN_1, TOKEN_2, TOKEN_3, TOKEN_5, TOKEN_6, TOKEN_8, TOKEN_9, TOKEN_12, TOKEN_13, TOKEN_14, TOKEN_15, TOKEN_16, TOKEN_17, TOKEN_18, TOKEN_19, TOKEN_21, TOKEN_22, TOKEN_23, TOKEN_24

regions = [
    {"id": 1, "token": TOKEN_1, "name": "Вінницька область",},
    {"id": 2, "token": TOKEN_2, "name": "Волинська область",},
    {"id": 3, "token": TOKEN_3, "name": "Дніпропетровська область",},
    {"id": 5, "token": TOKEN_5, "name": "Житомирська область",},
    {"id": 6, "token": TOKEN_6, "name": "Закарпатська область",},
    {"id": 8, "token": TOKEN_8, "name": "Івано-Франківська область",},
    {"id": 9, "token": TOKEN_9, "name": "Київська область",},
    {"id": 12, "token": TOKEN_12, "name": "Львівська область",},
    {"id": 13, "token": TOKEN_13, "name": "Миколаївська область",},
    {"id": 14, "token": TOKEN_14, "name": "Одеська область",},
    {"id": 15, "token": TOKEN_15, "name": "Полтавська область",},
    {"id": 16, "token": TOKEN_16, "name": "Рівненська область",},
    {"id": 17, "token": TOKEN_17, "name": "Сумська область",},
    {"id": 18, "token": TOKEN_18, "name": "Тернопільська область",},
    {"id": 19, "token": TOKEN_19, "name": "Харківська область",},
    {"id": 21, "token": TOKEN_21, "name": "Хмельницька область",},
    {"id": 22, "token": TOKEN_22, "name": "Черкаська область",},
    {"id": 23, "token": TOKEN_23, "name": "Чернівецька область",},
    {"id": 24, "token": TOKEN_24, "name": "Чернігівська область",}
]

def get_region_data(region_id):
    for region in regions:
        if str(region['id']) == str(region_id):
            return region
        