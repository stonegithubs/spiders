# -*- coding: utf-8 -*-


__author__ = 'wu_yong'

import datetime
import traceback

from ics.utils.md5_tool import to_md5
from ics.settings import default_settings
from ics.utils.db.mysql_util import KtggMysqlDb
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.utils.ktgg_data import KtggData
from ics.crawler.ktgg.core.constant import DATA_TABLE, STATUS_TABLE, RAW_TABLE, TASK_STATUS


class KtggTool(object):
    def __init__(self, ename, cname, developer, seed_dict, logger):
        self.logger = logger
        self.ename = ename
        self.cname = cname
        self.developer = developer
        self.seed_dict = seed_dict
        self.raw_table = RAW_TABLE
        self.data_table = DATA_TABLE
        self.status_table = STATUS_TABLE
        self.mysql_db = KtggMysqlDb(default_settings.MYSQL_TASK_DATA_DB, logger)

    def insert_ktgg_data(self, data, stat_dict, unique_id):
        """
        主要用于保存抓取到的每条数据,也可以用于保存其它数据到其它表，比如爬虫运行状态
        :param data:
        :return:
        """
        try:
            unique_id = to_md5(str(unique_id))
            check_sql = 'SELECT unique_id FROM {} WHERE unique_id="{}"'.format(self.data_table, unique_id)
            self.logger.info(u'开始保存ktgg详情数据')
            result = self.mysql_db.query(check_sql)
            if result:
                self.logger.info(u'data表中有重复的数据，不再插入，unique_id: {}'.format(unique_id))
                stat_dict['duplicate_cnt'] += 1
            else:
                if isinstance(data, KtggData):
                    data = data.to_dict()
                data['unique_id'] = unique_id

                self.mysql_db.insert_dic(self.data_table, data)
                self.logger.info(u'保存ktgg详情数据完成')
                stat_dict['success_cnt'] += 1
        except Exception:
            self.logger.error(u'保存ktgg详情数据出现异常:{}'.format(traceback.format_exc()))
            stat_dict['error_cnt'] += 1

    def insert_ktgg_spider_status(self, spider_name, cname, developer, do_time):
        """
        插入爬虫运行记录，状态
        :return:
        """
        try:
            data = {
                'crawl_date': do_time,
                'ename': spider_name,
                'cname': cname,
                'developer': developer,
                'state': TASK_STATUS.RUNNING,
                'create_time': self.now_datetime,
                'start_time': self.now_datetime,
                'end_time': "1970-01-01 08:00:00"
            }
            init_data = {
                'success_cnt': 0,
                'duplicate_cnt': 0,
                'error_cnt': 0
            }
            data.update(init_data)
            check_sql = 'SELECT id FROM {} WHERE ename="{}" AND crawl_date="{}";'.format(self.status_table, spider_name, do_time)
            self.logger.info(u'开始保存ktgg爬虫状态，do_time:{}, spider: {}'.format(do_time, spider_name))
            result = self.mysql_db.query(check_sql)
            if result:
                self.logger.info(u'spider_status表中有重复的数据，spider_name: {}, 开始更新爬虫初始状态'.format(spider_name))
                to_dict = {
                    'state': TASK_STATUS.RUNNING,
                    'start_time': self.now_datetime,
                    'end_time': "1970-01-01 08:00:00"
                }
                to_dict.update(init_data)
                query_dict = {
                    'id': result[0][0],
                }
                self.mysql_db.update_dict(self.status_table, to_dict, query_dict)
            else:
                self.mysql_db.insert_dic(self.status_table, data)
                self.logger.info(u'保存ktgg爬虫状态成功，do_time:{}, spider: {}'.format(do_time, spider_name))
        except Exception:
            self.logger.error(
                u'保存ktgg爬虫状态异常，do_time:{}, spider: {}, 原因{}'.format(do_time, spider_name, traceback.format_exc()))


    def update_ktgg_end_meta(self, spider_name, do_time, stat_dict, status):
        """
        爬虫结束时候调用，一次更新相应爬虫抓取完成时的相关信息，改成一次更新，给mysql减压
        :param spider_name:
        :param status:
        :param do_time:
        :return:
        """
        if not spider_name or not do_time:
            err_msg = u'输入参数不合法, do_time: {}, spider_name: {}'.format(do_time, spider_name)
            self.logger.error(err_msg)
            raise LogicException(err_msg)

        to_dict = {
            'state': status,
            'end_time': self.now_datetime
        }
        to_dict.update(stat_dict)
        condition_dict = {
            'ename': spider_name,
            'crawl_date': do_time
        }
        try:
            self.logger.info(u'开始更新爬虫结束信息，condition_dict:{}, to_dict:{}'.format(condition_dict, to_dict))
            self.mysql_db.update_dict(self.status_table, to_dict, condition_dict)
            self.logger.info(u'更新爬虫结束信息完成')
        except Exception:
            self.logger.error(u'更新爬虫状态异常, condition_dict:{}, to_dict:{},原因：{}'. \
                              format(condition_dict, to_dict, traceback.format_exc()))

    def update_ktgg_spider_status(self, spider_name, status, do_time):
        """
        更新爬虫运行状态，实时更新爬虫运行状态，启动、运行、异常、完成等
        :return:
        """

        if not spider_name or not do_time:
            err_msg = u'输入参数不合法, do_time: {}, spider_name: {}'.format(do_time, spider_name)
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        update_pattern = 'UPDATE {} SET state={} WHERE ename = "{}" AND crawl_date="{}";'. \
            format(self.status_table, status, spider_name, do_time)
        try:
            self.logger.info(u'开始更新爬虫状态，do_time:{}, spider_name:{}, to_status:{}'.format(do_time, spider_name, status))
            self.mysql_db.execSql(update_pattern)
            self.logger.info(u'更新爬虫状态完成，do_time:{}, spider_name:{}, to_status:{}'.format(do_time, spider_name, status))
        except Exception:
            self.logger.error(u'更新爬虫状态异常, do_time:{}, spider_name:{}, to_status:{},原因：{}'. \
                              format(do_time, spider_name, status, traceback.format_exc()))

    def update_ktgg_spider_cnt(self, spider_name, stat_dict, do_time):
        """
        更新爬虫运行状态，实时更新爬虫运行状态，启动、运行、异常、完成等
        :return:
        """

        if not spider_name or not do_time:
            err_msg = u'输入参数不合法, do_time: {}, spider_name: {}'.format(do_time, spider_name)
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        update_pattern = 'UPDATE {} SET success_cnt={},duplicate_cnt={},error_cnt={} WHERE ename = "{}" AND crawl_date="{}";'. \
            format(self.status_table, stat_dict['success_cnt'], stat_dict['duplicate_cnt'], stat_dict['error_cnt'],
                   spider_name, do_time)
        try:
            self.logger.info(
                u'开始更新爬虫抓取数量，do_time:{}, spider_name:{}, stat_dict:{}'.format(do_time, spider_name, stat_dict))
            self.mysql_db.execSql(update_pattern)
            self.logger.info(
                u'更新爬虫数量完成，do_time:{}, spider_name:{}, stat_dict:{}'.format(do_time, spider_name, stat_dict))
        except Exception:
            self.logger.error(u'更新爬虫数量异常, do_time:{}, spider_name:{}, stat_dict:{},原因：{}'. \
                              format(do_time, spider_name, stat_dict, traceback.format_exc()))

    def insert_page_source(self, raw, ename, cname, do_time):
        """
        保存原文，返回校验值
        :param raw:
        :param spider_flag:
        :return:
        """
        raw = unicode(raw) if isinstance(raw, str) else raw
        raw_id = to_md5(raw)
        check_sql = 'SELECT raw_id FROM {} WHERE raw_id="{}";'.format(self.raw_table, raw_id)
        sql = "INSERT INTO {} (crawl_date, ename, cname, raw, raw_id) VALUES (%s, %s, %s, %s, %s);".format(
            self.raw_table)
        try:
            self.logger.info(u'开始保存ktgg原文')
            result = self.mysql_db.query(check_sql)
            if result:
                self.logger.info(u'原文表中有重复的数据，不再插入，raw_id: {}'.format(raw_id))
            else:
                self.mysql_db.execSql(sql, [do_time, ename, cname, raw, raw_id])
                self.logger.info(u'插入原文完成，raw_id: {}'.format(raw_id))
        except Exception:
            self.logger.info(u'插入原文异常, 校验值为：{}, 原因：{}'.format(raw_id, traceback.format_exc()))
        return raw_id

    @property
    def now_date(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @property
    def now_datetime(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
