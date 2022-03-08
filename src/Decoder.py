import time
import datetime as dt
from dateutil.relativedelta import relativedelta
import platform
import logging
import warnings
warnings.filterwarnings('ignore')


global prev_slot, logger

def GetInfo():
    start = time.time()

    # 윈도우에서 테스트할 때와 EC2에서 실행할 때 Chrome 설정이 다름
    if 'Windows' in platform.platform():
        driver = webdriver.Chrome('task/chromedriver.exe')
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome('./chromedriver', options=options)

    available_slot = []
    try:
        # 0. 접속
        url = 'http://decoder.kr/?page_id=7082'
        driver.get(url)
        for i in range(10): # 접속 확인
            time.sleep(1)
            picker = driver.find_elements_by_class_name('picker__box')
            if len(picker) != 0: break

        if len(picker) == 0: return # 10초동안 접속되지 않으면 종료

        # 현재 달에서 가능한 datetime + 다음 달의 datetime
        today_date = dt.datetime.now()
        today_datetime = dt.datetime(today_date.year, today_date.month, today_date.day)
        for m in range(2):
            if m > 0: # 다음 달의 달력을 보기 위해서 Next 버튼을 클릭한다.
                driver.find_element_by_class_name('picker__nav--next').click()
                time.sleep(0.5)
                today_datetime += relativedelta(months=1)
                today_datetime = dt.datetime(today_datetime.year, today_datetime.month, 1)

            candidates = [] # 해당 월에 가능한 날짜
            for i in range(31):
                c = today_datetime + dt.timedelta(days=i)
                if today_datetime.month == c.month:
                    candidates.append(c)

            for candidate in candidates:
                # ① 달력 객체를 들고와서 특정일자를 클릭한다.
                td_list = driver.find_elements(By.TAG_NAME, 'td')
                for td in td_list:
                    day_string = td.find_element_by_tag_name('div').get_attribute('aria-label')
                    day_datetime = dt.datetime.strptime(day_string, '%Y년 %B %d일')
                    if (day_datetime - candidate).days == 0:
                        td.click()
                        time.sleep(2)
                        # ② 클릭하여 나타나는 시간이 예약가능한지 확인한다.
                        time_tables = driver.find_element_by_class_name('ab-time-screen').find_elements(By.TAG_NAME,'button')
                        time_tables = time_tables[1:]  # 처음 날짜 표시는 제외
                        for time_table in time_tables:
                            if not time_table.get_attribute('disabled'):
                                available_slot.append(time_table.get_attribute('value'))
                        break
    except Exception as ex:
        logger.error(candidate)
        logger.error(ex)

    # 가능한 시간이 있다면 전송!
    if len(available_slot) != 0:
        SendMail(available_slot)

    logger.info('Process: %d secs' % (time.time() - start))
    driver.quit()

if __name__ == '__main__':
    logger = logging.getLogger()
    formatter = logging.Formatter(u'%(asctime)s [%(levelname)8s] %(message)s')

    # StreamHandler
    streamingHandler = logging.StreamHandler()
    streamingHandler.setFormatter(formatter)

    # FileHandler
    file_handler = logging.FileHandler('./Log.log')
    file_handler.setFormatter(formatter)

    # logger.addHandler(streamingHandler)
    logger.addHandler(file_handler)
    logger.setLevel(level=logging.INFO)
    logger.info("Start")

    prev_slot = []
    while True:
        GetInfo()
        for i in range(300):
            if i % 60 == 0:
                logger.info("wait for %d minutes" % (i//60 + 1))
            time.sleep(1)