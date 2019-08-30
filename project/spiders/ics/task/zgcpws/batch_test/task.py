#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:task.py
description:
author:crazy_jacky
version: 1.0
date:2018/7/3
"""
import os
import re
import sys
import time
import json
import copy
import random
import requests
import traceback

from uuid import uuid4
from urllib import quote
from bs4 import BeautifulSoup

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.decorator import stable
from ics.utils.string_tool import is_json2, abstract, is_in_list
from ics.scheduler.new_task import StableTask
from ics.utils.cookie import cookiejar_from_dict
from ics.utils.task_util.batch_test.task_util import *
from ics.utils.exception_util import LogicException
from ics.proxy import get_proxy_from_zm, abandon_proxy
from ics.utils.js_server_client import excute_js
from ics.utils.duplicate.bloom_filter import BloomFilter
from ics.task.zgcpws.doc_id.get_cpws_vl5x import get_vl5x
import ics.settings.default_settings as setting

logger = get_ics_logger(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')

bloom_filter = BloomFilter(key='zgcpws_search')

basic_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://wenshu.court.gov.cn/'}

search_dic = {u'AH': u'案号',
              u'DSR': u'当事人',
              u'QWJS': u'全文检索',
              u'AJMC': u'案件名称'}

# 判断是否需要更换ip，并加黑名单的关键字
lst_change_ip = list()
# lst_change_ip.append('"[]"')
# lst_change_ip.append('"[check]"')
# lst_change_ip.append('"remind key"')
# lst_change_ip.append('ArgumentOutOfRangeException')
# lst_change_ip.append('"remind"')
# lst_change_ip.append('服务不可用')
lst_change_ip.append('<span>502</span>')
lst_change_ip.append('502 - Web')
lst_change_ip.append('<title>502</title>')
lst_change_ip.append(('<span>360安域</span>'))

vl5x = None
cookie = None


def create_guid():
    """
    use random create randnum and add 1,the turn oct to hex and get the last four char
    :return:
    """
    # js source code "var createGuid=function(){return(((1+Math.random())*0x10000)|0).toString(16).substring(1);}"
    num = int((random.random() + 1) * 0x10000)
    guid = hex(num)[3:]
    return guid


def guid_generator():
    guid_lst = [create_guid() for i in range(8)]
    # guid xxxxxxxx-xxxx-xxxxxxxx-xxxxxxxxxxxx
    for index in [5, 3, 2]:
        guid_lst.insert(index, '-')
    guid = ''.join(guid_lst)
    logger.info('generator guid success, guid:{}'.format(guid))
    return guid


def get_code(self, session):
    """
    get key params of code
    :return:
    """
    # 第一步获取param参数之一GetCode
    guid = guid_generator()
    first_header = copy.deepcopy(basic_header)
    first_header.update({'Origin': 'http://wenshu.court.gov.cn',
                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    max_cnt = 10
    number = ''
    while max_cnt:
        self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
        max_cnt -= 1
        number = session.post(
            url='http://wenshu.court.gov.cn/ValiCode/GetCode',
            headers=first_header,
            data='guid=' + guid,
            proxies=m_proxy,
            timeout=30,
            verify=False
        ).content
        logger.warn('get code ip {}'.format(self.abandon_ip))
        if number.isalnum():
            logger.info('get number success {}'.format(number))
            break
        time.sleep(random.randint(1, 4) * 0.5)
        if not max_cnt:
            raise LogicException('visit GetCode session failed')
    return number, guid


def update_vl5x(self, s_type):
    """
    get 'vjkl5' from cookie and calculate 'vl5x'
    :return:
    """
    global cookie
    global vl5x
    logger.info('开始更新,cookie:{},vl5x:{}'.format(cookie, vl5x))
    session = requests.session()
    second_header = copy.deepcopy(basic_header)
    second_header.update({'Origin': 'http://wenshu.court.gov.cn'})
    max_cnt = 10
    while max_cnt:
        max_cnt -= 1
        self.abandon_ip, content, m_proxy = get_proxy_from_zm(black_type='zgcpws')
        cookie_param = session.post(
            url='http://wenshu.court.gov.cn/List/SaveSession',
            headers=second_header,
            data='number={0}'.format(quote(s_type.encode('utf-8'))),
            proxies=m_proxy,
            timeout=30,
        ).content
        logger.warn('save session ip {}'.format(self.abandon_ip))
        time.sleep(random.randint(1, 4) * 0.5)
        if cookie_param.strip('"').isdigit():
            logger.info('get cookie success {}'.format(cookie_param))
            break
        if not max_cnt:
            raise LogicException('save session failed')
    url = 'http://wenshu.court.gov.cn/list/list'
    third_header = copy.deepcopy(basic_header)
    third_header.update({'Origin': 'http://wenshu.court.gov.cn/'})
    max_cnt = 10
    while max_cnt:
        max_cnt -= 1
        self.abandon_ip, port, m_proxy = get_proxy_from_zm(black_type='zgcpws')
        _ = session.get(
            url=url,
            headers=third_header,
            proxies=m_proxy,
            timeout=25,
        ).content
        logger.warn('update vjkl5 ip {}'.format(self.abandon_ip))
        time.sleep(random.randint(1, 4) * 0.5)
        cookie = requests.utils.dict_from_cookiejar(session.cookies)
        vjkl5 = cookie.get('vjkl5')
        if vjkl5:
            vl5x = get_vl5x(vjkl5, logger)
            break
        if not max_cnt:
            raise LogicException('visit list page get cookie failed')
    logger.info('更新结束,cookie:{},vl5x:{}'.format(cookie, vl5x))


def get_js_cont():
    """
    get local js content
    :return:
    """
    curr_path = os.path.dirname(__file__)
    file_path = os.path.join(curr_path, 'decrypt.js')
    with open(file_path, 'r') as fr:
        cont = fr.read()
    return cont


def get_com_str_key(cont, eval_str):
    """
    get com.str._KEY from listContent page param
    :param cont:
    :param eval_str:
    :return:
    """
    js_cont = cont + '''function get_des_key(RunEval) {
    var unzip_str = unzip(RunEval);
    eval("function temp(){" + unzip_str.replace("_=\\"constructor\\";_[_][_]", "_=\\"constructor\\";return ").replace("();", ";") + "}");
    return temp();}''' + '\n var temp_key = get_des_key("{}")\n return temp_key'.format(eval_str)
    code = excute_js(js_cont, logger)
    set_key = abstract(code, "('", ";'")
    logger.warn("get_com_str_key:{}".format(set_key))
    return set_key


def get_real_docid(cont, id_str, doc_key):
    """
    get real doc id from listContent page param
    :param cont:
    :param id_str:
    :param doc_key:
    :return:
    """
    js_cont = cont + '\n' + doc_key + '''\nfunction get_real_id(id) {
    var unzipid = unzip(id);
    return com.str.Decrypt(unzipid);}''' + '\n var temp_id = get_real_id("{}")\n return temp_id'.format(id_str)
    docid = excute_js(js_cont, logger)
    logger.warn("get docid:{}".format(docid))
    return docid


@app.task(bind=True, base=StableTask, default_retry_delay=5, max_retries=30,
          ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dic):
    global cookie
    global vl5x
    self.error_callback = search_error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.ZGCPWS_DATA_TABLE,
    }
    s_type = seed_dic.get('search_type', '')
    search_param = seed_dic.get('search_param', '')
    if s_type not in search_dic:
        logger.error('can not support the search key word of {}'.format(s_type))
    else:
        s_val = search_dic[s_type]
        base_form = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number={}&guid={}&conditions=searchWord+'
        search_param = '{}+{}++{}:{}'.format(quote(search_param.encode('utf-8')), s_type, quote(s_val.encode('utf-8')),
                                             quote(search_param.encode('utf-8')))
        refer = base_form + search_param
        app.send_task('ics.task.zgcpws.batch_test.task.get_total_cnt', [refer, seed_dic],
                      queue=setting.BATCH_TEST_ZGCPWS_NORMAL_TASK_QUEUE, priority=2)
        self.logger_meta['get_total_cnt'] = 'begin to search detail list page'


@app.task(bind=True, base=StableTask, default_retry_delay=5, max_retries=30,
          ignore_result=True)
@stable(LogicException, logger=logger)
def get_total_cnt(self, refer, seed_dic):
    global cookie
    global vl5x
    logger.info('开始执行get_total_cnt,cookie:{},vl5x{}'.format(cookie, vl5x))
    self.error_callback = search_error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.ZGCPWS_DATA_TABLE,
    }
    s_type = search_dic.get(seed_dic.get('search_type', ''), '')
    if not cookie:
        update_vl5x(self, s_type)
    self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
    session = requests.session()
    number, guid = get_code(self, session)
    session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
    search_param = seed_dic.get('search_param', '')
    refer_format = refer.format(number, guid)
    forth_header = copy.deepcopy(basic_header)
    forth_header.update({'Referer': refer_format,
                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                         'Origin': 'http://wenshu.court.gov.cn'})
    per_page = 20
    max_cnt = 10
    res_html = ''
    while max_cnt:
        max_cnt -= 1
        refer_format = refer.format(number, guid)
        forth_header.update({'Referer': refer_format})
        res_html = session.post(
            url='http://wenshu.court.gov.cn/List/ListContent',
            headers=forth_header,
            data='Param={0}&Index=1&Page={1}&Order={2}&Direction=asc&vl5x={3}&number={4}&guid={5}'.format(
                quote('{}:{}'.format(s_type, search_param)), per_page, quote('法院层级'), vl5x, number, guid),
            proxies=m_proxy,
            timeout=60,
            verify=False
        ).content
        logger.warn('get total cnt ip_ {}'.format(self.abandon_ip))
        time.sleep(random.randint(1, 4) * 0.5)
        logger.info('func get_total_cnt left {} times for retry'.format(max_cnt))
        if is_json2(res_html, logger):
            break
        elif max_cnt and is_in_list(lst_change_ip, res_html):  # 更新cookie 并更换ip 加ip黑名单
            abandon_proxy(self.abandon_ip, 'zgcpws')
            self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
            logger.warn('func process_page need change ip:{},update param then retry, reason:{}, cookie:{},'
                        ' vl5x:{}'.format(self.abandon_ip, res_html, cookie, vl5x))
            update_vl5x(self, s_type)
            number, guid = get_code(self, session)
            session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
            continue
        elif not max_cnt:
            raise LogicException('max retries and res_ html not json:res_html{}'.format(res_html))
        else:  # 更新cookie 并更换ip
            self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
            logger.warn('func process_page need change ip:{},update param then retry, reason:{}, cookie:{},'
                        ' vl5x:{}'.format(self.abandon_ip, res_html, cookie, vl5x))
            update_vl5x(self, s_type)
            number, guid = get_code(self, session)
            session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
            continue
    # 若没有搜索到相关结果，格式为"[{\"Count\":\"0\"}]"，不影响转为json
    try:
        dic_lst = json.loads(json.loads(res_html))
    except ValueError:
        logger.error('special res_html!!!!!!!:res_html{}'.format(res_html))
        raise LogicException('special res_html!!!!!!!:res_html{}'.format(res_html))
    if len(dic_lst) <= 1:
        logger.info('can not search any infomations of{}'.format(search_param))
        send_no_record(seed_dic, logger=logger, table_name=setting.ZGCPWS_DATA_TABLE)
    else:
        count = int(dic_lst[0].get('Count', 0))
        # minus one for count's dict
        page_cnt = len(dic_lst) - 1
        pages = count / per_page + 1 if (count % per_page) else count / per_page
        # 由于网站限制，仅能翻100页
        pages = min(100, pages)
        total_cnt = min(count, pages * page_cnt)
        # 若检索的列表页大于1，且当前页数为1，则执行翻页
        for page in range(2, pages + 1):
            logger.info('send {} page to task of process_page'.format(page))
            app.send_task('ics.task.zgcpws.batch_test.task.process_page',
                          [refer, seed_dic, page, total_cnt, page_cnt],
                          queue=setting.BATCH_TEST_ZGCPWS_NORMAL_TASK_QUEUE, priority=3)
        run_eval = dic_lst[0].get('RunEval')
        cont = get_js_cont()
        eval_key = get_com_str_key(cont, run_eval)
        for dic in dic_lst:
            eval_id = dic.get(u'文书ID', '')
            doc_id = get_real_docid(cont, eval_id, eval_key)
            pubdate = dic.get(u'裁判日期', '')
            if doc_id:
                url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={0}'.format(doc_id)
                logger.info('get doc id success {}'.format(url))
                app.send_task('ics.task.zgcpws.batch_test.task.process_detail',
                              [url, seed_dic, doc_id, pubdate, total_cnt],
                              queue=setting.BATCH_TEST_ZGCPWS_NORMAL_TASK_QUEUE, priority=4)


@app.task(bind=True, base=StableTask, default_retry_delay=5, max_retries=30,
          ignore_result=True)
@stable(LogicException, logger=logger)
def process_page(self, refer, seed_dic, page, total_cnt, page_cnt):
    global cookie
    global vl5x
    self.error_callback = error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.ZGCPWS_DATA_TABLE,
        'lose_cnt': page_cnt
    }
    s_type = search_dic.get(seed_dic.get('search_type', ''), '')
    if not cookie:
        update_vl5x(self, s_type)
    self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
    session = requests.session()
    session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
    number, guid = get_code(self, session)

    search_param = seed_dic.get('search_param', '')
    refer_format = refer.format(number, guid)
    forth_header = copy.deepcopy(basic_header)
    forth_header.update({'Referer': refer_format,
                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                         'Origin': 'http://wenshu.court.gov.cn'})
    per_page = 20
    res_html = ''
    max_cnt = 10
    while max_cnt:
        max_cnt -= 1
        refer_format = refer.format(number, guid)
        forth_header.update({'Referer': refer_format})
        res_html = session.post(
            url='http://wenshu.court.gov.cn/List/ListContent',
            headers=forth_header,
            data='Param={0}&Index={1}&Page={2}&Order={3}&Direction=asc&vl5x={4}&number={5}&guid={6}'.format(
                quote('{}:{}'.format(s_type, search_param)), page, per_page, quote('法院层级'), vl5x, number, guid),
            proxies=m_proxy,
            timeout=60,
        ).content
        time.sleep(random.randint(1, 4) * 0.5)
        logger.info('func process_page left {} times for retry'.format(max_cnt))
        if is_json2(res_html, logger):
            break
        elif max_cnt and is_in_list(lst_change_ip, res_html):  # 更新cookie 并更换ip 加ip黑名单
            abandon_proxy(self.abandon_ip, 'zgcpws')
            self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
            logger.warn('func process_page need change ip:{},update param then retry, reason:{}, cookie:{},'
                        ' vl5x:{}'.format(self.abandon_ip, res_html, cookie, vl5x))
            update_vl5x(self, s_type)
            number, guid = get_code(self, session)
            session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
            continue
        elif not max_cnt:
            raise LogicException('max retries and res_ html not json:res_html{}'.format(res_html))
        else:  # 更新cookie 并更换ip
            self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
            logger.warn('func process_page need change ip:{},update param then retry, reason:{}, cookie:{},'
                        ' vl5x:{}'.format(self.abandon_ip, res_html, cookie, vl5x))
            update_vl5x(self, s_type)
            number, guid = get_code(self, session)
            session.cookies = cookiejar_from_dict(cookie, domain='wenshu.court.gov.cn')
            continue
    dic_lst = json.loads(json.loads(res_html))
    logger.info('current process page is {}'.format(page))
    run_eval = dic_lst[0].get('RunEval')
    cont = get_js_cont()
    eval_key = get_com_str_key(cont, run_eval)
    for dic in dic_lst:
        eval_id = dic.get(u'文书ID', '')
        doc_id = get_real_docid(cont, eval_id, eval_key)
        pubdate = dic.get(u'裁判日期', '')
        if doc_id:
            url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={0}'.format(doc_id)
            logger.info('get doc id success {}'.format(url))
            app.send_task('ics.task.zgcpws.batch_test.task.process_detail',
                          [url, seed_dic, doc_id, pubdate, total_cnt],
                          queue=setting.BATCH_TEST_ZGCPWS_NORMAL_TASK_QUEUE, priority=4)


@app.task(bind=True, base=StableTask, default_retry_delay=5, max_retries=30,
          ignore_result=True)
@stable(LogicException, logger=logger)
def process_detail(self, url, seed_dic, doc_id, pubdate, total_cnt):
    # global cookie
    self.error_callback = error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.ZGCPWS_DATA_TABLE,
        'total_cnt': total_cnt,
        'lose_cnt': 1
    }
    session = requests.session()
    target_name = seed_dic.get('target_name', '')
    last_header = copy.deepcopy(basic_header)
    last_header.update(
        {'Referer': 'http://wenshu.court.gov.cn/content/content?DocID={0}&KeyWord={1}'.format(doc_id, quote(seed_dic.get(
            'search_param').encode('utf-8')))})
    max_cnt = 5
    source = ''
    while max_cnt:
        max_cnt -= 1
        self.abandon_ip, _, m_proxy = get_proxy_from_zm(black_type='zgcpws')
        source = session.get(
            url=url,
            headers=last_header,
            proxies=m_proxy,
            timeout=60,
        ).content
        time.sleep(random.randint(1, 4) * 0.5)
        logger.info('func process_detail left {} times for retry'.format(max_cnt))
        if u'文书ID' in source:
            break
        if not max_cnt:
            logger.info('func process_detail over retry times, then use decorator for retry'.format(max_cnt))
            self.logger_meta['content error'] = source
            raise LogicException('get detail conten failed')
    result_dic = {}
    add_common_key(result_dic, seed_dic, total_cnt=total_cnt, source_id=str(uuid4()), status='success',
                   page_source=source.decode('utf-8', "ignore"))
    result = parse_source(source, target_name)
    result_dic.update(result)
    result_dic[u'doc_id'] = doc_id
    result_dic[u'publishDate'] = pubdate
    insert_flag = False
    err_msg = ''
    try:
        insert_mysql("tbl_zgcpws", result_dic, logger)
        insert_flag = True
    except Exception as e:
        logger.warn('save data to mysql failed {} \n{}'.format(e, traceback.format_exc()))
        self.logger_meta['save data'] = traceback.format_exc()
        err_msg = e
        if not insert_flag:
            err_dic = {}
            add_common_key(err_dic, seed_dic, err_msg=e, status=TASK_STATUS.FAILED)
            insert_mysql(setting.ZGCPWS_DATA_TABLE, err_dic, logger)
        logger.warn('save data to mysql failed {} \n{}'.format(e, traceback.format_exc()))
    check_result_and_send_msg(setting.ZGCPWS_DATA_TABLE, total_cnt, seed_dic['task_id'], logger, err_msg=err_msg)
    logger.info('get detail content of DOCID {}'.format(doc_id))


def parse_source(source, target_name):
    """
    parse source content to structure data
    :param source:
    :param target_name:
    :return:
    """
    result_dic = {}
    try:
        base_info = ''.join(re.compile('JSON.stringify\s*\((.*?)\);\$', re.DOTALL).findall(source))
        html_info = ''.join(re.compile('jsonHtmlData\s*=\s*(.*?);\s*var', re.DOTALL).findall(source))
        base_dic = json.loads(base_info)
        html_dic = json.loads(json.loads(html_info))
        html_cont = html_dic.get('Html', '')
        judge_result_html = ''.join(
            re.compile("<a type='dir' name='PJJG'></a>\s*(.*?)\s*<a type='dir' name='WBWB'></a>",
                       re.DOTALL).findall(html_cont))
        attach_info = ''.join(re.compile('RelateInfo:\s*(.*?),\s*LegalBase', re.DOTALL).findall(source))
        attach_dic = turn_str_2_dict(attach_info)
        text = get_html_cont(html_cont)
        judge_result = get_html_cont(judge_result_html)
        result_dic[u'target_name'] = target_name
        result_dic[u'caseCode'] = base_dic.get(u'案号', '')
        result_dic[u'doc_id'] = base_dic.get(u'文书ID', '')
        result_dic[u'reason'] = attach_dic.get(u'案由', '')
        result_dic[u'trialRound'] = base_dic[u'审判程序']
        result_dic[u'main'] = text
        result_dic[u'title'] = base_dic[u'案件名称']
        result_dic[u'trialDate'] = attach_dic.get(u'裁判日期', '')
        result_dic[u'court'] = attach_dic.get(u'审理法院', '')
        result_dic[u'judge_result'] = judge_result
        result_dic[u'appellor'] = attach_dic.get(u'当事人', '')
    except Exception as e:
        logger.error('parse source content error: {}'.format(e))
    return result_dic


def get_html_cont(html, tag='div'):
    """
    get text content from html
    :return:
    """
    soup_list = BeautifulSoup(html, 'lxml').select(tag)
    text = '\r\n'.join([x.text for x in soup_list])
    return text


def turn_str_2_dict(dic_str):
    """
    turn string into dict
    :return:
    """
    res_dic = {}
    try:
        dic_str = dic_str.replace('name', '"name"').replace('key', '"key"').replace('value', '"value"')
        dic = eval(dic_str)
        for item in dic:
            res_dic[item['name'].decode('utf-8')] = item['value']
    except Exception as e:
        logger.error('parse attach info dict failed: {}'.format(e))
    return res_dic
