import datetime
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from task import decoder, mail
from util import common

if __name__ == '__main__':
    Log = common.Logger()
    while True:
        Log.info('process start!')
        try:
            total_slots = dict()
            total_slots["Decoder"] = dict()
            total_slots["Decoder"]["Tempo Rubato"] = decoder.Tempo_Rubato()
            mail.SendMail(total_slots)
        except Exception as e:
            Log.Error(e)

        Log.info('process end')
        time.sleep(600)
