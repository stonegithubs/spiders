# -*- coding: utf-8 -*-
import scrapy
from ..items import ZhipinItem
import re
from scrapy_redis.spiders import RedisCrawlSpider

n = 1

class ZhipinSpiderSpider(RedisCrawlSpider):
    name = 'zhipin_spider'
    allowed_domains = ['zhipin.com']
    redis_key = 'zhipin_spider:strat_urls'
    # start_urls = ['https://www.zhipin.com/job_detail/?query=python/']
    base_url = 'https://www.zhipin.com'

    def parse(self, response):
        next_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if next_url:
            next_url = self.base_url + next_url
            yield scrapy.Request(url=next_url)

        job_urls = response.xpath('//div[@class="job-primary"]/div[@class="info-primary"]/h3/a/@href').extract()
        for job_url in job_urls:
            yield scrapy.Request(url=self.base_url+job_url,callback=self.detail_parse)

    def detail_parse(self,response):
        items = ZhipinItem()
        global n
        n += 1
        items['number'] = n
        items['company'] = response.xpath('//h3[@class="name"]/a/text()').extract_first()
        items['time'] = response.xpath('//span[@class="time"]/text()').extract_first()
        items['name'] = response.xpath('//h1/text()').extract_first()
        items['money'] = response.xpath('//span[@class="badge"]/text()').extract()[-1]
        items['address'] = response.xpath('//div[@class="location-address"]/text()').extract_first()
        items['experience'] = re.findall(r'>经验：(.*?)<',response.text)
        job_secs = response.xpath('//div[@class="job-sec"]/div/text()').extract()
        content = []
        for job_sec in job_secs:
            job_sec = job_sec.strip()
            if job_sec:
                content.append(job_sec)
        items['content'] = content
        yield items
