# -*- coding: utf-8 -*-
import scrapy


class GithubLoginSpider(scrapy.Spider):
    name = 'github_login2'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response=response, formdata={'login': '31926990@qq.com',
                                                                            'password': 'z17025..', },
                                               callback=self.after_login)

    def after_login(self, response):
        print('*' * 100)
        print(response.text.find('dd31926990'))
        print('*' * 100)
