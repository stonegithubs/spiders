#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:task.py
description:
author:crazy_jacky
version: 1.0
date:2018/7/20
"""
import json
import traceback

from datetime import datetime

from ics.utils import get_ics_logger
from ics.task.fysx.mysql_pool import mysql_pool
from ics.task.fysx.task import insert_mysql

logger = get_ics_logger(__name__)


def get_connect():
    """
    ruturn db connect
    :return:
    """
    return mysql_pool.connection()


def parse():
    """
    parse source data
    :return:
    """
    dic_lst = turn2dic()
    for dic in dic_lst:
        for key in dic:
            if not isinstance(dic[key], str):
                dic[key] = str(dic[key])
        try:
            source = dic.pop('source', '{}')
            data_dic = json.loads(source)
            dic.update(data_dic)
            dic.pop('etl_status')
            etl_status = 'success'
            dic['qysler'] = str(dic['qysler'])
            dic['etl_time'] = str(datetime.now())[:19]
            insert_mysql('fysx_data', dic)
        except Exception as e:
            logger.warn('parse data {} failed:\n {}'.format(dic['source_id'], e))
            etl_status = 'failed'
        update_status(etl_status, dic['ics_id'])


def turn2dic():
    """
    turn db data into dict
    :return:
    """
    datas, keys = query_datas()
    key_lst = [item[0] for item in keys]
    dic_lst = [dict(zip(key_lst, each_data)) for each_data in datas]
    return dic_lst


def update_status(status, ics_id):
    """
    update etl status to source table
    :return:
    """
    conn = get_connect()
    cursor = conn.cursor()
    sql = 'UPDATE fysx SET etl_status="{}" WHERE ics_id="{}"'.format(status, ics_id)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception:
        conn.rollback()
        traceback.print_exc()
        raise RuntimeError('mysql error')
    conn.close()


def query_datas():
    """
    get data from database
    :return:
    """
    query_data_str = 'SELECT * FROM fysx WHERE etl_status="origin"'
    query_key_str = 'SHOW columns FROM fysx'
    conn = get_connect()
    cursor = conn.cursor()
    cursor.execute(query_data_str)
    datas = cursor.fetchall()
    cursor.execute(query_key_str)
    keys = cursor.fetchall()
    conn.close()
    return datas, keys



parse()
