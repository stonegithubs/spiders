#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import MySQLdb
from DBUtils.PooledDB import PooledDB

mysql_pool = PooledDB(MySQLdb, 8, host='192.168.2.2', user='zhangbo', passwd='ZXYyHI&^%$_@b', db='ent_sentiment',
                charset='utf8', port=3306)
