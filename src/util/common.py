import os, platform, time
if 'Windows' not in platform.platform():
    os.environ['TZ'] = 'Asia/Seoul'
    time.tzset()

import logging
import configparser as parser
import smtplib
from email.mime.text import MIMEText

class TimeCounter:
    def __init__(self, title):
        self.title = title
        self.start_time = time.time()
        self.Log = Logger()

    def end(self, content=""):
        self.Log.info("%s %s : %.5f secs" % (self.title, content, time.time() - self.start_time))

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("MyLogger")

        if len(self.logger.handlers) == 0:
            # StreamHandler
            formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s')
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            self.logger.addHandler(stream_handler)
            self.logger.setLevel(logging.INFO)

    def info(self, value):
        self.logger.info(value)

    def error(self, value):
        self.logger.error(value)

class Config:
    def __init__(self):
        self.properties = parser.ConfigParser()

        src_folder = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        config_path = os.path.join(src_folder, 'config.ini')
        if os.path.exists(config_path):
            self.properties.read(config_path)
        else:
            raise "Can not find config.ini"

    def get(self, section):
        if not section in self.properties.sections():
            raise "can not find {0} in config.ini".format(section)
        return self.properties[section]

class Mail:
    def __init__(self):
        config = Config()
        self.logon_info = config.get("MAIL")
        self.Log = Logger()

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.logon_info['id'], self.logon_info['pw'])

    def __del__(self):
        self.server.quit()

    def send(self, title, content, sendTo):
        msg = MIMEText(content)
        msg['Subject'] = title

        self.server.sendmail(
            "roomEscape@gmail.com",
            sendTo,
            msg.as_string()
        )
        self.Log.info('send mail to ' + sendTo)
