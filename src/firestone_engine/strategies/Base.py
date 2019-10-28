import logging
from datetime import datetime

class Base(object):

    _logger = logging.getLogger(__name__)
      
    def run(self, trade, config, data):
        self.trade = trade
        self.config = config
        self.data = data
        return self.matchCondition()


    def matchCondition(self):
        logging.info('{}, the strategy {} match the condition, data = {}'.format(datetime.now(), __name__, self.data[-1]))
        return True
