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
    
    def __init__(self, code_list, is_mock=False, date=None, hours=['9','11','10,13-14'], minutes=['30-59','0-29','*']):
        self.hours = hours
        self.minutes = minutes
        self.is_mock = is_mock
        self.is_finsih_flag = False
        self.date = date
        self.lastRows = {}
        self.client = MongoClient(DataLoader._MONFO_URL, 27017)
        self.db = self.client[DataLoader._DB]
        self.scheduler = BackgroundScheduler()
        today = datetime.now()
        self.today = '{}-{}-{}'.format(today.year,today.month,today.day)
        self.code_list = self.get_code_list(code_list, date)
        end_date = today + timedelta(days = 1)
        end_date = '{}-{}-{}'.format(end_date.year,end_date.month,end_date.day)
        self.scheduler.add_job(self.run,'cron',id="last_job", hour=hours[2],minute=minutes[2],second='*/3', end_date=end_date)
        self.scheduler.add_job(self.run,'cron',hour=hours[0],minute=minutes[0],second='*/3', end_date=end_date)
        self.scheduler.add_job(self.run,'cron',hour=hours[1],minute=minutes[1],second='*/3', end_date=end_date)


    def get_code_list(self, code_list, date):
        colls = list(self.db.list_collections())
        codes = []
        date = self.today if self.date is None else self.date
        for code in code_list:
            if(code not in [coll['name'] for coll in colls]):
                codes.append(code)   
        return codes        


    def start(self):
        self.scheduler.start()
        DataLoader._logger.info('job get data for {} is start'.format(self.code_list))

    def is_finsih(self):
        job = self.scheduler.get_job('last_job')
        return job is None or job.next_run_time is None or self.is_finsih_flag

    def stop(self):
        self.client.close()
        self.scheduler.shutdown(wait=True)
        DataLoader._logger.info('job get data for {} is stop'.format(self.code_list))


    def run(self):
        if(len(self.code_list) == 0):
            self.is_finsih_flag = True
            return
        if(self.is_mock):
            self.run_mock()
        else:
            df = tushare.get_realtime_quotes(self.code_list)
            json_list = json.loads(df.to_json(orient='records'))
            print(json_list)
            for json_data in json_list:
                code = json_data['code']
                if(code not in self.lastRows):
                   self.lastRows[code] = None
                if(self.lastRows[code] is None or self.lastRows[code]['time'] != json_data['time']):    
                    json_data['real_time'] = datetime.now()
                    self.db[json_data['code'] + '-' + self.today].insert(json_data)
                    self.lastRows[code] = json_data


    def run_mock(self):
        if(not hasattr(self, 'mock_count')):
            self.mock_count = 0
            self.data = {}
            if(self.date is None):
                today = datetime.now()
                self.date = '{}-{}-{}'.format(today.year,today.month,today.day)
            for code in self.code_list:
                self.data[code + '-' + self.date] = list(self.db[code + '-' + self.date].find()) 
                self.lastRows[code] = None
        for code in self.code_list: 
            if self.mock_count < len(self.data[code + '-' + self.date]):
                json_data = self.data[code + '-' + self.date][self.mock_count]
                json_data['real_time'] = datetime.now()
                if(self.lastRows[code] is None or self.lastRows[code]['time'] != json_data['time']):
                    self.db[code + '-' + self.date + '-m'].insert(json_data)
                    self.lastRows[code] = json_data    
        self.mock_count += 1

