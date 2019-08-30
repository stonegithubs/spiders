# -*- coding: utf-8 -*-


__author__ = 'wu_yong'

from abc import ABCMeta, abstractmethod
from ics.crawler.ktgg.core.ktgg_tool import KtggTool


class KtggBase(object):

    __metaclass__ = ABCMeta

    ename = None
    cname = None
    domain = None
    developer = None

    def __init__(self, seed_dict, logger):
        self.do_time = None
        self.logger = logger
        self.seed_dict = seed_dict
        self.ktgg_tool = KtggTool(self.ename, self.cname, self.developer, seed_dict, logger)
        self.stat_dict = {
            'success_cnt': 0,
            'duplicate_cnt': 0,
            'error_cnt': 0
        }     # 装抓取统计情况

    @abstractmethod
    def start(self):
        """
        每个爬虫必须重写此方法，爬虫启动函数，
        需要完善特定爬虫启动时的逻辑
        :return:
        """
        pass

