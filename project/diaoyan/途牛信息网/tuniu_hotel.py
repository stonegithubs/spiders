import json

import requests
from lxml import etree


class TuNiuHotelSpider(object):
    def __init__(self):
        self.headers ={'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        # pro = '115.152.143.147:4248'


    def get_html(self, url):
        ip = {
            'https': 'https://180.124.13.78:4243'
        }
        res = requests.get(url=url, headers=self.headers,proxies=ip)
        return res.content.decode()

    def run(self, url):
        res = self.get_html(url)
        res=json.loads(res)
        print(res)
        for i in res['data']['list']:
            print('https://hotel.tuniu.com'+i['url'])
            detail_html = self.get_html('https://hotel.tuniu.com'+i['url'])
            with open('./tu.html','w',encoding='utf8')as f:
                f.write(detail_html)
            detail_html = etree.HTML(detail_html)
            hotel_title = detail_html.xpath('//h1/text()')
            print(hotel_title)
            break




if __name__ == '__main__':
    url = 'https://hotel.tuniu.com/ajax/list?search%5BcityCode%5D=200&search%5BcheckInDate%5D=2019-08-06&search%5BcheckOutDate%5D=2019-08-07&search%5Bkeyword%5D=&suggest=&sort%5Bfirst%5D%5Bid%5D=recommend&sort%5Bfirst%5D%5Btype%5D=&sort%5Bsecond%5D=&sort%5Bthird%5D=cash-back-after&page=2&returnFilter=0'
    tu = TuNiuHotelSpider()
    tu.run(url)
