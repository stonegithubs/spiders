# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pro6.items import TencentItem
from scrapy_redis.spiders import RedisCrawlSpider


class TencentSpider(RedisCrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    # start_urls = ['https://hr.tencent.com/position.php']
    redis_key = 'tencent:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+?#a'), follow=True),
        Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+?&keywords=&tid=0&lid=0'), callback='parse_item'),
    )

    def parse_item(self, response):
        i = TencentItem()
        i['title'] = response.xpath('//td[@id="sharetitle"]/text()').extract()
        i['area'] = response.xpath('//tr[@class="c bottomline"]/td[1]/text()').extract()
        i['work'] = response.xpath('//*[@id="position_detail"]/div/table/tr[3]/td/ul/li/text()').extract()
        i['require'] = response.xpath('//*[@id="position_detail"]/div/table/tr[4]/td/ul/li/text()').extract()
        yield i
