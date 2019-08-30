# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用于定义企信网爬虫相关与爬虫业务逻辑无关公告代码
"""
import requests
from retry import retry
import json
import re
import uuid
import datetime
from ics.utils.db import CdrcbDb
from ics.utils.js_server_client import excute_js
from ics.utils.string_tool import abstract
from ics.task.gsxt.batch_test.constant import *


def judge_html_is_none(resp):
    """
    判断页面为空
    :param resp:
    :return:
    """
    res_html = resp.content
    if not res_html:
        logger.warning(u'页面返回html为空: status_code: {}, html: {}'.format(resp.status_code, res_html))
        return True


def judge_status_eq_521(resp):
    """
    处理网页出现521加速乐的情况
    :param resp:
    :return:
    """
    if resp.status_code == 521:
        err_msg = u'下载返回状态码不合法, 状态码为： {}'.format(str(resp.status_code))
        logger.warning(err_msg)
        refresh_cookie(resp.content)
        return True


def judge_status_gt_400(resp):
    if resp.status_code >= 400:
        err_msg = u'下载返回状态码不合法, 状态码为： {}'.format(str(resp.status_code))
        logger.warning(err_msg)
        downloader.change_add_grey_proxy()
        return True


def judge_invalid_link(resp):
    html = resp.content
    if invalid_link(html) is False:
        downloader.change_add_grey_proxy()
        return True


def assert_page_not_found(resp):
    html = resp.content
    if u'您访问的页面不存在' in html:
        logger.info(u'响应页面出现404页面: {}'.format(html))
        return True


def assert_too_busy(resp):
    html = resp.content
    if u'操作过于频繁' in html:
        logger.warning(u"操作过于频繁, 切换代理-重试......")
        return True


def assert_is_not_json(resp):
    try:
        html = resp.content
        json.loads(html)
    except Exception as e:
        logger.warning(u'模块下载页面非json，重试, {}'.format(str(e)))
        return True


def assert_invalid_cache_key_0_0(resp):
    try:
        if assert_is_not_json(resp) is None:
            resp_json = json.loads(resp.content)
            if '0_0' == resp_json.get('cacheKey'):
                logger.warning(u'执行断言函数检查失败，包含cache_key: {}， html为：{}'.format('0_0', resp_json))
                get_pictures()
                return True
    except Exception as e:
        logger.error(u'执行断言函数assert_invalid_cache_key_0_0异常: {}'.format(str(e)))

def assert_dos_attack(resp):
    try:
        html = resp.content
        if u'您的访问行为被判定为DoS攻击' in html:
            downloader.change_add_grey_proxy()
            return True
    except Exception as e:
        logger.warning(u'您的访问行为被判定为DoS攻击，重试, {}'.format(str(e)))
        return True


downloader.set_retry_solution(judge_html_is_none, retry_key='on_content')
downloader.set_retry_solution(judge_status_eq_521, retry_key='status_521')
downloader.set_retry_solution(judge_status_gt_400, retry_key='status_gt_400')
downloader.set_retry_solution(judge_invalid_link, retry_key='invalid_link')
downloader.set_retry_solution(assert_page_not_found, retry_key='page_not_found')
downloader.set_retry_solution(assert_too_busy, retry_key='too_busy')
downloader.set_retry_solution(assert_is_not_json, retry_key='is_not_json')
downloader.set_retry_solution(assert_invalid_cache_key_0_0, retry_key='invalid_cache_key_0_0')
downloader.set_retry_solution(assert_dos_attack, retry_key='dos_attack')


def insert_mysql(table, model):
    mysql_db = CdrcbDb("cdrcb_crawl", logger)   # 单例
    mysql_db.insert_dic(table, model)


def get_cookies_for_requests(session, js_521):
    try:
        js_str = 'function getClearance(){{{0}}};'.format(js_521)
        js_str = js_str.replace('</script>', '')
        js_str = js_str.replace('eval(y.replace(/\\b\w+\\b/g, function(y){return x[f(y,z)-1]||("_"+y)}));',
                                'var temp = y.replace(/\\b\w+\\b/g, function(y){return x[f(y,z)-1]||("_"+y)});eval(temp);return temp;')
        js_str = js_str.replace('<script>', '')
        js_str = js_str.replace(';break}catch', ';}catch')
        js_str = js_str.replace('\x00', '')
        js_str = js_str + ';return getClearance();'
        js_result1 = excute_js(js_str, logger)

        js = js_result1.replace(
            'setTimeout(\'location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\\\'\\\')\',1500);',
            'var window = [];')
        func_name = re.match('var (_.*?)=', js).group(1)
        js = js.replace('return return', 'return eval')
        js = js.replace('document.cookie', 'return cookie')
        js = 'var' + abstract(js ,'var' ,'if((function(){try')
        js = js + ('return {}();'.format(func_name))

        def relpace_str(args):
            pos_str = args.group(1)
            to_replace_str = args.group(2)
            var_name = re.findall(r'=\s*(.+?)\.match', to_replace_str)[0]
            ret_str = '{}var {}="http://www.gsxt.gov.cn/index.html";{}'.format(pos_str, var_name, args.group(2))
            return ret_str

        js = re.sub(r'(firstChild.href;)\s*(var\s*.+?=.+?\.match\(.+?;)', relpace_str, js, flags=re.S)

        result2 = excute_js(js, logger)
        cookie_list = result2.split('=', 1)
        cookie_dict = {
            cookie_list[0]: cookie_list[1].split(';')[0]
        }
        requests.utils.add_dict_to_cookiejar(session.cookies, cookie_dict)
        logger.info(u'破解企信网js完成，破解结果：{}'.format(cookie_dict))
        return cookie_dict
    except Exception as e:
        logger.error(u'企信网破解521失败，js： {}， 原因: {}'.format(js_521, str(e)))




def invalid_link(html):
    """
    断言页面出现非法图片
    :param html:
    :return:
    """
    if re.findall(r'window\.location\.href.+?index/invalidLink', html, flags=re.S):
        logger.warning(u'页面出现调整不合法链接,切换代理重试， html为{}'.format(html))
        return False
    return True



@retry(exceptions=RuntimeError, tries=3, delay=3, logger=logger)
def update_complete(company_uuid) :
    gsxt_db = CdrcbDb('gsxt_test')
    sql = "update gsxt_company set complete=1 where company_uuid='%s'" % company_uuid
    if gsxt_db.execSql(sql):
        logger.info(u'更新complete成功')
    else:
        logger.error(u"更新complete失败, sql: {}".format(sql))



def get_pictures():
    logger.info(u'开始请求图片')
    for pic in image_uri_list:
        url = '{}{}'.format(host, pic)
        send_request("get", url, data=None,  no_context=True, is_json=False)


def send_request(method, url, data=None, is_json=True, no_context=False, cache_key_switch=True, invalid_cache_key='0_0'):
    retry_key_list = [
        'on_content',
        'status_521',
        'status_gt_400',
        'invalid_link',
        'page_not_found',
        'too_busy',
        'is_not_json',
        'invalid_cache_key_0_0',
        'dos_attack',
    ]

    if no_context:  # 可以不包含html，就剔除该检测
        retry_key_list.pop(retry_key_list.index('on_content'))

    if not is_json:
        retry_key_list.pop(retry_key_list.index('is_not_json'))
        retry_key_list.pop(retry_key_list.index('invalid_cache_key_0_0'))

    if not cache_key_switch:
        retry_key_list.pop(retry_key_list.index('invalid_cache_key_0_0'))

    if method.lower() == "get":
        resp = downloader.get(
            headers=headers,
            params=data,
            url=url,
            timeout=20,
            retry_keys=retry_key_list,
            meta={}
        )
    elif method.lower() == "post":
        resp = downloader.post(
            headers=headers,
            url=url,
            data=data,
            timeout=20,
            retry_keys=retry_key_list,
            meta={}
        )
    else:
        logger.info(u'请求方法不支持')
        return
    return resp


def refresh_cookie(js_521):
    get_cookies_for_requests(downloader._session, js_521)


def get_total_page(html):
    """
    获取总页码
    :param html:
    :return:
    """
    page_list = []
    try:
        page_json = json.loads(html)
        total_page = page_json.get('totalPage', 0)
        page_list = range(1, int(total_page) + 1)
    except Exception as e:
        logger.info(u'获取总页数失败, {}'.format(str(e)))
    logger.info(u'总页数列表, {}'.format(page_list))
    return page_list


def get_xqid_list(html, key_name):
    """
    获取详情id列表 "invId"
    :param html:
    :return:
    """
    try:
        collection = []
        res_list = json.loads(html)
        for item in res_list['data']:
            xq_id = item.get(key_name)
            if xq_id:
                collection.append(xq_id)
        return collection
    except Exception as e:
        logger.warning(u'获取股东详情id失败, {}'.format(str(e)))


def insert_page_json(page_dict):
    company_name = page_dict.get('company_name')
    company_key = page_dict['seed_dict'].get("company_key")
    company_zch = page_dict.get('company_zch')
    insert_mysql("gsxt_page_json", {"company_uuid": uuid.uuid1().hex,
                                      "source_id": uuid.uuid1().hex,
                                      "task_id": page_dict['seed_dict']["task_id"],
                                      "company_name": company_name,
                                      "company_key": company_key,
                                      "company_zch": company_zch,
                                      "page_sources": json.dumps(page_dict, ensure_ascii=False),
                                      "create_time": now_time()})


def insert_error_record(page_dict, value_dict):
    error_type = page_dict.get("status")
    company_key = value_dict.get('seed_dict').get("company_key")
    # sql = "insert into gsxt_error_record (company_key, create_time, error_type) "
    # sql = sql + "values ({}, {}, {})".format(company_key, now_time(), error_type)
    insert_mysql("gsxt_error_record", {"company_key": company_key,
                                        "error_type": error_type,
                                        "create_time": now_time()
                                       }
                 )

def now_time():
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now_time


if __name__ == '__main__':
    session = ''
    get_cookies_for_requests(session, open('js.txt').read())

