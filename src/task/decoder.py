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


def Tempo_Rubato_no_requests():
    Log = common.Logger()
    driver, counter = None, None

    try:
        m = 0
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

        # 접속 확인
        picker = []
        for i in range(10):
            time.sleep(1)
            picker = driver.find_elements(By.CLASS_NAME, 'picker__box')
            if len(picker) != 0: break
        if len(picker) == 0: # 10초동안 접속되지 않으면 종료
            raise "Can't access picker box"

        today = datetime.date.today()
        current_date = datetime.datetime(today.year, today.month, today.day)
        for m in range(6):
            if m > 0:  # 다음 달의 달력을 보기 위해서 Next 버튼을 클릭한다.
                driver.find_element(By.CLASS_NAME, 'picker__nav--next').click()
                time.sleep(2)
                current_date += relativedelta(months=1)
                current_date = datetime.datetime(current_date.year, current_date.month, 1)

            td_list = driver.find_elements(By.TAG_NAME, 'td')
            disable_dict = {}
            for td in td_list:
                day_str = td.find_element_by_tag_name('div').get_attribute('aria-label')
                day_datetime = datetime.datetime.strptime(day_str, '%Y년 %B %d일')
                disable_dict[day_datetime] = td.find_element_by_tag_name('div').get_attribute('aria-disabled')

            candidates = []  # 해당 월에 가능한 날짜
            for i in range(31):
                c = current_date + datetime.timedelta(days=i)
                if current_date.month == c.month and not disable_dict[c]:
                    candidates.append(c)

            for candidate in candidates:
                # 달력 객체를 들고와서 특정일자를 클릭한다.
                td_list = driver.find_elements(By.TAG_NAME, 'td')
                for td in td_list:
                    day_str = td.find_element_by_tag_name('div').get_attribute('aria-label')
                    day_datetime = datetime.datetime.strptime(day_str, '%Y년 %B %d일')
                    if (day_datetime - candidate).days == 0:
                        td.click()
                        time.sleep(2)
                        # 클릭하여 나타나는 시간이 예약가능한지 확인한다.
                        time_tables = driver.find_element(By.CLASS_NAME, 'ab-time-screen').find_elements(By.TAG_NAME,
                                                                                                        'button')
                        time_tables = time_tables[1:]  # 처음 날짜 표시는 제외
                        for time_table in time_tables:
                            if not time_table.get_attribute('disabled'):
                                cancellation_list.append(time_table.get_attribute('value'))
                        break
        return cancellation_list
    except Exception as e:
        Log.error(e)
    finally:
        Log.info("Month finish in " + str(m) + "month.")
        if driver:
            driver.quit()
        if counter:
            counter.end()