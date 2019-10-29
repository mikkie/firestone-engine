import unittest
from .TestBase import TestBase
from firestone_engine.strategies.Basic import Basic

class TestBasic(TestBase, unittest.TestCase):


    def get_test_config(self):
        return {
            'tradeId' : '5db7e0a555609bb27252edb4',
            'configId' : '5db796e4429e4baab72826a0',
            'data_col' : '000793-2019-10-28',
            'index_col' : '000001-2019-10-28'
        }    


    def setUp(self):
        self.baseSetUp()


    def tearDown(self):
        self.baseTearDown()    


    def createStrategy(self):
        self.strategy = Basic()


    def runAssert(self):
        self.assertEqual(self.temp_data[-1]['time'], '09:31:00')


if __name__ == "__main__":
    unittest.main()

# to debug in vscode uncomment this block
import ptvsd
# 5678 is the default attach port in the VS Code debug configurations
print("start debug on port 5678")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()