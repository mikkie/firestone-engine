import logging
from .Basic import Basic

class Ydls(Basic):

    _MIN_TIME_PERIOD_LENGTH = 15


    def match_data(self):
        if(Basic.match_data(self)):
            return self.match_shape() and self.match_money()
        return False


    def match_shape(self):
        if(self.dataLastRow['time'] == '09:43:48'):
            print('xxx')
        stock_percent = self.get_current_data_percent()
        index_percent = self.get_current_index_percent()
        high = float(self.dataLastRow['high'])
        low = float(self.dataLastRow['low'])
        price = float(self.dataLastRow['price'])
        open_price = float(self.dataLastRow['open'])
        pre_close = float(self.dataLastRow['pre_close'])
        if(open_price >= price):
            return False
        if((high - low) / pre_close > self.trade['params']['speed']['vibration']):
            return False
        if(index_percent < 0):
            return stock_percent > index_percent * self.trade['params']['speed']['ratio_l']
        else:
            return stock_percent > self.trade['params']['speed']['ratio_r'] * index_percent


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
        return cur_amount - pre_amount >= amount