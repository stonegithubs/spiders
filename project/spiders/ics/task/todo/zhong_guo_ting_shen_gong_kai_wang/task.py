#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'wu_yong'

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.scheduler.new_task import StableTask
from ics.utils.decorator import stable2
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.spiders.province.qg.zhong_guo_ting_shen_gong_kai_wang import ZhongGuoTingShenGongKaiWang

logger = get_ics_logger('zhong_guo_ting_shen_gong_kai_wang')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable2(LogicException, logger=logger)
def start(self, seed_dict):
    spider = ZhongGuoTingShenGongKaiWang(logger, seed_dict)
    spider.start()
