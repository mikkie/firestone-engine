from decimal import Decimal, ROUND_HALF_UP

class Utils(object):

    @classmethod
    def round_dec(self, n, d=2):
        s = '0.' + '0' * d
        return Decimal(str(n)).quantize(Decimal(s), rounding=ROUND_HALF_UP)