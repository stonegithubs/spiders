# coding=utf-8
import os
import sys
import base64
import logging
import time
import traceback
import urlparse

import requests
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
from ics.settings.default_settings import JS_SERVER_AUTH_USERNAME, JS_SERVER_AUTH_PASSWORD, JS_SERVER_URL


def test_chrome_server():
    url = 'http://127.0.0.1:8888/execjs'
    test_js = """
    function myFunction(a)
    {
       return 10*a;
    }
    """
    js = "return myFunction(2)"+test_js

    js = open('js.txt').read()
    data = {
        'js': js
    }


    for i in range(100):
        s = time.time()
        # # res = requests.post('http://120.26.101.244:6666/execjs', data=data)
        # res = requests.post('http://47.99.51.210:6666/execjs', data=data)
        # # res = requests.post('http://127.0.0.1:8888/execjs', data=data)
        #

        base64string = base64.b64encode('{}:{}'.format(JS_SERVER_AUTH_USERNAME, JS_SERVER_AUTH_PASSWORD))
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': urlparse.urlparse(JS_SERVER_URL).hostname,
            'Authorization': "Basic {}".format(base64string),
        }
        data = {
            'js': js
        }
        url = 'http://47.99.51.210:6666/execjs'
        resp = requests.post(url=url, data=data, headers=headers, timeout=40)
        e = time.time()
        print (i, e-s, '==========>', resp.text)


# import sys
# sys.path.extend(['../', '../../', '../../../'])
#
# from ics.utils.exception_util import LogicException
# from ics.utils import get_ics_logger
#
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# CHROME_PATH = 'C:\\install\\chromedriver'
# CHROME_PATH = '/opt/google/chrome/chromedriver'
# logger = get_ics_logger('test_chrome')
#
# def get_driver():
#     start_time = time.time()
#     try:
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-gpu')
#         chrome_options.add_argument('user-agent= Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
#         chrome_options.add_argument('blink-settings=imagesEnabled=false')
#         driver = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=chrome_options)
#         end_time = time.time()
#         logger.debug('generate driver success cost time:{}'.format(end_time - start_time))
#         return driver
#     except Exception:
#         end_time = time.time()
#         logger.debug('generate driver error cost time:{}'.format(end_time - start_time))
#
#
# # def test_close_driver():
# #     CHROME_PATH = 'C:\\install\\chromedriver'
# #     from selenium.webdriver.chrome.service import Service
# #     c_service = Service(CHROME_PATH)
# #     # c_service.command_line_args()
# #     c_service.start()
# #     driver = webdriver.Chrome()
# #     driver.get("http://www.baidu.com")
# #     driver.quit()
# #     c_service.stop()
#
if __name__ == '__main__':
    test_chrome_server()
#     while True:
#         try:
#             web = get_driver()
#             logger.info('generate success, id: {}'.format(id(web)))
#             time.sleep(10)
#
#             web.quit()
#             logger.info('quit success')
#         except Exception as e:
#             logger.error(str(e))