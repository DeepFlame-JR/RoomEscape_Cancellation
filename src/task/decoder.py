import sys, os
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import common

import datetime, platform
from dateutil.relativedelta import relativedelta

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from seleniumrequests import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def Tempo_Rubato():
    try:
        counter = common.TimeCounter("Tempo Rubato")

        if 'Windows' in platform.platform():
            options = webdriver.ChromeOptions()
            driver = Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        else:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        available_slots = []
        url = 'http://decoder.kr/?page_id=7082'
        driver.get(url)

        form_id = driver.find_element(By.CLASS_NAME, 'ab-booking-form').get_attribute('data-form_id')
        # 최근 6개월
        for i in range(6) :
            if i == 0:
                re_url = 'http://decoder.kr/wp-admin/admin-ajax.php?action=ab_render_time&form_id=%s&cart_key=0' \
                         % form_id
            else:
                next_button = driver.find_element(By.CLASS_NAME, 'picker__nav--next')
                next_button.click()
                time.sleep(1)
                target_date = datetime.date.today() + relativedelta(months=i)
                re_url = 'http://decoder.kr/wp-admin/admin-ajax.php?action=ab_render_time&form_id=%s&selected_date=%s&cart_key=0' \
                        % (form_id, str(datetime.date(target_date.year, target_date.month, 1)))

            s = driver.request('GET', re_url)
            info = s.json()
            if not info['success']:
                raise "Can't get response"

            days = dict(info['slots'])
            for day in days.values():
                soup = BeautifulSoup(day, 'html.parser')
                buttons = soup.find_all('button')[1:]
                for button in buttons:
                    if button['disabled'] == 'disabled':
                        available_slots.append(button['value'])

        driver.close()
        counter.end()
        return available_slots
    except Exception as e:
        print(e)