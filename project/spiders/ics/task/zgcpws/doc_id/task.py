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
import sys
import json
import copy
import random

from urllib import quote

from ics.scheduler import app
from ics.utils import get_ics_logger
from ics.utils.decorator import stable2
from ics.scheduler.new_task import StableTask
from ics.http.http_downloader import Downloader
from ics.utils.js_server_client import excute_js
from ics.utils.task_util.cdrcb.task_util import *
from ics.utils.exception_util import LogicException, DownloaderException
from ics.utils.string_tool import is_json2, abstract
from ics.utils.duplicate.bloom_filter import BloomFilter
from ics.task.zgcpws.doc_id.get_cpws_vl5x import get_vl5x

import ics.settings.default_settings as setting

logger = get_ics_logger(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')

bloom_filter = BloomFilter(key='zgcpws_search')
download = Downloader(spider_no='zgcpws',logger=logger, abandon_model='grey', proxy_mode="dly")

basic_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://wenshu.court.gov.cn/'}

# 判断是否需要更换ip，并加黑名单的关键字
lst_change_ip = list()
# lst_change_ip.append('"[]"')
# lst_change_ip.append('"[check]"')
# lst_change_ip.append('"remind key"')
# lst_change_ip.append('"remind"')
lst_change_ip.append('<span>360安域</span>')
# lst_change_ip.append('点击刷新验证码')

lst_abandon_ip = list()
lst_abandon_ip.append('服务不可用')
lst_abandon_ip.append('<span>502</span>')
lst_abandon_ip.append('<title>502</title>')
lst_abandon_ip.append('ArgumentOutOfRangeException')

vl5x = None
cookie = None
page_cnt = 0
threshold = 220


def pc_judge_change_ip_func(resp, meta):
    for cont in lst_change_ip:
        if cont in resp.content:
            return True
    return False


def pc_solution_change_ip_func(resp, meta):
    download.change_add_grey_proxy()


def pc_judge_abandon_ip_func(resp, meta):
    for cont in lst_abandon_ip:
        if cont in resp.content:
            return True
    return False


def pc_solution_abandon_ip_func(resp, meta):
    download.change_add_black_proxy()


def pc_judge_is_json2_func(resp, meta):
    if not is_json2(resp.content, logger):
        return True
    return False


def pc_solution_is_json2_func(resp, meta):
    global vl5x
    update_vl5x()
    number, guid = get_code()
    param = meta.get("param")
    refer = meta.get("refer")
    if param:
        download.requests_param["data"] = param.format(vl5x, number, guid)
    if refer:
        refer_f = refer.format(number, guid)
        headers = meta["headers"]
        download.requests_param["headers"] = headers.update({"Referer": refer_f})


download.set_retry_solution(pc_judge_change_ip_func, pc_solution_change_ip_func, retry_key="normal_01")
download.set_retry_solution(pc_judge_abandon_ip_func, pc_solution_abandon_ip_func, retry_key="normal_02")
download.set_retry_solution(pc_judge_is_json2_func, pc_solution_is_json2_func, retry_key="is_json2")


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


def get_code():
    """
    get key params of code
    :return:
    """
    # 第一步获取param参数之一GetCode
    guid = guid_generator()
    first_header = copy.deepcopy(basic_header)
    first_header.update({'Origin': 'http://wenshu.court.gov.cn',
                         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
    url = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
    number = download.post(url, params={'guid': guid}, headers=first_header).content
    if not number.isalnum():
        raise LogicException('visit GetCode session failed')
    return number, guid


def update_vl5x():
    """
    get 'vjkl5' from cookie and calculate 'vl5x'
    :return:
    """
    global cookie
    global vl5x
    logger.info('开始更新,cookie:{},vl5x:{}'.format(cookie, vl5x))
    header = copy.deepcopy(basic_header)
    header.update({'Origin': 'http://wenshu.court.gov.cn'})
    url = 'http://wenshu.court.gov.cn/List/SaveSession'
    cookie_param = download.post(url, headers=header, param='number={0}'.format(quote('u案由'))).content
    if not cookie_param.strip('"').isdigit():
        raise LogicException('save session failed')
    url = 'http://wenshu.court.gov.cn/list/list'
    t_header = {'Origin': 'http://wenshu.court.gov.cn/',
                'Host': 'wenshu.court.gov.cn',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                }
    _ = download.get(url, t_header).content
    vjkl5 = download.get_cookie().get('vjkl5')
    if not vjkl5:
        raise LogicException('visit list page get cookie failed')
    vl5x = get_vl5x(vjkl5, logger)
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


def send_process_page(total_cnt, param_str, refer):
    pages = get_pages(total_cnt)
    for page in range(1, pages + 1):
        logger.info('send param:{}, count:{} page:{} to task of process_page'.format(param_str, total_cnt, page))
        app.send_task('ics.task.zgcpws.doc_id.task.process_page',
                      [refer, page, param_str, total_cnt],
                      queue=setting.ZGCPWS_DOC_ID_NORMAL_TASK_QUEUE, priority=6)


def save_data(dic):
    do_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res_dic = {}
    map_dic = {u'法院名称': 'court',
               u'案号': 'case_code',
               u'审判程序': 'judge_program',
               u'文书ID': 'doc_id',
               u'案件名称': 'case_name',
               u'裁判日期': 'judge_date',
               u'案件类型': 'case_type',
               u'裁判要旨段原文': 'source_text',
               u'不公开理由': 'unpub_reason',
               }
    for key, val in dic.items():
        if key not in map_dic:
            dic.pop(key, '')
            continue
        res_dic[map_dic[key]] = val
    res_dic.update({'do_time': do_time})
    insert_mysql('tbl_zgcpws_increment01', res_dic, logger)


def get_pages(cnt):
    global page_cnt
    if not page_cnt:
        get_page_cnt()
    pages = cnt / page_cnt + 1 if (cnt % page_cnt) else cnt / page_cnt
    pages = min(pages, 100)
    return pages


def get_page_cnt():
    global cookie
    global vl5x
    global page_cnt
    logger.info('开始执行get_page_cnt计算每页条数,cookie:{},vl5x{}'.format(cookie, vl5x))
    if not cookie:
        update_vl5x()
    number, guid = get_code()
    max_cnt = 5
    res_html = ''
    while max_cnt:
        max_cnt -= 1
        refer = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number={}&guid={}&conditions=searchWord+QWJS+++{}:{}'. \
            format(number, guid, quote('全文检索'), quote('张三'))
        header = copy.deepcopy(basic_header)
        header.update({'Referer': refer,
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Connection': 'Keep-Alive',
                       'Origin': 'http://wenshu.court.gov.cn'})
        url = 'http://wenshu.court.gov.cn/List/ListContent'
        res_html = download.post(url,
                                 headers=header,
                                 data='Param={0}&Index=1&Page=20&Order={1}&Direction=asc&vl5x={2}&number={3}&guid={4}'.
                                 format(quote_param('全文检索:张三'), quote('法院层级'), vl5x, number, guid)).content
        if is_json2(res_html, logger):
            break
        if not max_cnt:
            raise LogicException('param:{} process page failed'.format('全文检索:张三'))
    dic_lst = json.loads(json.loads(res_html))
    page_cnt = len(dic_lst) - 1


def quote_param(param_str):
    return quote(param_str.encode('utf-8'))


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable2((LogicException, DownloaderException), logger=logger)
def start(self, seed_dic):
    global cookie
    global vl5x
    case_type_lst = ['刑事案件', '民事案件', '行政案件', '赔偿案件', '执行案件']
    date_str = seed_dic.get('search_date').strip()
    search_param = '{} TO {}'.format(date_str, date_str)
    date_str = '{}+{}:{}'.format(quote_param(search_param), quote('上传日期'), quote_param(search_param))
    for case_type in case_type_lst:
        param_str = '上传日期:{},案件类型:{}'.format(search_param, case_type)
        type_str = '&conditions=searchWord+2+AJLX++{}:{}'.format(quote('案件类型'), quote_param(case_type))
        refer = date_str + type_str
        app.send_task('ics.task.zgcpws.doc_id.task.get_total_cnt', [refer, param_str],
                      queue=setting.ZGCPWS_DOC_ID_NORMAL_TASK_QUEUE, priority=1)
        logger.info('begin to search param:{} list page'.format(param_str))


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable2((LogicException, DownloaderException), logger=logger)
def get_total_cnt(self, refer, param_str):
    global cookie
    global vl5x
    logger.info('开始执行get_total_cnt,cookie:{},vl5x{}'.format(cookie, vl5x))
    if not cookie:
        update_vl5x()
    number, guid = get_code()
    url = 'http://wenshu.court.gov.cn/List/TreeContent'
    header = copy.deepcopy(basic_header)
    base_form = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+++'
    total_refer = base_form + refer
    header.update({'Referer': total_refer,
                   'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Origin': 'http://wenshu.court.gov.cn'})
    meta_para = 'Param={0}'.format(quote_param(param_str)) + '&vl5x={}&number={}&guid={}'
    res_html = download.post(url,
                             headers=header,
                             data='Param={0}&vl5x={1}&guid={2}&number={3}'.format(quote_param(param_str), vl5x,
                                                                                  guid, number),
                             meta={'param': meta_para},
                             retry_keys=["is_json2"]).content
    dic_lst = json.loads(json.loads(res_html))
    level_dic = {}
    for dic in dic_lst:
        if dic.get('Key') in u'法院层级':
            level_dic = copy.deepcopy(dic)
            break
    total_cnt = level_dic.get('IntValue', 0)
    base_form = 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number={}&guid={}&conditions=searchWord+++'
    if total_cnt > threshold:
        cj_lst = level_dic.get('Child', [])
        for item in cj_lst:
            level_name = item.get('Key')
            level_cnt = item.get('IntValue')
            if not level_cnt:
                continue
            param_str_cj = '{},法院层级:{}'.format(param_str, level_name)
            cj_str = quote('&conditions=searchWord+{}+++{}:{}'.format(level_name, '法院层级', level_name))
            cj_refer = base_form + refer + cj_str
            if level_cnt < threshold:
                send_process_page(level_cnt, param_str_cj, cj_refer)
            else:
                logger.info('send param:{}, count:{} to task of iter_fydy'.format(param_str_cj, level_cnt))
                app.send_task('ics.task.zgcpws.doc_id.task.iter_fydy',
                              [cj_refer, param_str_cj],
                              queue=setting.ZGCPWS_DOC_ID_NORMAL_TASK_QUEUE, priority=3)
    else:
        if not total_cnt:
            logger.info('search no record aboat param:{}'.format(param_str))
            return
        send_process_page(total_cnt, param_str, total_refer)


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable2((LogicException, DownloaderException), logger=logger)
def iter_fydy(self, refer, param_str):
    global cookie
    global vl5x
    logger.info('开始执行iter_fydy,cookie:{},vl5x{}'.format(cookie, vl5x))
    if not cookie:
        update_vl5x()
    number, guid = get_code()
    meta_para = 'Param={0}'.format(quote_param(param_str)) + '&vl5x={}&number={}&guid={}'
    refer_format = refer.format(number, guid)
    header = copy.deepcopy(basic_header)
    header.update({'Connection': 'Keep-Alive',
                   'Host': 'wenshu.court.gov.cn',
                   'Referer': refer_format,
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Origin': 'http://wenshu.court.gov.cn'})
    url = 'http://wenshu.court.gov.cn/List/TreeContent'
    res_html = download.post(url,
                             headers=header,
                             data='Param={0}&vl5x={1}&guid={2}&number={3}'.format(quote_param(param_str),
                                                                                  vl5x, guid, number),
                             meta={'headers': header, 'param': meta_para, 'refer': refer},
                             retry_keys=["is_json2"]).content
    dic_lst = json.loads(json.loads(res_html))
    dy_dic = {}
    for dic in dic_lst:
        if dic.get('Key') in u'法院地域':
            dy_dic = copy.deepcopy(dic)
            break
    total_cnt = dy_dic.get('IntValue', 0)
    if total_cnt > threshold:
        dy_lst = dy_dic.get('Child', [])
        for item in dy_lst:
            area_name = item.get('Key')
            area_cnt = item.get('IntValue')
            if not area_cnt:
                continue
            dy_param_str = param_str + ',法院地域:{}'.format(area_name) + ',法院地域:{}'.format(area_name)
            dy_refer = refer + quote('&conditions=searchWord+{}+++{}:{}'.format(area_name, '法院地域', area_name))
            if area_cnt < threshold:
                send_process_page(area_cnt, dy_param_str, dy_refer)
            else:
                logger.info('send param:{}, count:{} to task of iter_fy_lst'.format(dy_param_str, area_cnt))
                app.send_task('ics.task.zgcpws.doc_id.task.iter_fy_lst',
                              [dy_refer, dy_param_str, area_name],
                              queue=setting.ZGCPWS_DOC_ID_NORMAL_TASK_QUEUE, priority=4)
    else:
        if not total_cnt:
            logger.info('search no record aboat param:{}'.format(param_str))
            return
        send_process_page(total_cnt, param_str, refer)


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable2((LogicException, DownloaderException), logger=logger)
def iter_fy_lst(self, refer, param_str, province):
    global cookie
    global vl5x
    logger.info('开始执行iter_fy_lst,cookie:{},vl5x{}'.format(cookie, vl5x))
    if not cookie:
        update_vl5x()
    number, guid = get_code()
    refer_format = refer.format(number, guid)
    header = copy.deepcopy(basic_header)
    header.update({'Referer': refer_format,
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Connection': 'Keep-Alive',
                   'Host': 'wenshu.court.gov.cn'})

    url = 'http://wenshu.court.gov.cn/List/CourtTreeContent'
    res_html = download.post(url,
                             headers=header,
                             data='Param={0}&parval={1}'.format(quote_param(param_str), quote_param(province)),
                             meta={'headers': header, 'refer': refer},
                             retry_keys=["is_json2"]).content
    dic = json.loads(json.loads(res_html))[0]
    fy_lst_dic = dic.get('Child', [])
    for dic in fy_lst_dic:
        fy_name = dic.get('Key')
        fy_cnt = dic.get('IntValue')
        if not fy_cnt:
            continue
        fy_param_str = param_str + ',{}:{}'.format('中级法院', fy_name)
        fy_refer_str = refer + quote('&conditions=searchWord+{}+++{}:{}'.format(fy_name, '中级法院', fy_name))
        logger.info('send param:{}, count:{} to task of process_page'.format(fy_param_str, fy_cnt))
        send_process_page(fy_cnt, fy_param_str, fy_refer_str)


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable2((LogicException, DownloaderException), logger=logger)
def process_page(self, refer, page, param_str, total_cnt):
    global cookie
    global vl5x
    logger.info('开始执行process_page,cookie:{},vl5x{}'.format(cookie, vl5x))
    if not cookie:
        update_vl5x()
    number, guid = get_code()
    refer_format = refer.format(number, guid)
    meta_para = 'Param={0}&Index={1}&Page=20&Order={2}&Direction=asc'.format(
        quote_param(param_str), page, quote('法院层级')) + '&vl5x={}&number={}&guid={}'
    header = copy.deepcopy(basic_header)
    header.update({'Referer': refer_format,
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Connection': 'Keep-Alive',
                   'Origin': 'http://wenshu.court.gov.cn'})
    url = 'http://wenshu.court.gov.cn/List/ListContent'
    res_html = download.post(url,
                             headers=header,
                             data='Param={0}&Index={1}&Page=20&Order={2}&Direction=asc&vl5x={3}&number={4}&guid={5}'.format(
                                 quote_param(param_str), page, quote('法院层级'), vl5x, number, guid),
                             meta={'headers': header, 'param': meta_para, 'refer': refer},
                             retry_keys=["is_json2"]).content
    dic_lst = json.loads(json.loads(res_html))
    logger.info('current process page is {}'.format(page))
    run_eval = dic_lst[0].get('RunEval')
    cont = get_js_cont()
    eval_key = get_com_str_key(cont, run_eval)
    logger.info('search param:{}, page:{} and total:{} success'.format(param_str, page, total_cnt))
    for dic in dic_lst:
        eval_id = dic.get(u'文书ID', '')
        doc_id = get_real_docid(cont, eval_id, eval_key)
        if len(doc_id) > 36:
            logger.error('decode doc id failed:{}'.format(doc_id))
            # TODO warning encode method change
            pass
        dic.update({u'文书ID': doc_id, 'run_eval': run_eval})
        if doc_id:
            if bloom_filter.dup_filter(doc_id):
                logger.info('repeat data found {}'.format(doc_id))
                continue
            save_data(dic)
