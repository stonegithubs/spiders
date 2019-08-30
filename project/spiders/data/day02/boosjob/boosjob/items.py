# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoosjobItem(scrapy.Item):
    # define the fields for your item here like:
    job = scrapy.Field()
    salary = scrapy.Field()
    region = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    company = scrapy.Field()
    detail_url = scrapy.Field()
    duty = scrapy.Field()
