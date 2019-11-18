import requests
import logging
import json

class ProxyManager(object):

    _URL = 'http://http.tiqu.alicdns.com/getip3?num={}&type=2&pro=&city=0&yys=100017&port=1&time=4&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'

    _LOAD_PROXY_RETRY = 5
    
    _logger = logging.getLogger(__name__)

    def __init__(self):
        self.proxy_pool = []
        self.load_proxy_failed = 0
        self.proxy = None
        self.load_proxies()


    def load_proxies(self, number=10):
        try:
            response = requests.get(ProxyManager._URL.format(number))
            ProxyManager._logger.info('load proxies, retry = {} get response = {}'.format(self.load_proxy_failed, response.text))
            result = json.loads(response.text)
            if(result['code'] == 0):
                self.proxy_pool.extend(result['data'])
            else:
                ProxyManager._logger.error('get proxy failed code = {}'.format(result['code']))
                self.load_proxy_failed += 1
        except Exception as e:
            ProxyManager._logger.error('get proxy failed, e = {}'.format(e))
            self.load_proxy_failed += 1


    def get_proxy(self):
        if(self.proxy is not None):
            self.proxy_pool.append(self.proxy)
        length = len(self.proxy_pool)
        if(length == 0):
            if(self.load_proxy_failed < ProxyManager._LOAD_PROXY_RETRY):
                self.load_proxies()
            if(len(self.proxy_pool) == 0):
                return None
        self.proxy = self.proxy_pool.pop(0)
        return "{}:{}".format(self.proxy['ip'], self.proxy['port'])


    def remove_proxy(self):
        self.proxy = None