import requests
from lxml import etree
import re
import json


class Spiders(object):
    def __init__(self ):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

    def requests_url(self,url):
        res = requests.get(url=url, headers=self.headers).text
        # print(res)
        # with open('meituan.html','w',encoding='utf8')as f:
        #     f.write(res)
        return res

    def run(self,url):
        for i in range(1,67):
            res = self.requests_url(url.format(i))
            print(i)
            # print(res)
            # a = re.findall(r'"adsClickUrl":"","adsShowUrl":""},(.*?)"comHeader":',res)
            a = re.findall(r'{"totalCounts":1000,"poiInfos":(.*?)},"comHeader',res)[0]
            # print(a)
            a = json.loads(a)
            # print(a)
            # print(type(a))
            for i in a:
                # print(i['title'])
                with open('./meishi.txt','a',encoding='utf8')as f:
                    f.write(i['title']+'\n')

if __name__ == '__main__':
    url = 'https://nj.meituan.com/meishi/pn{}/'
    sp = Spiders()
    sp.run(url)
    # a = '[{"a":1,"b":2},{"a":1,"b":2}]'
    # b = json.loads(a)
    # print(type(b)