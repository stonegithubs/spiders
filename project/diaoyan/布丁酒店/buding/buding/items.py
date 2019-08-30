# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BudingItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    address = scrapy.Field()
    introduce = scrapy.Field()
    comment = scrapy.Field()
    tel = scrapy.Field()
