import time
import logging

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
            formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s (at %(filename)s)')
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)

            self.logger.addHandler(stream_handler)
            self.logger.setLevel(logging.INFO)

    def info(self, value):
        self.logger.info(value)

    def error(self, value):
        self.logger.error(value)

# log = Logger()
# log = Logger()
# log = Logger()
#
# log.info('test')
# log.error('test')