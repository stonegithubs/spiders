# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class BudingPipeline(object):
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"

        with open('./buding.json','a+',encoding='utf8')as f:
            f.write(content)
        return item
