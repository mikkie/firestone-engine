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
from .strategies.BasicSell import BasicSell
from .strategies.ConceptPick import ConceptPick
from .strategies.BatchYdls import BatchYdls

class Real(object):

    _MONFO_URL = '127.0.0.1'

    _DATA_DB = 'firestone-data'

    _logger = logging.getLogger(__name__)

    def __init__(self, tradeId, date=None):
        self.tradeId = tradeId
        if(date is None):
            today = datetime.now()
            date = '{}-{}-{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
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
        if(self.config['curBuyNum'] >= self.config['maxBuyNum']):
            force_state = {'state' : Constants.STATE[4]}
            self.updateTrade(force_state)
            return force_state
        if(self.trade['state'] == Constants.STATE[5]):
            return self.cancelOrder()
        if(self.trade['state'] != Constants.STATE[0]):
            return {'state' : self.trade['state']}
        if(self.strategy.need_create_order()):
            if(self.trade['result'] is not None and self.trade['result'] != '无' and self.trade['result'] != ''):
                self.updateTrade({'result' : '无'})
            self.load_data()
            if(len(self.data['data']) == 0):
                return {'state' : self.trade['state']}
            if(not self.is_batch()):
                if(self.data['data'][-1]['time'] == self.lastRunTime):
                    return {'state' : self.trade['state']}
                self.lastRunTime = self.data['data'][-1]['time']
            flag = False
            if(self.is_batch()):
                flag = self.strategy.run(self.trade, self.config, self.db, self.data['data'], self.data['index'])
            else:
                flag = self.strategy.run(self.trade, self.config, self.data['data'], self.data['index'])
            if(flag):
                result = self.createOrder()
                if(result['state'] == Constants.STATE[2]):
                    if(self.strategyMeta['op'] == 'buy'):
                        self.updateConfig({ '$inc': { 'curBuyNum': 1 } })
                    return {'state' : result['state'], 'htbh' : result['order']['result']['data']['htbh']}
        else:
            self.strategy.run(self.trade, self.config, self.db, type(self).__name__ == 'Mock')
        return {'state' : self.trade['state']}


    
    def load_trade(self):
        self.trade = self.db[self.cols['trades']].find_one({"_id" : ObjectId(self.tradeId)})
    
    def load_trade_config(self):
        self.load_trade()
        self.config = self.db[self.cols['configs']].find_one({"userId" : self.trade['userId']})  
        Real._logger.info('tradeId = {} load trade = {}, config = {}'.format(self.tradeId, self.trade, self.config))  


    def load_data(self):
        if(self.is_batch()):
            self.load_batch_data()
        else:
            data = self.data_db[self.trade['params']['code'] + '-' + self.date].find()
            if(self.trade['params']['code'].startswith('3')):
                index = self.data_db[Constants.INDEX[5] + '-' + self.date].find()
            else:
                index = self.data_db[Constants.INDEX[0] + '-' + self.date].find()    
            self.data = {
                'data' : list(data),
                'index' : list(index)
            }



    def is_batch(self):
        return ',' in self.trade['params']['code']


    def load_batch_data(self):
        self.data = {
            'data' : {},
            'index' : {}
        }
        codes = self.trade['params']['code'].split(',')
        for code in codes:
            data = self.data_db[code + '-' + self.date].find()
            self.data['data'][code] = list(data)
            if(code.startswith('3') and Constants.INDEX[5] not in self.data['index']):
                index = self.data_db[Constants.INDEX[5] + '-' + self.date].find()
                self.data['index'][Constants.INDEX[5]] = list(index)
            elif(Constants.INDEX[0] not in self.data['index']):
                index = self.data_db[Constants.INDEX[0] + '-' + self.date].find()
                self.data['index'][Constants.INDEX[0]] = list(index)




    def updateTrade(self, update):
        Real._logger.info('update tradeId={} with update = {}'.format(self.tradeId, update))
        return self.db[self.cols['trades']].update_one({"_id" : ObjectId(self.tradeId)},{"$set" : update})


    def updateConfig(self, update):
        Real._logger.info('update configId={} with update = {}'.format(self.config['_id'], update))
        return self.db[self.cols['configs']].update_one({"_id" : self.config['_id']}, update)


    def get_data(self):
        if(self.is_batch()):
            return self.strategy.get_match_data()
        return self.data['data']
    
    
    def get_code(self):
        if(self.is_batch()):
            return self.get_data()[-1]['code']
        return self.trade['params']['code']

    def createOrder(self):
        data = self.get_data()[-1]
        code = self.get_code()
        price = float(data['price'])
        Real._logger.info(f'start create order for code = {code}, time = {data["time"]}')
        if(self.strategyMeta['op'] == 'buy'):
            amount = float(self.trade['params']['volume'])
            volume = int(amount / price / 100) * 100
            if(volume >= 100):
                result = self.createDelegate(code, price, volume, self.strategyMeta['op'])
            else:
                result = {'result' : '买入总额不足100股', 'state' : Constants.STATE[3]}
        else:
            volume = int(self.trade['params']['volume'])
            result = self.createDelegate(code, price, volume, self.strategyMeta['op'])
        self.updateTrade(result)
        return result


    def createDelegate(self, code, price, volume, op):
        return {'result' : 'not allowed', 'state' : Constants.STATE[3]}


    def cancelOrder(self):
        if('order' not in self.trade):
            Real._logger.error('no order found in trade = {}, failde to cancel'.format(self.tradeId))
            update = {'state' : Constants.STATE[1], 'result' : '未找到订单'}
            self.updateTrade(update)
            return update
        htbh = self.trade['order']['result']['data']['htbh']
        today = datetime.now()
        htrq = '{}{}{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
        result = self.cancelDelegate(htbh, htrq)
        self.updateTrade(result)
        return result


    def cancelDelegate(self, htbh, wtrq):
        return {'result' : 'not allowed', 'state' : Constants.STATE[3]}  


    def reLogin(self):
        return {'result' : 'not allowed', 'state' : Constants.STATE[3]}  


    def check_chengjiao(self, htbh):
        if(self.trade['state'] == Constants.STATE[4]):
            return
        update = self.queryChenjiao(htbh)
        if(len(update) == 0):
            return
        self.updateTrade(update)
        

    def queryChenjiao(self, htbh):
        return {'result' : 'not allowed', 'state' : Constants.STATE[3]}


    


    def init_Config(self):
        self.load_trade_config()
        self.strategyMeta = self.db['strategies'].find_one({"_id" : self.trade['strategyId']})
        Real._logger.info('tradeId = {} load startegy = {}'.format(self.tradeId, self.strategyMeta))
        class_name = self.strategyMeta['url']
        strategyClass = locate('firestone_engine.strategies.{}.{}'.format(class_name, class_name))
        self.strategy = strategyClass()
        if(self.strategy is None):
            Real._logger.error(f'failed to load strategy {class_name}')


    def close(self):
        self.client.close()