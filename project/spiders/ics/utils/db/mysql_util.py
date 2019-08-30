#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'MaoJingwen'

import MySQLdb
from MySQLdb import OperationalError
from DBUtils.PooledDB import PooledDB
from ics.settings import default_settings
from retry import retry
import traceback
from ics.utils.singleton import Singleton


class MySQLUtil(object):
    def __init__(self, db_name, logger=None, host=default_settings.MYSQL_HOST, user=default_settings.MYSQL_USERNAME,
                 passwd=default_settings.MYSQL_PASSWORD, port=default_settings.MYSQL_PORT):
        self._init(db_name=db_name, logger=logger, host=host, user=user, passwd=passwd, port=port)

    @retry(exceptions=(OperationalError), tries=20, delay=1)
    def _init(self, db_name, logger, host, user, passwd, port):
        self.logger = logger
        self.mysql_pool = PooledDB(MySQLdb, mincached=3, host=host, user=user, passwd=passwd, db=db_name,
                                   charset='utf8', port=port, blocking=True, maxconnections=10, maxcached=5)

    def get_connect_pool(self):
        return self.mysql_pool

    @retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
    def execSql(self, sql, *args, **kwargs):
        result = 0
        db = None
        try:
            db = self.mysql_pool.connection()
            cursor = db.cursor()
            result = cursor.execute(sql, *args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            if db:
                db.rollback()
            if self.logger:
                self.logger.error(traceback.format_exc() + "\r\n" + "sql:" + sql)
            else:
                traceback.print_exc()
            raise RuntimeError('mysql error')
        finally:
            if db:
                db.close()

    @retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
    def trans_execSql(self, list_sql):
        result = 0
        db = None
        tmp_sql = None
        try:
            db = self.mysql_pool.connection()
            cursor = db.cursor()
            for sql in list_sql:
                tmp_sql = sql
                result = cursor.execute(sql)
            db.commit()
            return result
        except Exception as e:
            if db:
                db.rollback()
            if self.logger:
                self.logger.error(traceback.format_exc() + "\r\n" + "sql:" + tmp_sql)
            else:
                traceback.print_exc()
            raise RuntimeError('mysql error')
        finally:
            if db:
                db.close()

    @retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
    def query(self, sql):
        data = None
        db = None
        try:
            db = self.mysql_pool.connection()
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except Exception as e:
            if self.logger:
                self.logger.error(traceback.format_exc() + "\r\n" + "sql:" + sql)
            else:
                traceback.print_exc()
            raise RuntimeError('mysql error')
        finally:
            if db:
                db.close()

    def insert_dic(self, tbl, dic):
        """
        support insert dict data to mysql
        :return:
        """
        qmarks = ', '.join(['%s'] * len(dic))  # 用于替换记录值
        cols = ', '.join(dic.keys())  # 字段名
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (tbl, cols, qmarks)
        return self.execSql(sql, dic.values())

    def update_dict(self, tbl, to_dict, condition_dict=None):
        def trans_dict_to_query_str(args_dcit, connector_str=','):
            tmp_list = []
            for k, v in args_dcit.items():
                tmp_list.append('{}="{}"'.format(k, v))
            connector_str = ' {} '.format(connector_str)
            args_str = connector_str.join(tmp_list)
            return args_str

        to_dict_str = trans_dict_to_query_str(to_dict)
        sql = "UPDATE %s SET %s " % (tbl, to_dict_str)
        if condition_dict:
            condition_str = trans_dict_to_query_str(condition_dict, 'AND')
            sql += ' WHERE {}'.format(condition_str)
        update_sql = '{};'.format(sql)
        result = self.execSql(update_sql)
        return result

class CdrcbDb(MySQLUtil, Singleton):
    pass


class BatchTestDb(MySQLUtil, Singleton):
    pass


class ProxyDb(MySQLUtil, Singleton):
    pass

class BatchDocIdDb(MySQLUtil, Singleton):
    pass

class KtggMysqlDb(MySQLUtil, Singleton):
    pass


if __name__ == '__main__':
    from ics.utils import get_ics_logger
    logger = get_ics_logger('test')
    mysql_db = KtggMysqlDb(default_settings.MYSQL_TASK_DATA_DB, logger)
    to_dict = {
        'state': 103,
        'success_cnt': 0,
        'duplicate_cnt': 0,
        'error_cnt': 0,
        'start_time':'2018-10-18:08:00:10',
    }
    condition_dict = {
        'ename':'guang_zhou_fa_yuan_ting_shen_zhi_bo_wang',
        'crawl_date':'2018-10-18',
    }
    tbl = 'tbl_ktgg_status'
    res = mysql_db.update_dict(tbl, to_dict)
    print res

