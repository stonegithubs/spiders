#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import sys
import time
import copy
import random
from ics.scheduler import app
from ics.utils.decorator import stable2
from ics.utils.string_tool import is_in_list
from ics.scheduler.new_task import StableTask
from ics.utils.exception_util import LogicException

from ics.http.http_downloader import Downloader
from ics.task.zgcpws.batch.batch_dao import *

reload(sys)
sys.setdefaultencoding('utf-8')

SPIDER_NAME = "zgcpws"

basic_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://wenshu.court.gov.cn/'}

lst_change_add_grey_ip = list()
list_retry = list()

list_retry.append('"[]"')
list_retry.append('"[check]"')
list_retry.append('"remind key"')
list_retry.append('服务不可用')
list_retry.append('ArgumentOutOfRangeException')

lst_change_add_grey_ip.append('"remind"')
# lst_change_add_grey_ip.append('<span>502</span>')
lst_change_add_grey_ip.append('502 - Web')
lst_change_add_grey_ip.append('<title>502</title>')
lst_change_add_grey_ip.append(('<span>360安域</span>'))
lst_change_add_grey_ip.append(('window.location.href='))

downloader = Downloader(spider_no=SPIDER_NAME, logger=logger,session_keep=False, abandon_model="grey", grey_time=3, proxy_mode="dly")


def pc_judge_func_retry(resp, meta):
    result = is_in_list(list_retry, resp.content)
    if result:
        logger.warn(resp.content)
    return result


def pc_judge_func_retry_add_grey(resp, meta):
    result = is_in_list(lst_change_add_grey_ip, resp.content)
    if result:
        downloader.change_add_grey_proxy()
        logger.warn(resp.content)
    return result


downloader.set_retry_solution(pc_judge_func_retry)
downloader.set_retry_solution(pc_judge_func_retry_add_grey)


@app.task(bind=True, base=StableTask, default_retry_delay=1, max_retries=10, ignore_result=True)
@stable2(Exception, logger=logger)
def get_doc_id(self, doc_id):
    last_header = copy.deepcopy(basic_header)

    url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={0}'.format(doc_id)

    source = downloader.get(
        url=url,
        headers=last_header,
        timeout=20,
        retry_cnt=8,
    ).content

    time.sleep(random.randint(1, 4) * 0.5)

    # $(function(){$("#con_llcs").html("浏览：131次")});$(function(){$("#hidRequireLogin").val("0");$("#Content").html("此篇文书不存在!");});$(function(){});

    if u'文书ID' in source or u'此篇文书不存在' in source:
        result_dic = add_key(doc_id, source)
        save_data(result_dic, logger)
        update_status(result_dic.get("doc_id"), logger)
    else:
        logger.error('search doc_id:{} failed, req is :{}'.format(doc_id, source))
        raise LogicException('get detail conten failed')