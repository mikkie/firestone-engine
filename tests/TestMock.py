import unittest
from firestone_engine.Mock import Mock

class TestMock(unittest.TestCase):
    
    
    def setUp(self):
        self.mock = Mock('5da1800e87b64fb6f4c32503')


    def testInitConfig(self):
        self.mock.init_Config()
        self.assertEqual(self.mock.trade['code'], '300692')
        self.assertEqual(self.mock.trade['params']['index_percent']['low'], '-1.0')
        self.assertEqual(self.mock.trade['params']['percent']['high'], '2.5')

        self.assertEqual(self.mock.strategyMeta['url'], 'Basic')
        self.assertEqual(self.mock.strategyMeta['op'], 'buy')

        self.assertEqual(self.mock.config['ths_url'], 'http://mncg.10jqka.com.cn/cgiwt/index/index')
        self.assertEqual(self.mock.config['maxBuyNum'], 3.0)


    # def testCreateOrder(self):
    #     result = self.mock.createOrder('000793', 3.45, 100, 'buy')
    #     self.assertEqual(result['errorcode'], 0)
    #     result = self.mock.createOrder('300152', 4.11, 100, 'sell')
    #     self.assertEqual(result['errorcode'], 0)


    def testUpdateResult(self):
        result = self.mock.updateResult('订单提交失败, 请检查配置',state='异常')
        self.assertEqual(result.modified_count, 1)  

    def tearDown(self):
        self.mock.close()



if __name__ == "__main__":
    unittest.main()

# to debug in vscode uncomment this block
import ptvsd
# 5678 is the default attach port in the VS Code debug configurations
print("start debug on port 5678")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()