import logging
from .Basic import Basic

class Ydls(Basic):

    _MIN_TIME_PERIOD_LENGTH = 15


    def match_data(self):
        if(Basic.match_data(self)):
            return self.match_speed()
        return False


    def match_speed(self):
        if(self.dataLastRow['time'] == '09:43:48'):
            print(self.dataLastRow)
        length = self.get_data_length()
        if(length < Ydls._MIN_TIME_PERIOD_LENGTH):
            return False
        time = float(self.trade['params']['speed']['time'])
        percent = float(self.trade['params']['speed']['percent'])
        index = int(20 * time)
        index = index * -1 if length >= index else length * -1
        pre_percent = self.get_percent(self.data[index])
        cur_percent = self.get_current_data_percent()
        return cur_percent - pre_percent >= percent