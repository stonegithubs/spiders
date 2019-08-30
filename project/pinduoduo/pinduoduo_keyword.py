import json
import requests
from utils.suiji_useragent import getUserAgent


class PinDuoDuo_KeyWordSpider(object):
    def __init__(self):
        self.url = 'https://jinbao.pinduoduo.com/network/api/common/goodsList'
        self.data={
            'categoryId': "",
            'crawlerInfo': '0anAfxnpryljY9T6-r9P7Bhc99IVndCCWRz8Mzt1S1RdKs4ZY9ZMn0BcJ-n6kR5l25L9WStLDyM6S68JnJ7EegJmtoYY5WWqJa-099oRHgtkZXg1oOC7Bq9B11I0MwiPpCgIWaiytwBosLfYYuOZigLiri6N8EGWe_lhHevvmoij7k5bhgrHESUs8lFxJIdafbf7UkaMWsmfQMJ_x1DzK7ZH8Um-CWdQ40-XpnL5VU_Y6uFmTWTmomzWrP-_c_3bL49YVbVPWgrVRwj8E4_Xn_NgRScGtsJZ9x9GppfHBT5GoSUFjL97euTTA_IT9G4VA4i0JOSBV-nVKeIzgEQdR808a0cd_7GXNd-zmDOo6foNyKRSlSeQIR4y6G8HlDd8rXQynRBiYzwxzHbL4Av6w2-gE1LRzN7eNN8mfkUgKRPts7Di09cydpkpliq4BllbWSAhcT57ZehEL40-FF8dPZLo7wxFoW5ec4PfFA8dehj3zFNA8QdcHyEN-THWSayAFLNuRSsfhORRo',
            'keyword': "足球",
            'pageNumber': 3,
            'pageSize': 60,
        }
        self.headers = {
            'User-Agent': getUserAgent(1),
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/163.179.208.161 Safari/537.36',
            'Origin': 'https://youhui.pinduoduo.com',
            'Content-Type': 'application/json; charset=UTF-8',
            'Referer': 'https://youhui.pinduoduo.com/search/landing?keyword=%E8%B6%B3%E7%90%83'
        }
        self.proxys={
            'https':'https://163.179.208.161:23775'
        }

    def run(self):
        # res = requests.post(url=self.url,headers=self.headers,data=json.dumps(self.data),proxies=self.proxys)
        res = requests.post(url=self.url,headers=self.headers,data=json.dumps(self.data))
        # res = res.json(encoding='utf8')
        change = res.json()
        new_req = json.dumps(change, ensure_ascii=False)
        new_req = json.loads(new_req)
        print(new_req)
        detail_list = new_req['result']['goodsList']
        print(detail_list)
        for i in detail_list:
            i = i['goodsName']
            print(i)
            with open('pinduoduo.txt', 'a', encoding='utf-8')as f:
                f.write(i)
                f.write('\n')

if __name__ == '__main__':
    pin = PinDuoDuo_KeyWordSpider()
    pin.run()