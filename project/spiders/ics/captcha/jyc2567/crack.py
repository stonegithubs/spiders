#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

import json
import requests
import time



def jiyan_validate(challenge_html, logger):
    logger.info(u'开始打码')
    captcha_sign = json.loads(challenge_html)
    challenge = captcha_sign['challenge']
    gt = captcha_sign['gt']
    if captcha_sign['success'] == 0:
        model = '4'
    elif captcha_sign['success'] == 1:
        model = '3'
    else:
        logger.info(captcha_sign['success'])
        model = ''
    session_captcha = requests.session()
    url = 'http://jiyanapi.c2567.com/shibie'
    resp = session_captcha.post(
        url=url,
        json={
            'user': 'bingjian',
            'pass': 'Bingjian888',
            'gt': gt,
            'challenge': challenge,
            'referer': 'http://www.gsxt.gov.cn',
            'return': 'json',
            'model': model
        }
    )
    captcha_result = resp.text
    if 'ok' in captcha_result:
        if logger:
            logger.info(u'打码成功，结果: {}'.format(captcha_result))
        validate = json.loads(captcha_result)
        return validate
    else:
        logger.warning(u'打码失败，原因: {}'.format(captcha_result))



def get_validate(session, headers, m_proxy, logger=None):
    # 打码代理失效，程序有卡住的风险，故调整小了重试次数 ， modify wu_yong 2018-07-25
    max_retry_cnt = 10
    index = 0
    while index < max_retry_cnt:  # 该下while True 重试，加日志，以防程序一直卡在这里，不知道原因
        if logger:
            logger.info(u'开始打码,第{}次'.format(index))
        challenge_html = session.get(
            url='http://www.gsxt.gov.cn/SearchItemCaptcha?t=%s' % str(int(round(time.time() * 1000))),
            headers=headers,
            proxies=m_proxy,
            timeout=60
        ).content

        captcha_sign = json.loads(challenge_html)
        challenge = captcha_sign['challenge']
        gt = captcha_sign['gt']

        if captcha_sign['success'] == 0:
            model = '4'
        elif captcha_sign['success'] == 1:
            model = '3'
        else:
            print captcha_sign['success']

        session_captcha = requests.session()
        url = 'http://jiyanapi.c2567.com/shibie'

        resp = session_captcha.post(
            url=url,
            json={
                'user': 'bingjian',
                'pass': 'Bingjian888',
                'gt': gt,
                'challenge': challenge,
                'referer': 'http://www.gsxt.gov.cn',
                'return': 'json',
                'model': model
            }
        )
        captcha_result = resp.text

        if 'ok' in captcha_result:
            if logger:
                logger.info(u'打码成功，结果: {}'.format(captcha_result))
            validate = json.loads(captcha_result)
            return validate
        if logger:
            logger.warning(u'打码失败，次数： {}，原因: {}'.format(index, captcha_result))

        index += 1