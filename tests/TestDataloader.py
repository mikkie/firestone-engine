import unittest
from firestone_engine.DataLoader import DataLoader

class TestDataloader(unittest.TestCase):

    def setUp(self):
        self.dl = DataLoader('000000', is_mock=False, mock_trade=True)


    def test_get_code_list_from_db(self):
        code_list = self.dl.get_code_list_from_db()
        self.assertEqual(len(code_list),5)
        print(code_list)    


    def tearDown(self):
        self.dl.client.close()

if __name__ == "__main__":
    unittest.main()