from pymongo import MongoClient
from bson.objectid import ObjectId

class Real(object):

    _MONFO_URL = '127.0.0.1'

    _DB = 'firestone'

    _DATA_DB = 'firestone-data'
    
    def __init__(self, tradeId):
        self.tradeId = tradeId
        self.client = MongoClient(Real._MONFO_URL, 27017)
        self.db = self.client[Real._DB]
        self.data_db = self.client[Real._DATA_DB]
        self.init_cols()
        self.init_config()


    def init_cols(self):
        self.cols = {
            'trades' : 'trades',
            'configs' : 'configs'
        }    


    def run(self):
        self.data = self.data_db[self.trade['params']['code']].find()
        print(self.config)


    def init_config(self):
        self.trade = self.db[self.cols['trades']].find_one({"_id" : ObjectId(self.tradeId)})  
        self.strategy = self.db['strategies'].find_one({"_id" : self.trade['strategyId']})
        self.config = self.db[self.cols['configs']].find_one({"userId" : self.trade['userId']})


    def close(self):
        self.client.close() 