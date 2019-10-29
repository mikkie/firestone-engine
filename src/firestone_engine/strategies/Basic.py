import logging
from .Base import Base
from datetime import datetime
from firestone_engine.Utils import Utils

class Basic(Base):

    _logger = logging.getLogger(__name__)
    
    def matchCondition(self):
        if(self.match_index() and self.match_data()):
            return Base.matchCondition(self)   
        return False 


    def match_index(self):
        price = float(self.indexLastRow['price'])
        pre_close = float(self.indexLastRow['pre_close'])
        percent = Utils.round_dec((price - pre_close) / pre_close * 100)
        percent_low = float(self.trade['params']['index_percent']['low'])
        percent_high = float(self.trade['params']['index_percent']['high'])
        percent_high = 10.1 if percent_high >= 10.0 else percent_high
        flag = (percent >= percent_low and percent <= percent_high)
        if(flag):
            Base._logger.info('real_time = {}, tradeId = {} match index, time = {}, percent = {}, low = {}, high = {}'.format(datetime.now(), self.trade['_id'], self.indexLastRow['time'], percent, percent_low, percent_high))
        return flag


    def match_data(self):
        price = float(self.dataLastRow['price'])
        pre_close = float(self.dataLastRow['pre_close'])
        percent = Utils.round_dec((price - pre_close) / pre_close * 100)
        percent_low = float(self.trade['params']['percent']['low'])
        percent_high = float(self.trade['params']['percent']['high'])
        percent_high = 10.1 if percent_high >= 10.0 else percent_high
        flag = (percent >= percent_low and percent <= percent_high)
        if(flag):
            Base._logger.info('real_time = {}, tradeId = {} match data, time = {}, percent = {}, low = {}, high = {}'.format(datetime.now(), self.trade['_id'], self.dataLastRow['time'], percent, percent_low, percent_high))
        return flag
