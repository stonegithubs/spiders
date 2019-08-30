#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:get_config.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/3
"""
import os
import ConfigParser


def read_config():
    """
    read and get specific file content
    :return:
    """
    curr_path = os.path.dirname(__file__)
    file_name = os.path.join(curr_path, 'config.ini')
    cfg = ConfigParser.RawConfigParser()
    cfg.read(file_name)
    res_dic = {}
    sections = cfg.sections()
    for sec in sections:
        lst = []
        dic = {}
        for key, val in cfg.items(sec):
            dic[key] = eval(val)
        lst.append(dic)
        res_dic[sec] = lst
    return res_dic


