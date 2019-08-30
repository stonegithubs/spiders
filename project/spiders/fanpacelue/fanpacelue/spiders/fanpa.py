# -*- coding: utf-8 -*-
import scrapy
import re


class FanpaSpider(scrapy.Spider):
    name = 'fanpa'
    allowed_domains = ['www.urlteam.org']
    start_urls = ['https://www.urlteam.org/category/web_crawlers']

    def parse(self, response):
        resp = response.xpath('//div[@id="primary"]//h1/a')
        # print('*'*100)
        # print(len(resp))
        # print('*' * 100)
        # print(resp)
        # print('*' * 100)
        for i in resp:
            detail_url = i.xpath('./@href').extract_first()
            # print('*' * 100)
            # print(detail_url)
            yield scrapy.Request(
                url=detail_url,
                callback=self.detail_parse,
            )

    def detail_parse(self, response):
        # item = {}
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        content = response.xpath('//div[@class="entry-content"]//text()').extract()
        # print('*' * 100)
        # print(item)

        with open('fanpa.txt', 'a')as f:
            f.write('标题:\n' + title + '\n')

        # print(type(content))
        for i in content:
            content = i.replace(r'\n', '').replace(r'\r', '').replace(r'\t', '')
            # print(type(content))
            # print(content)
            if content:
                with open('fanpa.txt', 'a')as w:
                        w.write(content)
        # content = str(content)
        # content = list(content)
        # print(type(content))
        # print(content)
        # for i in content:
        #     if i:
        #         with open('fanpa.txt', 'a')as w:
        #             w.write('内容:\n' + i)
        with open('fanpa.txt', 'a')as e:
            e.write('\n\n\n')
