#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'HeZhen'

import requests

import re
import time
import json

from ics.utils.string_tool import abstract
from ics.utils.chrome import get_chrome_web_driver
from ics.proxy import get_proxy_for_phantom_test

def get_session():
    from requests.adapters import HTTPAdapter
    session  = requests.session()
    request_retry = HTTPAdapter(max_retries=3)
    session.mount('https://', request_retry)
    session.mount('http://', request_retry)
    return session

def get_cookies_for_requests(ip, port, m_proxy):
    while True:
        session = get_session()

        # headers = dict()
        headers = {
            'Host': 'www.gsxt.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'http://www.gsxt.gov.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Upgrade-Insecure-Requests': '1'
        }

        resHtml = session.get(
            url='http://www.gsxt.gov.cn/index.html',
            headers=headers,
            proxies=m_proxy
        ).content

        resHtml = 'function getClearance(){{{0}}};'.format(resHtml)
        resHtml = resHtml.replace('</script>', '')
        resHtml = resHtml.replace('eval(y.replace(/\\b\w+\\b/g, function(y){return x[f(y,z)-1]||("_"+y)}));', 'var temp = y.replace(/\\b\w+\\b/g, function(y){return x[f(y,z)-1]||("_"+y)});eval(temp);return temp;')
        resHtml = resHtml.replace('<script>', '')
        resHtml = resHtml.replace(';break}catch', ';}catch')
        resHtml = resHtml.replace('\x00', '')
        js = resHtml + ';return getClearance();'
        data = {'js': js}
        _response = requests.post('http://120.26.101.244:6666/execjs', data=data)
        response = json.loads(_response.content)
        js = response.get("result")
        # web = get_chrome_web_driver(ip, port)
        # js = web.execute_script(resHtml+';return getClearance();')

        # func = execjs.compile(resHtml)
        # js = func.call('getClearance')

        if 'location.href=location.1+location.new' in js:
            pass
        elif 'setTimeout(\'location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\\\'\\\')\',1500);' in js:
            break
        else:
            print js
            time.sleep(2)


    js = js.replace(
        'setTimeout(\'location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\\\'\\\')\',1500);',
        'var window = [];')
    # js = js.replace('document.', 'return ').replace('\x00', '')

    func_name = re.match('var (_.*?)=', js).group(1)
    # second_vair = re.search('{var (_.*?)=', js).group(1)
    # third_vair = re.search('>(_.*?)<', js).group(1)
    #
    # replace_attr = "document.createElement('div');%s.innerHTML='<a href=\\'/\\'>%s</a>';%s=%s.firstChild.href;var %s=%s.match(/https?:\\/\\//)[0];%s=%s.substr(%s.length).toLowerCase()" % (
    #     func_name, third_vair, func_name, func_name, second_vair, func_name, func_name, func_name, second_vair)
    #
    # js = js.replace(replace_attr, "'www.gsxt.gov.cn'")

    # js = js.replace('return return(\'String.fromCharCode(\'+' + func_name + '+\')\')',
    #                 'return String.fromCharCode({0})'.format(func_name))

    js = js.replace('return return', 'return eval')
    js = js.replace('document.cookie', 'return cookie')
    js = 'var' + abstract(js,'var','if((function(){try')
    js = js + ('return {}();'.format(func_name))
    # js = re.sub('if.*', '', js)

    # func = execjs.compile(js)
    # result = func.call(func_name)
    # result = web.execute_script(js)

    data['js'] = js
    _response = requests.post('http://120.26.101.244:6666/execjs', data=data)
    response = json.loads(_response.content)
    result = response.get("result")
    cookie_dict = requests.utils.dict_from_cookiejar(session.cookies)
    name = result.split('=')[0]
    value = result.split('=')[1].split(';')[0]

    cookie_dict[name] = value
    return cookie_dict


ip, port, my_proxy = get_proxy_for_phantom_test()
get_cookies_for_requests(ip, port, my_proxy)