# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

client = pymongo.MongoClient()['sun']['yangguangwang']


class Pro10Pipeline(object):
    def process_item(self, item, spider):
        client.insert(dict(item))
        return item
