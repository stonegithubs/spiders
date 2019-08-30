#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import MySQLdb
from DBUtils.PooledDB import PooledDB

from ics.settings import default_settings


mysql_pool = PooledDB(MySQLdb,
                      8,
                      host=default_settings.MYSQL_HOST,
                      user=default_settings.MYSQL_USERNAME,
                      passwd=default_settings.MYSQL_PASSWORD,
                      db='gsxt_test',
                      charset='utf8',
                      port=default_settings.MYSQL_PORT)
