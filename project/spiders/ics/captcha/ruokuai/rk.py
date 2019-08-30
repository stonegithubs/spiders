#!/usr/bin/env python
# coding:utf-8

import sys
import hashlib
import requests
from ics.settings.default_settings import RK_USER, RK_PWD, RK_KEY, RK_SOFT_ID

reload(sys)
sys.setdefaultencoding('utf-8')


class RClient(object):
    """
    RK_USER:注册账户名
    RK_PWD:注册密码
    RK_SOFT_ID:用户ID，通讯加密用途
    RK_KEY:通讯加密用途
    my_logger:记录日志用途
    4位图片英数组合 3040
    """

    def __init__(self, my_logger):
        self.username = RK_USER
        self.password = hashlib.md5(RK_PWD).hexdigest()
        self.soft_id = RK_SOFT_ID
        self.soft_key = RK_KEY
        self.logger = my_logger
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type=3040, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        result = {}
        max_cnt = 10
        while max_cnt:
            max_cnt -= 1
            try:
                r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
                result = r.json()
                if type(result) == type(dict()):
                    break
            except Exception as e:
                self.logger.warn('RK get captcha code failed:[{}], left {} times for retry'.format(e, max_cnt))
        return result.get('pic_str')

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        max_cnt = 10
        result = {}
        while max_cnt:
            max_cnt -= 1
            try:
                r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
                result = r.json()
                if type(result) == type(dict()):
                    break
            except Exception as e:
                self.logger.warn(
                    ' report error captcha code failed:[{}], left {} times for retry'.format(e, max_cnt))
        return result.get('pic_str')


if __name__ == '__main__':
    rc = RClient('username', 'password', 'soft_id', 'soft_key')
    im = open('a.jpg', 'rb').read()
    print rc.rk_create(im, 3040)
