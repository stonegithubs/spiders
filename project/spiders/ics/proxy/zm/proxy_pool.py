#!/usr/bin/env python
# -*- coding: utf-8 -*-
from MySQLdb import OperationalError

__author__ = 'MaoJingwen'
import requests
from retry import retry
import traceback
import time
from ics.settings import default_settings
from ics.utils.db.mysql_util import CdrcbDb
from ics.utils import get_ics_logger

logger = get_ics_logger('proxy_service')
mysql_db = CdrcbDb(default_settings.MYSQL_TASK_DATA_DB, logger)
mysql_pool = mysql_db.get_connect_pool()


def get_proxy_from_zm_base(database_proxy_num, api_num, from_type, black_type):
    '''
    获取代理ip
    :return:
    '''
    database_count = get_proxy_count_from_mysql(black_type)

    if database_count >= database_proxy_num:
        proxy_type = 'database'
    else:
        proxy_type = 'api'

    if proxy_type == 'api':
        proxy_list = get_zm_proxy(from_type, api_num, database_proxy_num, black_type)
        if isinstance(proxy_list, list):
            insert_proxy_list(proxy_list)
            return proxy_list[0]
        elif proxy_list == 'database':
            proxy_type = 'database'
        else:
            raise RuntimeError('no proxy in api !!!!')
    if proxy_type == 'database':
        proxy = get_proxy_from_mysql(black_type)
        return proxy


def get_zm_proxy(from_type, num, database_proxy_num, black_type):
    while True:
        if from_type == '3hour':
            proxy_url = default_settings.PROXY_3HOUR % str(
                num)
        elif from_type == '25min':
            proxy_url = default_settings.PROXY_25MIN % str(
                num)
        elif from_type == '25mintest':
            proxy_url = default_settings.PROXY_25MIN_TEST % str(
                num)
        session = requests.session()
        result = session.get(proxy_url)
        result = result.json()
        if result['code'] == 0:
            return result['data']
        elif result['code'] == 111:
            # {"code":111,"success":false,"msg":"请在1秒后再次请求","data":[]}

            database_count = get_proxy_count_from_mysql(black_type)

            if database_count >= database_proxy_num:
                return 'database'
            else:
                time.sleep(2)
                continue
        else:
            return None


@retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
def insert_proxy_list(proxy_list):
    db = None
    try:
        db = mysql_pool.connection()

        cursor = db.cursor()

        for model in proxy_list:
            qmarks = ', '.join(['%s'] * len(model))  # 用于替换记录值
            cols = ', '.join(model.keys())  # 字段名
            sql = "INSERT INTO tbl_proxy (%s) VALUES (%s)" % (cols, qmarks)
            cursor.execute(sql, model.values())

        sql = "UPDATE tbl_proxy SET used_count = used_count + 1 WHERE ip = \'%s\'" % (proxy_list[0]['ip'],)
        cursor.execute(sql)

        db.commit()
    except Exception:
        if db:
            db.rollback()
        traceback.print_exc()
        raise RuntimeError('mysql error')
    finally:
        if db:
            db.close()


@retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
def get_proxy_from_mysql(black_type):
    '''
    从数据库获取代理ip，至少5分钟可用时间
    :return:
    '''
    db = None
    try:
        db = mysql_pool.connection()
        cursor = db.cursor()
        sql = 'select * from tbl_proxy where expire_time>date_add(now(), interval 5 minute) and %s IS NULL ' % (
        black_type)

        if 'gsxt' in black_type:
            sql = sql + ' and (gsxt_gray_time is NULL or NOW()>date_add(gsxt_gray_time, interval 5 minute)) '

        sql = sql + 'order by used_count limit 1'

        cursor.execute(sql)
        data = cursor.fetchone()
        # <type 'tuple'>: (1L, u'49.68.68.197', datetime.datetime(2017, 6, 20, 20, 40, 24), u'\u5f90\u5dde\u5e02', u'\u7535\u4fe1', u'33220')

        sql = "UPDATE tbl_proxy SET used_count = used_count + 1 WHERE ip = \'%s\'" % (data[1],)
        cursor.execute(sql)

        db.commit()
    except Exception:
        if db:
            db.rollback()
        traceback.print_exc()
        raise RuntimeError('mysql error')
    finally:
        if db:
            db.close()

    proxy_dict = dict()
    proxy_dict['ip'] = data[1]
    proxy_dict['expire_time'] = data[2]
    proxy_dict['city'] = data[3]
    proxy_dict['isp'] = data[4]
    proxy_dict['port'] = data[5]
    return proxy_dict


@retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
def abandon_proxy(ip, name):
    db = None
    try:
        db = mysql_pool.connection()

        cursor = db.cursor()

        if 'zgcpws' in name:
            sql = "UPDATE tbl_proxy SET zgcpws = \'%s\' WHERE ip = \'%s\'" % ('black', ip)
        elif 'zhixing' in name:
            sql = "UPDATE tbl_proxy SET zhixing = \'%s\' WHERE ip = \'%s\'" % ('black', ip)
        elif 'fysx' in name:
            sql = "UPDATE tbl_proxy SET fysx = \'%s\' WHERE ip = \'%s\'" % ('black', ip)
        elif 'gsxt' in name:
            # sql = "UPDATE tbl_proxy SET gsxt = \'%s\' WHERE ip = \'%s\'" % ('black', ip)
            if ip_gsxt_status(ip):
                sql = "UPDATE tbl_proxy SET gsxt = \'%s\' WHERE ip = \'%s\'" % ('black', ip)
            else:
                sql = "UPDATE tbl_proxy SET gsxt_gray_time = %s WHERE ip = \'%s\'" % ('NOW()', ip)
        else:
            sql = "UPDATE tbl_proxy SET other = \'%s\' WHERE ip = \'%s\'" % ('black', ip)

        cursor.execute(sql)
        db.commit()
    except Exception:
        if db:
            db.rollback()
        traceback.print_exc()
        raise RuntimeError('mysql error')
    finally:
        if db:
            db.close()


@retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
def ip_gsxt_status(ip):
    db = None
    try:
        db = mysql_pool.connection()
        cursor = db.cursor()
        sql = "select gsxt_gray_time from tbl_proxy where ip= '%s'" % (ip)
        cursor.execute(sql)
        data = cursor.fetchone()
        if isinstance(data, tuple):
            return data[0]
        return data
    except Exception:
        if db:
            db.rollback()
        traceback.print_exc()
        raise RuntimeError('mysql error')
    finally:
        if db:
            db.close()


@retry(exceptions=(RuntimeError, OperationalError), tries=20, delay=1)
def get_proxy_count_from_mysql(black_type):
    '''
    从数据库获取代理ip数量，至少5分钟可用时间
    :return:
    '''
    db = None
    try:
        data = [0, ]
        db = mysql_pool.connection()
        cursor = db.cursor()
        sql = 'select count(*) from tbl_proxy where expire_time>date_add(now(), interval 5 minute) and %s IS NULL' % (
        black_type)
        if 'gsxt' in black_type:
            sql = sql + ' and (gsxt_gray_time is NULL or (now()>date_add(gsxt_gray_time, interval 5 minute))) '
        cursor.execute(sql)
        data = cursor.fetchone()
        return data[0]
    except Exception:
        traceback.print_exc()
        raise RuntimeError('mysql error')
    finally:
        if db:
            db.close()
