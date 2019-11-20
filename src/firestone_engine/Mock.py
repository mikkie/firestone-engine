from .Real import Real
import requests
import logging
import json
from datetime import datetime
from .Constants import Constants

class Mock(Real):
    
    _logger = logging.getLogger(__name__)

    def __init__(self, tradeId, date=None):
        super(Mock,self).__init__(tradeId, date)
        self.__header = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.9',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'mncg.10jqka.com.cn',
            'Referer':'http://mncg.10jqka.com.cn/cgiwt/index/index',
            'X-Requested-With':'XMLHttpRequest',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        }


    def init_cols(self):
        self.cols = {
            'trades' : 'mocktrades',
            'configs' : 'configmocks'
        }


    def load_cookie(self):
        self.__header['Cookie'] = self.config['cookie']


    def createDelegate(self, code, price, volume, op):
        self.load_cookie()
        tradeType = 'cmd_wt_mairu' if op == 'buy' else 'cmd_wt_maichu'
        postData = {
            'type' : tradeType,
            'mkcode' : 1,
            'gdzh' : self.config['gdzh'],
            'stockcode' : code,
            'price' : price,
            'amount' : volume
        }
        if code.startswith('6'):
            postData['mkcode'] = 2
            postData['gdzh'] = self.config['sh_gdzh']
        try:   
            response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/tradestock/',data=postData,headers=self.__header)
            Mock._logger.info('mock tradeId = {}, code = {}, price = {}, volume = {}, op = {}, submit order get response = {}'.format(self.tradeId, code, price, volume, op, response.text))
            result = json.loads(response.text)
            if(result['errorcode'] == 0):
                op_cn = '买入' if op == 'buy' else '卖出'
                message = '订单提交: 在{},以{}{}[{}] {}股'.format(datetime.now(), price, op_cn, code, volume)
                return {'state' : Constants.STATE[2], 'result' : message, 'order' : result}
            return {'state' : Constants.STATE[3], 'result' : result['errormsg']}
        except Exception as e:
            Mock._logger.error('mock tradeId = {}, code = {}, price = {}, volume = {}, op = {}, faield with exception = {}'.format(self.tradeId, code, price, volume, op, e))
            return {'state' : Constants.STATE[3], 'result' : '创建订单失败'}


    def queryChenjiao(self, htbh):
        self.load_cookie()
        try:   
            response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/qryChengjiao',headers=self.__header)
            Mock._logger.info('mock tradeId = {} htbh = {} query chengjiao, get response = {}'.format(self.tradeId, htbh, response.text))
            result = json.loads(response.text)
            if(result['errorcode'] == 0):
                orders = result['result']['list']
                if(orders is not None and len(orders) > 0):
                    for order in orders:
                        if(order['d_2135'] == htbh):
                            message = '以{}成交{}股,合同编号{}'.format(order['d_2129'], order['d_2128'], htbh)
                            return {'state' : Constants.STATE[4], 'result' : message, 'order' : order}
                return {}
            return {'state' : Constants.STATE[3], 'result' : result['errormsg']}   
        except Exception as e:
                Mock._logger.error('mock tradeId = {} query chengjiao faield e = {}'.format(self.tradeId, e))
                return {'state' : Constants.STATE[3], 'result' : '查询订单[{}]成交状况失败，请检查配置'.format(htbh)}  



    def cancelDelegate(self, htbh, wtrq):
        self.load_cookie()                   
        postData = {
            'htbh' : htbh,
            'wtrq' : wtrq
        }
        try:   
            response = requests.post('http://mncg.10jqka.com.cn/cgiwt/delegate/cancelDelegated/',data=postData,headers=self.__header)
            Mock._logger.info('mock tradeId = {} htbh = {} cancel delegate get response = {}'.format(self.tradeId, htbh, response.text))
            result = json.loads(response.text)
            if(result['errorcode'] == 0):
                return {'state' : Constants.STATE[1], 'result' : '合同[{}]已撤销'.format(htbh)}
            return {'state' : Constants.STATE[3], 'result' : result['errormsg']}
        except Exception as e:
                Mock._logger.error('can deligate [{}] faield, e = {}'.format(htbh, e))
                return {'state' : Constants.STATE[3], 'result' : '合同[{}]撤销失败，请检查配置'.format(htbh)} 


    def reLogin(self):
        self.load_cookie()
        try:   
            response = requests.get('http://mncg.10jqka.com.cn/cgiwt/login/doths/?type=auto&uname={}&password='.format(self.config['username']),headers=self.__header)
            Mock._logger.info('mock tradeId = {} reLogin get response = {}'.format(self.tradeId, response.text))
            result = json.loads(response.text)
            if(result['errorcode'] == 0):
                return {}
            return {'state' : Constants.STATE[3], 'result' : result['errormsg']}    
        except Exception as e:
            Mock._logger.error('mock tradeId = {} faield, e = {}'.format(self.tradeId, e))
            return {'state' : Constants.STATE[3], 'result' : '登录失败'} 