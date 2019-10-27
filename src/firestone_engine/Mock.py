from .Real import Real

class Mock(Real):

    def init_cols(self):
        self.cols = {
            'trades' : 'mocktrades',
            'configs' : 'configmocks'
        }