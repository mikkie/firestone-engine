import logging
import time
import pytz
from datetime import datetime, timedelta
import tushare as ts
import pandas as pd
from decimal import Decimal
from firestone_engine.Utils import Utils
from bson.objectid import ObjectId

class ConceptPick(object):
    
    _logger = logging.getLogger(__name__)

    UTC_8 = pytz.timezone('Asia/Shanghai')

    _BATCH_SIZE = 50

    _MAX_SIZE = 150

    def run(self, trade, config, db, is_mock):
        self.is_mock = is_mock
        self.db = db
        today = datetime.now()
        self.today = '{}-{}-{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
        self.trade = trade
        self.config = config
        self.get_match_concepts()
        self.pick_all_match_stocks()


    def get_match_concepts(self):
        try:
            load_time = datetime.now(tz=ConceptPick.UTC_8) - timedelta(minutes=2)
            hot_concepts = list(self.db['hot_concept'].find({'time' : {'$gte' : load_time}}).sort([('time', -1)]).limit(10))
            if(len(hot_concepts) == 0):
                self.match_concepts = []
                ConceptPick._logger.warning('failed to get hot concepts')
                return
            concepts = []
            for concept in hot_concepts:
                if(float(concept['index_percent'][:-1]) < float(self.trade['params']['index_percent']) or int(concept['company_count']) > int(self.trade['params']['company_count']) or float(concept['stock_percent'][:-1]) < float(self.trade['params']['stock_percent'])):
                    continue
                concepts.append(concept)
            self.match_concepts = concepts
            ConceptPick._logger.info(f'match hot concepts are {concepts}')
        except Exception as e:
            ConceptPick._logger.error(f'get match concept failed, e = {e}')
            self.match_concepts = []


    def pick_all_match_stocks(self):
        if(len(self.match_concepts) == 0):
            ConceptPick._logger.warning(f'no match hot concepts')
            return
        for concept in self.match_concepts:
            try:
                if(concept['name'] not in self.config['monitor_concept']): 
                    self.pick_match_stocks(concept)
            except Exception as e:
                ConceptPick._logger.error(f"pick_match_stocks for concept {concept['name']} failed, e = {e}")


    def pick_match_stocks(self, concept):
        condition = []
        for i in range(int(self.trade['params']['top_concept'])):
            condition.append({f'concepts.{i}' : concept['name']})
        stocks = list(self.db['concepts'].find({'$or' : condition}))
        if(len(stocks) == 0):
            ConceptPick._logger.warning(f"no match stocks for concept {concept['name']}")
            return
        self.filter_stocks(stocks, concept)


    def rank_concept(self, stock, hot_concept):
        concepts = stock['concepts']
        stock['rank_concept'] = [int(k) for k, concept in concepts.items() if concept == hot_concept['name']][0]


    def filter_stocks(self, stocks, concept):
        result = []
        for stock in stocks:
            now = datetime.now()
            if(stock['type'] in ['大盘股','超大盘股']):
                continue
            if(stock['xsjj'] is not None and stock['xsjj'] != ''):
                xsjj = datetime.strptime(stock['xsjj'], '%Y-%m-%d')
                if(xsjj > now and (xsjj - now).days < 30):
                    continue
            self.rank_concept(stock, concept)        
            result.append(stock)
        if(len(result) == 0):
            ConceptPick._logger.warning(f"no match stocks for concept {concept['name']} after filter")
            return
        result.sort(key=lambda x: x['rank_concept'])
        self.get_top_rank_stocks(result, concept)


    def get_top_rank_stocks(self, stocks, concept):
        full_df = pd.DataFrame()
        codes = [stock['code'] for stock in stocks][:ConceptPick._MAX_SIZE]
        length = len(codes)
        start = 0
        while(start < length):
            end = start + ConceptPick._BATCH_SIZE
            temp_codes = codes[start : end]
            df = ts.get_realtime_quotes(temp_codes)
            full_df = full_df.append(df)
            start = end
            time.sleep(3)
        full_df['percent'] = (full_df['price'].astype(float) - full_df['pre_close'].astype(float)) / full_df['pre_close'].astype(float) * 100
        index_percent = float(concept['index_percent'][:-1])
        full_df = full_df[(full_df['percent'] > index_percent) & (full_df['percent'] < float(self.trade['params']['max_percent']))]
        if(len(full_df) == 0):
            ConceptPick._logger.warning(f"no match stocks for concept {concept['name']} after rank")
            return
        concept_df = pd.DataFrame(stocks)
        full_df = pd.merge(full_df, concept_df,  how='left', left_on=['code'], right_on = ['code'])
        full_df = full_df.sort_values('rank_concept')  
        full_df = full_df[0 : int(self.trade['params']['monitor_count'])]
        self.start_monitor(full_df)
        self.config['monitor_concept'].append(concept['name'])
        self.updateConfig({'$set' : {'monitor_concept' : self.config['monitor_concept']}})


    def updateConfig(self, update):
        ConceptPick._logger.info('update configId={} with update = {}'.format(self.config['_id'], update))
        collname = 'configmocks' if self.is_mock else 'configs'
        return self.db[collname].update_one({"_id" : self.config['_id']}, update)


    def start_monitor(self, df):
        collname = 'mocktrades' if self.is_mock else 'trades'
        codes_data = self.db[collname].find({"deleted":False, "params.executeDate" : self.today},{"code" : 1, "_id" : 0})
        code_list = [code_data["code"] for code_data in list(codes_data)]
        codes = [code for code in list(df['code']) if code not in code_list]
        strategyId = self.trade['params']['strategyId']
        strategy_data = list(self.db['strategies'].find({"_id" : ObjectId(strategyId)}))
        if(len(strategy_data) == 0):
            ConceptPick._logger.error(f"failed to get strategy, id = {strategyId}")
            return
        strategy = strategy_data[0]    
        for code in set(codes):
            strategy['parameters']['code'] = code
            strategy['parameters']['executeDate'] = self.today
            trade_json = {
                'code' : code,
                "state" : "运行中",
                "result" : "无",
                "userId" : self.config['userId'],
                "strategyId" : ObjectId(strategyId),
                "createDate" : datetime.now(),
                "deleted" : False,
                "params" : strategy['parameters']
            }
            self.db[collname].insert_one(trade_json)
            ConceptPick._logger.info(f"create trade = {trade_json}")