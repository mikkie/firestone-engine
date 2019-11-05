from .Mock import Mock
import logging
from datetime import datetime
from .Constants import Constants

class NoTrade(Mock):

    _logger = logging.getLogger(__name__)


    def createDelegate(self, code, price, volume, op):
        NoTrade._logger.info('mock tradeId = {}, code = {}, price = {}, volume = {}, op = {}, submit order get response = {}'.format(self.tradeId, code, price, volume, op, 'mock no trade createDelegate success'))
        op_cn = '买入' if op == 'buy' else '卖出'
        message = '订单提交: 在{},以{}{}[{}] {}股'.format(datetime.now(), price, op_cn, code, volume)
        return {'state' : Constants.STATE[2], 'result' : message, 'order' : {'result' : {'data' : {'htbh' : '000000'}}}}


    def queryChenjiao(self, htbh):
        NoTrade._logger.info('mock tradeId = {} htbh = {} query chengjiao, get response = {}'.format(self.tradeId, htbh, 'mock no trade queryChenjiao success'))
        message = '以xx.xx成交xx股,合同编号{}'.format(htbh)
        return {'state' : Constants.STATE[4], 'result' : message, 'order' : {'result' : {'data' : {'htbh' : '000000'}}}}


    def cancelDelegate(self, htbh, wtrq):
        NoTrade._logger.info('mock tradeId = {} htbh = {} cancel delegate get response = {}'.format(self.tradeId, htbh, 'mock no trade cancelDelegate success'))
        return {'state' : Constants.STATE[1], 'result' : '合同[{}]已撤销'.format(htbh)}


