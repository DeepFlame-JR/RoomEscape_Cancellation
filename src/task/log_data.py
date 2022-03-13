import sys, os, platform, time, datetime
if 'Windows' not in platform.platform():
    os.environ['TZ'] = 'Asia/Seoul'
    time.tzset()

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import database, common

def set(data):
    if len(data) > 0:
        now = datetime.datetime.now()
        input_data = []
        for cancellation_time in data:
            input_data.append({'datetime': now, 'cancellation_time': cancellation_time})

        mongo = database.MongoDB()
        mongo.insert_item_many(input_data, db_name='roomdb', collection_name='log')

        Log = common.Logger()
        Log.info("Set Log data | length: {0}".format(str(len(data))))
