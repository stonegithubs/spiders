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
from ics.crawler.ktgg.spiders.province.gd.guang_dong_fa_yuan_wang import GuangDongFaYuanWang

logger = get_ics_logger('guang_dong_fa_yuan_wang')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dict):
    spider = GuangDongFaYuanWang(logger, seed_dict)
    spider.start()
