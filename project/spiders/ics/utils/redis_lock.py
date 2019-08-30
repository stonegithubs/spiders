#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import time
import redis
from ics.utils.singleton import Singleton
from ics.settings import default_settings
import datetime


class RedisLock(Singleton):
    def __init__(self, key):
        self.rdcon = redis.Redis(host=default_settings.REDIS_HOST, port=default_settings.REDIS_PORT,
                                 password=default_settings.REDIS_PASSWORD, db=default_settings.REDIS_LOCK_DB)
        self._lock = 0
        self.lock_key = "%s_lock_key" % key

    @staticmethod
    def get_lock(cls, timeout=100):
        index = 0
        while cls._lock != 1:
            index += 1
            timestamp = time.time() + timeout + 1
            cls._lock = cls.rdcon.setnx(cls.lock_key, timestamp)

            # if cls._lock == 1:
            #     expire = timestamp
            #     expire_time = datetime.datetime.fromtimestamp(float(expire))
            #     cls.rdcon.expireat(cls.lock_key, expire_time)

            if cls._lock == 1:
                print "get lock"
                break
            elif cls._lock != 1 and index >= 100:
                print "timeout and break lock,wait to release lock"
                break
                # result = cls.rdcon.delete(cls.lock_key)
                # print "timeout and release lock,result:{}".format(result)
            else:
                print "wait to get lock"
                time.sleep(1)

    @staticmethod
    def release(cls):
        if time.time() < cls.rdcon.get(cls.lock_key):
            result = cls.rdcon.delete(cls.lock_key)
            print "release lock result:{}".format(result)
            cls._lock = 0


def redis_locker(cls):
    def _redis_locker(func):
        def __redis_locker(*args, **kwargs):
            # print "before %s called [%s]." % (func.__name__, cls)
            cls.get_lock(cls)
            try:
                return func(*args, **kwargs)
            finally:
                cls.release(cls)

        return __redis_locker

    return _redis_locker
