from ast import pattern
import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import requests
import redis
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from bot.config import API_KEY
import os
from bot.parser import Parser
from bot.utils.imagePreparator import ImagePreparator
import json
import re

logging.basicConfig(level=logging.WARNING, filename='bot/log/redis-log.txt')


async def parse_photo():
    try:
        options = Options()
        options.add_argument("--remote-debugging-port=9230")
        options.add_argument("start-maximized")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--log-level=3')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        webd = webdriver.Chrome(options=options)
        wd = Parser(webd)
        wd.openPage('https://alerts.in.ua')
        wd.setLocalStorage('darkMode', 'true')
        wd.setLocalStorage('showOblastLabels', 'true')
        wd.setLocalStorage('showRaion', "false")
        wd.setLocalStorage('showDurationGradient', "true")
        wd.setLocalStorage('interactiveMap', "true")
        wd.setLocalStorage('liteMap', "false")

        webd.refresh()
        await asyncio.sleep(4)
        # await wd.wait('//div[@id="map"]/*[name()="svg"]/*[name()="g"]//*[@id="a"]')
        # await asyncio.sleep(1)
        wd.getImage('bot/screenshot.png')
        image = ImagePreparator()
        image.cutImage('bot/screenshot.png')
        print('finished')
        webd.stop_client()
        webd.quit()
    except Exception as ex:
        with open('bot/log/parser-log.txt', 'a') as file:
            file.write(str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n' + str(ex) + '\n')
        logging.exception('\n'+'Parse photo log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


def api_parse_info():
    try:
        headers = {
            "X-API-Key": API_KEY
        }
        url = 'https://alerts.com.ua/api/states'
        req = requests.get(url, headers=headers)
        res = json.loads(req.text)
        # with open('bot/regions.json') as f:
        #     res = json.load(f)

        # pattern = r'(.+)(:?\..+)'
        # last_update = re.search(pattern, res['last_update']).group(1)
        for i in res["states"]:
            if i["name"] == "Луганська область":
                i['changed'] = "19:45 04-04-2022"
            else:
                clear_date = datetime.fromisoformat(i['changed']).strftime("%H:%M %d-%m-%Y")
                i['changed'] = clear_date
                # i['last_update'] = str(datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S').strftime("%H:%M %d-%m-%Y"))
        return res['states']
    except:
        return None

def main():
    # parse_photo()
    # api_parse_info()
    # get_updated_regions()
    pass


if __name__ == '__main__':
    main()