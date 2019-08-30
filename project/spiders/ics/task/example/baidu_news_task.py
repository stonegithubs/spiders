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
from celery.utils.log import get_task_logger
import time
import json

logger = get_task_logger(__name__)

task_queue = 'baidu_news_queue'


@app.task
def start(company_name):
    for r in [
        Request(url="http://news.baidu.com/ns?word={0}&pn={1}&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0".format(
            company_name, 20 * page), meta={'company_name': company_name},
            callback='ics.task.example.baidu_news_task.process') for page in range(1, 2)]:
        send_download_request(r, task_queue)


@app.task
def process(response):
    result_list = []
    response = response_from_dict(response)
    soup = response.get_soup()
    content_list = soup.select('div.result')

    for content in content_list:
        result = dict()
        title = content.select('h3')[0].text.strip()
        content_0 = content.select('p.c-author')[0].text.replace('\n','').replace('\t','')
        from_ = content_0.split('  ')[0]
        date = content_0.split('  ')[1]
        temp_content = content.select('div.c-summary.c-row')[0]
        temp_content.p.clear()
        content_ = temp_content.text.strip().replace('\n','').replace('\t','')
        url = content.select('h3 a')[0]['href'].strip()

        result['searcher'] = 'baidu'
        result['title'] = title
        result['from_'] = from_
        result['date'] = date
        result['content_'] = content_
        result['url'] = url

        result_list.append(result)

    result__ =  {'timestamp': int(time.time()),
            'snapshot': result_list,
            'keyword': response.request.meta['company_name']
            }

    logger.info('-------------' + json.dumps(result__).decode('unicode_escape'))

    return result__
