import logging
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler

class Trader(object):


    _logger = logging.getLogger(__name__)

    _DB = 'firestone'
    
    def __init__(self, tradeId):
        self.tradeId = tradeId


    def calculate(self):
        pass    

    def is_finsih(self):
        pass

    def stop(self):
        pass        