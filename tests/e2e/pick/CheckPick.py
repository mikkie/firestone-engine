from firestone_engine.Mock import Mock
import unittest

class CheckPick(unittest.TestCase):

    def setUp(self):
        self.mock = Mock('5db7e0a555609bb27252edb7', date='2020-01-06')
        self.mock.init_Config()
        self.mock.load_trade()
        
    def testTradeState(self):
        self.assertGreaterEqual(self.mock.trade['result'].find('创建监控:'), 0)

    def tearDown(self):
        self.mock.close()

if __name__ == "__main__":
    unittest.main()