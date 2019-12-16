import logging
from .Basic import Basic
from decimal import Decimal
from firestone_engine.Utils import Utils

class Ydls(Basic):

    _logger = logging.getLogger(__name__)

    _MIN_TIME_PERIOD_LENGTH = 15


    def match_data(self):
        if(Basic.match_data(self)):
            return self.match_shape() and self.match_money()
        return False


    def match_shape(self):
        stock_percent = self.get_current_data_percent()
        index_percent = self.get_current_index_percent()
        high = Decimal(self.dataLastRow['high'])
        low = Decimal(self.dataLastRow['low'])
        price = Decimal(self.dataLastRow['price'])
        lower_shadow = Utils.round_dec((price - low) / (high - low))
        if(price == low):
            return False
        if(lower_shadow > Decimal(self.trade['params']['speed']['lower_shadow'])):
            return False    
        flag = False
        if(index_percent < 0):
            flag = stock_percent > index_percent * Decimal(self.trade['params']['speed']['ratio_l'])
        else:
            flag = stock_percent > Decimal(self.trade['params']['speed']['ratio_r']) * index_percent
        if(flag):
            Ydls._logger.info(f'Ydls matched shape lower_shadow = {lower_shadow}, stock_percent = {stock_percent}')
        return flag


    def match_money(self):
        length = self.get_data_length()
        if(length < Ydls._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['speed']['time'])
        amount = float(self.trade['params']['speed']['amount']) * 10000
        index = int(20 * time) + 1
        index = index * -1 if length >= index else length * -1
        buy_amount = 0
        while(index < -1):
            pre_amount = float(self.data[index]['amount'])
            next_amount = float(self.data[index + 1]['amount'])
            if(self.is_positive_buy(self.data[index + 1], self.data[index])):
                buy_amount += (next_amount - pre_amount)
            index += 1
        flag = buy_amount >= amount
        if(flag):
            Ydls._logger.info(f'Ydls matched money buy_amount = {buy_amount}')
        return flag