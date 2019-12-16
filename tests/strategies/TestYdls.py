import unittest
from .TestBasic import TestBasic
from firestone_engine.strategies.Ydls import Ydls

class TestYdls(TestBasic, unittest.TestCase):
    
    
    def get_test_config(self):
        return {
            'tradeId' : '5db7e0a555609bb27252edb5',
            'configId' : '5db796e4429e4baab72826a0',
            'data_col' : '300448-2019-12-10',
            'index_col' : 'cyb-2019-12-10'
        }    


    def setUp(self):
        self.baseSetUp()


    def tearDown(self):
        self.baseTearDown()

    def createStrategy(self):
        self.strategy = Ydls()


    def runAssert(self):
        self.assertEqual(self.temp_data[-1]['time'], '09:33:03')


if __name__ == "__main__":
    unittest.main()

# # to debug in vscode uncomment this block
# import ptvsd
# # 5678 is the default attach port in the VS Code debug configurations
# print("start debug on port 5678")
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()