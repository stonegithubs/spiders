#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ics.settings.default_settings import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_PROXY_DLY, DLY_PROXY_URL

__author__ = 'MaoJingwen'

import requests
from retry import retry
import datetime
import redis
import time
from ics.utils import get_ics_logger


class ProxyPool(object):
    def __init__(self, logger=None):
        self._logger = logger or get_ics_logger('proxy_service')
        self._server = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT, db=REDIS_PROXY_DLY)

    @retry(exceptions=Exception, tries=8, delay=1)
    def get_proxy(self, spider_no):
        while True:
            proxy = self._get_proxy_from_redis(spider_no)
            if not proxy:
                self._get_dly_proxy(spider_no)
                time.sleep(0.5)
                continue
            break
        return proxy

    @retry(exceptions=Exception, tries=8, delay=1)
    def _get_dly_proxy(self, spider_no):
        proxy_url = DLY_PROXY_URL
        session = requests.session()
        result = session.get(proxy_url).content
        proxy_list = result.split('\r\n')
        for proxy in proxy_list:
            value_list = proxy.split(',')
            ip = value_list[1]
            port = value_list[0].split(':')[1]
            expire = value_list[4]
            key = "{}|{}|{}|{}".format(spider_no, ip, port, expire)
            self._server.set(key, "{}:{}".format(ip, port))
            expire_time = datetime.datetime.fromtimestamp(float(expire))
            self._server.expireat(key, expire_time)

    @retry(exceptions=Exception, tries=8, delay=1)
    def _get_proxy_from_redis(self, spider_no):
        temp = self._server.keys("{}|*".format(spider_no))
        if len(temp) > 0:
            key = temp[0]
            data = self._server.get(key).split(':')
            self._server.delete(key)
            proxy_dict = dict()
            proxy_dict['ip'] = data[0]
            proxy_dict['port'] = data[1]
            return proxy_dict
        else:
            return None

    @retry(exceptions=Exception, tries=8, delay=1)
    def _get_count_from_redis(self, spider_no):
        return len(self._server.keys("{}|*".format(spider_no)))

    @retry(exceptions=Exception, tries=2, delay=1)
    def add_black(self, ip, spider_no):
        pass

    @retry(exceptions=Exception, tries=2, delay=1)
    def add_grey(self, ip, spider_no):
        pass
