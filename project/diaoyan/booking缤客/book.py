import re

import requests
from lxml import etree


class BooKingSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        self.base_url = 'https://www.booking.com'

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers)
        return res.content.decode()

    def get_all_page(self, url):
        all_page_list = self.get_html(url)
        return all_page_list

    def etree_html(self, html):
        res = etree.HTML(html)
        return res

    def write_html(self, path, content):
        with open(path, 'w', encoding='utf8')as f:
            f.write(content)

    def hotel_url_list(self, url):
        hotel_html = self.get_html(url)
        # self.write_html('./booking.html',hotel_html)
        hotel_html = self.etree_html(hotel_html)
        url_list = hotel_html.xpath('//*[@id="hotellist_inner"]//div[1]/h3/a/@href')
        for detail_url_list in url_list:
            # break
            # detail_url = self.base_url+detail_url_list
            # print(detail_url)
            a = detail_url_list.split()
            # print(a)
            c = ''
            for i in a:
                c += i
            d = self.base_url + c
            print(d)
            detail_html = requests.get(url=d,headers = self.headers).content.decode()
            self.write_html('./detail.html',detail_html)
            break

    def run(self, url):
        self.hotel_url_list(url)

    def start(self,url):
        res = self.get_html(url)
        # a = re.findall(r'"streetAddress" : "(.*?)",',res)
        # self.write_html('./detail.html',res)
        res = self.etree_html(res)
        a = res.xpath('//*[@id="hp_hotel_name_reviews"]/text()')
        print(a)

if __name__ == '__main__':
    book = BooKingSpider()
    # for i in range(0, 220, 20):
    #     url = 'https://www.booking.com/searchresults.zh-cn.html?aid=334565&label=baidu-brandzone_booking-brand-list1&sid=69db5ac6a68e89c8031cbf4c68953961&tmpl=searchresults&age=12&checkin_month=8&checkin_monthday=6&checkin_year=2019&checkout_month=8&checkout_monthday=7&checkout_year=2019&class_interval=1&dest_id=-1919548&dest_type=city&from_sf=1&group_adults=1&group_children=0&label_click=undef&no_rooms=1&raw_dest_type=city&room1=A&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&srpvid=1144129620ee01fc&ss=%E5%8D%97%E4%BA%AC&ssb=empty&ssne=%E5%8D%97%E4%BA%AC&ssne_untouched=%E5%8D%97%E4%BA%AC&rows=20&offset={}'.format(
    #         i)
    #     print(i)
    #     book.run(url)
    #     break
    url = 'https://www.booking.com/hotel/cn/nan-jing-jia-yu-you-peng-jiu-dian.zh-cn.html?aid=334565;label=baidu-brandzone_booking-brand-list1;sid=69db5ac6a68e89c8031cbf4c68953961;all_sr_blocks=539350002_193476184_1_2_0;checkin=2019-08-06;checkout=2019-08-07;dest_id=-1919548;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=21;highlighted_blocks=539350002_193476184_1_2_0;hpos=1;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;srepoch=1565060980;srpvid=eeec16391dae007d;type=total;ucfs=1&'
    book.start(url)