import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import common, database

import datetime, copy
from dateutil.relativedelta import relativedelta
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
    Log = common.Logger()
    try:
        # initialize
        total_counter = common.TimeCounter("Send Mails")
        mongo = database.MongoDB()
        config = common.Config()
        logon_info = config.get("MAIL")

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
                    if 'send_info' in user.keys():
                        send_info = copy.deepcopy(user['send_info'])
                    else:
                        send_info = dict()

                    now = datetime.datetime.now()
                    # remove over 1 day
                    remove_keys = []
                    for k, v in send_info.items():
                        if (now - v).days > 0:
                            remove_keys.append(k)
                    Log.info("removed: " + str(remove_keys))
                    for remove_key in remove_keys:
                        del send_info[remove_key]

                    # Check if the time was sent
                    send_list = []
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
                        content = 'cafe' + " | " + 'theme' + '의 빈 자리가 있습니다! 🙋‍\n\n' + \
                                  '아래 시간을 확인해주세요.\n' + \
                                  '\n'.join(send_list) + \
                                  '\n\n예약 URL: http://decoder.kr/?page_id=7082'
                        msg = MIMEText(content)
                        msg['Subject'] = title

                        server.sendmail(
                            "roomEscape@gmail.com",
                            user['email'],
                            msg.as_string()
                        )
                        Log.info('send mail to ' + user['email'] + ' / length of send_list: ' + str(len(send_list)))

                    # Update cancellation DB
                    mongo.update_item_one(condition=user, update_value={'$set': {'send_info': send_info}},
                                          db_name='roomdb', collection_name='user')
                counter.end()
        server.quit()
        total_counter.end()
    except Exception as e:
        Log.error(e)