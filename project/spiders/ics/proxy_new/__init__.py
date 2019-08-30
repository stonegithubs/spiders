#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.proxy_new.zm.proxy_pool import ProxyPool
from ics.proxy_new.dly.proxy_pool import ProxyPool as DlyProxyPool
from ics.settings.default_settings import DLY_AUTH


class IcsProxy(object):

    def __init__(self, supplier="zm", logger=None):
        self._supplier = supplier
        if supplier == "zm":
            self.proxy_pool = ProxyPool(logger)
        elif supplier == "dly":
            self.proxy_pool = DlyProxyPool(logger)

    def get_proxy(self, spider_no, from_type='25mintest', api_num=3, database_proxy_num=3, model='black', grey_time=3):
        '''
        获取代理
        :param from_type: 25min/25mintest
        :param api_num: 每次从api获取数量
        :param database_proxy_num: 数据库代理补充阈值
        :param model: black/grey
        :param spider_no: 爬虫包名
        :param grey_time: 加灰维持时间
        :return:
        '''
        if self._supplier == "zm":
            proxy = self.proxy_pool.get_proxy(from_type, api_num, database_proxy_num, model, spider_no, grey_time)
        elif self._supplier == "dly":
            proxy = self.proxy_pool.get_proxy(spider_no=spider_no)
        if not proxy:
            return None, None, None
        else:
            ip = proxy['ip']
            port = proxy['port']
            if self._supplier == "zm":
                m_proxy = {"http": "http://%s:%s" % (ip, port),
                           "https": "https://%s:%s" % (ip, port)}
            elif self._supplier == "dly":
                m_proxy = {"http": "http://%s@%s:%s" % (DLY_AUTH, ip, port),
                           "https": "https://%s@%s:%s" % (DLY_AUTH, ip, port)}
            return ip, port, m_proxy

    def add_black(self, ip, spider_no):
        """
        加黑
        :param ip:
        :param spider_no:
        :return:
        """
        self.proxy_pool.add_black(ip, spider_no)

    def add_grey(self, ip, spider_no):
        """
        加灰
        :param ip:
        :param spider_no:
        :return:
        """
        self.proxy_pool.add_grey(ip, spider_no)


def get_fidder_proxy():
    ip = '127.0.0.1'
    port = '8888'
    m_proxy = {"http": "http://%s:%s" % (ip, port),
               "https": "http://%s:%s" % (ip, port)}
    return ip, port, m_proxy
