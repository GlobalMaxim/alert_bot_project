from aiogram import Bot

def send_text(region):
    if region['alert'] == True:
        return f'🔴<b>Повітряна тривога у "{region["name"]}"</b>\nПочаток тривоги у {region["changed"]}\n\n@Official_alarm_bot'
    elif region['alert'] == False:
        return f'🟢<b>Відбій повітряної тривоги у "{region["name"]}"</b>\nОновлено у {region["changed"]}\n\n@Official_alarm_bot'

async def send_regions_to_chanel(region, bot: Bot):
        match region['name']:
            case "Черкаська область":
                await bot.send_message(-1001524523161, send_text(region), parse_mode='HTML')
            case "Харківська область":
                await bot.send_message(-1001701593241, send_text(region), parse_mode='HTML')
            case "Вінницька область":
                await bot.send_message(-1001700738280, send_text(region), parse_mode='HTML')
            case "Київська область":
                await bot.send_message(-1001744303536, send_text(region), parse_mode='HTML')
            case "Одеська область":
                await bot.send_message(-1001790545853, send_text(region), parse_mode='HTML')
            case "Дніпропетровська область":
                await bot.send_message(-1001841011801, send_text(region), parse_mode='HTML')
            case "Львівська область":
                await bot.send_message(-1001819333583, send_text(region), parse_mode='HTML')
            case "Рівненська область":
                await bot.send_message(-1001772963484, send_text(region), parse_mode='HTML')
            case "Черкаська область":
                await bot.send_message(-1001804699733, send_text(region), parse_mode='HTML')
            case "Сумська область":
                await bot.send_message(-1001889349479, send_text(region), parse_mode='HTML')
            case "Полтавська область":
                await bot.send_message(-1001884477607, send_text(region), parse_mode='HTML')
            case "Тернопільска область":
                await bot.send_message(-1001832195839, send_text(region), parse_mode='HTML')
            case "Хмельницька область":
                await bot.send_message(-1001121976501, send_text(region), parse_mode='HTML')
            case "Чернігівська область":
                await bot.send_message(-1001818028503, send_text(region), parse_mode='HTML')
            case "Житомирська область":
                await bot.send_message(-1001881765476, send_text(region), parse_mode='HTML')
            case "Івано-Франківська область":
                await bot.send_message(-1001823730708, send_text(region), parse_mode='HTML')
            case "Миколаївська область":
                await bot.send_message(-1001879590389, send_text(region), parse_mode='HTML')
            case "Волинська область":
                await bot.send_message(-1001243567511, send_text(region), parse_mode='HTML')
            case "Чернівецька область":
                await bot.send_message(-1001841438028, send_text(region), parse_mode='HTML')