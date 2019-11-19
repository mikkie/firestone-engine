from pymongo import MongoClient
from bson.objectid import ObjectId
from pydoc import locate
from datetime import datetime
import os
import logging
from .Constants import Constants
from .strategies.Base import Base
from .strategies.Basic import Basic
from .strategies.Ydls import Ydls

class Real(object):

    _MONFO_URL = '127.0.0.1'

    _DATA_DB = 'firestone-data'

    _logger = logging.getLogger(__name__)

    def __init__(self, tradeId, date=None):
        self.tradeId = tradeId
        if(date is None):
            today = datetime.now()
            date = '{}-{}-{}'.format(today.year,today.month,today.day)
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
        self.load_trade_config()
        self.load_data()
        if(self.config['curBuyNum'] >= self.config['maxBuyNum']):
            force_state = {'state' : Constants.STATE[4]}
            self.updateTrade(force_state)
            return force_state
        if(len(self.data['data']) == 0):
            return {'state' : self.trade['state']}
        if(self.trade['state'] == Constants.STATE[5]):
            return self.cancelOrder()
        if(self.trade['state'] != Constants.STATE[0]):
            return {'state' : self.trade['state']}
        elif(self.trade['result'] is not None and self.trade['result'] != '无' and self.trade['result'] != ''):
            self.updateTrade({'result' : '无'})
        if(self.data['data'][-1]['time'] == self.lastRunTime):
            return {'state' : self.trade['state']}
        self.lastRunTime = self.data['data'][-1]['time']
        if(self.strategy.run(self.trade, self.config, self.data['data'], self.data['index'])):
            result = self.createOrder()
            if(result['state'] == Constants.STATE[2]):
                return {'state' : result['state'], 'htbh' : result['order']['result']['data']['htbh']}
        return {'state' : self.trade['state']}


    
    def load_trade(self):
        self.trade = self.db[self.cols['trades']].find_one({"_id" : ObjectId(self.tradeId)})
    
    def load_trade_config(self):
        self.load_trade()
        self.config = self.db[self.cols['configs']].find_one({"userId" : self.trade['userId']})  
        Real._logger.info('tradeId = {} load trade = {}, config = {}'.format(self.tradeId, self.trade, self.config))  


    def load_data(self):
        data = self.data_db[self.trade['params']['code'] + '-' + self.date].find()
        if(self.trade['params']['code'].startswith('3')):
            index = self.data_db[Constants.INDEX[5] + '-' + self.date].find()
        else:
            index = self.data_db[Constants.INDEX[0] + '-' + self.date].find()    
        self.data = {
            'data' : list(data),
            'index' : list(index)
        }



    def updateTrade(self, update):
        Real._logger.info('update tradeId={} with update = {}'.format(self.tradeId, update))
        return self.db[self.cols['trades']].update_one({"_id" : ObjectId(self.tradeId)},{"$set" : update})


    def updateConfig(self, update):
        Real._logger.info('update configId={} with update = {}'.format(self.config['_id'], update))
        return self.db[self.cols['configs']].update_one({"_id" : self.config['_id']}, update)


    def createOrder(self):
        code = self.trade['params']['code']
        price = float(self.data['data'][-1]['price'])
        volume = int(self.trade['params']['volume'])
        result = self.createDelegate(code, price, volume, self.strategyMeta['op'])
        self.updateTrade(result)
        return result


    def createDelegate(self, code, price, volume, op):
        return {'errorcode' : -1, 'message' : 'not allowed', 'state' : Constants.STATE[3]}


    def cancelOrder(self):
        if('order' not in self.trade):
            Real._logger.error('no order found in trade = {}, failde to cancel'.format(self.tradeId))
            update = {'state' : Constants.STATE[1], 'result' : '未找到订单'}
            self.updateTrade(update)
            return update
        htbh = self.trade['order']['result']['data']['htbh']
        today = datetime.now()
        htrq = '{}{}{}'.format(today.year,today.month,today.day)
        result = self.cancelDelegate(htbh, htrq)
        self.updateTrade(result)
        return result


    def cancelDelegate(self, htbh, wtrq):
        return {'errorcode' : -1, 'message' : 'not allowed', 'state' : Constants.STATE[3]}  


    def reLogin(self):
        return {'errorcode' : -1, 'message' : 'not allowed', 'state' : Constants.STATE[3]}    


    def check_chengjiao(self, htbh):
        update = self.queryChenjiao(htbh)
        if(len(update) == 0):
            return
        self.updateTrade(update)
        if(update['state'] == Constants.STATE[4]):
            self.updateConfig({ '$inc': { 'curBuyNum': 1 } })


    def queryChenjiao(self, htbh):
        return {'errorcode' : -1, 'message' : 'not allowed', 'state' : Constants.STATE[3]}


    


    def init_Config(self):
        self.load_trade_config()
        self.strategyMeta = self.db['strategies'].find_one({"_id" : self.trade['strategyId']})
        Real._logger.info('tradeId = {} load startegy = {}'.format(self.tradeId, self.strategyMeta))
        class_name = self.strategyMeta['url']
        strategyClass = locate('firestone_engine.strategies.{}.{}'.format(class_name, class_name))
        self.strategy = strategyClass()


    def close(self):
        self.client.close() 