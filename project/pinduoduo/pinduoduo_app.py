import json
from time import sleep
import requests


class PinDuoDuoSpider(object):
    def __init__(self):
        # appKey = 'RERUbXZleUpDNE9qeFh3VjplNDJuN000SmlyNkNOUFU4'
        self.url = 'https://jinbao.pinduoduo.com/network/api/common/goodsList'
        self.headers = {
            # "Proxy-Authorization": 'Basic ' + appKey,
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://youhui.pinduoduo.com',
            'Referer': 'https://youhui.pinduoduo.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        # ip_port = 'secondtransfer.moguproxy.com:9001'
        # self.proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
        self.proxy = {
            'http':'http://119.3.253.33:8080'
        }

    def run(self):
        """
        爬取指定关键字
        """
        for j,i in enumerate(range(1,2)):
            values = {
                'crawlerInfo': '0anAfxn5ry1ys9daYNlzZjJm4zcFPHJXSzkIbhm-yVtBDwv6tc4VwF7fm-NXYMqleFXYopdwR92w60hoIyQJ1lJg1NTokvoJ6Wib8ril2S9kGRC9TJaoUruOtrP1PQi9AB3oUAgjoKWg9JdhHguLsSuOOJ5WPmOYP1egKicaXvMeEOPvuLNO7RrE8A8EPIeJ5VKj8INx0pLkKnHd1nl_LBKv2VaveVIBpeaEceVtufxAe5fh1Hkmp93J1QfrzVxN4mfIfsQ9zbCMcZ93HpjkLZ61DqIzGLFjKT3OcOaZNHQDENwLIcdcC6Mm9jp40z9iy5Ua67ZwA2sy2uAkgzjs7g--Xm0Jmwig9dXOMgvkL84g4IHJlvtRu0AV9OHe7n_0z-AV3eMzBTrdaNd8e1rQ47XHQAfYHqufbWX8_zpcHLFpgDpO0dNxC8tx653LQpUawLfYYx_KqGl1F8xlB-1TKKmLpXSbbeVcobbgxL4fIYkCq8HyinbGmLM1itrNfDN82fNze8sTqeFqLcqOYrBcyRtT4DZyvfyDNIRLhJn-r4sgo',
                'pageNumber': '{}'.format(i),
                'keyword': '篮球',
                'pageSize': 60
            }
            values_json = json.dumps(values)
            # sleep(0.1)
            req = requests.post(self.url, headers=self.headers, data=values_json, proxies=self.proxy,verify=False,allow_redirects=False)
            # req = requests.post(self.url, headers=self.headers, data=values_json)
            change = req.json()
            new_req = json.dumps(change, ensure_ascii=False)
            new_req = json.loads(new_req)
            print(new_req)
            try:
                detail_list = new_req['result']['goodsList']
                print(detail_list)
            except Exception:
                print(j)
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
