# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用于定义企信网爬虫相关常亮和全局变量

"""
import time
from datetime import datetime



__author__ = 'wu_yong'


from ics.utils import get_ics_logger
from ics.http.http_downloader import Downloader, PROXY_STRATEGY

# from ics.http.downloader import Downloader, PROXY_STRATEGY


URL_PARAMS = 'draw=%s&start=%s&length=5'

GSXT_TASK_QUEUE = "task_queue"

RETRY_CNT = 5       # 重试次数

PROXY_TYPE = 'zm'

# PROXY_TYPE = 'test'
SPIDER_NAME = 'gsxt'


headers = {
    'Host': 'www.gsxt.gov.cn',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://www.gsxt.gov.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://www.gsxt.gov.cn/index.html',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}


logger = get_ics_logger(SPIDER_NAME)

downloader = Downloader(
    spider_no="gsxt",
    logger=logger,
    abandon_model='grey',
    grey_time=3,
    proxy_mode=PROXY_TYPE,
    proxy_strategy=PROXY_STRATEGY.CONTINUITY_USE
)



current_timestamp = lambda: int(time.time()*1000)  # 用于组装每个部分url的时间戳

current_datetime = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S')

image_uri_list = [
    '/image/map1.jepg',
    '/image/user1.jepg',
    '/image/marker1.jepg',
    '/image/circle1.jepg',
    '/image/icon2.jepg',
    '/image/icon3.jepg',
    '/image/icon4.jepg'
]

host = 'http://www.gsxt.gov.cn'

value_dict = {}  # 用于存储爬虫临时变量
page_dict = {}   # 用于存储网页


class Status(object):
    """
    爬虫抓取结果状态
    """
    SUCCESS = 0         # 成功
    EXCEPTION = 1       # 抓取异常
    NON_COMPANY = 2     # 无此公司， 网页搜索不到该公司


if __name__ == '__main__':
    pass