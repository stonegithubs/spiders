# -*- coding: utf-8 -*-
import scrapy


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['book.jd.com']
    start_urls = ['http://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')
        for dt in dt_list:
            item = {}
            item['d_class'] = dt.xpath('./a/text()').extract_first()
            em_list = dt.xpath('./following-sibling::dd[1]/em')
            for em in em_list:
                item['x_href'] = em.xpath('./a/@href').extract_first()
                item['x_class'] = em.xpath('./a/text()').extract_first()
                if item['x_href'] is not None:
                    item['x_href'] = 'https:' + item['x_href']
                    yield scrapy.Request(
                        url=item['x_href'],
                        callback=self.parse_book_list,
                        meta={'item': item}
                    )
                # print(item)

    def parse_book_list(self, response):
        item = response.meta['item']
        li_list = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for li in li_list:
            item['btitle'] = li.xpath('./div/div[3]/a/em/text()').extract_first()
            print(item)
