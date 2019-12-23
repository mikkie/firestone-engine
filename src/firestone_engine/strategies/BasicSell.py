import logging
import math
from decimal import Decimal
from .Base import Base
from firestone_engine.Utils import Utils

class BasicSell(Base):

    _logger = logging.getLogger(__name__)

    def matchCondition(self):
        if(self.match_hard_stop() or self.match_soft_stop()):
            return Base.matchCondition(self)   
        return False


    def match_hard_stop(self):
        cb = float(self.trade['params']['cb'])
        percent = self.get_percent_by_price(cb, self.dataLastRow)
        hard_stop = Decimal(self.trade['params']['hard_stop'])
        flag = percent < hard_stop
        if(flag):
            BasicSell._logger.info(f"BasicSell code={self.dataLastRow['code']} match hard_stop percent={percent}, hard_stop={hard_stop}")
        return flag


    def match_sell_on_zt(self):
        price = Decimal(self.dataLastRow['price'])
        pre_close = float(self.dataLastRow['pre_close'])
        if(abs(price - Utils.round_dec(pre_close * 1.1)) < Base.SMALL_NUMBER):
            if(self.trade['params']['sell_on_zt'] == '1'):
                return 1
            return 0    
        return -1

    def match_start_line(self):
        cb = float(self.trade['params']['cb'])
        percent = self.get_percent_by_price(cb, self.dataLastRow)
        start_line = Decimal(self.trade['params']['start_line'])
        return percent > start_line

    def match_soft_stop(self):
        if(not self.match_start_line()):
            return False
        if(self.match_sell_on_zt() == 1):
            BasicSell._logger.info(f"BasicSell code={self.dataLastRow['code']} match sell_on_zt")
            return True
        elif(self.match_sell_on_zt() == 0):
            return False
        if(not hasattr(self, 'soft_stop')):
            self.soft_stop = self.calc_soft_stop()
            return False
        if(self.get_data_length() < 2):
            return False
        percent = self.get_current_data_percent()
        last_percent = self.get_percent(self.data[-2])
        if(percent < self.soft_stop):
            BasicSell._logger.info(f"BasicSell code={self.dataLastRow['code']} match soft_stop percent={percent} soft_stop={self.soft_stop}")
            if(not hasattr(self, 'hit_stop_count')):
                self.hit_stop_count = 1
                return False
            else:
                self.hit_stop_count += 1
                if(self.hit_stop_count >= int(self.trade['params']['soft_stop']['hit_stop_limit'])):
                    return True
        else:
            self.hit_stop_count = 0
        if(percent > last_percent):
            self.soft_stop = self.calc_soft_stop()
        return False


    def calc_soft_stop(self):
        percent = float(self.get_current_data_percent())
        index_percent = float(self.get_current_index_percent())
        max_loss = float(self.trade['params']['soft_stop']['max_loss'])
        max_index = float(self.trade['params']['soft_stop']['max_index'])
        ratio_stock = float(self.trade['params']['soft_stop']['ratio_stock'])
        ratio_index = float(self.trade['params']['soft_stop']['ratio_index'])
        pre_close = float(self.dataLastRow['pre_close'])
        zt_p = float(Utils.round_dec((Utils.round_dec(pre_close * 1.1) - Decimal(pre_close)) / Decimal(pre_close) * 100))
        if(index_percent > max_index):
            ratio_index = 0
        y1 = (max_loss / 100) * math.pow(percent - zt_p, 2) if percent >= 0 else (max_loss / 100) * math.pow(percent + zt_p, 2)
        y2 = (max_loss / math.pow(max_index, 2)) * math.pow(index_percent - max_index, 2) if(index_percent >= 0) else (max_loss / math.pow(max_index, 2)) * math.pow(index_percent + max_index, 2)
        y = ((y1 * ratio_stock) + (y2 * ratio_index)) / (ratio_stock + ratio_index)
        return Utils.round_dec(percent - y)