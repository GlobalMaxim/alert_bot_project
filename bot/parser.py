from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys



class Parser():
    def __init__(self, driver):
        self.driver = driver

    def openPage(self, url):
        self.driver.get(url)
    
    def refresh(self):
        self.driver.refresh()
    
    def clearLocalStorage(self):
        self.driver.execute_script("window.localStorage.clear();")
    
    def setLocalStorage(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def getImage(self, name):
        self.driver.save_screenshot(name)

    def wait(self, path):
        WebDriverWait(self.driver, 10, poll_frequency=1,
                             ignored_exceptions=[NoSuchElementException,
                                                 ElementNotVisibleException,
                                                 ElementNotSelectableException])\
                                                     .until(EC.visibility_of_all_elements_located((By.XPATH,path)))

    
    def getRegions(self):
        dict = {}
        self.wait('//div[@class="amo-map-alarms-list"]/div')
        elements = self.driver.find_elements_by_xpath('//div[@class="amo-map-alarms-list"]/div')
        
        for elem in elements:
            region = elem.find_element(By.XPATH, './div[2]/div[1]').text
            time_al = elem.find_element(By.XPATH, './div[2]/div[2]/div[2]/span').text
            if 'область' in region:
                dict[region] = time_al
            elif 'місто' in region:
                dict[region] = time_al
        return dict

    def changeScale(self):
        try:
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.SUBTRACT).key_up(Keys.CONTROL).perform()
            print('Scrolled')
        except Exception:
            print(Exception)