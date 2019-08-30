import json
from time import sleep
import requests


class PinDuoDuoSpider(object):
    """
    爬取首页
    """
    def __init__(self):
        self.url = "https://jinbao.pinduoduo.com/network/api/common/brand/goodsList"
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://youhui.pinduoduo.com',
            'Referer': 'https://youhui.pinduoduo.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
        # self.proxys = {
        #     'https': 'https://1.198.73.168:9999'
        # }

    def run(self):
        for i in range(1000,2000):
            values = {
                'crawlerInfo': "0anAfxn5HsloU9TVSWuS9mQM5x1Bid9duOcOLHIA5tkkg4ww2GoVtvukB-V2EIThSKQSE-hJu-DeNR4nWg2p4DbX5QRnbU_9fwAJTCv6SkMnoo67aZruox6GaZBjbIWBgk9SuGz7BHlE2cOXCqF2Stz7cad94nR99mSBcJBzeEcqUoqpbD2X5p_mlShgyjBFYaXC4Yd2a5TKLDDzC5vMHjUWd1FTqUvvnIZV6G2Kf0muc1z2wHSBt9_T9vnE1GUYQkJmV7FG1vXigqN0VVMIciL5CnFnQntcdDVk-xZNTq0RCmrSYqnLbPZ5BQ7bPes1F8NvLfkUsk64PlAgNYGbbxHVvX5sjUk13JknXQXbgokpf21r3equ8OXJ52_bsKbdvP5Frgr-_Vp3MHBUNPx1Blp28WSqHXR0Ebwh15jdMRm-Y8BdqLtAbkWpblivYwnYv5y63rt-SNd7T7iRdZMFN-RYqN4j7Qn",
                'pageNumber': '{}'.format(i),
                'pageSize': 50
            }
            values_json = json.dumps(values)
            # sleep(0.1)
            # req = requests.post(self.url, headers=self.headers, data=values_json, proxies=self.proxys)
            req = requests.post(self.url, headers=self.headers, data=values_json)
            change = req.json()
            new_req = json.dumps(change, ensure_ascii=False)
            new_req = json.loads(new_req)
            try:
                detail_list = new_req['result']['goodsList']
            except Exception:
                continue
            # print(type(detail_list))
            for i in detail_list:
                i = i['goodsName']
                print(i)
                with open('pinduoduo.txt','a',encoding='utf-8')as f:
                    f.write(i)
                    f.write('\n')


if __name__ == '__main__':
    pin = PinDuoDuoSpider()
    pin.run()
    print('OK')
