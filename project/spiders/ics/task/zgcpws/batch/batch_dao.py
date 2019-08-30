#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from ics.utils import get_ics_logger
from ics.utils.db import BatchDocIdDb
from ics.settings import default_settings

logger = get_ics_logger("cpws_doc_id")

TABLE_NAME = 'cpws_batch_02'
mysql_db = BatchDocIdDb(default_settings.MYSQL_TASK_DATA_DB, logger=logger)


def update_status(doc_id, logger=None):
    sql = "update cpws_doc_id set status=1 where doc_id='{}'".format(doc_id.strip())
    mysql_db.execSql(sql)
    if logger:
        logger.info("update doc_id:{} status is success".format(doc_id))


def add_key(doc_id, source='',err_msg='null',  status=0):
    result_dic = dict()
    result_dic[u"source"] = source
    result_dic[u"status"] = status
    result_dic[u"doc_id"] = doc_id
    result_dic[u"crawl_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_dic[u"error_msg"] = err_msg
    return result_dic


def save_data(result_dic, logger=None):
    mysql_db.insert_dic(TABLE_NAME, result_dic)
