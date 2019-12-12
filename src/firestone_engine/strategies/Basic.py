import logging
from .Base import Base
from datetime import datetime
from decimal import Decimal
from firestone_engine.Utils import Utils

class Basic(Base):

    _logger = logging.getLogger(__name__)
    
    def matchCondition(self):
        if(self.match_index() and self.match_data()):
            return Base.matchCondition(self)   
        return False 


    def match_index(self):
        percent = self.get_current_index_percent()
        percent_low = Decimal(self.trade['params']['index_percent']['low'])
        percent_high = Decimal(self.trade['params']['index_percent']['high'])
        percent_high = 10.1 if percent_high >= 10.0 else percent_high
        flag = (percent >= percent_low and percent <= percent_high)
        if(flag):
            Basic._logger.info('real_time = {}, tradeId = {} match index, time = {}, percent = {}, low = {}, high = {}'.format(datetime.now(), self.trade['_id'], self.indexLastRow['time'], percent, percent_low, percent_high))
        return flag


    def match_data(self):
        percent = self.get_current_data_percent()
        percent_low = Decimal(self.trade['params']['percent']['low'])
        percent_high = Decimal(self.trade['params']['percent']['high'])
        percent_high = 10.1 if percent_high >= 10.0 else percent_high
        flag = (percent >= percent_low and percent <= percent_high)
        if(flag):
            Basic._logger.info('real_time = {}, tradeId = {} match data, time = {}, percent = {}, low = {}, high = {}'.format(datetime.now(), self.trade['_id'], self.dataLastRow['time'], percent, percent_low, percent_high))
        return flag

