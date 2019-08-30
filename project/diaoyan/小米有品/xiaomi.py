import time

import requests
from lxml import etree


class KuaiDiSpider(object):
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '145',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'youpindistinct_id=16c69f01e38709-0c0c5fd21079fb-3f385c06; mjclient=PC; youpin_sessionid=1565145439803_16c69f01e3b73e-0116abf4d6d768-3f385c06; youpindistinct_id=16c69f01e38709-0c0c5fd21079fb-3f385c06; mjclient=PC; UM_distinctid=16c69f024c5452-0d0a9da33ee455-3f385c06-100200-16c69f024c6364; CNZZDATA1267968936=2041065572-1565145402-null%7C1565145402; Hm_lvt_025702dcecee57b18ed6fb366754c1b8=1565145442,1565145476; Hm_lpvt_025702dcecee57b18ed6fb366754c1b8=1565145788; youpin_sessionid=16c69f5aec0-0ab3be086b9c98-205b',
            'Host': 'www.xiaomiyoupin.com',
            'Origin': 'https://www.xiaomiyoupin.com',
            'Referer': 'https://www.xiaomiyoupin.com/goodsbycategory?firstId=579&secondId=579&title=%E6%89%8B%E6%9C%BA%E7%94%B5%E8%84%91&spmref=YouPinPC.$Home$.list.0.49249520',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Yp-App-Source': 'front-PC',
        }
        self.data = {"uClassList": {"model": "Homepage", "action": "BuildHome", "parameters": {"id": "579"}}}

    def get_html(self, url):
        res = requests.post(url=url, headers=self.headers, data=self.data, proxies=self.proxies())
        return res.text

    def write_html(self, path, content):
        with open(path, 'w', encoding='utf8')as f:
            f.write(content)

    def etree_html(self, content):
        res = etree.HTML(content)
        return res

    def proxies(self):
        proxies = {
            'https': 'https://122.194.249.84:4217'
        }
        return proxies

    def run(self, url):
        all_html = self.get_html(url)
        print(all_html)


if __name__ == '__main__':
    url = 'https://www.xiaomiyoupin.com/app/shopv3/pipe'
    kuaidi = KuaiDiSpider()
    kuaidi.run(url)
    print(time.time())
