#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import redis

redis_pool = redis.ConnectionPool(host='192.168.2.2', password='ICK_Dev_2017', port=6379, decode_responses=True)
