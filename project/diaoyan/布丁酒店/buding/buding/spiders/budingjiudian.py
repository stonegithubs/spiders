# -*- coding: utf-8 -*-
import scrapy

from buding.items import BudingItem


class BudingjiudianSpider(scrapy.Spider):
    name = 'budingjiudian'
    # allowed_domains = ['www.podinns.com/Hotel/AreaSearch']
    start_urls = ['http://www.podinns.com/Hotel/AreaSearch/']
    base_url = 'http://www.podinns.com'

    def parse(self, response):
        city_url = response.xpath('//*[@id="left_content"]//div//a/@href').extract()
        for i in city_url:
            all_url = self.base_url + i
            # print(all_url)
            # print('8' * 100)
            # print(all_url)
            yield scrapy.Request(url=all_url, callback=self.city_parse)

    def city_parse(self, response):
        # print('*' * 100)
        hotel_list = response.xpath('//*[@id="left_content"]/div/div[1]/a/@href').extract()
        # print('*' * 100)
        # print(hotel_list)
        # print('*' * 100)
        if hotel_list:
            for i in hotel_list:
                detail_url = self.base_url + i
                yield scrapy.Request(url=detail_url, callback=self.detail_parse)

    def detail_parse(self, response):
        items = BudingItem()
        items['title']=response.xpath('/html/body/div[4]/div/div[2]/div[1]/span[1]/text()').extract_first()
        items['address']=response.xpath('//*[@id="hadd"]/text()').extract_first()
        jianjie1 = response.xpath('//*[@id="discData"]/text()').extract_first()
        jianjie2 = response.xpath('//*[@id="discMore"]/@data').extract_first()
        items['introduce']=jianjie1+jianjie2
        comment=response.xpath('/html/body/div[4]/div/div[11]/div/div[2]/div[2]/span[2]/text()').extract()
        if comment:
            items['comment']=comment
        else:
            items['comment']=''
        items['tel']=response.xpath('/html/body/div[4]/div/div[3]/div[1]/div[2]/div[1]/div[2]/span[1]/text()').extract_first()
        yield items