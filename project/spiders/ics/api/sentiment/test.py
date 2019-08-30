#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import redis
from ics.task.baidu_news.m_redis import redis_pool
from ics.scheduler import app
import json

r = redis.Redis(connection_pool=redis_pool)


# while True:
#     s = r.lpop('ent:sentiment:content:crawl_task')
#     if not s:
#         break
# for i in range(20):
#     r.lpush('ent:sentiment:content:crawl_task',
#             '{"companyName":"上海冰鉴信息科技有限公司","crawlTaskId":' + str(i) + ',"keyword":"冰鉴","timestamp":1527751942850,"uuid":"d7d7d0ae35be3323b40b42ed73f97a0a"}')


# print r.blpop('ent:sentiment:snapshot:crawl_task')[1]

# r.lpush('ent:sentiment:snapshot:crawl_task','{"companyName":"上海冰鉴信息科技有限公司3","crawlTaskId":5,"keyword":"上海冰鉴3","timestamp":1527751942850,"uuid":"d7d7d0ae35be3323b40b42ed73f97a0a"}')

# 消费 ent:sentiment:snapshot:crawl_task 新闻快照页爬虫请求
def consumer_0():
    craw_request = json.loads(r.blpop('ent:sentiment:snapshot:crawl_task')[1])
    craw_request['need_content'] = False
    # 发送任务到celery
    app.send_task('ics.task.baidu_news.task.start', [craw_request], queue='baidu_news_queue')


# consumer_0()


########################################################################################################

def consumer_1():
    craw_request = json.loads(r.blpop('ent:sentiment:content:crawl_task')[1])
    craw_request['need_content'] = True
    # 发送任务到celery
    app.send_task('ics.task.baidu_news.task.start', [craw_request], queue='baidu_news_queue')


def test_0():
    for i in range(1):
        r.lpush('ent:sentiment:snapshot:crawl_task',
                '{"companyName":"上海冰鉴信息科技有限公司","crawlTaskId":1 ,"keyword":"冰鉴","timestamp":1527751942850,"uuid":"d7d7d0ae35be3323b40b42ed73f97a0a"}')
        consumer_0()


def test_1():
    for i in range(1):
        r.lpush('ent:sentiment:content:crawl_task',
                '{"companyName":"上海冰鉴信息科技有限公司","crawlTaskId":1 ,"keyword":"冰鉴","timestamp":1527751942850,"uuid":"d7d7d0ae35be3323b40b42ed73f97a0a"}')
        consumer_1()

# test_1()
