import logging
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from .Ydls import Ydls
from decimal import Decimal
from ..Constants import Constants
from firestone_engine.Utils import Utils
import pandas as pd

class BatchYdls(object):
    
    _logger = logging.getLogger(__name__)

    def run(self, trade, config, db, data, index):
        self.trade = trade
        self.config = config
        self.db = db
        self.data = data
        self.index = index
        self.ydls = Ydls()
        self.load_ydls_strategy()
        today = datetime.now()
        self.today = '{}-{}-{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
        if(self.match_monitorTime()):
            return self.matchCondition()
        return False

    def need_create_order(self):
        return True

    def match_monitorTime(self):
        start = datetime.strptime('{} {}:00'.format(self.today, self.trade['params']['monitorTime']['start']), '%Y-%m-%d %H:%M:%S')    
        end = datetime.strptime('{} {}:00'.format(self.today, self.trade['params']['monitorTime']['end']), '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        return now >= start and now <= end


    def matchCondition(self):
        max_percent = self.get_max_stock_percent()
        if(max_percent < float(self.trade['params']['max_stock_percent'])):
            return False
        for code, data in self.data.items():
            open_percent = self.get_percent_by_price(float(data[-1]['open']), data[-1])
            if(open_percent < Decimal(self.trade['params']['open_percent_low']) or open_percent > Decimal(self.trade['params']['open_percent_high'])):
                continue
            if(code.startswith('3')):
                index = self.index[Constants.INDEX[5]]
            else:
                index = self.index[Constants.INDEX[0]]
            trade = {
                '_id' : self.trade['_id'],
                'code' : code,
                'params' : self.strategyMeta['parameters']
            }
            trade['params']['volume'] = self.trade['params']['volume']
            if(self.ydls.run(trade, self.config, data, index)):
                self.match_data = data
                BatchYdls._logger.info(f'code = {code} matched in trade = {self.trade["_id"]}')
                return True
        return False


    def get_match_data(self):
        return self.match_data


    def get_max_stock_percent(self):
        data_list = []
        for item in self.data.items():
            data = item[1]
            data_list.append(data[-1])
        df = pd.DataFrame(data_list)
        df['percent'] = (df['price'].astype(float) - df['pre_close'].astype(float)) / df['pre_close'].astype(float) * 100
        row = df.loc[df['percent'].idxmax()]
        return float(row['percent'])


    def get_percent_by_price(self, price, row):
        pre_close = float(row['pre_close'])
        return Utils.round_dec((price - pre_close) / pre_close * 100)

    
    def load_ydls_strategy(self):
        strategyId = self.trade['params']['strategyId']
        self.strategyMeta = self.db['strategies'].find_one({"_id" : ObjectId(strategyId)})
