# -*- coding: utf-8 -*-
import scrapy


class GithubLoginSpider(scrapy.Spider):
    name = 'github_login'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        commit = response.xpath('//input[@name="commit"]/@value').extract_first()
        token = response.xpath('//input[@name="authenticity_token"]/@value').extract_first()
        utf8 = response.xpath('//input[@name="utf8"]/@value').extract_first()
        post_data = dict(
            login='31926990@qq.com',
            password='z17025..',
            commit=commit,
            utf8=utf8,
            authenticity_token=token
        )
        # print(post_data)
        yield scrapy.FormRequest(url='https://github.com/session', formdata=post_data, callback=self.after_login)

    def after_login(self, response):
        print('*' * 100)
        print(response.text.find('dd31926990'))
        print('*' * 100)
