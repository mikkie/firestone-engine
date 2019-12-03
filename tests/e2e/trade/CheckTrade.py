from firestone_engine.Mock import Mock
import unittest

class CheckTrade(unittest.TestCase):

    def setUp(self):
        self.mock = Mock('5da1800e87b64fb6f4c32503', date='2019-10-30')
        self.mock.init_Config()
        self.mock.load_trade()
        
    def testTradeState(self):
        self.assertEqual(self.mock.trade['state'], '已完成')
        self.assertEqual(self.mock.trade['result'], '以xx.xx成交xx股,合同编号000000')

    def tearDown(self):
        self.mock.close()

if __name__ == "__main__":
    unittest.main()