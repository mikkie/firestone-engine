import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .Real import Real
from .Mock import Mock

class Trader(object):

    _logger = logging.getLogger(__name__)

    def __init__(self, tradeId, is_mock, date):
        self.tradeId = tradeId
        self.is_mock = is_mock
        self.scheduler = BackgroundScheduler()
        end_date = datetime.now() + timedelta(days = 1)
        end_date = '{}-{}-{}'.format(end_date.year,end_date.month,end_date.day)
        self.scheduler.add_job(self.run,'cron',id="last_job", hour='10,13-14',minute='*',second='*/4', end_date=end_date)
        self.scheduler.add_job(self.run,'cron',hour='9',minute='30-59',second='*/4', end_date=end_date)
        self.scheduler.add_job(self.run,'cron',hour='11',minute='0-29',second='*/4', end_date=end_date)
        if(date is None):
            today = datetime.now()
            date = '{}-{}-{}'.format(today.year,today.month,today.day)
        if(self.is_mock):
            self.handler = Mock(tradeId, date)
        else:
            self.handler = Real(tradeId, date)  


    def start(self):
        self.scheduler.start()
        Trader._logger.info('job execute trade for {} is start'.format(self.tradeId))


    def run(self):
        htbh = self.handler.run()
        if(htbh is not None):
            #query the ths trade result
            pass


    def is_finsih(self):
        job = self.scheduler.get_job('last_job')
        return job is None or job.next_run_time is None

    def stop(self):
        self.handler.close()
        self.scheduler.shutdown(wait=True)
        Trader._logger.info('job execute trade for {} is stop'.format(self.tradeId))        