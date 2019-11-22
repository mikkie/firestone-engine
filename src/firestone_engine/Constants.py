class Constants(object):

    STATE = ['运行中','暂停','已提交','异常','已完成','撤销']

    INDEX = ['sh','sz','hs300','sz50','zxb','cyb']


    @classmethod
    def map_code(self, name, code):
        if(name == '上证指数'):
            return Constants.INDEX[0]
        elif(name == '创业板指'):
            return Constants.INDEX[5]
        return code
            