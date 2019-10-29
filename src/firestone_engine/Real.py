from pymongo import MongoClient
from bson.objectid import ObjectId
from pydoc import locate
from datetime import datetime
import os
import logging
from .Constants import Constants

class Real(object):

    _MONFO_URL = '127.0.0.1'

    _DATA_DB = 'firestone-data'

    _logger = logging.getLogger(__name__)

    def __init__(self, tradeId, date=None):
        self.tradeId = tradeId
        self.date = date
        self.lastRunTime = None
        self.client = MongoClient(Real._MONFO_URL, 27017)
        self.db = self.client[os.environ['FR_DB']]
        self.data_db = self.client[Real._DATA_DB]
        self.init_cols()
        self.init_Config()


    def init_cols(self):
        self.cols = {
            'trades' : 'trades',
            'configs' : 'configs'
        }    


    def run(self):
        self.trade = self.db[self.cols['trades']].find_one({"_id" : ObjectId(self.tradeId)})
        self.data = self.get_data()
        if(self.trade['state'] != Constants.STATE[0]):
            return None
        if(self.data[-1]['time'] == self.lastRunTime):
            return None
        self.lastRunTime = self.data[-1]['time']
        logging.info('tradeId = {} load trade = {}'.format(self.tradeId, self.trade))
        self.config = self.db[self.cols['configs']].find_one({"userId" : self.trade['userId']})
        logging.info('tradeId = {} load config = {}'.format(self.tradeId, self.config))
        if(self.strategy.run(self.trade, self.config, self.data['data'], self.data['index'])):
            code = self.trade['params']['code']
            price = float(self.data['data'][-1]['price'])
            volume = int(self.trade['params']['volume'])
            op_cn = '买入' if self.strategy['op'] == 'buy' else '卖出'
            result = self.createOrder(code, price, volume, self.strategy['op'])
            if(result is not None and result['errorcode'] == 0):
                self.updateResult('订单提交: 在{},以{}{}[{}] {}股, 当前数据时间{}'.format(datetime.now(), price, op_cn, code, volume, self.data['data'][-1]['time']), state=Constants.STATE[2])
                self.updateOrder(result)
                return result['result']['data']['htbh']
            else:
                self.updateResult('订单提交失败, 请检查配置', state=Constants.STATE[3])
        return None


    def get_data(self):
        data = self.data_db[self.trade['params']['code'] + '-' + self.date].find()
        if(self.trade['params']['code'].startswith('3')):
            index = self.data_db[Constants.INDEX[5]].find()
        else:
            index = self.data_db[Constants.INDEX[0]].find()    
        return {
            'data' : list(data),
            'index' : list(index)
        }


    def updateOrder(self, order):
        return self.db[self.cols['trades']].update_one({"_id" : ObjectId(self.tradeId)},{"$set" : {"order" : order}})

    def updateResult(self, result, state=None):
        update = {"result" : result}
        if(state is not None):
            update["state"] = state
        Real._logger.info('update tradeId = {}, data = {}'.format(self.tradeId, update))    
        return self.db[self.cols['trades']].update_one({"_id" : ObjectId(self.tradeId)},{"$set" : update})    


    def createOrder(self, code, price, volume, op):
        return {'errorcode' : -1, 'message' : 'not allowed'}



    def init_Config(self):
        self.trade = self.db[self.cols['trades']].find_one({"_id" : ObjectId(self.tradeId)})
        self.strategyMeta = self.db['strategies'].find_one({"_id" : self.trade['strategyId']})
        self.config = self.db[self.cols['configs']].find_one({"userId" : self.trade['userId']})
        logging.info('tradeId = {} load startegy = {}'.format(self.tradeId, self.strategyMeta))
        class_name = self.strategyMeta['url']
        strategyClass = locate('firestone_engine.strategies.{}.{}'.format(class_name, class_name))
        self.strategy = strategyClass()


    def close(self):
        self.client.close() 