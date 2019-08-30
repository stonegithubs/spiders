import json
import time

import requests


class QuNaSpider(object):
    def __init__(self):
        self.headers = {
            'cache-status': 'BYPASS',
            'content-disposition': 'inline;filename=f.txt',
            'content-encoding': 'gzip',
            'content-type': 'application/javascript;charset=UTF-8',
            'date': 'Tue, 30 Jul 2019 03:50:02 GMT',
            'req-id': '00002800074817b22348a29b',
            'server': 'QWS/1.0',
            'status': '200',
            'vary': 'Accept-Encoding',
        }

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers)
        return res.text

    def run(self, url):
        res = self.get_html(url)
        res = res.replace('/**/jQuery17205213751318001172_1564458598671(','').replace(');','')
        res = json.loads(res)
        print(res['data']['s2sBeanList'][1]['trainNo'])
        # res = json.dumps(res)
        # print(res)


if __name__ == '__main__':
    url = 'https://train.qunar.com/dict/open/s2s.do?callback=jQuery17205213751318001172_1564458598671&dptStation=%E5%8D%97%E4%BA%AC&arrStation=%E4%B8%8A%E6%B5%B7&date=2019-07-31&type=normal&user=neibu&source=site&start=1&num=500&sort=3&_=' + str(
        int(time.time() * 1000))
    tu = QuNaSpider()
    tu.run(url)
