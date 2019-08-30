#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:spider_zhixing.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/3
"""
import re
import time
import json
import requests

from ics.utils.md5_tool import to_md5
from ics.proxy import get_proxy_from_zm, abandon_proxy
from ics.captcha.chaojiying.crack_captch import CjyCaptcha


def get_pic_content(url, header, black_type, logger):
    """
    get picture content by picture url
    :param url:
    :param header:
    :param black_type:
    :param logger:
    :return:
    """
    session = requests.session()
    max_cnt = 5
    while max_cnt:
        max_cnt -= 1
        m_ip, _, m_proxy = get_proxy_from_zm(black_type=black_type, from_type='25mintest')
        try:
            req = session.get(url, headers=header, proxies=m_proxy, timeout=30)
        except Exception as e:
            logger.warn('request image content failed {}'.format(e))
            abandon_proxy(m_ip, 'zhixing')
            continue
        pic_cont = req.content
        if 'PNG' in pic_cont:
            return pic_cont
    return None


def update_captcha(c_url, headers, black_type, logger):
    max_cnt = 3
    cjy_captcha = CjyCaptcha(logger)
    while max_cnt:
        max_cnt -= 1
        captcha_id = to_md5(str(time.time() * 1000))
        url = c_url.format(captcha_id)
        pic_cont = get_pic_content(url, headers, black_type, logger)
        if not pic_cont:
            return None, None
        code, _ = cjy_captcha.crack_captcha(pic_cont, yzm_dir='zhixing')
        if code:
            logger.info('get code success {}'.format(code))
            return code, captcha_id
    return None, None


def get_zhixing_status(logger):
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'zhixing.court.gov.cn',
        'Referer': 'http://zhixing.court.gov.cn/search',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }
    url = 'http://zhixing.court.gov.cn/search/newsearch'
    c_url = 'http://zhixing.court.gov.cn/search/captcha.do?captchaId={}'
    code, captcha_id = update_captcha(c_url, headers, 'zhixing', logger)
    if not code:
        msg = 'captcha code failed, please check captcha service'
        logger.info(msg)
        return False, msg
    m_ip, _, m_proxy = get_proxy_from_zm(black_type='zhixing', from_type='25mintest')
    data = {
        'currentPage': 1,
        'searchCourtName': u'全国法院（包含地方各级法院）',
        'selectCourtId': '',
        'selectCourtArrange': '1',
        'pname': '张三',
        'cardNum': '',
        'j_captcha': code,
        'captchaId': captcha_id
    }
    session = requests.session()
    req = ''
    max_cnt = 5
    while max_cnt:
        max_cnt -= 1
        data.update({'j_captcha': code,
                     'captchaId': captcha_id})
        try:
            req = session.post(url, data=data, headers=headers, proxies=m_proxy).content
            if u'查询结果' in req:
                break
            elif not max_cnt:
                msg = u'zhixing spider search no record aboat 张三 over max retry times'
                logger.warn(msg)
                return False, msg
            else:
                code, captcha_id = update_captcha(c_url, headers, 'zhixing', logger)
                logger.info('zhixing spider captcha code left {} time'.format(max_cnt))
        except Exception as e:
            logger.warn('zhixing requests failed:{}'.format(e))
            if not max_cnt:
                return False, 'fysx max retries with search page:{},params:{}'.format(url, data)
            abandon_proxy(m_ip, 'zhixing')
            m_ip, _, m_proxy = get_proxy_from_zm(black_type='zhixing', from_type='25mintest')
            code, captcha_id = update_captcha(c_url, headers, 'zhixing', logger)
    id_lst = re.compile('\"View\"\s*id=\"(\w+)\"').findall(req)
    if not id_lst:
        return False, u'zhixing spider search no record aboat 张三'
    else:
        test_id = id_lst[0]
        max_cnt = 5
        msg = ''
        while max_cnt:
            max_cnt -= 1
            url = 'http://zhixing.court.gov.cn/search/newdetail?id={}&j_captcha={}&captchaId={}'.format(
                test_id, code, captcha_id)
            try:
                cont = session.get(url, headers=headers, proxies=m_proxy, timeout=60).content
                dic = json.loads(cont)
            except Exception as e:
                logger.warn('zhixing spider request detail failed:{}'.format(e))
                if not max_cnt:
                    return False, 'zhixing spider max retries with request detail:{},params:{}'.format(url, e)
                abandon_proxy(m_ip, 'zhixing')
                continue
            if dic:
                msg = 'request specific url {} success:{}'.format(url, cont)
                logger.info(msg)
                return True, 'request specific url {} success\r\n result:{}'.format(url, cont)
            else:
                if not max_cnt:
                    msg = 'request specific url {} and get content empty, please check'.format(url)
                    logger.info(msg)
                    return False, msg
                m_ip, _, m_proxy = get_proxy_from_zm(black_type='zhixing', from_type='25mintest')
                code, captcha_id = update_captcha(c_url, headers, 'zhixing', logger)
        return False, msg
