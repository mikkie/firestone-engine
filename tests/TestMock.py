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


    # def testUpdateResult(self):
    #     result = self.mock.updateResult('订单提交失败, 请检查配置',state='异常')
    #     self.assertEqual(result.modified_count, 1)

    def testUpdateOrder(self):
        order = {"errorcode":0,"errormsg":"\u8bf7\u6c42\u6210\u529f   ","result":{"list":[],"data":{"ret_code":"0","ret_msg":"\u8bf7\u6c42\u6210\u529f   ","request_begin_time":"2019-10-29","gdxm":"UID_415399","zjzh":"48039195","yyb_ip":"trade.10jqka.com.cn","client_ip":"120.41.213.196","lg_account":"48039195","cmd":"cmd_wt_mairu","amount":"100","stockcode":"000793","req_time":"12","option":"1","yyb_id":"0","lg_account_type":"0","price":"3.27","usedeftxmm":"1","mkcode":"1","gdzh":"0098894246","extend":"wtfs*web|mobile*web|client*web|solicated*|zjzh*48039195|notcheck*1|","iskfjj":"0","htbh":"1249578371","yyb_port":"8002"},"extend":{"extend_data":""}}}
        result = self.mock.updateOrder(order)
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