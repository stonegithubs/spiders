# -*- coding: utf-8 -*-
import scrapy


class AmazonbookSpider(scrapy.Spider):
    name = 'amazonbook'
    allowed_domains = ['www.amazon.cn']
    start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=topnav_storetab_b?ie=UTF8&node=658390051']

    def parse(self, response):
        li_list = response.xpath('//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-one"]//a')
        for li in li_list:
            item = {}
            item['d_class_url'] = li.xpath('./@href').extract_first()
            item['d_class_title'] = li.xpath('./span/text()').extract_first()
            print(item)
