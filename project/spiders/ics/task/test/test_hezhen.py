#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'HeZhen'

import time
import  sys
import csv
from ics.utils.db.mysql_util import MySQLUtil
from ics.utils import get_ics_logger
from ics.task.gsxt.cdrcb.mysql_pool import mysql_pool

logger = get_ics_logger(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')

dao = MySQLUtil("gsxt_test", logger)

error = ['安徽洽洽食品有限公司']
with open("C:/Users/Administrator/Desktop/2.txt") as f :
    for line in f :
        # print line.decode("utf8").strip()
        company_key = line.strip()
        if company_key in error:
            continue
        #company_key = '荣成泰祥食品股份有限公司'
        sql = "select source_id from gsxt_page_json where (company_name='{}' or company_key='{}') and create_time>'2018-09-04 11:55:4' and status=0 order by create_time desc limit 1".format(company_key, company_key)
        res = dao.query(sql)
        with open("C:/Users/Administrator/Desktop/res.csv", 'ab+') as  t:
            print line.decode("utf8").strip(), res
            temp = [company_key, res[0][0]]
            writer = csv.writer(t)
            writer.writerow(temp)
            t.close()