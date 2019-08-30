#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:spider_monitor.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/5
"""
import os
import sys
import time
import traceback
import importlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

from ics.utils import get_ics_logger
from ics.utils.email.ics_email import Send_Email
from ics.utils.monitor.cfg.get_config import read_config

reload(sys)

sys.setdefaultencoding('utf-8')

logger = get_ics_logger(__name__)


def check_status(head, spider_lst):
    text = ''
    status_dic = {}
    for key in spider_lst:
        logger.info('begin to check spider:{}'.format(key))
        module = importlib.import_module('ics.utils.monitor.spider.spider_{}'.format(key))
        try:
            spider_status, msg = eval('module.get_{}_status(logger)'.format(key))
        except Exception as e:
            spider_status =False
            msg = 'spider {} run with exception:{}\n{}'.format(key, e, traceback.format_exc())
        status_dic[key] = spider_status
        if spider_status:
            text += u'{}{}运行：OK！\n{}\r\n\r\n'.format(head, key, msg)
        else:
            text += u'{}{}运行异常！！！\n{}\r\n\r\n'.format(head, key, msg)
    return status_dic, text


if __name__ == '__main__':
    cfg_dic = read_config()
    key = 'cdrcb'
    spider_cfg = cfg_dic[key][0]
    theme = key + '-' + spider_cfg.get('theme', u'冰鉴邮件服务通知')
    spider_lst = spider_cfg.get('spider_lst', [])
    check_fq = spider_cfg.get('check_fq')
    text_head = spider_cfg.get('text_head')
    status_dic, txt = check_status(text_head, spider_lst)
    data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    res_lst = []
    if not all(status_dic.values()):
        for key, val in status_dic.items():
            if val:
                theme += key + ':【OK】'
            else:
                theme += key + ':【NOK】'
        ss = Send_Email(theme)
        ss.send_mail(txt)
        logger.info('{} all spider run status not OK!!!'.format(data_time))
    else:
        logger.info('{} all spider run status OK!!!'.format(data_time))
