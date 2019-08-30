# coding:utf-8

import json
import traceback

import pymongo
import pymysql


class MysqlUtil(object):

    def __init__(self, *args, **kwargs):
        self.conn = pymysql.connect(*args, **kwargs)
        self.cursor = self.conn.cursor()

    def query(self, sql):
        cnt = self.cursor.execute(sql)
        results = self.cursor.fetchall()  # 获取查询的所有记录
        return cnt, results

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()


class MongoUtil(object):

    def __init__(self, database, host=None, port=None, *args, **kwargs):
        '''初始化 MongoClient'''
        try:
            self.client = pymongo.MongoClient(host, port, *args, **kwargs)
            self.db = self.client[database]
        except Exception:
            # 返回错误信息
            print('Connect Database Fail!')
            traceback.print_exc()

    def insert_one(self, collection, doc):
        '''insert one doc'''
        try:
            result = self.db[collection].insert_one(doc)
            return result.inserted_id
        except Exception:
            # 返回错误信息
            print('insert doc Fail!')
            traceback.print_exc()

    def insert_many(self, collection, docs):
        '''insert many docs, docs is list'''
        try:
            result = self.db[collection].insert_many(docs)
            return result.inserted_ids
        except Exception:
            # 返回错误信息
            print('insert docs Fail!')
            traceback.print_exc()

    def delete(self, collection, deletesql):
        '''delete docs  deletesql: {'':''}'''
        try:
            result = self.db[collection].delete_many(deletesql)
            return result.deleted_count
        except Exception:
            # 返回错误信息
            print('delete docs Fail!')
            traceback.print_exc()

    def update(self, collection, doc, updatesql):
        '''update doc updatesql: {'':''}'''
        try:
            result = self.db[collection].update_many(doc, updatesql, True)
            return result.matched_count
        except Exception:
            # 返回错误信息
            print('update doc Fail!')
            traceback.print_exc()

    def query(self, collection, querysql=None):
        '''query doc'''
        try:
            if querysql:
                results = self.db[collection].find(querysql)
            else:
                results = self.db[collection].find().limit(100)
            return results
        except Exception:
            # 返回错误信息
            print('query docs Fail!')
            traceback.print_exc()


# c = pymongo.MongoClient('localhost', 27017)
# doc = c.mingluji.jx
# for d in doc.find().limit(10000000):
#     print(d)


if __name__ == '__main__':
    util = MongoUtil("huangfei", '218.94.82.249', 3125)

    ss = "{'corpStatusString': '开业', 'islicense': '0', 'pripid': '59797F955764B6679A48A249B466902FE92F6A2F6A2FE12FB8FD6A2FB87E06E572DDA5B17786C3057D9E09BC8E9AFF1C8B246D6A6D6A-1563878482537', 'entTypeCn': '有限责任公司分公司(法人独资)', 'illCount': 0, 'estDate': '2016-03-18', 'historyName': None, 'opFrom': None, 'nodeNum': '110000', 'legelRep': '王瑾', 'entTypeString': '有限责任公司分公司(法人独资)', 'corpStatusReason': None, 'entName': '南京中新赛克科技有限责任公司北京分公司', 'entType': 2152, 'uniscId': '91110108MA00478Q15', 'opTo': None, 'isPublicPeriod': None, 'regOrg': '北京市工商行政管理局海淀分局', 'corpStatus': 1, 'busExceptCount': 0, 'noticeFrom': None, 'simpleCanrea': '', 'noticeTo': None, 'corpStatusDate': None, 'regNo': '110108020854380', 'info_id': '', 'regCap': 0.0}"
    d = json.loads(json.dumps(eval(ss)))
    print(d)
    util.insert_one('hf', d)

    # config = {
    #     'host': '218.94.82.249',
    #     'port': 8015,  # MySQL默认端口
    #     'user': 'rhino',  # mysql默认用户名
    #     'password': 'rhino',
    #     'db': 'company_list',  # 数据库
    #     'use_unicode': True,
    #     'charset': 'utf8',
    # }
    #
    # util = MysqlUtil(**config)
    # cnt, ret = util.query("select * from Data_Minglu_Company limit 10")
    # print(ret)
