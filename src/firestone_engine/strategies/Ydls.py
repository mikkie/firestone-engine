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
        open_price = Decimal(self.dataLastRow['open'])
        pre_close = Decimal(self.dataLastRow['pre_close'])
        if(open_price >= price):
            return False
        vibration = Utils.round_dec((high - low) / pre_close * 100)
        if(vibration > Decimal(self.trade['params']['speed']['max_vibration']) or vibration < Decimal(self.trade['params']['speed']['min_vibration'])):
            return False
        upper_shadow = Utils.round_dec((high - price) / (high - low))
        if(upper_shadow > Decimal(self.trade['params']['speed']['upper_shadow'])):
            return False    
        flag = False
        if(index_percent < 0):
            flag = stock_percent > index_percent * Decimal(self.trade['params']['speed']['ratio_l'])
        else:
            flag = stock_percent > Decimal(self.trade['params']['speed']['ratio_r']) * index_percent
        if(flag):
            Ydls._logger.info(f'Ydls matched shape open_price = {open_price}, price = {price}, vibration = {vibration}, upper_shadow = {upper_shadow}, stock_percent = {stock_percent}')
        return flag


    def match_money(self):
        length = self.get_data_length()
        if(length < Ydls._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['speed']['time'])
        amount = float(self.trade['params']['speed']['amount']) * 10000
        index = int(20 * time)
        index = index * -1 if length >= index else length * -1
        pre_amount = float(self.data[index]['amount'])
        cur_amount = float(self.dataLastRow['amount'])
        buy_amount = cur_amount - pre_amount
        flag = buy_amount >= amount
        if(flag):
            Ydls._logger.info(f'Ydls matched money buy_amount = {buy_amount}')
        return flag