# coding=utf-8


__author__ = 'wu_yong'

import base64
import json
import time
import urlparse
import requests

from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException
from ics.settings.default_settings import JS_SERVER_AUTH_USERNAME, JS_SERVER_URL, JS_SERVER_AUTH_PASSWORD


def excute_js(js, logger):
    total_cnt = 3
    index = 0
    result = ''
    while index < total_cnt:
        try:
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
            resp = requests.post(url=JS_SERVER_URL, data=data, headers=headers, timeout=40)
            status_code = resp.status_code
            res_json = json.loads(resp.text)
            if status_code == 401:
                logger.info(u'破解js服务，用户名密码错误')
                break
            if status_code >= 400:
                err_msg = u'破解js服务响应状态码错误: {}'.format(status_code)
                logger.error(err_msg)
                raise LogicException(err_msg)

            resp_msg = res_json.get('msg', '')
            if res_json.get('status') != 0:
                logger.error(resp_msg)
                raise LogicException(resp_msg)
            logger.info(u'调用js服务破解js成功')
            result = res_json['result']
            break

        except Exception as e:
            logger.error(u'破解js异常,第{}次，原因:{}'.format(index+1, str(e)))
        index += 1
        time.sleep(2)
    return result


if __name__ == '__main__':
    test_js = """
        function myFunction(a)
        {
           return 10*a;
        }
        """
    js = "return myFunction(2)"+test_js
    logger = get_ics_logger('test_server_client')
    # js = open('js.txt').read()
    for i in range(100):
        res = excute_js(js, logger)
        print 'res',  res
