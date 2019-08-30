#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:task.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/18
"""

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.decorator import stable
from ics.scheduler.new_task import StableTask
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.spiders.province.qg.zhong_guo_shen_pan_liu_cheng_xin_xi_gong_kai_wang import \
    ZhongGuoShenPanLiuChengXinXiGongKaiWang

logger = get_ics_logger('zhong_guo_shen_pan_liu_cheng_xin_xi_gong_kai_wang')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dict):
    spider = ZhongGuoShenPanLiuChengXinXiGongKaiWang(logger, seed_dict)
    spider.start()
