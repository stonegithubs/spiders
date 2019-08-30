#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'wu_yong'


import json
from ics.utils.exception_util import LogicException


def zhixing_parse(source, logger):
    """
       source_json = {
        "id": 26545187, "caseCode": "（2018）沪0117执3987号", "caseState": "0", "execCourtName": "上海市松江区人民法院",
        "execMoney": 420000, "partyCardNum": "31022719691****3024", "pname": "张三妹", "gistId": "(2017)沪0117民初21595号",
        "sexname": "女性", "caseCreateTime": "2018年07月02日"
        }
    """
    try:
        source_json = json.loads(source)
        source_json['detail_id'] = source_json['id']
        source_json.pop('id', '')
        return source_json
    except Exception as e:
        err_msg = u'解析数据出错: {}, 原因: {}'.format(source, str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


