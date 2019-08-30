# -*- coding: utf-8 -*-
import scrapy


class JingdongSpider(scrapy.Spider):
    name = 'jingdong'
    allowed_domains = ['www.jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=670,671,1105']

    def parse(self, response):
        with open('jd.html','w')as f:
            f.write(response.text)
        li_list = response.xpath('//div[@id="plist"]/ul/li')
        for li in li_list:
            item = {}
            item['price'] = li.xpath('.//div[@class="p-price"]/strong/i/text()')
            print(item['price'])
