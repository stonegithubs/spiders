#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from ics.scheduler import app
from ics.http.spider_request import Request
from ics.task.core import send_download_request, send_to_download_pic, send_to_mysql, send_to_console
from ics.utils.seq_util import SeqUtil
from ics.utils.reqser import response_from_dict

import copy
import hashlib
import random
import time

task_queue = 'tuliu_queue'


@app.task
def start():
    for r in [
        Request(url='http://www.tuliu.com/news/list-c165/%s.html' % page, meta={'newsCateId': '20171102111907007'},
                callback='ics.task.example.tuliu_task.process')
        for page in range(1, 9)]:
        send_download_request(r, task_queue)


@app.task
def process(response):
    response = response_from_dict(response)
    if '404错误' not in response.m_response.content:
        soup = response.get_soup()

        tuliu_div_list = soup.select('div.news_list_list ul li.list_box')
        for tuliu_div in tuliu_div_list:
            if tuliu_div.select('a img'):
                detail_url = tuliu_div.select('a')[0]['href']
                img_url = tuliu_div.select('a img')[0]['src']
                name = tuliu_div.select('h1.category_title nobr.l')[0].text.strip()
                createTime = tuliu_div.select('h1.category_title nobr.r')[0].text.replace('发布时间 ', '').strip()
                shortDes = tuliu_div.select('div')[0].text.replace('[查看全文]', '')

                md5 = hashlib.md5()
                rand_name = str(time.time()) + str(random.random())
                md5.update(rand_name)
                img_name = md5.hexdigest() + '.jpg'

                request = Request(url=img_url, is_img=True,
                                  callback='ics.task.example.tuliu_task.process_pic')
                request.meta['img_name'] = img_name
                send_download_request(request, task_queue, callback_queue='pipe_queue')

                request = Request(url=detail_url, callback='ics.task.example.tuliu_task.process_detail')
                request.meta['name'] = name
                request.meta['createTime'] = createTime
                request.meta['shortDes'] = shortDes
                request.meta['img_name'] = img_name
                request.meta['newsCateId'] = response.request.meta['newsCateId']
                send_download_request(request, task_queue, callback_queue='pipe_queue')


@app.task
def process_pic(response):
    response = response_from_dict(response)
    item = dict()
    item['content'] = response.m_response.content
    item['name'] = response.request.meta['img_name']
    send_to_download_pic(item, 'pipe_queue')


@app.task
def process_detail(response):
    response = response_from_dict(response)
    soup = response.get_soup()
    result = dict()
    result['newsProductId'] = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + SeqUtil.get_seq()
    result['newsCateId'] = response.request.meta['newsCateId']
    result['name'] = response.request.meta['name']
    result['imageUrl'] = response.request.meta['img_name']
    result['newsCateId'] = response.request.meta['newsCateId']
    result['shortDes'] = response.request.meta['shortDes']
    result['createTime'] = response.request.meta['createTime']
    result['newsFromWebUrl'] = response.request.url
    span_list = soup.select('div.article-header p.text-gray-9 span')
    for span in span_list:
        if '来源：' in span.text:
            result['newsFrom'] = span.text.replace('来源：', '').strip()
            break
        else:
            result['newsFrom'] = '互联网'
    longDes = soup.select('div.article-content')[0]

    tag_list = longDes.find_all()
    # 去除样式
    for tag in tag_list:
        attrs = copy.copy(tag.attrs)
        for key in attrs.iterkeys():
            if key != 'src':
                del tag.attrs[key]

    result['longDes'] = str(longDes)

    send_to_mysql(result, 'pipe_queue')
    send_to_console(result, 'pipe_queue')
