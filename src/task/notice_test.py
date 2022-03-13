import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import common, database

import smtplib
from email.mime.text import MIMEText

config = common.Config()
logon_info = config.get("MAIL")

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(logon_info['id'], logon_info['pw'])

send_list = ['2022-03-10 16:00:00', '2022-03-11 16:10:00']
title = 'theme' + " 빈자리 알림"
content = 'cafe' + " | " + 'theme' + '의 빈 자리가 있습니다! 🙋‍\n\n' + \
          '아래 시간을 확인해주세요.\n' + \
          '\n'.join(send_list) + \
          '\n\n예약 URL: http://decoder.kr/?page_id=7082'
msg = MIMEText(content)
msg['Subject'] = title

server.sendmail(
    "roomEscape@gmail.com",
    "wnsfuf0121@naver.com",
    msg.as_string()
)