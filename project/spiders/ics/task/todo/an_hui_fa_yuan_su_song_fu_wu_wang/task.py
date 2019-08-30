#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.decorator import stable
from ics.scheduler.new_task import StableTask
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.spiders.province.ah.an_hui_fa_yuan_su_song_fu_wu_wang import AnHuiFaYuanSuSongFuWuWang

logger = get_ics_logger('an_hui_fa_yuan_su_song_fu_wu_wang')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dict):
    spider = AnHuiFaYuanSuSongFuWuWang(logger, seed_dict)
    spider.start()
