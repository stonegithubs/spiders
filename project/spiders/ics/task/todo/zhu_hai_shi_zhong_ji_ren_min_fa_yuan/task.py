#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.decorator import stable
from ics.scheduler.new_task import StableTask
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.spiders.province.gd.zhu_hai_shi_zhong_ji_ren_min_fa_yuan import \
    ZhuHaiShiZhongJiRenMinFaYuan

logger = get_ics_logger('zhu_hai_shi_zhong_ji_ren_min_fa_yuan')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dict):
    spider = ZhuHaiShiZhongJiRenMinFaYuan(logger, seed_dict)
    spider.start()
