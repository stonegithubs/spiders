# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class Pro6Pipeline(object):

    # def open_spider(self, spider):
    #     self.client = pymongo.MongoClient()["1807b"]["tencent"]

    def process_item(self, item, spider):
        # self.client.insert(dict(item))
        return item
