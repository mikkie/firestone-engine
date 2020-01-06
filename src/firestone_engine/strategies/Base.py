import logging
from datetime import datetime
from decimal import Decimal
from firestone_engine.Utils import Utils
import math

class Base(object):

    _logger = logging.getLogger(__name__)

    SMALL_NUMBER = math.pow(10, -6)
      
    def run(self, trade, config, data, index):
        self.trade = trade
        self.config = config
        self.data = data
        self.dataLastRow = self.data[-1]
        self.index = index
        self.indexLastRow = self.index[-1]
        if(self.match_monitorTime()):
            return self.matchCondition()
        return False


    def need_create_order(self):
        return True

        
    def match_monitorTime(self):
        start = datetime.strptime('{} {}:00'.format(self.dataLastRow['date'], self.trade['params']['monitorTime']['start']), '%Y-%m-%d %H:%M:%S')    
        end = datetime.strptime('{} {}:00'.format(self.dataLastRow['date'], self.trade['params']['monitorTime']['end']), '%Y-%m-%d %H:%M:%S')
        dataTime = datetime.strptime('{} {}'.format(self.dataLastRow['date'], self.dataLastRow['time']), '%Y-%m-%d %H:%M:%S')
        return dataTime >= start and dataTime <= end


    def matchCondition(self):
        Base._logger.info('tardeId = {}, {}, the strategy {} match the condition, data = {}, index = {}'.format(self.trade['_id'], datetime.now(), self.__class__, self.data[-1], self.index[-1]))
        return True


    def get_percent(self, row):
        price = float(row['price'])
        pre_close = float(row['pre_close'])
        return Utils.round_dec((price - pre_close) / pre_close * 100)

    def get_percent_by_price(self, price, row):
        pre_close = float(row['pre_close'])
        return Utils.round_dec((price - pre_close) / pre_close * 100)


    def get_current_data_percent(self):
        return self.get_percent(self.dataLastRow)

    def get_current_index_percent(self):
        return self.get_percent(self.indexLastRow)


    def get_data_length(self):
        return len(self.data)

    def is_positive_buy(self, row, last_row):
        if(last_row['time'] <= '09:30:03'):
            return False
        if((datetime.strptime(row['time'], '%H:%M:%S') - datetime.strptime(last_row['time'], '%H:%M:%S')).seconds >= 5):
            return False
        price = Decimal(row['price'])
        a1_p = Decimal(last_row['a1_p'])
        return price >= a1_p
    
