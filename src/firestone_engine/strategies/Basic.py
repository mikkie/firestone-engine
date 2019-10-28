from .Base import Base

class Basic(Base):
    
    def run(self, trade, config, data):
        Base.run(self, trade, config, data)


    def matchCondition(self):
        #TODO
        return Base.matchCondition(self)    
