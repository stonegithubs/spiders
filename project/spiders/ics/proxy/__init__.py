#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'
import requests
import json
import random
from ics.proxy.zm.proxy_pool import get_proxy_from_zm_base
from ics.proxy.zm.proxy_pool import abandon_proxy

abandon_proxy = abandon_proxy


def get_proxy_from_zm(database_proxy_num=3, api_num=3, from_type='25min', black_type='other'):
    '''
    获取代理
    :param database_proxy_num: 数据库中代理阈值，默认3
    :param api_num: 每次从api取代理的数量，默认3
    :param from_type: 25分钟有效期；3小时有效期；25min;3hour
    :param black_type: 黑名单类型，zgcpws/zhixing/fysx/other
    :return:
    '''
    proxy = get_proxy_from_zm_base(database_proxy_num, api_num, from_type, black_type)
    if not proxy:
        return None, None, None
    else:
        ip = proxy['ip']
        port = proxy['port']
        m_proxy = {"http": "http://%s:%s" % (ip, port),
                   "https": "http://%s:%s" % (ip, port)}
        return ip, port, m_proxy


def get_proxy():
    result = requests.session().get('http://proxy.icekredit.com/api/v2/proxy/adsl')
    result_dict = json.loads(result.text)
    if result_dict['msg'] == 'ok':
        proxy = random.sample(result_dict['data']['proxy_list'], 1)[0]
        ip = proxy.split(':')[0]
        port = proxy.split(':')[1]

        m_proxy = {"http": "http://%s:%s" % (ip, port),
                   "https": "http://%s:%s" % (ip, port)}
        return m_proxy
    else:
        return None


def get_proxy_for_phantom():
    result = requests.session().get('http://proxy.icekredit.com/api/v2/proxy/adsl')
    result_dict = json.loads(result.text)
    if result_dict['msg'] == 'ok':
        proxy = random.sample(result_dict['data']['proxy_list'], 1)[0]
        ip = proxy.split(':')[0]
        port = proxy.split(':')[1]
        m_proxy = {"http": "http://%s:%s" % (ip, port),
                   "https": "http://%s:%s" % (ip, port)}
        return ip, port, m_proxy
    else:
        return None, None, None


def get_proxy_for_phantom_test():
    ip = '127.0.0.1'
    port = '8888'
    m_proxy = {"http": "http://%s:%s" % (ip, port),
               "https": "http://%s:%s" % (ip, port)}
    return ip, port, m_proxy


def get_fidder_proxy():
    ip = '127.0.0.1'
    port = '8888'
    m_proxy = {"http": "http://%s:%s" % (ip, port),
               "https": "http://%s:%s" % (ip, port)}
    return ip, port, m_proxy
