# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pro.items import TencentItem


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    rules = (
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+?#a'), follow=True),
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+?&keywords=&tid=0&lid=0'), callback='parse_item'),
    )

    def parse_item(self, response):
        # print(response.request.headers)

        i = TencentItem()
        i['title'] = response.xpath('//td[@id="sharetitle"]/text()').extract()
        i['area'] = response.xpath('//tr[@class="c bottomline"]/td[1]/text()').extract()
        i['work'] = response.xpath('//*[@id="position_detail"]/div/table/tr[3]/td/ul/li/text()').extract()
        i['require'] = response.xpath('//*[@id="position_detail"]/div/table/tr[4]/td/ul/li/text()').extract()
        # print(i)
        return i
