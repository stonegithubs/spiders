# -*- coding: utf-8 -*-
import scrapy
from pro10.items import Pro10Item


class YangguangwangSpider(scrapy.Spider):
    name = 'yangguangwang'
    allowed_domains = ['wz.sun0769.com']
    offset = 0
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page='
    start_urls = [url + str(offset)]

    def parse(self, response):
        links = response.xpath('//tr/td[2]/a[@class="news14"]/@href').extract()
        stop_num = response.xpath('//div[@class="pagination"]//text()')
        stop_num = stop_num[-1].extract()
        stop_num = stop_num.replace(' 共', '').replace('条记录', '')
        stop_num = int(stop_num)

        for link in links:
            yield scrapy.Request(link, callback=self.parse_item)

        if self.offset <= stop_num:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item = Pro10Item()
        title = response.xpath('//div[@class="wzy1"]//tr/td/span[@class="niae2_top"]/text()').extract_first()
        if title:
            item['title'] = title.replace('提问：', '')
        else:
            item['title'] = None
        number = response.xpath('//div[@class="wzy1"]//tr/td/span[2]/text()').extract_first()
        if number:
            item['number'] = number.replace('\xa0\xa0', '')
        else:
            item['number']=None
        content = response.xpath('//tr[1]/td[@class="txt16_3"]/text()').extract_first()
        if content:
            item['content'] = content.replace('\xa0\xa0\xa0\xa0', '')
        else:
            item['content'] = None
        yield item
