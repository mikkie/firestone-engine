import tushare
from datetime import datetime, timedelta
import pytz
import logging
import json
import os
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .ProxyManager import ProxyManager
from .Constants import Constants
from .HotConcept import HotConcept

class DataLoader(object):

    UTC_8 = pytz.timezone('Asia/Shanghai')

    _logger = logging.getLogger(__name__)

    _MONFO_URL = '127.0.0.1'

    _DATA_DB = 'firestone-data'

    _CODE_FROM_DB = '000000'

    def __init__(self, code_list, is_mock=False, mock_trade=False, date=None, hours=['9','11','10,13-14'], minutes=['30-59','0-29','*']):
        self.proxyManager = ProxyManager()
        self.use_proxy = False
        self.hours = hours
        self.minutes = minutes
        self.is_mock = is_mock
        self.mock_trade = mock_trade
        self.is_finsih_flag = False
        self.lastRows = {}
        self.client = MongoClient(DataLoader._MONFO_URL, 27017)
        self.data_db = self.client[DataLoader._DATA_DB]
        self.db = self.client[os.environ['FR_DB']]
        self.hot_concept = HotConcept(self.db)
        self.scheduler = BackgroundScheduler()
        self.date = date
        today = datetime.now()
        self.today = '{}-{}-{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
        # self.today_datetime = datetime(today.year,today.month,today.day,tzinfo=DataLoader.UTC_8)
        if(self.date is None):
            self.date = self.today
        end_date = today + timedelta(days = 1)
        end_date = '{}-{}-{}'.format(end_date.year,('0' + str(end_date.month))[-2:],('0' + str(end_date.day))[-2:])
        self.load_codes_from_db = False
        self.code_list = self.get_code_list(code_list)
        for i, hour in enumerate(hours):
            trigger = CronTrigger(hour=hour,minute=minutes[i],second='*/3', end_date=end_date)
            trigger_concept = CronTrigger(hour=hour,minute=minutes[i],second='0', end_date=end_date)
            if(i == len(hours) - 1):
                self.scheduler.add_job(self.run,id="last_job",trigger=trigger)
            else:
                self.scheduler.add_job(self.run,trigger=trigger)
            self.scheduler.add_job(self.run_concept,trigger=trigger_concept)

    def get_code_list(self, code_list):
        if(DataLoader._CODE_FROM_DB in code_list):
            self.load_codes_from_db = True
            return [DataLoader._CODE_FROM_DB]
        colls = list(self.data_db.list_collections())
        codes = []
        for code in code_list:
            if(code == 'N/A'):
                continue
            name = code + '-' + self.date + ('-m' if self.is_mock else '')
            if(name not in [coll['name'] for coll in colls]):
                codes.append(code)
                self.data_db.create_collection(name)
        if(len(codes) == 0):
            self.is_finsih_flag = True        
        return codes        


    def start(self):
        if(self.is_finsih_flag):
            return
        self.scheduler.start()
        DataLoader._logger.info('job get data for {} is start'.format(self.code_list))

    def is_finsih(self):
        job = self.scheduler.get_job('last_job')
        return self.is_finsih_flag or job is None or job.next_run_time is None

    def stop(self):
        self.client.close()
        self.scheduler.shutdown(wait=True)
        DataLoader._logger.info('job get data for {} is stop'.format(self.code_list))


    def get_code_list_from_db(self):
        colname = 'trades'
        if(self.mock_trade):
            colname = 'mocktrades'
        codes_data = self.db[colname].find({"deleted":False, "params.executeDate" : self.today},{"code" : 1, "_id" : 0})
        code_list = [code_data["code"] for code_data in list(codes_data) if code_data["code"] != 'N/A']
        temp_list = []
        for code in code_list:
            if(',' in code):
                temp_list.extend(code.split(','))
            else:
                temp_list.append(code)
        code_list = temp_list        
        for code in code_list:
            if(code.startswith('3')):
                if(Constants.INDEX[5] not in code_list):
                    code_list.append(Constants.INDEX[5])
            else:  
                if(Constants.INDEX[0] not in code_list):
                    code_list.append(Constants.INDEX[0])
        return list(set(code_list)) 


    def load_data(self):
        list_wrapper = []
        size = len(self.code_list)
        df_result = None
        if(size > 50):
            list_size = (size // 50) + (1 if (size % 50) > 0 else 0)
            for i in range(list_size):
                list_wrapper.append(self.code_list[i * 50 : i * 50 + 50])
        else:
            list_wrapper.append(self.code_list)
        if(self.use_proxy):
            for l in list_wrapper:
                try:
                    df = tushare.get_realtime_quotes(l, proxyManager=self.proxyManager)
                    if(df_result is None):
                        df_result = df
                    else:
                        df_result = df_result.append(df)
                except Exception as e:
                    DataLoader._logger.error('load data error, use_proxy = {}, e = {}'.format(self.use_proxy, e))
                    self.use_proxy = True
                    self.proxyManager.remove_proxy()
        else:
            for i, l in enumerate(list_wrapper):
                try:
                    if(i == 0):
                        df = tushare.get_realtime_quotes(l)
                    else:
                        df = tushare.get_realtime_quotes(l, proxyManager=self.proxyManager)
                    if(df_result is None):
                        df_result = df
                    else:
                        df_result = df_result.append(df)    
                except Exception as e:
                    DataLoader._logger.error('load data error, use_proxy = {}, e = {}'.format(self.use_proxy, e))
                    self.use_proxy = True
                    self.proxyManager.remove_proxy()
        return df_result
        



    def run(self):
        try:
            if(self.load_codes_from_db):
                self.code_list = self.get_code_list_from_db()
            DataLoader._logger.info('start get the data for {}'.format(self.code_list))
            if(len(self.code_list) < 2):
                return    
            if(self.is_mock):
                self.run_mock()
            else:
                df = self.load_data()
                if(df is None):
                    DataLoader._logger.error('failed to get the data for {}'.format(self.code_list))
                    return      
                json_list = json.loads(df.to_json(orient='records'))
                DataLoader._logger.info('get data length = {}'.format(len(json_list)))
                for json_data in json_list:
                    code = json_data['code']
                    code = Constants.map_code(json_data['name'], json_data['code'])
                    if(code not in self.lastRows):
                        self.lastRows[code] = None
                    if(self.lastRows[code] is None or self.lastRows[code]['time'] != json_data['time']):    
                        json_data['real_time'] = datetime.now()
                        self.data_db[code + '-' + self.today].insert(json_data)
                        self.lastRows[code] = json_data
        except Exception as e:
            DataLoader._logger.error(e)


    def run_concept(self):
        try:
            self.hot_concept.load_hot_concept()
        except Exception as e:
            DataLoader._logger.error(f'load hot concept failed, e = {e}')


    def run_mock(self):
        try:
            if(not hasattr(self, 'mock_count')):
                self.mock_count = 0
                self.data = {}
                for code in self.code_list:
                    self.data[code + '-' + self.date] = list(self.data_db[code + '-' + self.date].find()) 
                    self.lastRows[code] = None
            for code in self.code_list: 
                if self.mock_count < len(self.data[code + '-' + self.date]):
                    json_data = self.data[code + '-' + self.date][self.mock_count]
                    json_data['real_time'] = datetime.now()
                    if(self.lastRows[code] is None or self.lastRows[code]['time'] != json_data['time']):
                        self.data_db[code + '-' + self.date + '-m'].insert(json_data)
                        self.lastRows[code] = json_data    
            self.mock_count += 1
        except Exception as e:
            DataLoader._logger.error(e)

