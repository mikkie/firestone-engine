import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from .Real import Real
from .Mock import Mock
from .Constants import Constants

class Trader(object):

    _logger = logging.getLogger(__name__)

    def __init__(self, tradeId, is_mock, date ,hours=['9','11','10,13-14'], minutes=['30-59','0-29','*']):
        self.hours = hours
        self.minutes = minutes
        self.tradeId = tradeId
        self.is_mock = is_mock
        self.is_finsih_flag = False
        self.scheduler = BackgroundScheduler()
        end_date = datetime.now() + timedelta(days = 1)
        self.end_date = '{}-{}-{}'.format(end_date.year,end_date.month,end_date.day)
        self.scheduler.add_job(self.run,'cron',id="last_job", hour=hours[2],minute=minutes[2],second='*/4', end_date=self.end_date)
        self.scheduler.add_job(self.run,'cron',hour=hours[0],minute=minutes[0],second='*/4', end_date=self.end_date)
        self.scheduler.add_job(self.run,'cron',hour=hours[1],minute=minutes[1],second='*/4', end_date=self.end_date)
        if(self.is_mock):
            self.handler = Mock(tradeId, date)
        else:
            self.handler = Real(tradeId, date)  


    def start(self):
        self.scheduler.start()
        Trader._logger.info('job execute trade for {} is start'.format(self.tradeId))


    def run(self):
        result = self.handler.run()
        #order submit
        if(result['state'] == Constants.STATE[2] and 'htbh' in result):
            htbh = result['htbh']
            self.scheduler.add_job(self.check_chengjiao,'cron',kwargs={'htbh' : htbh},hour=self.hours[1],minute=self.minutes[1],second='*/10', end_date=self.end_date)
            self.scheduler.add_job(self.check_chengjiao,'cron',kwargs={'htbh' : htbh},hour=self.hours[0],minute=self.minutes[0],second='*/10', end_date=self.end_date)
            self.scheduler.add_job(self.check_chengjiao,'cron',kwargs={'htbh' : htbh},hour=self.hours[2],minute=self.minutes[2],second='*/10', end_date=self.end_date)
        #done
        elif (result['state'] == Constants.STATE[4]):
            self.is_finsih_flag = True


    def check_chengjiao(self, htbh):
        self.handler.check_chengjiao(htbh)





    def is_finsih(self):
        job = self.scheduler.get_job('last_job')
        return job is None or job.next_run_time is None or self.is_finsih_flag

    def stop(self):
        self.handler.updateTrade({'state' : Constants.STATE[4]})
        self.handler.close()
        self.scheduler.shutdown(wait=False)
        Trader._logger.info('job execute trade for {} is stop'.format(self.tradeId))        