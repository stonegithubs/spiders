#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:spider_zgcpws.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/3
"""
import os
import sys
import time
import copy
import json
import random
import requests

from urllib import quote

from ics.utils.js_server_client import excute_js
from ics.utils.cookie import cookiejar_from_dict
from ics.utils.string_tool import is_json2, abstract
from ics.task.zgcpws.cdrcb.task import guid_generator
from ics.proxy import get_proxy_from_zm, abandon_proxy
from ics.task.zgcpws.doc_id.get_cpws_vl5x import get_vl5x

reload(sys)

sys.setdefaultencoding('utf-8')


def get_code(session, header, logger):
    """
    get key params of code
    :return:
    """
    # 第一步获取param参数之一GetCode
    guid = guid_generator()
    headers = copy.deepcopy(header)
    headers.update({'Origin': 'http://wenshu.court.gov.cn',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    max_cnt = 10
    number = ''
    while max_cnt:
        abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws', from_type='25mintest')
        max_cnt -= 1
        try:
            number = session.post(
                url='http://wenshu.court.gov.cn/ValiCode/GetCode',
                headers=headers,
                data='guid=' + guid,
                proxies=m_proxy,
                timeout=30,
                verify=False
            ).content
        except Exception as e:
            msg = 'zgcpws spider get number failed: {}'.format(e)
            abandon_proxy(abandon_ip, 'zgcpws')
            logger.warn(msg)
            continue
        logger.warn('get code ip {}'.format(m_proxy))
        if number.isalnum():
            logger.info('get number success {}'.format(number))
            break
        time.sleep(random.randint(1, 4) * 0.5)
    return number, guid


def get_js_cont():
    """
    get local js content
    :return:
    """
    curr_path = os.path.dirname(__file__)
    file_path = os.path.join(curr_path, '../decrypt.js')
    with open(file_path, 'r') as fr:
        cont = fr.read()
    return cont


def get_com_str_key(cont, eval_str, logger):
    """
    get com.str._KEY from listContent page param
    :param cont:
    :param eval_str:
    :param logger:
    :return:
    """
    js_cont = cont + '''function get_des_key(RunEval) {
    var unzip_str = unzip(RunEval);
    eval("function temp(){" + unzip_str.replace("_=\\"constructor\\";_[_][_]", "_=\\"constructor\\";return ").replace("();", ";") + "}");
    return temp();}''' + '\n var temp_key = get_des_key("{}")\n return temp_key'.format(eval_str)
    code = excute_js(js_cont, logger)
    set_key = abstract(code, "('", ";'")
    return set_key


def get_real_docid(cont, id_str, doc_key, logger):
    """
    get real doc id from listContent page param
    :param cont:
    :param id_str:
    :param doc_key:
    :param logger:
    :return:
    """
    js_cont = cont + '\n' + doc_key + '''\nfunction get_real_id(id) {
    var unzipid = unzip(id);
    return com.str.Decrypt(unzipid);}''' + '\n var temp_id = get_real_id("{}")\n return temp_id'.format(id_str)
    docid = excute_js(js_cont, logger)
    return docid


def update_vl5x(header, logger):
    """
    get 'vjkl5' from cookie and calculate 'vl5x'
    :return:
    """
    cookie = ''
    vl5x = ''
    logger.info('开始更新,cookie:{},vl5x:{}'.format(cookie, vl5x))
    session = requests.session()
    headers = copy.deepcopy(header)
    headers.update({'Origin': 'http://wenshu.court.gov.cn'})
    max_cnt = 10
    while max_cnt:
        max_cnt -= 1
        abandon_ip, content, m_proxy = get_proxy_from_zm(black_type='zgcpws', from_type='25mintest')
        try:
            cookie_param = session.post(
                url='http://wenshu.court.gov.cn/List/SaveSession',
                headers=headers,
                data='number={0}'.format(quote('案号')),
                proxies=m_proxy,
                timeout=30,
            ).content
        except Exception as e:
            logger.warn('zgcpws spider save session failed:{}'.format(e))
            if not max_cnt:
                return cookie, vl5x
            abandon_proxy(abandon_ip, 'zgcpws')
            continue
        logger.warn('save session ip {}'.format(abandon_ip))
        time.sleep(random.randint(1, 4) * 0.5)
        if cookie_param.strip('"').isdigit():
            logger.info('get cookie success {}'.format(cookie_param))
            break
    url = 'http://wenshu.court.gov.cn/list/list'
    headers = copy.deepcopy(header)
    headers.update({'Origin': 'http://wenshu.court.gov.cn/'})
    max_cnt = 10
    while max_cnt:
        max_cnt -= 1
        abandon_ip, port, m_proxy = get_proxy_from_zm(black_type='zgcpws', from_type='25mintest')
        try:
            _ = session.get(
                url=url,
                headers=headers,
                proxies=m_proxy,
                timeout=25,
            ).content
        except Exception as e:
            logger.warn('zgcpws spider request vl5x failed:{}'.format(e))
            if not max_cnt:
                return cookie, vl5x
            abandon_proxy(abandon_ip, 'zgcpws')
            continue
        logger.warn('update vjkl5 ip {}'.format(abandon_ip))
        time.sleep(random.randint(1, 4) * 0.5)
        cookie = requests.utils.dict_from_cookiejar(session.cookies)
        vjkl5 = cookie.get('vjkl5')
        if vjkl5:
            vl5x = get_vl5x(vjkl5, logger)
            break
    logger.info('更新结束,cookie:{},vl5x:{}'.format(cookie, vl5x))
    return cookie, vl5x


def get_zgcpws_status(logger):
    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://wenshu.court.gov.cn/'}
    ah = '（2015）民申字第739号'
    number, guid = get_code(session, header, logger)
    if not guid:
        msg = 'zgcpws spider get guid, number over max retry times'
        return False, msg
    cookie, vl5x = update_vl5x(header, logger)
    session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
    if not vl5x:
        msg = 'zgcpws spider get cookie, vl5x over max retry times'
        return False, msg
    base = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number={}&guid={}&conditions=searchWord+'
    para = '{}+{}++{}:{}'.format(quote(ah), 'QWJS', quote('全文检索'), quote(ah))
    refer = base + para
    headers = copy.deepcopy(header)
    headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Origin': 'http://wenshu.court.gov.cn'})
    res_html = ''
    max_cnt = 20
    while max_cnt:
        max_cnt -= 1
        refer_format = refer.format(number, guid)
        abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws', from_type='25mintest')
        headers.update({'Referer': refer_format})
        try:
            res_html = session.post(
                url='http://wenshu.court.gov.cn/List/ListContent',
                headers=headers,
                data='Param={0}&Index=1&Page={1}&Order={2}&Direction=asc&vl5x={3}&number={4}&guid={5}'.format(
                    quote('{}:{}'.format('全文检索', ah)), 20, quote('法院层级'), vl5x, number, guid),
                proxies=m_proxy,
                timeout=25,
                verify=False
            ).content
            time.sleep(random.randint(1, 4) * 0.5)
        except Exception as e:
            logger.warn('zgcpws spider search failed:{}'.format(e))
            if not max_cnt:
                return False, 'zgcpws spider search over max retry times:{}'.format(e)
            abandon_proxy(abandon_ip, 'zgcpws')
            continue
        if is_json2(res_html, logger) and 'RunEval' in res_html:
            break
        elif max_cnt:
            number, guid = get_code(session, header, logger)
            cookie, vl5x = update_vl5x(header, logger)
            session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
            logger.warn('zgcpws spider search result is {}'.format(res_html))
            continue
        if not max_cnt:
            msg = 'zgcpws spider request search page over max retry times:{}'.format(res_html)
            return False, msg
    msg = ''
    max_cnt = 10
    url = ''

    try:
        lst = json.loads(json.loads(res_html))
        js_cont = get_js_cont()
        eval_key = get_com_str_key(js_cont, lst[0].get('RunEval'), logger)
    except Exception as e:
        msg = 'zgcpws get list page failed: {} \n {}'.format(res_html, e)
        logger.warn(msg)
        return False, msg
    for dic in lst:
        eval_id = dic.get(u'文书ID')
        doc_id = get_real_docid(js_cont, eval_id, eval_key, logger)
        if doc_id:
            url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(doc_id)
            break
    if not url:
        return False, 'get no record by search result{}, please check web site manual'.format(res_html)
    while max_cnt:
        max_cnt -= 1
        abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws', from_type='25mintest')
        session = requests.session()
        try:
            cont = session.get(url, headers=header, proxies=m_proxy, timeout=60).content
            if u'文书ID' in cont:
                msg = 'request specific url {} success：{}'.format(url, cont)
                logger.info(msg)
                return True, 'request specific url {} success\r\n result:{}'.format(url, cont)
            elif not max_cnt:
                msg = 'request specific url {} and get content empty, please check'.format(url)
                logger.info(msg)
                return False, msg
        except Exception as e:
            msg = 'request specific zgcpws url:{} failed:{}'.format(url, e)
            logger.warn(msg)
            abandon_proxy(abandon_ip, 'zgcpws')
    return False, msg


