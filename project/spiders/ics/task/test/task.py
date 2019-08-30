#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.scheduler import app
from celery.utils.log import get_task_logger
from ics.utils.phantom import get_web_driver
import time

logger = get_task_logger(__name__)


# 等待多久重试的时间，以及最大的重试次数
@app.task(rate_limit='10/m')
def add(x, y):
    if x == 10:
        app.control.rate_limit('ics.task.test.task.add', '1000/m')
    return x + y


@app.task(bind=True)
def multi(self, x, y):
    time.sleep(0.1)
    logger.info(self.request.__dict__)
    return x * y


@app.task()
def test_phantomjs():
    web = get_web_driver()
    web.get('https://www.jd.com/')
    resHtml = web.execute_script("return document.documentElement.outerHTML")
    web.quit()
    print resHtml


@app.task()
def print_str(str_):
    return str_


from ics.utils.decorator import stable
from ics.scheduler.new_task import StableTask


@app.task(bind=True, base=StableTask, default_retry_delay=10, max_retries=3, rate_limit='120/m', ignore_result=True)
@stable((RuntimeError, ValueError))
def test_stable(self, parm_1, parm_2, parm_3):
    self.url = "http://www.baidu.com"
    self.logger_meta["asdf"] = "adsfdf"
    print parm_1
    print parm_2
    print parm_3
    raise ValueError('test')

# 对任务指定队列运行
#
# 方式1
# @app.task(bind=True, queue='middle', name='send_wx_text')
# def send_wx_text(self, target_origin_id, to_user, txt):
#
#
# 方式2
# send_wx_text.apply_async((target_origin_id, to_user, txt), queue='middle')
#
# 方式3
# CELERY_ROUTES = {
#     'send_wx_text': {
#         'queue': 'middle',
#     },
# }
