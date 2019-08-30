# -*- coding: utf-8 -*-
import scrapy
import re
from qiushibaike.items import QiushibaikeItem


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    def parse(self, response):
        div_list = response.xpath('//div[@id="content-left"]/div')
        # print('*'*100)
        # print(len(div_list))
        for div in div_list:
            # 内容
            content = ''
            # 神评论
            comment = ''
            item = QiushibaikeItem()
            # 用户名
            user_name = div.xpath('.//h2/text()').extract_first()
            # print('user_name:',user_name)
            # 入库
            item['user_name'] = user_name.replace('\n', '')
            # 赞
            funny = div.xpath('.//span[@class="stats-vote"]/i[@class="number"]/text()').extract_first()
            # 入库
            item['funny'] = funny
            # 神评论
            comment = div.xpath('.//a//div[@class="main-text"]/text()').extract_first()
            if comment:
                item['comment'] = comment.replace('\n', '')
            else:
                item['comment'] = '暂无神评'
            # 内容
            content_list = div.xpath('.//a[@class="contentHerf"]/div[@class="content"]//span/text()').extract()
            for i in content_list:
                content += i
                content = content.replace('\n', '')
                # print('content',content)
                item['content'] = content
            yield item
