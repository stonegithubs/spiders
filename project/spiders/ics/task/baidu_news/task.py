#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'MaoJingwen'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from ics.scheduler import app
from ics.http.spider_request import Request
from ics.task.core import send_download_request
from ics.utils.reqser import response_from_dict
from ics.task.baidu_news.m_redis import redis_pool
from ics.task.baidu_news.mysql_pool import mysql_pool
from ics.utils.document import get_summery
from celery.utils.log import get_task_logger
import redis
import json
import traceback

logger = get_task_logger(__name__)

r = redis.Redis(connection_pool=redis_pool)

baidu_news_queue = 'baidu_news_queue'


@app.task
def start(crawl_request):
    for request in [Request(url="http://news.baidu.com/ns?word={0}&pn={1}&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0"
            .format(crawl_request['keyword'], 20 * page), meta=crawl_request,
                            callback='ics.task.baidu_news.task.process') for page in range(1, 2)]:
        send_download_request(request, baidu_news_queue)


@app.task
def process(response):
    response = response_from_dict(response)
    soup = response.get_soup()
    content_list = soup.select('div.result')

    for content in content_list:
        result_mysql = dict()
        title = content.select('h3')[0].text.strip()
        content_0 = content.select('p.c-author')[0].text.replace('\n', '').replace('\t', '')
        from_ = content_0.split('  ')[0]
        date = content_0.split('  ')[1]
        temp_content = content.select('div.c-summary.c-row')[0]
        temp_content.p.clear()
        content_ = temp_content.text.strip().replace('\n', '').replace('\t', '') \
            .replace('...      查看更多相关新闻>>  -                                            百度快照', '...') \
            .replace('...                      百度快照', '...')

        url = content.select('h3 a')[0]['href'].strip()

        result_mysql['company_name'] = response.request.meta['companyName']
        result_mysql['uuid'] = response.request.meta['uuid']
        result_mysql['crawl_task_id'] = response.request.meta['crawlTaskId']
        result_mysql['keyword'] = response.request.meta['keyword']
        result_mysql['searcher'] = 'baidu'
        result_mysql['snapshot_source'] = from_
        result_mysql['title'] = title
        result_mysql['url'] = url
        result_mysql['content'] = content_
        result_mysql['snapshot_date'] = date.split(' ')[0].replace('年', '-').replace('月', '-').replace('日', '')

        if response.request.meta['need_content']:
            response.request.meta['searcher'] = 'baidu'
            response.request.meta['snapshot_source'] = from_
            response.request.meta['snapshot_date'] = date.split(' ')[0].replace('年', '-').replace('月', '-').replace('日',
                                                                                                                    '')
            response.request.meta['title'] = title
            send_download_request(
                Request(url=url, meta=response.request.meta, callback='ics.task.baidu_news.task.get_content'),
                queue=baidu_news_queue)
        else:
            insert_mysql("sentiment_snapshot", result_mysql)

    redis_result = {
        'companyName': response.request.meta['companyName'],
        'uuid': response.request.meta['uuid'],
        'crawlTaskId': response.request.meta['crawlTaskId'],
        'keyword': response.request.meta['keyword'],
        'timestamp': response.request.meta['timestamp'],
    }

    r.lpush('ent:sentiment:snapshot:crawl_result', json.dumps(redis_result).decode('unicode_escape'))

    # 发送结果到队列作为通知
    if response.request.meta['need_content']:
        response.request.meta.pop('need_content')
        r.lpush('ent:sentiment:content:crawl_result', response.request.meta)
    return redis_result


@app.task(bind=True, default_retry_delay=10, max_retries=3, rate_limit='120/m', ignore_result=True)
def get_content(self, response):
    response = response_from_dict(response)
    result_mysql = dict()
    result_mysql['searcher'] = response.request.meta['searcher']
    result_mysql['news_source'] = response.request.meta['snapshot_source']
    result_mysql['news_date'] = response.request.meta['snapshot_date']
    result_mysql['title'] = response.request.meta['title']
    result_mysql['uuid'] = response.request.meta['uuid']
    result_mysql['company_name'] = response.request.meta['companyName']
    result_mysql['crawl_task_id'] = response.request.meta['crawlTaskId']
    result_mysql['keyword'] = response.request.meta['keyword']
    result_mysql['url'] = response.request.url
    result_mysql['content'] = get_summery(response.m_response.content.decode("utf-8", "ignore"))
    if not result_mysql['content']:
        logger.error('content None:' + response.request.url + response.m_response.content.decode("utf-8",
                                                                                                 "ignore") + '\r\n' + json.dumps(
            response.request).decode('unicode_escape'))
    try:
        insert_mysql("sentiment_news", result_mysql)
    except Exception as e:
        import traceback
        traceback.print_exc()
        self.retry(exc=e, response=response)


def insert_mysql(table, model):
    db = mysql_pool.connection()

    cursor = db.cursor()

    qmarks = ', '.join(['%s'] * len(model))  # 用于替换记录值
    cols = ', '.join(model.keys())  # 字段名
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
    try:
        cursor.execute(sql, model.values())
        db.commit()
    except Exception:
        db.rollback()
        db.close()
        traceback.print_exc()
        raise RuntimeError('mysql error')
    db.close()
