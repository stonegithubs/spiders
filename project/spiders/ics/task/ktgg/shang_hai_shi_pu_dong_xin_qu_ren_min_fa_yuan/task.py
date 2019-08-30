#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:task.py
description:
author:crazy_jacky
version: 1.0
date:2018/10/16
"""
from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.decorator import stable
from ics.scheduler.new_task import StableTask
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.spiders.province.sh.shang_hai_shi_pu_dong_xin_qu_ren_min_fa_yuan import\
    ShangHaiShiPuDongXinQuRenMinFaYuan

logger = get_ics_logger('shang_hai_shi_pu_dong_xin_qu_ren_min_fa_yuan')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dict):
    spider = ShangHaiShiPuDongXinQuRenMinFaYuan(logger, seed_dict)
    spider.start()
