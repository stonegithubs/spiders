#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:task.py
description:
author:crazy_jacky
version: 1.0
date:2018/7/5
"""
import re
import sys
import json
import time
import requests
import traceback

from uuid import uuid4
from urllib3.exceptions import HTTPError

from ics.scheduler import app
from ics.proxy import abandon_proxy
from ics.utils import get_ics_logger
from ics.utils.md5_tool import to_md5
from ics.utils.decorator import stable
from ics.proxy import get_proxy_from_zm
from ics.utils.string_tool import is_json
from ics.scheduler.new_task import StableTask
from ics.utils.decorator import http_exception
from ics.utils.cookie import cookiejar_from_dict
from ics.utils.task_util.cdrcb.task_util import *
from ics.utils.string_tool import string_2_datetime
from ics.utils.exception_util import LogicException
from ics.captcha.chaojiying.crack_captch import CjyCaptcha
import ics.settings.default_settings as setting

reload(sys)

sys.setdefaultencoding('utf-8')

logger = get_ics_logger(__name__)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'zxgk.court.gov.cn',
    'Origin': 'http://zxgk.court.gov.cn',
    'Referer': 'http://zxgk.court.gov.cn/index_new_form.do',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

code = None
captcha_id = None


def get_pic_content(url, header):
    """
    get picture content by picture url
    :param url:
    :param header:
    :return:
    """
    session = requests.session()
    _, _, m_proxy = get_proxy_from_zm(black_type='fysx')
    req = ''
    try:
        req = session.get(url, headers=header, proxies=m_proxy, timeout=30).content
    except Exception as e:
        logger.warn('get picture content failed:{}'.format(e))
    return req


def update_captcha():
    global code
    global captcha_id
    max_cnt = 8
    captcha = CjyCaptcha(logger)
    while max_cnt:
        max_cnt -= 1
        captcha_id = to_md5(str(time.time() * 1000))
        url = 'http://zxgk.court.gov.cn/shixin/captcha.do?captchaId=' + captcha_id
        pic_cont = get_pic_content(url, headers)
        if not pic_cont:
            continue
        code, report_id = captcha.crack_captcha(pic_cont, yzm_dir='fysx')
        if code:
            logger.info('get code success {}'.format(code))
            break


@app.task(bind=True, base=StableTask, default_retry_delay=5, max_retries=10,
          ignore_result=True)
@stable(LogicException, logger=logger, )
def start(self, seed_dic):
    global code
    global captcha_id
    self.error_callback = search_error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.SHIXIN_DATA_TABLE,
    }
    target_name = seed_dic.get('target_name', '')
    target_id = seed_dic.get('target_id', '')
    self.logger_meta['logger_meta'] = 'begin to request of company of {}'.format(target_name.encode('utf-8'))
    session = requests.session()
    url = 'http://zxgk.court.gov.cn/shixin/findDis'
    self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx')
    max_cnt = 8
    req = ''
    update_captcha()
    while max_cnt:
        max_cnt -= 1
        params = {
            'pName': target_name,
            'pCardNum': target_id,
            'pProvince': '0',
            'pCode': code,
            'captchaId': captcha_id
        }
        if not code and max_cnt:
            continue
        try:
            req = session.post(url, data=params, headers=headers, proxies=m_proxy, timeout=30).content
            if u'查询结果' in req:
                break
            if u'验证码已过期' in req:
                update_captcha()
                continue
            if u'网站当前访问量较大' in req:
                raise HTTPError('current ip :{} need to change now'.format(m_proxy))
        except http_exception as e:
            logger.warn('start failed:{}'.format(e))
            abandon_proxy(self.abandon_ip, 'fysx')
            self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx')
    if u'查询结果' not in req:
        raise LogicException('process_page over retry times then need decorator for retring')
    pages = int(''.join(re.compile('页\s*\d+/(\d+)').findall(req)).strip())
    cnt = int(''.join(re.compile('共(\d+)条').findall(req)).strip())
    if not cnt:
        logger.info('can not get any record of {}'.format(target_name))
        send_no_record(seed_dic, logger=logger, table_name=setting.SHIXIN_DATA_TABLE)
    else:
        cookie = requests.utils.dict_from_cookiejar(session.cookies)
        if pages > 1:
            for page in range(2, pages + 1):
                page_cnt = 10 if page < pages else min(10, cnt - (pages - 1) * 10)
                params.update({'currentPage': page})
                logger.info('send {} page to task of process_page'.format(page))
                app.send_task('ics.task.fysx.cdrcb.task.process_page', [seed_dic, params, page_cnt, cookie, url, cnt],
                              queue=setting.SHIXIN_NORMAL_TASK_QUEUE, proiority=2)
        id_lst = re.compile('\"View\"\s*id=\"(\w+)\"').findall(req)
        for each_id in id_lst:
            app.send_task('ics.task.fysx.cdrcb.task.process_detail', [seed_dic, each_id, cookie, cnt],
                          queue=setting.SHIXIN_NORMAL_TASK_QUEUE,
                          proiority=3)


@app.task(bind=True, base=StableTask, default_retry_delay=5, max_retries=10,
          ignore_result=True)
@stable(LogicException, logger=logger)
def process_page(self, seed_dic, params, page_cnt, cookie, url, cnt):
    global code
    global captcha_id
    self.error_callback = error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.SHIXIN_DATA_TABLE,
        'lose_cnt': page_cnt
    }
    self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx')
    if not code:
        update_captcha()
    session = requests.session()
    session.cookies = cookiejar_from_dict(cookie, domain='zxgk.court.gov.cn')
    max_cnt = 8
    req = ''
    while max_cnt:
        max_cnt -= 1
        params['pCode'] = code
        params['captchaId'] = captcha_id
        try:
            req = session.post(url, data=params, headers=headers, proxies=m_proxy, timeout=30).content
            if u'查询结果' in req:
                break
            if u'验证码已过期' in req:
                update_captcha()
                continue
            if u'网站当前访问量较大' in req:
                raise HTTPError('current ip :{} need to change now'.format(m_proxy))
        except http_exception as e:
            logger.warn('process_page failed:{}'.format(e))
            abandon_proxy(self.abandon_ip, 'fysx')
            self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx')
    if u'查询结果' not in req:
        raise LogicException('process_page over retry times then need decorator for retring:{}'.format(req))
    id_lst = re.compile('\"View\"\s*id=\"(\w+)\"').findall(req)
    for each_id in id_lst:
        app.send_task('ics.task.fysx.cdrcb.task.process_detail', [seed_dic, each_id, cookie, cnt],
                      queue=setting.SHIXIN_NORMAL_TASK_QUEUE,
                      proiority=3)


@app.task(bind=True, base=StableTask, default_retry_delay=5, max_retries=10,
          ignore_result=True)
@stable(LogicException, logger=logger)
def process_detail(self, seed_dic, each_id, cookie, cnt):
    global code
    global captcha_id
    self.error_callback = error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.SHIXIN_DATA_TABLE,
        'total_cnt': cnt,
        'lose_cnt': 1
    }
    self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx')
    if not code:
        update_captcha()
    session = requests.session()
    session.cookies = cookiejar_from_dict(cookie, domain='zxgk.court.gov.cn')
    max_cnt = 8
    cont = ''
    while max_cnt:
        max_cnt -= 1
        url = 'http://zxgk.court.gov.cn/shixin/disDetail?id={}&pCode={}&captchaId={}'.format(each_id, code, captcha_id)
        try:
            cont = session.get(url, headers=headers, proxies=m_proxy, timeout=30).content
            if is_json(cont, logger):
                break
            if u'网站当前访问量较大' in cont:
                raise HTTPError('current ip :{} need to change now'.format(m_proxy))
            if '{}' == cont.replace(' ', ''):
                logger.info('empty json string,重新打码')
                update_captcha()
        except http_exception as e:
            logger.warn('process_detail failed'.format(e))
            abandon_proxy(self.abandon_ip, 'fysx')
            self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx')
    if not is_json(cont, logger):
        raise LogicException('process_detail over retry times then need decorator for retring')
    try:
        result_dic = dict()
        result_dic.update(json.loads(cont))
        add_common_key(result_dic, seed_dic, total_cnt=cnt, source_id=str(uuid4()), status='success',
                       page_source=cont.decode('utf-8', "ignore"))
        result_dic['qysler'] = str(result_dic.get('qysler', ''))
        if 'publishDate' in result_dic:
            result_dic['publishDate'] = string_2_datetime(result_dic['publishDate'])
        if 'regDate' in result_dic:
            result_dic['regDate'] = string_2_datetime(result_dic['regDate'])
        result_dic['detail_id'] = result_dic.pop('id', '')
        insert_mysql(setting.SHIXIN_DATA_TABLE, result_dic, logger)
        check_result_and_send_msg(setting.SHIXIN_DATA_TABLE, cnt, seed_dic['task_id'], logger)
        logger.info('get detail content of {}'.format(result_dic.get('iname', '')))
    except Exception as e:
        err_dic = {}
        add_common_key(err_dic, seed_dic, err_msg=e, status=TASK_STATUS.FAILED)
        insert_mysql(setting.SHIXIN_DATA_TABLE, err_dic, logger)
        logger.warn('save data to mysql failed {} \n{}'.format(e, traceback.format_exc()))
        check_result_and_send_msg(setting.SHIXIN_DATA_TABLE, cnt, seed_dic['task_id'], logger, err_msg=e)
