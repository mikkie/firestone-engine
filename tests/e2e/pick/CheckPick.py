from firestone_engine.Mock import Mock
from pymongo import MongoClient
import unittest

class CheckPick(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['firestone-test']
        self.mock = Mock('5db7e0a555609bb27252edb7', date='2020-01-06')
        self.mock.init_Config()
        self.mock.load_trade()
        
    def testTradeState(self):
        mocktrades = list(self.db['mocktrades'].find({}))
        self.assertGreater(len(mocktrades), 1)

    def tearDown(self):
        self.mock.close()

if __name__ == "__main__":
    unittest.main()