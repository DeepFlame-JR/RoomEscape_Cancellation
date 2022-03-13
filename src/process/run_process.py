import datetime
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from task import decoder, notice
from util import common

def Get_Dictionary():
    data = dict()
    data["Decoder"] = dict()
    data["Decoder"]["Tempo Rubato"] = []
    return data

if __name__ == '__main__':
    Today, Today_cancellation_slots = None, None
    Log = common.Logger()
    Mail = common.Mail()

    while True:
        Log.info('---------- process start! ----------')
        counter = common.TimeCounter("Process Time")
        try:
            # 날이 넘어가면 진행 상황 메일보내기
            if not Today or Today != datetime.date.today():
                if Today:
                    Mail.send("진행 상황", str(Today) + '\n' + str(Today_cancellation_slots), "wnsfuf0121@naver.com")
                Today_cancellation_slots = Get_Dictionary()
                Today = datetime.date.today()

            # 데이터 크롤링
            cancellation_slots = Get_Dictionary()
            # data = decoder.Tempo_Rubato()
            data = ['2022-05-04 16:01:00']
            cancellation_slots["Decoder"]["Tempo Rubato"].extend(data)
            Today_cancellation_slots["Decoder"]["Tempo Rubato"].extend(data)

            Log.info("Total Slots: " + str(cancellation_slots))
            notice.SendNotice(cancellation_slots)
        except Exception as e:
            Log.error(e)

        counter.end()
        Log.info('---------- process end ----------')
        time.sleep(600)
