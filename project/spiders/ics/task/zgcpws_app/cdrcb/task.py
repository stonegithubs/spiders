#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:task.py
description:
author:crazy_jacky
version: 1.0
date:2018/9/4
"""
import re
import json
import time
import random
import traceback

from uuid import uuid4
from urllib import quote

from bs4 import BeautifulSoup

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.md5_tool import to_md5
from ics.utils.decorator import stable
from ics.utils.string_tool import is_in_list
from ics.scheduler.new_task import StableTask
from ics.http.http_downloader import Downloader
from ics.utils.task_util.cdrcb.task_util import *
from ics.utils.exception_util import LogicException

from ics.settings import default_settings as setting

from ics.task.zgcpws_app.cdrcb.decrypt_tool import dec_aes

logger = get_ics_logger(__name__)

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


# lst_change_ip.append(('<span>360安域</span>'))
# lst_change_ip.append(('window.location.href'))


def pc_judge_func(resp):
    for cont in lst_change_ip:
        if cont in resp.content:
            return True
    return False


def pc_solution_func(resp, meta):
    download_pc.change_add_black_proxy()


def app_judge_func(resp):
    if not resp.content:
        return True
    return False


def app_solution_func(resp, meta):
    global token
    update_token()
    data = meta.get('data')
    headers = meta.get('headers')
    data.update({'reqtoken': token})
    head_param = get_head_param()
    headers.update(head_param)
    download_app.requests_param['data'] = str(json.dumps(data, ensure_ascii=False))
    download_app.requests_param['headers'] = headers


download_app = Downloader(spider_no='zgcpws_app', logger=logger, abandon_model='grey')
download_pc = Downloader(spider_no='zgcpws', logger=logger, abandon_model='grey')

device_id = ''
token = ''
header = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; LLD-AL30 Build/HONORLLD-AL30)',
    'Content-Type': 'application/json',
    'Connection': 'Keep-Alive',
    'Host': 'wenshuapp.court.gov.cn'
}

download_pc.set_retry_solution(pc_judge_func, pc_solution_func)
download_app.set_retry_solution(app_judge_func, app_solution_func, retry_key='update_token')


def get_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def get_nonce():
    seed = "abcdefghijklmnopqrstuvwxyz0123456789"
    sa = []
    for i in range(4):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def update_device_id(md5_str):
    global device_id
    char_str = 'abcdefghijklmnopqrstuvwxyz'
    tail = random.randint(1, 14)
    for i in range(tail):
        md5_str += random.choice(char_str)
    device_id = to_md5(md5_str)


def update_token():
    global device_id
    global token
    data = {"devid": device_id, "apptype": "1", "app": "cpws"}
    url = 'http://wenshuapp.court.gov.cn/MobileServices/GetToken'
    head_param = get_head_param()
    header.update(head_param)
    req = download_app.post(url, json=data, headers=header, retry_cnt=2).json()
    token = req.get('token')
    logger.info('current token is:{}'.format(token))


def get_signature(timespan, nonce):
    global device_id
    lists = [timespan, nonce, device_id]
    lists.sort()
    value = ''.join(lists)
    return to_md5(value)


def get_head_param():
    global device_id
    nonce = get_nonce()
    timespan = get_time()
    signature = get_signature(timespan, nonce)
    return {'devid': device_id,
            'nonce': nonce,
            'signature': signature,
            'timespan': timespan}


@app.task(bind=True, base=StableTask, default_retry_delay=0.5, max_retries=5,
          ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dic):
    global device_id
    global token
    self.error_callback = search_error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.ZGCPWS_DATA_TABLE,
    }
    if not device_id or not token:
        update_device_id(get_time())
        update_token()
    case_code = seed_dic.get('search_param')
    if not case_code:
        logger.info('rabbit MQ service seed_dic without case_code:{}'.format(seed_dic))
        return
    data = {"limit": "20",
            "dicval": "asc",
            "skip": "0",
            "dickey": "/CaseInfo/案/@法院层级".encode('utf-8'),
            "app": "cpws",
            'condition': "/CaseInfo/案/@DocContent={}".format(case_code)}
    app_url = 'http://wenshuapp.court.gov.cn/MobileServices/GetLawListData'
    head_param = get_head_param()
    header.update(head_param)
    data.update({'reqtoken': token})
    req = download_app.post(app_url, data=str(json.dumps(data, ensure_ascii=False)), headers=header,
                            retry_cnt=2, meta={'data': data, 'headers': header}, retry_keys=['update_token']).content
    dec_cont = dec_aes(token, head_param['timespan'], req, device_id)
    dic_lst = json.loads(dec_cont)
    total_cnt = len(dic_lst)
    if not total_cnt:
        logger.info('search no record aboat {}'.format(case_code))
        send_no_record(seed_dic, logger=logger, table_name=setting.ZGCPWS_DATA_TABLE)
        return
    for dic in dic_lst:
        doc_id = dic.get(unicode('文书ID'))
        pubdate = dic.get(unicode('裁判日期'))
        logger.info('get docid:{} success'.format(doc_id))
        app.send_task('ics.task.zgcpws_app.cdrcb.task.process_detail', [seed_dic, doc_id, pubdate, total_cnt],
                      queue=setting.ZGCPWS_APP_NORMAL_TASK_QUEUE, priority=2)


@app.task(bind=True, base=StableTask, default_retry_delay=0.5, max_retries=5,
          ignore_result=True)
@stable(LogicException, logger=logger)
def process_detail(self, seed_dic, doc_id, pubdate, total_cnt):
    url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={0}'.format(doc_id)
    self.error_callback = error_callback
    self.callback_param = {
        'seed_dict': seed_dic,
        'logger': logger,
        'table_name': setting.ZGCPWS_DATA_TABLE,
        'total_cnt': total_cnt,
        'lose_cnt': 1
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'text/javascript, application/javascript, */*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Host': 'wenshu.court.gov.cn'}
    target_name = seed_dic.get('target_name', '')
    refer = 'http://wenshu.court.gov.cn/content/content?DocID={0}&KeyWord={1}'
    header.update({'Referer': refer.format(doc_id, quote(seed_dic.get('search_param').encode('utf-8')))})
    source = download_pc.get(url, headers=header).content
    if 'window.location.href' in source or 'HtmlNotExist' in source:
        download_pc.change_add_grey_proxy()
        raise LogicException('get detail content need change ip')
    result_dic = {}
    add_common_key(result_dic, seed_dic, total_cnt=total_cnt, source_id=str(uuid4()), status='success',
                   page_source=source.decode('utf-8', "ignore"))
    logger.info('begin to parse doc_id:{}'.format(doc_id))
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
        logger.error('parse source:{}\n error: {}\n{}'.format(source, e, traceback.format_exc()))
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
