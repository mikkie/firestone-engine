from pymongo import MongoClient
from lxml import etree
from datetime import datetime
import requests
import time

class HotConcept(object):
    
    def __init__(self, db):
        self.db = db
        self.__header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'searchGuide=sg; BAIDU_SSP_lcr=http://www.yamixed.com/fav/article/2/157; __utma=156575163.1101180334.1557107567.1575014992.1577545628.7; __utmc=156575163; __utmz=156575163.1577545628.7.4.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1575015038,1577545645; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1575015038,1575876694,1577545645; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1575015038,1577545646; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1577545792; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1577545795; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1577545802; v=AjMla89iad2WrCUJPFtBhjgjwjxeaMcqgfwLXuXQj9KJ5F2qbThXepHMm6r2',
            'Host': 'data.10jqka.com.cn',
            'If-Modified-Since': 'Fri, 27 Dec 2019 07:41:13 GMT',
            'If-None-Match': "5e05b599-cf6c",
            'Referer': 'http://data.10jqka.com.cn/funds/ggzjl/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        }


    def load_hot_concept(self):
        response = requests.get(f'http://data.10jqka.com.cn/funds/gnzjl/',headers=self.__header)
        response.encoding = response.apparent_encoding
        page = etree.HTML(response.text)
        data = []
        for i in range(10):
            url = f'//*[@id="J-ajax-main"]/table/tbody/tr[{i+1}]'
            tr = page.xpath(url)[0]
            json_hot = self.get_hot_concept(tr)
            data.append(json_hot)
        self.db['hot_concept'].insert(data)

    
    def get_hot_concept(self, tr):
        json_hot = {}
        tds = tr.getchildren()
        json_hot['name'] = tds[1].getchildren()[0].text
        json_hot['index_percent'] = tds[3].text
        json_hot['net_buy'] = tds[6].text
        json_hot['company_count'] = tds[7].text
        json_hot['stock_percent'] = tds[9].text
        json_hot['time'] = datetime.now()
        return json_hot



# if __name__ == "__main__":
#     # # to debug in vscode uncomment this block
#     # import ptvsd
#     # # 5678 is the default attach port in the VS Code debug configurations
#     # print("start debug on port 5678")
#     # ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
#     # ptvsd.wait_for_attach()
#     client = MongoClient('127.0.0.1', 27017)
#     data_db = client['firestone']
#     hc = HotConcept(data_db)
#     for i in range(240):
#         hc.load_hot_concept()
#         time.sleep(30)