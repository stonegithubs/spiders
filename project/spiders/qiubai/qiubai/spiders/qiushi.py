# -*- coding: utf-8 -*-
import scrapy


class QiushiSpider(scrapy.Spider):
    name = 'qiushi'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['http://www.qiushibaike.com/']

    def parse(self, response):
        print('*'*100)
