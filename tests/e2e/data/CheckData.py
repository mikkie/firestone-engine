from pymongo import MongoClient
from datetime import datetime
import unittest

class CheckData(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client['firestone-data']

    def testData(self):
        today = datetime.now()
        today = '{}-{}-{}'.format(today.year,('0' + str(today.month))[-2:],('0' + str(today.day))[-2:])
        for code in ['000993', '300694', '000793' , 'sh', 'cyb']:
            data = self.db[code + '-' + today].find()
            self.assertGreaterEqual(len(list(data)), 1)

    def tearDown(self):
        self.client.close()

if __name__ == "__main__":
    unittest.main()
    