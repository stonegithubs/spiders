# -*- coding: utf-8 -*-
import scrapy

from boosjob.items import BoosjobItem


class BoosSpider(scrapy.Spider):
    name = 'boos'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=python&scity=101190100']

    def parse(self, response):
        li_list = response.xpath('//div[@class="job-list"]/ul/li')
        for i in li_list:
            item = BoosjobItem()
            item['job'] = i.xpath('.//div[@class="job-title"]/text()').extract_first()
            item['salary'] = i.xpath('.//a/span/text()').extract_first()
            item['region'] = i.xpath('.//div[@class="info-primary"]/p/text()[1]').extract_first()
            item['experience'] = i.xpath('.//div[@class="info-primary"]/p/text()[2]').extract_first()
            item['education'] = i.xpath('.//div[@class="info-primary"]/p/text()[3]').extract_first()
            item['company'] = i.xpath('.//div[@class="company-text"]/h3[@class="name"]/a/text()').extract_first()
            item['detail_url'] = i.xpath('./div/div[1]/h3/a/@href').extract_first()
            item['detail_url'] = 'https://www.zhipin.com' + item['detail_url']
            yield scrapy.Request(
                url=item['detail_url'],
                callback=self.parse_detail,
                meta={'item': item}
            )

    def parse_detail(self, response):
        item = response.meta['item']
        item['duty'] = response.xpath('//div[@class="text"]/text()').extract()
        print(item)
