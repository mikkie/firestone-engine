import unittest
import time
from firestone_engine.Mock import Mock
from firestone_engine.strategies.Basic import Basic

class TestMock(unittest.TestCase):
    
    
    def setUp(self):
        self.mock = Mock('5da1800e87b64fb6f4c32503', date='2019-10-30')


    def testInitConfig(self):
        self.mock.init_Config()
        self.assertEqual(self.mock.trade['code'], '000993')
        self.assertEqual(self.mock.trade['params']['index_percent']['low'], '-0.18')
        self.assertEqual(self.mock.trade['params']['percent']['high'], '0.0')

        self.assertEqual(self.mock.strategyMeta['url'], 'Basic')
        self.assertEqual(self.mock.strategyMeta['op'], 'buy')

        self.assertEqual(self.mock.config['ths_url'], 'http://mncg.10jqka.com.cn/cgiwt/index/index')
        self.assertEqual(self.mock.config['maxBuyNum'], 3.0)

        self.assertIsInstance(self.mock.strategy, Basic)


    def test_load_data(self):
        self.mock.load_data()    
        self.assertEqual(len(self.mock.data['data']), 4794)
        self.assertEqual(len(self.mock.data['index']), 4794)


    def testUpdateTrade(self):
        result = self.mock.updateTrade({'state' : '停止'})
        self.assertEqual(result.matched_count, 1)
        self.mock.load_trade()
        self.assertEqual(self.mock.trade['state'], '停止')


    def testUpdateTrade1(self):
        result = self.mock.updateTrade({'result' : '订单提交失败, 请检查配置', 'state' : '异常'})
        self.assertEqual(result.matched_count, 1)
        self.mock.load_trade()
        self.assertEqual(self.mock.trade['result'], '订单提交失败, 请检查配置')
        self.assertEqual(self.mock.trade['state'], '异常')

        

    def testUpdateOrder(self):
        order = {"errorcode":0,"errormsg":"\u8bf7\u6c42\u6210\u529f   ","result":{"list":[],"data":{"ret_code":"0","ret_msg":"\u8bf7\u6c42\u6210\u529f   ","request_begin_time":"2019-10-29","gdxm":"UID_415399","zjzh":"48039195","yyb_ip":"trade.10jqka.com.cn","client_ip":"120.41.213.196","lg_account":"48039195","cmd":"cmd_wt_mairu","amount":"100","stockcode":"000793","req_time":"12","option":"1","yyb_id":"0","lg_account_type":"0","price":"3.27","usedeftxmm":"1","mkcode":"1","gdzh":"0098894246","extend":"wtfs*web|mobile*web|client*web|solicated*|zjzh*48039195|notcheck*1|","iskfjj":"0","htbh":"1249578371","yyb_port":"8002"},"extend":{"extend_data":""}}}
        result = self.mock.updateTrade({'order' : order})
        self.assertEqual(result.matched_count, 1) 
        self.mock.load_trade()
        self.assertEqual(self.mock.trade['order']['result']['data']['htbh'], '1249578371')


    def testUpdateConfig(self):
        self.mock.updateConfig({ '$inc': { 'curBuyNum': 1 } })
        self.mock.load_trade_config()
        self.assertEqual(self.mock.config['curBuyNum'], 1)



    # def testCreateOrder(self):
    #     result = self.mock.createDelegate('000793', 2.74, 100, 'buy')
    #     self.assertEqual(result['state'], '已提交')
    #     print(result['result'])
    #     result = self.mock.createDelegate('000793', 3.34, 100, 'sell')
    #     self.assertEqual(result['state'], '已提交')
    #     print(result['result'])

    # def testCreateOrder1(self):
    #     for i in range(0, 12):
    #         result = self.mock.queryChenjiao('heart_beat')
    #         print(result)
    #         time.sleep(600)
    #     result = self.mock.createDelegate('300017', 8.96, 100, 'buy')
    #     self.assertEqual(result['state'], '已提交')
    #     print(result['result'])


    # def testQueryChengjiao(self):
    #     result = self.mock.queryChenjiao('1252365040')
    #     self.assertEqual(result['state'],'已完成')
    #     print(result['result'])


    # def testCancelDeligate(self):
    #     result = self.mock.cancelDelegate('1253762489', '20191101')
    #     self.assertEqual(result['state'],'暂停')
    #     print(result['result'])

    # def testRelogin(self):
    #     result = self.mock.reLogin()
    #     self.assertEqual(len(result),0)
    #     print(result)


    def tearDown(self):
        self.mock.close()



if __name__ == "__main__":
    unittest.main()

# # to debug in vscode uncomment this block
# import ptvsd
# # 5678 is the default attach port in the VS Code debug configurations
# print("start debug on port 5678")
# ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
# ptvsd.wait_for_attach()