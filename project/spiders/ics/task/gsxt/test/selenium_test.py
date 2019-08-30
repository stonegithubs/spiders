#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'
import random

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ics.utils.cookie import formart_selenium_cookies,cookiejar_from_dict
import requests
import time
import json
from urllib import quote

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 10
dcap["phantomjs.page.settings.loadImages"] = True
dcap[
    "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

# from ics.proxy import get_proxy
#
# m_proxy = get_proxy()
#
# print m_proxy['http'].replace('http://','')
#
# PHANTOMJS_SERVICE = [
#     '--proxy=%s' % m_proxy['http'].replace('http://',''),
#     '--proxy-type=http',
#     # '--proxy-auth=username:password'
# ]

PHANTOMJS_SERVICE = [
    '--proxy=localhost:8888',
    '--proxy-type=http',
    # '--proxy-auth=username:password'
]

PHANTOMJS_PATH = 'E:/Python27/phantomjs.exe'

web = webdriver.PhantomJS(service_args=PHANTOMJS_SERVICE, executable_path=PHANTOMJS_PATH, desired_capabilities=dcap)

web.get('http://www.gsxt.gov.cn/index.html')

time.sleep(10)

cookies = formart_selenium_cookies(web.get_cookies())

##############################################################################

m_proxy = {"http": "http://%s:%s" % ('127.0.0.1', '8888'),
           "https": "http://%s:%s" % ('127.0.0.1', '8888')}

session = requests.session()

headers = dict()
headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate, sdch'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
headers['Referer'] = 'http://www.gsxt.gov.cn/'
headers['X-Requested-With'] = 'XMLHttpRequest'

session.cookies = cookiejar_from_dict(cookies, 'www.gsxt.gov.cn')
resHtml = session.get(
    url='http://www.gsxt.gov.cn/SearchItemCaptcha?t=%s' % str(int(round(time.time() * 1000))),
    headers=headers,
    proxies=m_proxy
).content

captcha_sign = json.loads(resHtml)

challenge = captcha_sign['challenge']
gt = captcha_sign['gt']

if captcha_sign['success'] == 0:
    model = '4'
elif captcha_sign['success'] == 1:
    model = '3'
else:
    print captcha_sign['success']

session_captcha = requests.session()
url = 'http://jiyanapi.c2567.com/shibie'

captcha_result = session_captcha.post(url=url, json={
    'user': 'darksand',
    'pass': 'dElete2400',
    'gt': gt,
    'challenge': challenge,
    'referer': 'http://www.gsxt.gov.cn',
    'return': 'json',
    'model': model
}, proxies=m_proxy).content

time.sleep(2)

captcha_result = json.loads(captcha_result)

headers.pop('X-Requested-With')
headers['Content-Type'] = 'application/x-www-form-urlencoded'
headers['Referer'] = 'http://www.gsxt.gov.cn/index.html'


token = str(random.randint(100000000, 999999999))
resHtml = session.post(
    headers=headers,
    url='http://www.gsxt.gov.cn/corp-query-search-1.html',
    data='tab=ent_tab&province=&geetest_challenge={0}&geetest_validate={1}&geetest_seccode={1}%7Cjordan&token={2}&searchword={3}'
        .format(captcha_result['challenge'], captcha_result['validate'], token, quote('冰鉴')),
    proxies=m_proxy
).content

print resHtml

time.sleep(60)

headers.pop('Content-Type')
headers['Referer'] = 'http://www.gsxt.gov.cn/corp-query-search-1.html'
headers['X-Requested-With'] = 'XMLHttpRequest'
url = 'http://www.gsxt.gov.cn/corp-query-search-advancetest.html?geetest_seccode={0}%7Cjordan&tab=ent_tab&province=&geetest_validate={0}&searchword={1}&geetest_challenge={2}&token={3}&page=2'.format(
    captcha_result['validate'], quote('冰鉴'), captcha_result['challenge'], token
)

resHtml = session.post(
    headers=headers,
    url=url,
    proxies=m_proxy
).content

print resHtml

time.sleep(60)

url = 'http://www.gsxt.gov.cn/corp-query-search-advancetest.html?geetest_seccode={0}%7Cjordan&tab=ent_tab&province=&geetest_validate={0}&searchword={1}&geetest_challenge={2}&token={3}&page=3'.format(
    captcha_result['validate'], quote('冰鉴'), captcha_result['challenge'], token
)

resHtml = session.post(
    headers=headers,
    url=url,
    proxies=m_proxy
).content

print resHtml
