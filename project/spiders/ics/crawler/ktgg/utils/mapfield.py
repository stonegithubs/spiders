#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:mapfield.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/29
"""
field_dic = {
    u'法庭': 'court_room',
    u'开庭地点': 'court_room',
    u'开庭日期': 'court_date',
    u'开庭时间': 'court_date',
    u'案号': 'case_number',
    u'案由': 'case_cause',
    u'原告/上诉人': 'prosecutor',
    u'被告/被上诉人': 'defendant',
    u'审判长': 'chief_judge',
    u'承办人': 'undertake_person',
}


def map_field(dic):
    res = {}
    for key, val in dic.items():
        eng = field_dic.get(key, key)
        res[eng] = val
    return res
