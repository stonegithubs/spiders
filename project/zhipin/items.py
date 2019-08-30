# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhipinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    money = scrapy.Field()
    experience = scrapy.Field()
    content = scrapy.Field()
    address = scrapy.Field()
    number = scrapy.Field()
    time = scrapy.Field()
    company = scrapy.Field()
