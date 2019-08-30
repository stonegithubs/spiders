#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.http.http_downloader import Downloader
from ics.utils import get_ics_logger

logger =get_ics_logger("test")

downloader = Downloader(logger=logger,black_type="other")

headers = {}
downloader.get("http://www.baidu.com",headers=headers)
