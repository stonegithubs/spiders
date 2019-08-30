import pymongo
import datetime


class INfoPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.datetime.now()
        item["spider"] = spider.name
        return item


class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient()["aaa"]["ddbook"]

    def process_item(self, item, spider):
        self.client.insert(dict(item))
        return item
