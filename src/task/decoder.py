import sys, os, platform, time, datetime
if 'Windows' not in platform.platform():
    os.environ['TZ'] = 'Asia/Seoul'
    time.tzset()

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import common

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from seleniumrequests import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def Tempo_Rubato():
    Log = common.Logger()
    driver, counter = None, None
    i = -1
    try:
        Log.info("Crawling Tempo Rubato")
        counter = common.TimeCounter("Tempo Rubato")

        options = webdriver.ChromeOptions()
        if 'Windows' not in platform.platform():
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("--single-process")
            options.add_argument("--disable-dev-shm-usage")
        driver = Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)

        cancellation_list = []
        url = 'http://decoder.kr/book-rubato/'
        driver.get(url)

        form_id = driver.find_element(By.CLASS_NAME, 'ab-booking-form').get_attribute('data-form_id')
        while True:
            i += 1
            if i == 0:
                re_url = 'http://decoder.kr/wp-admin/admin-ajax.php?action=ab_render_time&form_id=%s&cart_key=0' \
                         % form_id
            else:
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
                    if 'booked' not in button['class']:
                        cancellation_list.append(button['value'])

            try:
                next_button = driver.find_element(By.CLASS_NAME, 'picker__nav--next')
                next_button.click()
                time.sleep(2)
            except:
                Log.info("picker__nav--next is not existed")
                break
        return cancellation_list

    except Exception as e:
        Log.error(e)
    finally:
        Log.info("Month finish in " + str(i) + "month.")
        if driver:
            driver.quit()
        if counter:
            counter.end()