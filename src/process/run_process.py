import sys, os, platform, time, datetime
if 'Windows' not in platform.platform():
    os.environ['TZ'] = 'Asia/Seoul'
    time.tzset()

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from task import decoder, notice, log_data
from util import common

def Get_Dictionary():
    data = dict()
    data["Decoder"] = dict()
    data["Decoder"]["Tempo Rubato"] = []
    return data

if __name__ == '__main__':
    Today, Today_cancellation_slots = None, None
    Log = common.Logger()
    while True:
        Log.info('---------- process start! ----------')
        counter = common.TimeCounter("Process Time")
        try:
            # 날이 넘어가면 진행 상황 메일보내기
            if not Today or Today != datetime.date.today():
                if Today:
                    mail = common.Mail()
                    mail.send("진행 상황", str(Today) + '\n' + str(Today_cancellation_slots), "wnsfuf0121@naver.com")
                Today_cancellation_slots = Get_Dictionary()
                Today = datetime.date.today()

            # 데이터 크롤링
            data = decoder.Tempo_Rubato()
            # data = ['2022-05-04 16:01:00']

            # 자료 세팅
            cancellation_slots = Get_Dictionary()
            cancellation_slots["Decoder"]["Tempo Rubato"].extend(data)
            Today_cancellation_slots["Decoder"]["Tempo Rubato"].extend(data)
            Log.info("Total Slots: " + str(cancellation_slots))

            # 로그에 기록하고, 메일 보내기
            log_data.set(data)
            notice.SendNotice(cancellation_slots)
        except Exception as e:
            Log.error(e)

        counter.end()
        Log.info('---------- process end ----------\n\n\n')
        time.sleep(600)
