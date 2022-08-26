from ast import pattern
import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import redis
import time
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from config import API_KEY, OS
import os
from parser import Parser
from imagePreparator import ImagePreparator
import json
import re

logging.basicConfig(level=logging.WARNING, filename='log/redis-log.txt')

async def parse_photo():
    try:
        options = Options()
        if OS == 'Windows':
            options.add_argument('--disable-gpu')
            options.add_experimental_option('excludeSwitches', ['enable-automation',"enable-logging"])
        elif OS == 'Ubuntu':
            os.environ['DISPLAY'] = ':10.0'
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--remote-debugging-port=9230")
            options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("window-size=1920,1080")
        options.add_argument('log-level=3')
        proxy = "185.173.26.47:41659"
        options.add_argument(f'--proxy-server={proxy}')
        webd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        wd = Parser(webd)
        wd.openPage('https://map.ukrainealarm.com')
        # wd.setLocalStorage('darkMode', 'true')

        webd.refresh()
        await asyncio.sleep(2)
        # await wd.wait('//div[@id="map"]/*[name()="svg"]/*[name()="g"]//*[@id="a"]')
        # await asyncio.sleep(1)
        wd.getImage('screenshot.png')
        image = ImagePreparator()
        image.cutImage('screenshot.png')
        print('finished')
        webd.stop_client()
        webd.quit()
    except Exception as ex:
        with open('log/parser-log.txt', 'a') as file:
            file.write(str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n' + str(ex) + '\n')
        logging.exception('\n'+'Parse photo log! ' + '\n' + str(datetime.now().strftime("%d-%m-%Y %H:%M"))+ '\n')


def api_parse_info():
    headers = {
         "X-API-Key": API_KEY
    }
    url = 'https://alerts.com.ua/api/states'
    req = requests.get(url, headers=headers)
    res = json.loads(req.text)
    # pattern = r'(.+)(:?\..+)'
    # last_update = re.search(pattern, res['last_update']).group(1)
    for i in res["states"]:
            clear_date = datetime.fromisoformat(i['changed']).strftime("%H:%M %d-%m-%Y")
            i['changed'] = clear_date
            # i['last_update'] = str(datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S').strftime("%H:%M %d-%m-%Y"))
            i.pop('id')
    return res['states']

def main():
    # parse_photo()
    # api_parse_info()
    # get_updated_regions()
    pass


if __name__ == '__main__':
    main()