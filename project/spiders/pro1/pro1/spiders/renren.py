# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['www.renren.com']
    start_urls = ['http://www.renren.com/968561367']

    def start_requests(self):
        cookie_str = 'anonymid=joihulkr-rwdy3v; jebe_key=8c27648a-d245-4859-8717-72b357044c6a%7Ccfcd208495d565ef66e7dff9f98764da%7C1542280266075%7C0%7C1542280265391; jebe_key=8c27648a-d245-4859-8717-72b357044c6a%7Ccfcd208495d565ef66e7dff9f98764da%7C1542280266075%7C0%7C1542280265394; depovince=HEN; _r01_=1; JSESSIONID=abcLtenRvBU_lcHduexCw; wp_fold=0; jebecookies=7fcf3722-90c2-419e-a77c-ff97d5e9a9dd|||||; ick_login=8c7e6a5c-ebaa-4681-bda7-3bcdcdbcf536; _de=0EA171ACA3C2F5B99DEC90D2B7E6F15B; p=a2152b594b4ded6e66772ed3a12a11647; first_login_flag=1; ln_uact=18568453967; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; t=4368e5a6d8136c57d111a894513f67927; societyguester=4368e5a6d8136c57d111a894513f67927; id=968561367; xnsid=e8eeab86; loginfrom=syshome'

        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookie_str.split(';')}

        yield scrapy.Request(url=self.start_urls[0], cookies=cookies, callback=self.parse)

    def parse(self, response):
        print('*' * 100)
        print(response.text.find('<title>人人网 - 李万栋</title>'))
        print('*' * 100)
        yield scrapy.Request(url='http://www.renren.com/968561367/profile', callback=self.parse_detail)

    def parse_detail(self, response):
        print('*' * 100)
        print(response.text.find('0人看过'))
        print('*' * 100)
