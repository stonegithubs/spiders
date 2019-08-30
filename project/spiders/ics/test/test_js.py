#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from ics.utils.chrome import get_chrome_web_driver
from ics.proxy import get_proxy_for_phantom_test
import execjs
import requests

driver = get_chrome_web_driver()

with open('encrypt.js', 'r') as f:
    encrypt_js = f.read()

result=driver.execute_script(encrypt_js)
name = result.split('=')[0]
value = result.split('=')[1].split(';')[0]
print(result)

def get_session():
    from requests.adapters import HTTPAdapter
    session  = requests.session()
    request_retry = HTTPAdapter(max_retries=3)
    session.mount('https://', request_retry)
    session.mount('http://', request_retry)
    return session

# func = execjs.compile(encrypt_js)
# result = func.call('a')
