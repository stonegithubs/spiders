# -*- coding: utf-8 -*-
import requests
import scrapy


class HafoSpider(scrapy.Spider):
    name = 'hafo'
    allowed_domains = ['car.bitauto.com']
    start_urls = ['http://car.bitauto.com/hafu-196/']

    def parse(self, response):
        # with open('./hafo.html','w')as f:
        #     f.write(response.text)
        ul_list = response.xpath(r'//div[@id="data_table_MasterSerialList_0"]//ul')
        for i in ul_list:
            item = {}
            item['ctitle'] = i.xpath(r'./li[1]/a/text()').extract_first()
            item['cprice'] = i.xpath(r'.//li[2]//text()').extract_first()
            detail_url = i.xpath(r'./li[1]/a/@href').extract_first()
            detail_url = 'http://car.bitauto.com' + detail_url
            # print(detail_url)
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={'item': item}
            )

    def parse_detail(self,response):
        item = response.meta['item']
        # print('*'*100)
        # print(response)
        # print('*'*100)
        detail_url = response.xpath(r'//*[@id="car_tag"]/nav/div/div/ul/li[2]/a/@href').extract_first()
        detail_url = 'http://car.bitauto.com' + detail_url
        yield scrapy.Request(
            url=detail_url,
            callback=self.parse_detail_list,
            meta={'item': item}
        )

    def parse_detail_list(self,response):
        item = response.meta['item']
        resp = response.xpath(r'//*[@id="draggcarbox_0"]/dl/dd[1]/a')
        print('*'*100)
        print(resp)
        print('*'*100)