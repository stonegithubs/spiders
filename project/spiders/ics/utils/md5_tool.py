#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import time

__author__ = 'wu_yong'


def to_md5(s):
    """
    将字符串转换成MD5
    :return:
    """
    return hashlib.md5(s).hexdigest()
