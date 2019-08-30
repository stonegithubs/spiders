#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'wu_yong'

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.decorator import stable
from ics.scheduler.new_task import StableTask
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.spiders.province.gd.zhao_qing_shi_duan_zhou_qu_ren_min_fa_yuan import \
    ZhaoQingShiDuanZhouQuRenMinFaYuan

logger = get_ics_logger('zhao_qing_shi_duan_zhou_qu_ren_min_fa_yuan')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dict):
    spider = ZhaoQingShiDuanZhouQuRenMinFaYuan(logger, seed_dict)
    spider.start()
