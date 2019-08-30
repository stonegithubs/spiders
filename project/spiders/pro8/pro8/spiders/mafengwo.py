# -*- coding: utf-8 -*-
import scrapy


class MafengwoSpider(scrapy.Spider):
    name = 'mafengwo'
    allowed_domains = ['club.autohome.com.cn']
    start_urls = ['https://club.autohome.com.cn/bbs/thread/4047cefd9e361119/67252775-1.html']

    def parse(self, response):
        data = response.xpath('//*[@id="F0"]/div[2]/div[2]/div[1]/div/div[2]')
        print(data)