# -*- coding: utf-8 -*-
import scrapy


import re
import csv
import pymongo
from taobao.items import TaobaoItem

class TaobaoSpiderSpider(scrapy.Spider):
    name = 'taobao_spider'
    allowed_domains = ['www.taobao.com']

    start_url = 'https://s.taobao.com/search?data-key=s&data-value=88&ajax=true&_ksTS=1546944266575_1129&callback=jsonp1130&q=%E5%A5%B3%E8%A3%85&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190108&ie=utf8&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=44'
    detail_urls = []
    data = []
    # client = pymongo.MongoClient("localhost", 27017)
    # db = client.taobao
    # db = db.items


def start_requests(self):
    for i in range(30):  # 爬31页数据差不多了
        url = self.start_url + '&s=' + str(i * 44)
        yield scrapy.FormRequest(url=url, callback=self.parse)


def url_decode(self, temp):
    while '\\' in temp:
        index = temp.find('\\')
        st = temp[index:index + 7]
        temp = temp.replace(st, '')

    index = temp.find('id')
    temp = temp[:index + 2] + '=' + temp[index + 2:]
    index = temp.find('ns')
    temp = temp[:index] + '&' + 'ns=' + temp[index + 2:]
    index = temp.find('abbucket')
    temp = 'https:' + temp[:index] + '&' + 'abbucket=' + temp[index + 8:]
    return temp


def parse(self, response):
    item = response.xpath('//script/text()').extract()
    pat = '"raw_title":"(.*?)","pic_url".*?,"detail_url":"(.*?)","view_price":"(.*?)"'
    urls = re.findall(pat, str(item))
    urls.pop(0)
    row = {}.fromkeys(['name', 'price', 'link'])
    for url in urls:  # 解析url并放入数组中
        weburl = self.url_decode(temp=url[1])
        item = TaobaoItem()
        item['name'] = url[0]
        item['link'] = weburl
        item['price'] = url[2]
        row['name'] = item['name']
        row['price'] = item['price']
        row['link'] = item['link']
        self.db.insert(row)
        row = {}.fromkeys(['name', 'price', 'link'])
        self.detail_urls.append(weburl)
        self.data.append(item)
        return item
    for item in self.detail_urls:  # 这个可以抓取评论等更多相关信息
        yield scrapy.FormRequest(url=item, callback=self.detail)
