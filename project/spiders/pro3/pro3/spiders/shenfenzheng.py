# -*- coding: utf-8 -*-
import scrapy

from pro3.items import InfoItem


class ShenfenzhengSpider(scrapy.Spider):
    name = 'shenfenzheng'
    allowed_domains = ['95nw.com']
    start_urls = ['http://95nw.com/daquan/']

    def parse(self, response):
        item = InfoItem()
        item['info'] = response.xpath('//td/text()').extract()
        # print(item)
        for i in item['info']:
            with open('./身份证号.txt', 'a')as f:
                f.write(i + '\n')
