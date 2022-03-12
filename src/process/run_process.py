import datetime
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from task import decoder, mail
from util import common

if __name__ == '__main__':
    Log = common.Logger()
    while True:
        Log.info('---------- process start! ----------')
        counter = common.TimeCounter("Process Time")
        try:
            total_slots = dict()
            total_slots["Decoder"] = dict()
            total_slots["Decoder"]["Tempo Rubato"] = decoder.Tempo_Rubato()
            # total_slots["Decoder"]["Tempo Rubato"] = ['2022-05-02 16:00:00']
            Log.info("Total Slots: " + str(total_slots))
            mail.SendMail(total_slots)
        except Exception as e:
            Log.error(e)

        counter.end()
        Log.info('---------- process end ----------')
        time.sleep(600)
