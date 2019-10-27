import tushare
from datetime import datetime, timedelta
import logging
import json
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler

class DataLoader(object):

    _logger = logging.getLogger(__name__)

    _MONFO_URL = '127.0.0.1'

    _DB = 'firestone-data'
    
    def __init__(self, code_list):
        self.client = MongoClient(DataLoader._MONFO_URL, 27017)
        self.db = self.client[DataLoader._DB]
        self.code_list = code_list
        self.scheduler = BackgroundScheduler()
        end_date = datetime.now() + timedelta(days = 1)
        end_date = '{}-{}-{}'.format(end_date.year,end_date.month,end_date.day)
        self.scheduler.add_job(self.run,'cron',id="last_job", hour='10,13-14',minute='*',second='*/3', end_date=end_date)
        self.scheduler.add_job(self.run,'cron',hour='9',minute='30-59',second='*/3', end_date=end_date)
        self.scheduler.add_job(self.run,'cron',hour='11',minute='0-29',second='*/3', end_date=end_date)
        #self.scheduler.add_job(self.run,'cron',id='last_job', hour='17',minute='35',second='*/3', end_date=end_date)


    def start(self):
        self.scheduler.start()
        DataLoader._logger.info('job get data for {} is start'.format(self.code_list))

    def is_finsih(self):
        job = self.scheduler.get_job('last_job')
        return job is None or job.next_run_time is None

    def stop(self):
        self.client.close()
        self.scheduler.shutdown(wait=True)
        DataLoader._logger.info('job get data for {} is stop'.format(self.code_list))


    def run(self):
        df = tushare.get_realtime_quotes(self.code_list)
        json_list = json.loads(df.to_json(orient='records'))
        print(json_list)
        for json_data in json_list:
            self.db[json_data['code']].insert(json_data)