import time
import datetime
import chromedriver_binary # 必須
import warnings
import random
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

from logging import StreamHandler, Formatter, INFO, getLogger

from config import LoginInfo, LineNotifyToken


# 設定値#########################################################################################################
min_sleeptime = 1
max_sleeptime = 3
waittime = 1 #driverのタイムアウト時間

URL = 'https://www1.kenkou-p.hitachi-kenpo.or.jp/kenpoLogin/contents1/KIdLoginAction.do?pageFrom=00&viewNum=5'

line_notification_flag = True
###############################################################################################################


# Python警告非表示設定
warnings.simplefilter('ignore', DeprecationWarning)


class LoginBotHiKenpo:
    def __init__(self, id ,pw):

        self.id = id
        self.pw = pw

        # set option
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--lang=ja')

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.wtime = waittime


    def send_line_notify(self, line_notify_token, notification_message):
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': notification_message}
        requests.post(line_notify_api, headers = headers, data = data)

    
    def login(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, self.wtime)
        
        wait.until(EC.visibility_of_all_elements_located)
        time.sleep(random.randint(min_sleeptime, max_sleeptime))
        
        element_id_box = self.driver.find_element_by_id('loginId')
        element_id_box.send_keys(self.id)
        element_pw_box = self.driver.find_element_by_id('loginPW')
        element_pw_box.send_keys(self.pw)

        time.sleep(random.randint(min_sleeptime, max_sleeptime))
        
        element_login_btn = self.driver.find_element_by_xpath('//*[@id="mainDiv"]/div[2]/div[3]/button[2]')
        element_login_btn.click()

        if line_notification_flag:
            self.send_line_notify(LineNotifyToken.TOKEN, 'MY HEALTH WEB にログインしました。at:'+ str(datetime.datetime.now()))

        time.sleep(10)

    def quit(self):
        self.driver.quit()



model = LoginBotHiKenpo(id=LoginInfo.ID, pw=LoginInfo.PW)
model.login(URL)

model.quit()
