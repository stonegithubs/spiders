#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:spider_fysx.py
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
            abandon_proxy(m_ip, 'fysx')
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
        if not pic_cont and not max_cnt:
            break
        code, _ = cjy_captcha.crack_captcha(pic_cont, yzm_dir='fysx')
        if code:
            logger.info('get code success {}'.format(code))
            return code, captcha_id
    return None, None


def get_fysx_status(logger):
    session = requests.session()
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
    c_url = 'http://zxgk.court.gov.cn/shixin/captcha.do?captchaId={}'
    url = 'http://zxgk.court.gov.cn/shixin/findDis'
    req = ''
    code, captcha_id = update_captcha(c_url, headers, 'fysx', logger)
    if not code:
        msg = 'captcha code failed, please check captcha service'
        logger.info(msg)
        return False, msg
    params = {
        'pName': '张三',
        'pCardNum': '',
        'pProvince': '0',
        'pCode': code,
        'captchaId': captcha_id
    }
    max_cnt = 5
    while max_cnt:
        max_cnt -= 1
        m_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx', from_type='25mintest')
        params.update({'pCode': code,
                       'captchaId': captcha_id})
        try:
            req = session.post(url, data=params, headers=headers, proxies=m_proxy).content
            if u'查询结果' in req:
                break
            elif not max_cnt:
                msg = u'fysx spider search no record aboat 张三 over max retry times'
                logger.warn(msg)
                return False, msg
            else:
                code, captcha_id = update_captcha(c_url, headers, 'zhixing', logger)
                logger.info('fysx spider captcha code left {} time'.format(max_cnt))
        except Exception as e:
            logger.warn('fysx requests failed:{}'.format(e))
            if not max_cnt:
                return False, 'fysx max retries with search page:{},params:{}'.format(url, params)
            abandon_proxy(m_ip, 'fysx')
            m_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx', from_type='25mintest')
            code, captcha_id = update_captcha(c_url, headers, 'fysx', logger)
    id_lst = re.compile('\"View\"\s*id=\"(\w+)\"').findall(req)
    if not id_lst:
        return False, u'fysx spider search no record aboat 张三'
    else:
        test_id = id_lst[0]
        max_cnt = 10
        msg = ''
        m_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx', from_type='25mintest')
        while max_cnt:
            max_cnt -= 1
            url = 'http://zxgk.court.gov.cn/shixin/disDetail?id={}&pCode={}&captchaId={}'.format(
                test_id, code, captcha_id)
            try:
                cont = session.get(url, headers=headers, proxies=m_proxy, timeout=60).content
                dic = json.loads(cont)
            except Exception as e:
                logger.warn('fysx spider request detail failed:{}'.format(e))
                if not max_cnt:
                    return False, 'fysx spider request detail over max retry times:{}'.format(e)
                abandon_proxy(m_ip, 'fysx')
                m_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx', from_type='25mintest')
                continue
            if dic:
                msg = 'request specific url {} success'.format(url)
                logger.info(msg)
                return True, 'request specific url {} success\r\n result: {}'.format(url, cont)
            else:
                if not max_cnt:
                    msg = 'request specific url {} and get content empty, please check'.format(url)
                    logger.info(msg)
                    return False, msg
                m_ip, _, m_proxy = get_proxy_from_zm(black_type='fysx', from_type='25mintest')
                code, captcha_id = update_captcha(c_url, headers, 'fysx', logger)
        return False, msg
