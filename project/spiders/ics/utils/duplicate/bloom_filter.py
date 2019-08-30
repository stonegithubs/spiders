#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file_name:bloom_filter.py
description:
author:crazy_jacky
version: 1.0
date:2018/7/5
"""
import md5
import sys
import redis
from ics.utils.redis_lock import redis_locker, RedisLock
from ics.settings import default_settings

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, host=default_settings.REDIS_HOST, port=default_settings.REDIS_PORT,
                 password=default_settings.REDIS_PASSWORD, db=default_settings.REDIS_BLOOM_FILTER_DB, block_num=1, key='bloomfilter'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param block_num: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.server = redis.Redis(host=host, password=password, port=port, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = block_num
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def is_contains(self, str_input):
        if not str_input:
            return False
        m5 = md5.new()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return bool(ret)

    def insert(self, str_input):
        m5 = md5.new()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)

    @redis_locker(RedisLock('bloom_filter'))
    def dup_filter(self, str_input):
        result = self.is_contains(str_input)
        if not result:
            self.insert(str_input)
        return result


if __name__ == '__main__':
    bf1 = BloomFilter(key='test1')
    bf1.insert('www.baidu.com')
    bf1.is_contains('www.baidu.com')
