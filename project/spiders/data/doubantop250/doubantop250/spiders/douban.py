# -*- coding: utf-8 -*-
import scrapy
from doubantop250.items import Doubantop250Item

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com/top250']
    start_urls = ['http://movie.douban.com/top250/']

    def parse(self, response):
        li_list = response.xpath('//ol[@class="grid_view"]/li')
        for i in li_list:
            item =Doubantop250Item()
            item['title'] = i.xpath('.//a/span[1]/text()').extract_first()
            next_url = i.xpath('//div[@class="paginator"]/span/a/@href').extract()
            print(next_url)
