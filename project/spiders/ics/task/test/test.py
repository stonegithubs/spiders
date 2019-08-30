#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'


import requests
from urllib import quote
import random
import time

session = requests.session()

session.headers = {'Accept': 'application/json',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.9',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Referer': 'https://m.umu.cn/model/ssu_BWlQb4cb&mode=user_result?fwx=1&from=singlemessage&isappinstalled=0',
                   'Content-Type': 'application/x-www-form-urlencoded'}

cookies = {'Hm_lpvt_0dda0edb8e4fbece1e49e12fc49614dc': '1528103373',
           'Hm_lvt_0dda0edb8e4fbece1e49e12fc49614dc': '1526268974,1526279581,1528103373',
           'JSESSID': 'jj9bmcib6gbnrmls5o2054sf25',
           'umuU': '3aa2914a6b7d8638718d98ff2f84c73d'}

# m_proxy = {"http": "http://%s:%s" % ('127.0.0.1', 8888),
#            "https": "http://%s:%s" % ('127.0.0.1', 8888)}



for i in range(300):
    id = str(random.randint(1000000, 9999999))
    data = 'q=' + quote(
        '{\"answerList\": [\"52731564\", \"52731566\", \"52731567\"], \"answerInfo\": [{\"text\": \"\"}], \"answerNumber\": {},\"isAnonymous\": 0, \"enrollId\": 0, \"sessionId\": \"' + id + '\"}')
    time.sleep(0.7)
    print session.post('https://m.umu.cn/ajax/insertAnswer', data=data, cookies=cookies, verify=False).text


