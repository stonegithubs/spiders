#!/usr/bin/env python
# coding:utf-8

from ics.settings.default_settings import CJY_USER, CJY_PWD, CJY_SOFT_ID, SAVE_CAPTCHA, BASE_DIR
from ics.utils.exception.http_exception import requests_exception
from ics.captcha.common import BaseCrackPic
from ics.utils import is_json
import hashlib
import requests
import traceback
import time
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')


class CjyCaptcha(BaseCrackPic):
    """
    CJY_USER:注册账户名
    CJY_PWD:注册密码
    CJY_SOFT_ID:用户ID，通讯加密用途
    my_logger:记录日志用途
    4位图片英数组合 1902
    """

    def __init__(self, my_logger):
        self._username = CJY_USER
        password = CJY_PWD.encode('utf8')
        self._password = hashlib.md5(password).hexdigest()
        self._soft_id = CJY_SOFT_ID
        self._logger = my_logger
        self._base_params = {
            'user': self._username,
            'pass2': self._password,
            'softid': self._soft_id,
        }
        self._headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def crack_captcha(self, im, codetype=1902, yzm_dir='test'):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        if not im or 'html' in im:
            self._logger.error(u'图片content异常， {}'.format(im))
            return None, None

        params = {
            'codetype': codetype,
        }
        params.update(self._base_params)
        file_name = str(int(time.time() * 1000))
        files = {'userfile': (file_name, im)}
        result = {}
        max_cnt = 20
        while max_cnt:
            max_cnt -= 1
            try:
                session = requests.session()
                r = session.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                                 headers=self._headers, timeout=60)
                if is_json(r.content, self._logger):
                    # {u'err_str': u'OK', u'err_no': 0, u'md5': u'58312b5ef5ed33d86b14464a6a13de39',
                    # u'pic_id': u'6039914371666600002', u'pic_str': u'x4qu'}
                    result = r.json()
                    if result['err_no'] != 0:
                        self._logger.info('CJY captcha crack fail! result:{}'.format(result.get('err_str')))
                        return None, None
                    break
                self._logger.warn('CJY captcha platform return wrong content {}'.format(r.content))
            except requests_exception as e:
                self._logger.warn('CJY get captcha code http failed:[{}], left {} times for retry'.format(e, max_cnt))
            except Exception as e:
                self._logger.error('CJY get captcha code failed:[{}]'.format(e))
                return None, None
            if not max_cnt:
                self._logger.error('CJY captcha crack failed!!!')
                return None, None
        self._logger.info(
            'captcha crack success! result:{},pic_id:{}'.format(result.get('pic_str'), result.get('pic_id')))
        self.save_captcha(yzm_dir, result.get('pic_str'), im)
        return result.get('pic_str'), result.get('pic_id')

    def report_error(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self._base_params)
        max_cnt = 20
        while max_cnt:
            max_cnt -= 1
            try:
                session = requests.session()
                r = session.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params,
                                 headers=self._headers, timeout=60)
                if is_json(r.content, self._logger):
                    # {u'err_str': u'OK', u'err_no': 0}
                    # {"err_no":-1012,"err_str":"无此图片ID"}
                    result = r.json()
                    if result['err_no'] != 0:
                        self._logger.warn('CJY captcha platform return false {}'.format(result['err_str']))
                        return False
                    break
                self._logger.warn('CJY captcha platform return wrong content {}'.format(r.content))
            except requests_exception as e:
                self._logger.warn('CJY get captcha code http failed:[{}], left {} times for retry'.format(e, max_cnt))
            except Exception as e:
                self._logger.error('CJY report error captcha code failed:[{}]'.format(e))
                return False
            if not max_cnt:
                self._logger.error('CJY report error captcha code failed!!!')
                return False
        self._logger.info('captcha report error success,pic_id:{}'.format(im_id))
        return True

    def save_captcha(self, yzm_dir, code, content):
        try:
            if SAVE_CAPTCHA:
                YZM_DIR = os.path.join(BASE_DIR, 'images', yzm_dir)
                if not os.path.exists(YZM_DIR):
                    os.makedirs(YZM_DIR)

                img_name = os.path.join(YZM_DIR, '{}.png'.format(code))
                with open(img_name, 'wb') as f:
                    f.write(content)
                    f.flush()
        except Exception:
            if self._logger:
                self._logger.error(u'保存图片异常:{}'.format(traceback.format_exc()))


if __name__ == '__main__':
    from ics.utils import get_ics_logger

    logger = get_ics_logger(__name__)
    chaojiying = CjyCaptcha(logger)
    # im = requests.get(
    #     'http://zhixing.court.gov.cn/search/captcha.do?captchaId=cf9109f99f874a5eb983c16377e113a6').content
    # print chaojiying.crack_captcha(im, 1902)
    chaojiying.report_error('1324')
