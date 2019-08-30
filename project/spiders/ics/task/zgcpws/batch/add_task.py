#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ics.utils import get_ics_logger
from ics.utils.db import BatchDocIdDb
from ics.settings import default_settings
from ics.scheduler import app

logger = get_ics_logger("cpws_doc_id")

mysql_db = BatchDocIdDb(default_settings.MYSQL_TASK_DATA_DB,logger=logger)

MAX_LIMIT = 100000

def iter_doc_id(status=0):
    i = 0
    LIMIT = 2000
    table_name = "cpws_doc_id"
    while LIMIT*i<MAX_LIMIT:
        sql = "select doc_id from {} where status={} limit {},{}".format(table_name, status, LIMIT * i, LIMIT)
        res = mysql_db.query(sql)
        if not res:
            break
        for data in res:
            doc_id = data[0]
            # app.send_task('ics.task.zgcpws.batch.task_app.start_with_doc_id', [doc_id], queue=default_settings.ZGCPWS_BATCH_NORMAL_TASK_QUEUE)
            app.send_task('ics.task.zgcpws.batch.task.get_doc_id', [doc_id], queue=default_settings.ZGCPWS_BATCH_NORMAL_TASK_QUEUE)
            print(doc_id)
        i += 1
        print LIMIT*i

iter_doc_id()