# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiushibaikeItem(scrapy.Item):
    user_name = scrapy.Field()
    content = scrapy.Field()
    funny = scrapy.Field()
    comment = scrapy.Field()