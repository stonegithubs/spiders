#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'
import random

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ics.utils.cookie import formart_selenium_cookies, cookiejar_from_dict
import requests
import time
import json
from urllib import quote
from bs4 import BeautifulSoup as bs

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 10
dcap["phantomjs.page.settings.loadImages"] = True
dcap[
    "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

# from ics.proxy import get_proxy

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

web.execute_script('window[\'temp_callPhantom\'] = window[\'callPhantom\'];')
web.execute_script('window[\'callPhantom\'] = undefined;')

web.get('http://www.gsxt.gov.cn/index.html')

web.execute_script('window[\'callPhantom\'] = window[\'temp_callPhantom\'];')

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

print resHtml
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

headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Referer'] = 'http://www.gsxt.gov.cn/index.html'

token = str(random.randint(100000000, 999999999))
resHtml = session.post(
    headers=headers,
    url='http://www.gsxt.gov.cn/corp-query-search-1.html',
    data='tab=ent_tab&province=&geetest_challenge={0}&geetest_validate={1}&geetest_seccode={1}%7Cjordan&token={2}&searchword={3}'
        .format(captcha_result['challenge'], captcha_result['validate'], token, quote('上海冰鉴信息科技有限公司')),
    proxies=m_proxy
).content

soup = bs(resHtml, 'lxml')
url = 'http://www.gsxt.gov.cn' + soup.select('a.search_list_item.db')[0]['href']
refer = url
headers['Referer'] = 'http://www.gsxt.gov.cn/corp-query-search-1.html'
headers.pop('Content-Type')

web.get(url)
resHtml = web.execute_script("return document.documentElement.outerHTML")
time.sleep(3)
# resHtml = session.get(
#     headers=headers,
#     url=url,
#     proxies=m_proxy
# ).content

soup = bs(resHtml, 'lxml')

list_s = soup.select('div.mainContent script')

sc = soup.select('div.mainContent script')[0].text.strip()

sc = '{' + sc.replace('var ', '\'').replace(' ', '').replace('=\"', '\':\'').replace('%7D\"', '%7D\',').replace(';',
                                                                                                                '').replace(
    '\"', '\',').strip(',') + '}'

url_list = eval(sc)

# for url in url_list.itervalues():
#     url = 'http://www.gsxt.gov.cn' + url  # shareholderUrl
#     print url
#     web.get(url)
#     time.sleep(1)
#     resHtml = bs(web.execute_script("return document.documentElement.outerHTML")).text
#     print resHtml

url = 'http://www.gsxt.gov.cn' + url_list['alterInfoUrl']  # shareholderUrl

print url

web.get(url)

resHtml = web.execute_script("return document.documentElement.outerHTML")
print bs(resHtml, 'lxml').text

# resHtml = session.get(
#     url='http://www.gsxt.gov.cn/SearchItemCaptcha?t=%s' % str(int(round(time.time() * 1000))),
#     headers=headers,
#     proxies=m_proxy
# ).content
#
# print resHtml
#
# headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
# headers['X-Requested-With'] = 'XMLHttpRequest'
# headers['Referer'] = refer
# headers['Origin'] = 'http://www.gsxt.gov.cn'
#
# # headers.pop('Content-Type')
# # headers.pop('X-Requested-With')
# # headers.pop('Referer')
#
# time.sleep(3)
# resHtml = session.post(
#     headers=headers,
#     url=url,
#     data='draw=1&start=0&length=5',
#     proxies=m_proxy
# ).content
#
# print resHtml

# {
# 	"cacheKey" : "0_5",
# 	"currentPage" : 0,
# 	"data" : [{
# 			"abntime" : 1499414528000,
# 			"decOrg_CN" : "中国（上海）自由贸易试验区市场监督管理局",
# 			"reDecOrg_CN" : "上海市浦东新区市场监督管理局",
# 			"remDate" : 1501123948000,
# 			"remExcpRes_CN" : "列入经营异常名录3年内且依照《经营异常名录管理办法》第六条规定被列入经营异常名录的企业，可以在补报未报年份的年度报告并公示后，申请移出",
# 			"speCause_CN" : "未依照《企业信息公示暂行条例》第八条规定的期限公示年度报告的"
# 		}
# 	],
# 	"draw" : 1,
# 	"error" : "",
# 	"perPage" : 5,
# 	"recordsFiltered" : 1,
# 	"recordsTotal" : 1,
# 	"start" : 0,
# 	"totalPage" : 1
# }

# callPhantom
