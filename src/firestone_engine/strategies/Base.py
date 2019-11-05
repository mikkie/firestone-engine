import logging
from datetime import datetime

class Base(object):

    _logger = logging.getLogger(__name__)
      
    def run(self, trade, config, data, index):
        self.trade = trade
        self.config = config
        self.data = data
        self.dataLastRow = self.data[-1]
        self.index = index
        self.indexLastRow = self.index[-1]
        if(self.match_monitorTime()):
            return self.matchCondition()
        return False

        
    def match_monitorTime(self):
        start = datetime.strptime('{} {}:00'.format(self.dataLastRow['date'], self.trade['params']['monitorTime']['start']), '%Y-%m-%d %H:%M:%S')    
        end = datetime.strptime('{} {}:00'.format(self.dataLastRow['date'], self.trade['params']['monitorTime']['end']), '%Y-%m-%d %H:%M:%S')
        dataTime = datetime.strptime('{} {}'.format(self.dataLastRow['date'], self.dataLastRow['time']), '%Y-%m-%d %H:%M:%S')
        return dataTime >= start and dataTime <= end


    def matchCondition(self):
        Base._logger.info('tardeId = {}, {}, the strategy {} match the condition, data = {}, index = {}'.format(self.trade['_id'], datetime.now(), self.__class__, self.data[-1], self.index))
        return True
