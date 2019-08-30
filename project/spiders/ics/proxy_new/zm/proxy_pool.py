#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import requests
from retry import retry
import time
from ics.settings import default_settings
from ics.utils.db.mysql_util import ProxyDb
from ics.utils import get_ics_logger


class ProxyPool(object):
    def __init__(self, logger=None):
        self._logger = logger or get_ics_logger('proxy_service')
        self._proxy_db = ProxyDb(default_settings.MYSQL_TASK_DATA_DB, self._logger)

    @retry(exceptions=Exception, tries=8, delay=1)
    def get_proxy(self, from_type, api_num, database_proxy_num, model, spider_no, grey_time):
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
        database_count = self._get_count_from_mysql(model, spider_no, grey_time)

        if database_count >= database_proxy_num:
            proxy = self._get_proxy_from_mysql(model, spider_no, grey_time)
            return proxy
        else:
            proxy_list = self._get_zm_proxy(from_type, api_num, database_proxy_num, model, spider_no, grey_time)
            if isinstance(proxy_list, list):
                self._insert_proxy_list(proxy_list)
                data = proxy_list[0]
                return {'ip': data['ip'], 'port': data['port']}
            elif proxy_list == 'database':
                proxy = self._get_proxy_from_mysql(model, spider_no, grey_time)
                return proxy
            else:
                raise RuntimeError('no proxy in api !!!!')

    @retry(exceptions=Exception, tries=8, delay=1)
    def _insert_proxy_list(self, proxy_list):
        sql_list = []
        for model in proxy_list:
            sql = "INSERT INTO tbl_proxy_new (ip,port,expire_time) VALUES ('%s','%s','%s')" % (
                model['ip'], model['port'], model['expire_time'])
            sql_list.append(sql)

        sql = "UPDATE tbl_proxy_new SET used_count = used_count + 1 WHERE ip = \'%s\'" % (proxy_list[0]['ip'],)
        sql_list.append(sql)
        self._proxy_db.trans_execSql(sql_list)

    @retry(exceptions=Exception, tries=8, delay=1)
    def _get_zm_proxy(self, from_type, api_num, database_proxy_num, model, spider_no, grey_time):
        while True:
            if from_type == '25min':
                proxy_url = default_settings.PROXY_25MIN % str(
                    api_num)
            elif from_type == '25mintest':
                proxy_url = default_settings.PROXY_25MIN_TEST % str(
                    api_num)
            session = requests.session()
            result = session.get(proxy_url)
            result = result.json()
            if result['code'] == 0:
                return result['data']
            elif result['code'] == 111:
                # {"code":111,"success":false,"msg":"请在1秒后再次请求","data":[]}
                database_count = self._get_count_from_mysql(model, spider_no, grey_time)
                if database_count >= database_proxy_num:
                    return 'database'
                else:
                    time.sleep(2)
                    continue
            else:
                return None

    @retry(exceptions=Exception, tries=8, delay=1)
    def _get_proxy_from_mysql(self, model, spider_no, grey_time):
        sql = 'select * from tbl_proxy_new where expire_time>date_add(now(), interval 5 minute) and %s IS NULL' % (
            spider_no)
        if model == "grey":
            sql += ' and (%s_grey is NULL or (NOW()>date_add(%s_grey, interval %s minute)))' % (
                spider_no, spider_no, grey_time)
        # sql += ' order by last_use_time, used_count limit 1'
        sql += ' order by used_count limit 1'
        data = self._proxy_db.query(sql)
        sql = "UPDATE tbl_proxy_new SET used_count = used_count + 1 WHERE ip = \'%s\'" % (data[0][1],)
        self._proxy_db.execSql(sql)

        proxy_dict = dict()
        proxy_dict['ip'] = data[0][1]
        proxy_dict['port'] = data[0][2]
        return proxy_dict

    @retry(exceptions=Exception, tries=8, delay=1)
    def _get_count_from_mysql(self, model, spider_no, grey_time):
        sql = 'select count(*) from tbl_proxy_new where expire_time>date_add(now(), interval 5 minute) and %s IS NULL' % (
            spider_no)
        if model == "grey":
            sql += ' and (%s_grey is NULL or (NOW()>date_add(%s_grey, interval %s minute)))' % (
                spider_no, spider_no, grey_time)
        data = self._proxy_db.query(sql)
        return data[0][0]

    @retry(exceptions=Exception, tries=2, delay=1)
    def add_black(self, ip, spider_no):
        sql = "UPDATE tbl_proxy_new SET %s = \'black\' WHERE ip = \'%s\'" % (spider_no, ip)
        self._proxy_db.execSql(sql)

    @retry(exceptions=Exception, tries=2, delay=1)
    def add_grey(self, ip, spider_no):
        sql = "UPDATE tbl_proxy_new SET %s_grey = NOW() WHERE ip = \'%s\'" % (spider_no, ip)
        self._proxy_db.execSql(sql)
