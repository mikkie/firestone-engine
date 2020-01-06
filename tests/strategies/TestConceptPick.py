from pymongo import MongoClient
from firestone_engine.strategies.ConceptPick import ConceptPick
from bson import ObjectId
import unittest

class TestConceptPick(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['firestone-test']
        self.trade = self.db['mocktrades'].find_one({"_id" : ObjectId('5db7e0a555609bb27252edb7')})
        self.config = self.db['configmocks'].find_one({"_id" : ObjectId('5db796e4429e4baab72826a0')})
        self.is_mock = True
        self.userId = '5d905db9fc84d3224b0eb59c'
        self.cp = ConceptPick()


    def test_pick_concepts(self):
        self.cp.run(self.trade, self.config, self.db, self.is_mock)
        self.config = self.db['configmocks'].find_one({"_id" : ObjectId('5db796e4429e4baab72826a0')})
        print(self.config['monitor_concept'])
        self.assertEqual(self.config['monitor_concept'], ["小金属概念", "黄金概念"])


    def tearDown(self):
        self.client.close()


if __name__ == "__main__":
    unittest.main()

# # to debug in vscode uncomment this block
# import ptvsd
# # 5678 is the default attach port in the VS Code debug configurations
# print("start debug on port 5678")
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()
    