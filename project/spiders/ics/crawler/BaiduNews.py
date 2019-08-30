#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from urllib import quote
from bs4 import BeautifulSoup as bs
import json



class BaiduNews:
    def __init__(self):
        self.s = requests.session()
        self.encoding = "utf-8"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"}

    def fetch(self, keyword_string):
        result = []
        search_string = quote(keyword_string.encode(self.encoding))
        urls = ["http://news.baidu.com/ns?word={0}&pn={1}&cl=2&ct=1&tn=news&rn=20"
                "&ie=utf-8&bt=0&et=0".format(search_string, 20 * p) for p in range(1)]

        for url in urls:
            content = self.s.get(url=url).text
            list1 = bs(content,'lxml').select('div.result h3 a')
            for l in list1:
                result.append(l.text)

        return json.dumps(result).decode('unicode-escape')