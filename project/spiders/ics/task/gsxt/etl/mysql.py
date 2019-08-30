#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'HeZhen'

from ics.utils.mysql.mysqldb import MySQLUtil

class MySQLInit(MySQLUtil):


    def __init__(self):
        self.inited = False
        self.display = True
        self.init('rm-bp11towre3n815e78o.mysql.rds.aliyuncs.com', 'gouchao', 'Gouchao!2018', 'gsxt_test', 3306, min_connections=3)

    