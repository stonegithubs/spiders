# -*- coding: utf-8 -*-


__author__ = 'wu_yong'

import traceback
from abc import ABCMeta, abstractmethod
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.core.ktgg_base import KtggBase


class KtggIterPageBase(KtggBase):
    __metaclass__ = ABCMeta

    def __init__(self, seed_dict, logger):
        super(KtggIterPageBase, self).__init__(seed_dict, logger)

    def iter_page_start(self):
        try:
            self.logger.info(u'开始抓取爬虫:{}'.format(self.ename))
            self.do_time = self.ktgg_tool.now_date
            self.ktgg_tool.insert_ktgg_spider_status(self.ename, self.cname, self.developer, self.do_time)
            total_page = self.get_total_page()

            if self.seed_dict.get('is_increment'):
                page = self.seed_dict.get('page', 20)  # 默认抓取前20页
                total_page = page if page <= total_page else total_page
                self.logger.info(u'开始增量抓取，spider_name:{}, 抓取前{}页'.format(self.ename, total_page))
            else:
                self.logger.info(u'开始全量抓取，spider_name:{}, 抓取前{}页'.format(self.ename, total_page))
            self.iter_page_list(total_page)

            if self.status != TASK_STATUS.NO_RECORD:
                self.status = TASK_STATUS.SUCCESS

            self.ktgg_tool.update_ktgg_end_meta(self.ename, self.do_time, self.stat_dict, self.status)
        except Exception:
            err_msg = u'抓取ktgg爬虫异常：爬虫名称: {}, 异常原因: {}'.format(self.ename, traceback.format_exc())
            self.logger.error(err_msg)
            self.status = TASK_STATUS.FAILED
            self.ktgg_tool.update_ktgg_end_meta(self.ename, self.do_time, self.stat_dict, self.status)
            raise LogicException(err_msg)

        self.logger.info(u'爬虫抓取完成:{}'.format(self.ename))

    def start(self):
        self.iter_page_start()

    @abstractmethod
    def get_total_page(self):
        pass

    @abstractmethod
    def iter_page_list(self, total_page):
        pass