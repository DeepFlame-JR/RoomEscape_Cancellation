import sys, os
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import common, database
import configparser as parser

import smtplib
from email.mime.text import MIMEText

def SendMail(slot_dict):
    for theme, slots in slot_dict:
        a = 1
    counter = common.TimeCounter("Send Mails")

    properties = parser.ConfigParser()
    properties.read('../config.ini')
    logon_info = properties['MAIL']

    # 과거에 확인된 자리는 제외한다.
    # (5분 간격으로 진행되기에 중복으로 게속 메일을 보내는 상황 방지)
    # send_content = []
    # for cur in available_slot:
    #     if cur not in prev_slot:
    #         send_content.append(cur)
    #         prev_slot.append(cur)
    # if len(send_content) == 0: return

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(logon_info['id'], logon_info['pw'])

    msg = MIMEText('test')
    msg['Subject'] = 'Tempo Rubato 빈자리 알림'

    server.sendmail(
        "roomEscape@gmail.com",
        "wnsfuf0121@naver.com",
        msg.as_string()
    )

    server.quit()
    counter.end()