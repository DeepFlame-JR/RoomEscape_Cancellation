import datetime
import sys, os, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from task import decoder, mail

if __name__ == '__main__':
    while True:
        print('start at ', str(datetime.datetime.now()))
        try:
            total_slots = dict()
            total_slots["Decoder"] = dict()
            total_slots["Decoder"]["Tempo Rubato"] = decoder.Tempo_Rubato()
            mail.SendMail(total_slots)
        except Exception as e:
            print(e)
        time.sleep(600)
