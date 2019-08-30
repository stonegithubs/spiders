#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:proxy_check.py
description:
author:crazy_jacky
version: 1.0
date:2018/8/27
"""
import os
import sys
import json
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)
from ics.utils import get_ics_logger
from ics.utils.email.ics_email import Send_Email
from ics.utils.monitor.cfg.get_config import read_config


logger = get_ics_logger(__name__)


def get_proxy_cnt(proxy_url):
    """
    get count of proxies that can use
    :param proxy_url:
    :return:
    """
    cont = ''
    try:
        logger.info('begin to check left proxies')
        session = requests.session()
        cont = session.get(proxy_url).content
        dic = json.loads(cont).get('data', {})
        total_cnt = dic.get('package_balance')
        return True, total_cnt
    except Exception as e:
        msg = 'check left proxies cause excption: {}\n proxy_url content is:【{}】'.format(e, cont)
        return False, msg


if __name__ == '__main__':
    send = Send_Email(u'代理余量')
    cfg = read_config()
    proxy_url = cfg['proxy'][0]['proxy_url']
    proxy_warn_cnt = cfg['proxy'][0]['proxy_warn_cnt']
    status, txt = get_proxy_cnt(proxy_url)
    if status:
        if txt is None:
            send = Send_Email(u'代理余量-None')
            send.send_mail(u'从代理接口{}获取代理数据异常'.format(proxy_url))
        elif int(txt) <= proxy_warn_cnt:
            send = Send_Email(u'代理余量低于阈值{}'.format(proxy_warn_cnt))
            send.send_mail(u'当前代理余量为：{}'.format(txt))
        else:
            pass
    else:
        send = Send_Email(u'获取代理异常')
        logger.warn()
        send.send_mail(u'异常原因如下：\n'.format(txt))
