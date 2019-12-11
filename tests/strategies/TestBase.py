from pymongo import MongoClient
from firestone_engine.strategies.Base import Base
from bson import ObjectId

class TestBase(object):


    def baseSetUp(self):
        self.test_config = self.get_test_config()
        self.client = MongoClient('127.0.0.1', 27017)
        self.DB = self.client['firestone-test']
        self.DB_DATA = self.client['firestone-data']
        self.trade = self.DB['mocktrades'].find_one({"_id" : ObjectId(self.test_config['tradeId'])})
        self.config = self.DB['configmocks'].find_one({"_id" : ObjectId(self.test_config['configId'])})
        self.data = list(self.DB_DATA[self.test_config['data_col']].find())
        self.index = list(self.DB_DATA[self.test_config['index_col']].find())


    def get_test_config(self):
        return {
            'tradeId' : '5da1800e87b64fb6f4c32503',
            'configId' : '5db796e4429e4baab72826a0',
            'data_col' : '000793-2019-10-28',
            'index_col' : 'sh-2019-10-28'
        }    


    def testRunWrapper(self):
        self.createStrategy()
        self.temp_data = []
        self.temp_index = []
        i = 0
        while i < len(self.data):
            self.temp_data.append(self.data[i])
            if i < len(self.index):
                self.temp_index.append(self.index[i])
            if(self.strategy.run(self.trade, self.config, self.temp_data, self.temp_index)):
                self.runAssert()
                return
            i += 1
        self.runAssert()


    def runAssert(self):
        pass


    def createStrategy(self):
        self.strategy = Base()


    def baseTearDown(self):
        self.client.close()

