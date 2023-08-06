from bot.config import  TOKEN_1, TOKEN_2, TOKEN_3, TOKEN_5, TOKEN_7, TOKEN_8, TOKEN_9, TOKEN_12, TOKEN_13, TOKEN_14, TOKEN_15, TOKEN_16, TOKEN_17, TOKEN_18, TOKEN_19, TOKEN_21, TOKEN_22, TOKEN_23, TOKEN_24

regions = [
    {"id": 1, "token": TOKEN_1, "name": "Вінницька область", "link": "@Vinnytsia_alarm_bot"},
    {"id": 2, "token": TOKEN_2, "name": "Волинська область", "link": "@Volyn_alarm_bot"},
    {"id": 3, "token": TOKEN_3, "name": "Дніпропетровська область", "link": "@Dnipro_alarm_bot"},
    {"id": 5, "token": TOKEN_5, "name": "Житомирська область", "link": "@Zhytomyr_alarm_bot"},
    {"id": 7, "token": TOKEN_7, "name": "Запорізька область", "link": "@Zp_alarm_bot"},
    {"id": 8, "token": TOKEN_8, "name": "Івано-Франківська область", "link": "@Frank_alarm_bot"},
    {"id": 9, "token": TOKEN_9, "name": "Київська область", "link": "@Kyiv_alarm_bot"},
    {"id": 12, "token": TOKEN_12, "name": "Львівська область", "link": "@Liviv_alarm_bot"},
    {"id": 13, "token": TOKEN_13, "name": "Миколаївська область", "link": "@Mykolaiv_alarm_bot"},
    {"id": 14, "token": TOKEN_14, "name": "Одеська область", "link": "@Odes_alarm_bot"},
    {"id": 15, "token": TOKEN_15, "name": "Полтавська область", "link": "@poltava_alarm_bot"},
    {"id": 16, "token": TOKEN_16, "name": "Рівненська область", "link": "@Rivn_alarm_bot"},
    {"id": 17, "token": TOKEN_17, "name": "Сумська область", "link": "@Summy_alarm_bot"},
    {"id": 18, "token": TOKEN_18, "name": "Тернопільська область", "link": "@Ternopil_alarm_bot"},
    {"id": 19, "token": TOKEN_19, "name": "Харківська область", "link": "@Harkiv_alarm_bot"},
    {"id": 21, "token": TOKEN_21, "name": "Хмельницька область", "link": "@Khmlv_alarm_bot"},
    {"id": 22, "token": TOKEN_22, "name": "Черкаська область", "link": "@Cherkasy_alarm_bot"},
    {"id": 23, "token": TOKEN_23, "name": "Чернівецька область", "link": "@Chernivtsi_alarm_bot"},
    {"id": 24, "token": TOKEN_24, "name": "Чернігівська область", "link": "@Chernihiv_alarm_bot"}
]

def get_region_data(region_id):
    for region in regions:
        if str(region['id']) == str(region_id):
            return region