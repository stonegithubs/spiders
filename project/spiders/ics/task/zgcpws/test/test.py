#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import execjs
import requests
from urllib import quote
from ics.utils.string_tool import abstract
from ics.proxy import get_proxy_for_phantom_test
import time

m_proxy = get_proxy_for_phantom_test()[2]


def create_guid():
    guid_js = "var createGuid=function(){return(((1+Math.random())*0x10000)|0).toString(16).substring(1);}"
    function = execjs.compile(guid_js)
    result_guid = function.call('createGuid')
    return result_guid


def guid_generator():
    return create_guid() + create_guid() + "-" + create_guid() + "-" + create_guid() + create_guid() + "-" + create_guid() + create_guid() + create_guid();


guid = guid_generator()

headers = dict()
headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
headers['Accept'] = '*/*'
headers['Accept-Encoding'] = 'gzip, deflate, sdch'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
headers['Referer'] = 'http://wenshu.court.gov.cn/'
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Origin'] = 'http://wenshu.court.gov.cn'
headers['X-Requested-With'] = 'XMLHttpRequest'

session = requests.session()

# from ics.utils.cookie import cookiejar_from_dict
# session.cookies = cookiejar_from_dict({
#     '_gscu_2116842793':'29994471u4kec313',
#     '_gscbrs_2116842793':'1',
#     '_gscs_2116842793':'29994471nehpog13|pv:1',
#     'Hm_lvt_3f1a54c5a86d62407544d433f6418ef5':'1529994472',
#     'Hm_lpvt_3f1a54c5a86d62407544d433f6418ef5':'1529994472'
# },'wenshu.court.gov.cn')

resHtml = session.post(
    url='http://wenshu.court.gov.cn/ValiCode/GetCode',
    headers=headers,
    data='guid=' + guid,
    proxies=m_proxy
).content
time.sleep(1)

print resHtml

number = resHtml

headers = dict()
headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
headers['Accept'] = '*/*'
headers['Accept-Encoding'] = 'gzip, deflate, sdch'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
headers['Referer'] = 'http://wenshu.court.gov.cn/'
headers['Origin'] = 'http://wenshu.court.gov.cn'
headers['X-Requested-With'] = 'XMLHttpRequest'

resHtml = session.post(
    url='http://wenshu.court.gov.cn/List/SaveSession',
    headers=headers,
    data='number={0}'.format(quote('山东富海实业股份有限公司')),
    proxies=m_proxy
).content
time.sleep(1)

print resHtml


url = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number={0}&guid={1}&conditions=searchWord+QWJS+++{2}:{3}'.format(
    number, guid, quote('全文检索'), quote('山东富海实业股份有限公司'))
refer = url

headers = dict()
headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
headers['Accept'] = '*/*'
headers['Accept-Encoding'] = 'gzip, deflate, sdch'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
headers['Referer'] = 'http://wenshu.court.gov.cn/'
headers['Origin'] = 'http://wenshu.court.gov.cn'

resHtml = session.get(
    url=url,
    headers=headers,
    proxies=m_proxy
).content
time.sleep(1)

print resHtml

vjkl5 = session.cookies.get('vjkl5')

with open('encrypt.js', 'r') as f:
    encrypt_js = f.read()

print encrypt_js
get_key_js = 'function getKey() {' + abstract(resHtml, 'function getKey() {', 'return result;').replace(
    'getCookie(\'vjkl5\')', '\'{0}\''.format(vjkl5)) + 'return result;}' + encrypt_js

print get_key_js

func = execjs.compile(get_key_js)
result = func.call('getKey')

print result

vl5x = result

guid = guid_generator()

headers = dict()
headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
headers['Accept'] = '*/*'
headers['Accept-Encoding'] = 'gzip, deflate, sdch'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
headers['Referer'] = refer
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Origin'] = 'http://wenshu.court.gov.cn'
headers['X-Requested-With'] = 'XMLHttpRequest'

resHtml = session.post(
    url='http://wenshu.court.gov.cn/ValiCode/GetCode',
    headers=headers,
    data='guid=' + guid,
    proxies=m_proxy
).content
time.sleep(1)

print resHtml

number = resHtml

headers = dict()
headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
headers['Accept'] = '*/*'
headers['Accept-Encoding'] = 'gzip, deflate, sdch'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
headers['Referer'] = refer
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Origin'] = 'http://wenshu.court.gov.cn'
headers['X-Requested-With'] = 'XMLHttpRequest'

resHtml = session.post(
    url='http://wenshu.court.gov.cn/List/ListContent',
    headers=headers,
    data='Param={0}&Index=1&Page=5&Order={1}&Direction=asc&vl5x={2}&number={3}&guid={4}'.format(
        quote('全文检索:山东富海实业股份有限公司'), quote('法院层级'), vl5x, number, guid),
    proxies=m_proxy
).content
time.sleep(1)

print resHtml

DocID = abstract(resHtml,'\\\"文书ID\\\":\\\"','\\\"')

print DocID

if DocID:
    url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={0}'.format(DocID)

    headers = dict()
    headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    headers['Accept'] = '*/*'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
    headers['Referer'] = 'http://wenshu.court.gov.cn/content/content?DocID={0}&KeyWord={1}'.format(DocID,quote('山东富海实业股份有限公司'))
    headers['X-Requested-With'] = 'XMLHttpRequest'

    resHtml = session.get(
        url=url,
        headers=headers,
        proxies=m_proxy
    ).content

    print resHtml
