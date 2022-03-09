import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import common, database

import datetime, copy
from dateutil.relativedelta import relativedelta
import configparser as parser
import smtplib
from email.mime.text import MIMEText

'''
아래 조건에 해당하는 경우, 메일을 전송한다.
1. 특정 User에게 특정 취소 시간을 최초로 전송하는 경우
2. 특정 User에게 특정 취소 시간을 전송한 기간이 하루가 지났을 경우
'''

def IsSent(cancel_time, send_info, now):
    if cancel_time in send_info.keys():
        if (now - send_info[cancel_time]).days == 0:
            return True
    return False

def SendMail(slot_dict):
    # initialize
    total_counter = common.TimeCounter("Send Mails")
    mongo = database.MongoDB()
    properties = parser.ConfigParser()
    properties.read('../config.ini')
    logon_info = properties['MAIL']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(logon_info['id'], logon_info['pw'])

    # Send Mail
    for cafe in slot_dict.keys():
        for theme in slot_dict[cafe]:
            counter = common.TimeCounter(cafe + " | " + theme)
            cancel_times = slot_dict[cafe][theme]
            if cancel_times == None or len(cancel_times) == 0:
                continue

            users = mongo.find_item(condition={'cafe':cafe, 'theme':theme},
                                    db_name='roomdb', collection_name='user')
            for user in users:
                user_info = mongo.find_item_one(condition={'email':user['email']},
                                                db_name='roomdb', collection_name='user')
                if 'send_info' in user_info.keys():
                    send_info = copy.deepcopy(user_info['send_info'])
                else:
                    send_info = dict()

                # Check if the time was sent
                send_list = []
                now = datetime.datetime.now()
                for cancel_time in cancel_times:
                    if (datetime.datetime.strptime(cancel_time, '%Y-%m-%d %H:%M:%S')
                            > now + relativedelta(months=user['untilMonth'])):
                        continue

                    if not IsSent(cancel_time, send_info, now):
                        send_list.append(cancel_time)
                        send_info[cancel_time] = now

                # Send mail
                if len(send_list) > 0:
                    title = theme + " 빈자리 알림"
                    content = cafe + " | " + theme + '의 빈 자리가 있습니다!\n\n' + \
                              '아래 시간을 확인해주세요.\n' +\
                              '\n'.join(send_list)
                    msg = MIMEText(content)
                    msg['Subject'] = title

                    server.sendmail(
                        "roomEscape@gmail.com",
                        "wnsfuf0121@naver.com",
                        msg.as_string()
                    )
                    print('send mail to ' + user_info['email'] + '\nlength of send_list: ' + str(len(send_list)))

                # Update cancellation DB
                mongo.update_item_one(condition=user_info, update_value={'$set': {'send_info': send_info}},
                                      db_name='roomdb', collection_name='user')
            counter.end()
    server.quit()
    total_counter.end()


# total_slots = dict()
# total_slots["Decoder"] = dict()
# total_slots["Decoder"]["Tempo Rubato"] = ['2022-08-08 18:00:00','2022-08-09 18:00:00']
# SendMail(total_slots)