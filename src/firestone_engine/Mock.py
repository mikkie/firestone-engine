from .Real import Real
import requests
import logging
import json

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


    def createOrder(self, code, price, volume, op):
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
            return json.loads(response.text)
        except Exception as e:
            Mock._logger.error('mock tradeId = {}, code = {}, price = {}, volume = {}, op = {}, faield with exception = {}'.format(self.tradeId, code, price, volume, op, e))
            return {'errorcode' : -1, 'message' : e}