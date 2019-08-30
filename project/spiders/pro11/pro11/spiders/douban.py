# -*- coding: utf-8 -*-
import scrapy
import requests

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['read.douban.com']
    start_urls = ['https://read.douban.com/ebooks/?dcs=book-nav&dcm=douban']

    def parse(self, response):
        print('*' * 100)
        url_list = response.xpath('//div[@class="bd"]/ul[@class="list kinds-list tab-panel"]/li/a/@href').extract()
        # url_list = 'read.douban.com'+
        print(type(url_list))
        print(url_list)
        for url in url_list:
            detail_url = 'https://read.douban.com' + url
            print(detail_url)
            yield scrapy.Request(url=detail_url, callback=self.parse_item)


# yield scrapy.Request(url=detail_url, callback=self.parse_item)
#         print('*' * 100)

    def parse_item(self, response):
        item = {}
        print(response)
        # with open('./douban.html','w')as f:
        #     f.write(response.text)
        title = response.xpath('//h4[@class="title"]/a/span/span/text()')
        print(title)
