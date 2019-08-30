#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:crack_captch.py
description:
author:crazy_jacky
version: 1.0
date:2018/8/8
"""
import sys
import hashlib
import requests

from ics.utils import is_json
from ics.captcha.common import BaseCrackPic
from ics.utils.exception.http_exception import requests_exception
from ics.settings.default_settings import RK_USER, RK_PWD, RK_KEY, RK_SOFT_ID

reload(sys)
sys.setdefaultencoding('utf-8')


class RkCaptcha(BaseCrackPic):
    """
    RK_USER:注册账户名
    RK_PWD:注册密码
    RK_SOFT_ID:用户ID
    RK_KEY:通讯加密用途
    my_logger:记录日志用途
    4位图片英数组合 3040
    """

    def __init__(self, my_logger):
        self._username = RK_USER
        password = RK_PWD.encode('utf8')
        self._password = hashlib.md5(password).hexdigest()
        self._soft_id = RK_SOFT_ID
        self._soft_key = RK_KEY
        self._logger = my_logger
        self.base_params = {
            'username': self._username,
            'password': self._password,
            'softid': self._soft_id,
            'softkey': self._soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def crack_captcha(self, im, im_type=3040, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型 参考 http://www.ruokuai.com/home/pricetype
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        max_cnt = 20
        while max_cnt:
            max_cnt -= 1
            try:
                session = requests.session()
                r = session.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
                if is_json(r.content, self._logger):
                    result = r.json()
                    # {"Result":"答题结果","Id":"题目Id(报错使用)"}
                    if 'Result' in result:
                        self._logger.info('RK captcha crack success! result:{}, Id:{}'.format(result.get('Result'),
                                                                                              result.get('Id')))
                        return result.get('Result'), result.get('Id')
                    else:
                        self._logger.info('RK captcha crack fail! Error:{}, Error_Code:{}'.format(result.get('Error'),
                                                                                                  result.get(
                                                                                                      'Error_Code')))
                        return None, None
            except requests_exception as e:
                self._logger.warn('RK get captcha code http failed:[{}], left {} times for retry'.format(e, max_cnt))
            except Exception as e:
                self._logger.error('RK get captcha code failed:[{}]'.format(e))
                return None, None
            if not max_cnt:
                self._logger.error('RK captcha crack failed!!!')
                return None, None

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        max_cnt = 20
        while max_cnt:
            max_cnt -= 1
            try:
                session = requests.session()
                r = session.post('http://api.ruokuai.com/reporterror.json', data=params,
                                 headers=self.headers, timeout=60)
                if is_json(r.content, self._logger):
                    result = r.json()
                    # {"Result":"报错成功/报错成功2"}
                    # {"Error":"错误提示信息","Error_Code":"错误代码（详情见错误代码表）","Request":""}
                    if 'Result' in result:
                        self._logger.warn('RK captcha platform report error success {}'.format(result['Result']))
                        return True
                    else:
                        self._logger.warn('RK captcha platform report error failed Error:{}，Error_Code{}'.format(
                            result['Error'], result['Error_Code']))
            except requests_exception as e:
                self._logger.warn('RK get captcha code http failed:[{}], left {} times for retry'.format(e, max_cnt))
            except Exception as e:
                self._logger.error('RK report error captcha code failed:[{}]'.format(e))
                return False
            if not max_cnt:
                self._logger.error('RK report error captcha code failed!!!')
                return False
