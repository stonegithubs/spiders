#!/usr/bin/env python
# coding:utf-8

import os
import sys
import time
import base64
import requests
import traceback
from ics.captcha.common import BaseCrackPic
from ics.settings.default_settings import SAVE_CAPTCHA, BASE_DIR, APPKEY

from ics.utils import is_json
from ics.utils.exception.http_exception import requests_exception

reload(sys)
sys.setdefaultencoding('utf-8')


class JuheCaptcha(BaseCrackPic):
    def __init__(self, logger, yzm_dir='test'):
        self.logger = logger
        self.yzm_dir = yzm_dir

    headers = {
        'Referer': 'http://op.juhe.cn/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    service_url = 'http://op.juhe.cn/vercode/index'  # 接口地址

    def crack_captcha(self, im, codetype='1004'):
        if not im or 'html' in im:
            logger.error(u'图片content异常， {}'.format(im))
            return None
        base64_str = base64.b64encode(im)
        data = {
            'key': APPKEY,
            'codeType': codetype,
            'base64Str': base64_str,
            'dtype': 'json',
        }

        file_name = str(int(time.time() * 1000))
        result = {}
        max_cnt = 20
        while max_cnt:
            max_cnt -= 1
            try:
                session = requests.session()
                resp = session.post(url=self.service_url, data=data, headers=self.headers, timeout=60)
                if is_json(resp.content, self.logger):
                    result = resp.json()
                    if result['error_code'] != 0:
                        self.logger.info('JuHe captcha crack fail! result:{}'.format(result.get('result')))
                        return None, None
                    self.save_captcha(self.yzm_dir, result.get('result'), im, logger)
                    break
                self.logger.warn('JuHe captcha platform return wrong content {}'.format(resp.content))
            except requests_exception as e:
                self.save_captcha('{}_error'.format(self.yzm_dir), file_name, im, logger)
                self.logger.warn('JuHe get captcha code http failed:[{}], left {} times for retry'.format(e, max_cnt))
            except Exception as e:
                self.save_captcha('{}_error'.format(self.yzm_dir), file_name, im, logger)
                self.logger.error('JuHe get captcha code failed:[{}]'.format(e))
                return None, None
            if not max_cnt:
                self.logger.error('JuHe captcha crack failed!!!')
                return None, None
        self.logger.info(
            'captcha crack success! result:{},pic_id:{}'.format(result.get('result'), result.get('pic_id')))
        return result.get('result'), result.get('pic_id')

    def report_error(self, im, codetype=1902):
        return True

    def save_captcha(self, yzm_dir, code, content, logger=None):
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
            if logger:
                logger.error(u'保存图片异常:{}'.format(traceback.format_exc()))


if __name__ == '__main__':
    from ics.utils import get_ics_logger
    logger = get_ics_logger(__name__)
    ins = JuheCaptcha(logger, 'zhix')
    b64 = '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'
    pic_content = base64.b64decode(b64)
    res = ins.crack_captcha(pic_content)
    print res
