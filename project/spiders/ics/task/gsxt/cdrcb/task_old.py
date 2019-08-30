#!/usr/bin/env python
# -*- coding: utf-8 -*-
from retry import retry

from ics.scheduler.new_task import StableTask
from ics.utils import get_ics_logger
from ics.utils.decorator import stable
from ics.utils.exception_util import LogicException

__author__ = 'MaoJingwen'

import requests
from celery.utils.log import get_task_logger
from urllib import quote
from bs4 import BeautifulSoup as bs

import inspect
import traceback
import time
import json
import random
import sys
import re
import uuid
import datetime

from ics.scheduler import app
from ics.utils.chrome import get_chrome_web_driver
from ics.proxy import get_proxy_for_phantom_test, get_proxy_for_phantom, get_proxy_from_zm
from ics.utils.cookie import formart_selenium_cookies, cookiejar_from_dict, selenium_add_cookies
from ics.captcha.jyc2567.crack import get_validate
from ics.task.gsxt.mysql_pool import mysql_pool
from ics.utils.db import CdrcbDb

logger = get_ics_logger(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')

# m_proxy = {"http": "http://%s:%s" % ('127.0.0.1', '8888'),
#            "https": "http://%s:%s" % ('127.0.0.1', '8888')}

DATA = 'draw=%s&start=%s&length=5'

task_queue = "task_queue"
RETRY_CNT = 20


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=RETRY_CNT, rate_limit='120/m', ignore_result=True)
@stable(LogicException, logger=logger)
# @retry(exceptions=LogicException, tries=10, delay=1, logger=logger)
def init(keyword):
    logger.info(u'开始抓取，搜索种子为: {}'.format(keyword))
    # ip, port, m_proxy = get_proxy_for_phantom_test()
    # ip, port, m_proxy = get_proxy_from_zm()
    ip, port, m_proxy = get_proxy_for_phantom()
    logger.info(u'取得代理为: {}:{}'.format(ip, port))
    cookies, web = from_webdriver_get_cookies(ip, port)
    if not cookies :
        """
        restart -> change proxy
        """
        raise LogicException("no cookies!!!")

    headers = dict()
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
    headers['Referer'] = 'http://www.gsxt.gov.cn/index.html'
    headers['X-Requested-With'] = 'XMLHttpRequest'

    session = get_session()

    session.cookies = cookiejar_from_dict(cookies, 'www.gsxt.gov.cn')

    # 打码
    try:
        logger.info(u'开始打码')
        validate = get_validate(session, headers, m_proxy)
        logger.info(u'打码完成, 结果为: {}'.format(validate))
    except ValueError as e:
        web.quit()
        err_msg = u'打码失败, 结果为: {}, 准备重试'.format(str(e))
        logger.info(err_msg)
        raise LogicException(err_msg)

    except Exception as e:
        web.quit()
        err_msg = u'打码失败, 结果为: {}, 准备重试'.format(str(e))
        logger.info(err_msg)
        raise LogicException(err_msg)

    headers = dict()
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Origin'] = 'http://www.gsxt.gov.cn'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['Cache-Control'] = 'max-age=0'
    headers['Referer'] = 'http://www.gsxt.gov.cn/index.html'

    time.sleep(2)
    token = str(random.randint(100000000, 999999999))
    try :
        resHtml = session.post(
            headers=headers,
            url='http://www.gsxt.gov.cn/corp-query-search-1.html',
            data='tab=ent_tab&province=&geetest_challenge={0}&geetest_validate={1}&geetest_seccode={1}%7Cjordan&token={2}&searchword={3}'
                .format(validate['challenge'], validate['validate'], token, quote(keyword.encode('utf8'))),
            proxies=m_proxy
        ).content
    except Exception as e:
        err_msg = u"获取搜索列表页面失败, 原因: {}".format(traceback.format_exc())
        logger.error(err_msg)
        web.quit()
        raise LogicException(err_msg)

    time.sleep(2)
    soup = bs(resHtml, 'lxml')
    company_uuid = uuid.uuid1().__str__()
    source_id = uuid.uuid1().__str__()
    insert_mysql("gsxt_company", {"company_name": keyword,
                                  "company_uuid": company_uuid,
                                  "source_id": source_id,
                                  "create_time": now_time()})

    # 暂时只取第一条记录
    _url = soup.select('a.search_list_item.db')
    history_name = ""
    if _url.__len__() > 0 :
        has_history = _url[0].select('div.div-info-circle3 span.g3')
        url = 'http://www.gsxt.gov.cn' + _url[0]['href']

        if has_history:
            history_name = has_history[0].text.strip()

    else :
        logger.info("This keyword : " + keyword + " No result!!!!")
        web.quit()
        logger.info(u'种子搜索结果为空, 结束搜索， 种子为: {}'.format(keyword))
        return

    refer = url
    try :
        web.get(url)
    except:
        err_msg = u"请求基本信息页面失败， 原因: {}".format(traceback.format_exc())
        logger.error(err_msg)
        web.quit()
        raise LogicException(err_msg)

    time.sleep(2)
    resHtml = web.execute_script("return document.documentElement.outerHTML")

    insert_mysql("gsxt_home", {"page_source": resHtml,
                               "company_uuid": company_uuid,
                               "history_name": history_name,
                               "source_id": source_id,
                               "create_time": now_time()})
    soup = bs(resHtml, 'lxml')
    ent_type = soup.select('input#entType')[0]['value']
    sc = soup.select('div.mainContent script')[0].text.strip()

    sc = '{' + sc.replace('var ', '\'') \
        .replace(' ', '') \
        .replace('=\"', '\':\'') \
        .replace('%7D\"', '%7D\',') \
        .replace(';', '') \
        .replace('\"', '\',') \
        .strip(',') + '}'

    # 详细地址信息列表
    url_dict = eval(sc)

    cookies = formart_selenium_cookies(web.get_cookies())

    web.quit()


    # 股东及出资信息/发起人及出资信息 post
    download_share_holder(url_dict['shareholderUrl'], cookies, refer, m_proxy, company_uuid, source_id)
    # app.send_task('ics.task.gsxt.task.download_share_holder', [url_dict['shareholderUrl'], cookies, refer, m_proxy, company_uuid], queue='task_queue', priority=99)
    # download_share_holder.apply_async(args=(url_dict['keyPersonUrl'], cookies, refer, m_proxy, company_uuid), queue='task_queue', priority=99)

    # 主要人员信息 get
    if '16' == ent_type :
        keyPersonUrl = url_dict['gtKeyPersonUrl']
        alterInfoUrl = url_dict['gtAlertInfoUrl']
    else :
        keyPersonUrl = url_dict['keyPersonUrl']
        alterInfoUrl = url_dict['alterInfoUrl']

    download_key_person(keyPersonUrl, cookies, refer, m_proxy, company_uuid, url_dict, source_id)

    # 变更信息 post
    download_alter_info(alterInfoUrl, cookies, refer, m_proxy, company_uuid, source_id)

    # 清算信息 get
    download_liquidation(url_dict['liquidationUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 双随机抽查结果信息 get
    download_getDrRaninsResUrl(url_dict['getDrRaninsResUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 分支机构信息 get
    download_branch(url_dict['branchUrl'], cookies, refer, m_proxy, company_uuid, url_dict, source_id)

    time.sleep(3)
    # # 动产抵押登记信息 post
    # download_mort_reg_info(url_dict['mortRegInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 股权出质登记信息 post
    temp = download_stak_qualit(url_dict['stakQualitInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 知识产权出质登记信息 post
    download_pro_pledge_reg_info(url_dict['proPledgeRegInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 商标注册信息  get
    download_trade_mark(url_dict['trademarkInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 抽查检查结果信息 post
    download_spot_check_info(url_dict['spotCheckInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 司法协助信息 post
    download_assist(url_dict['assistUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    time.sleep(3)
    # 企业年报信息 get
    # download_anche_year(url_dict['anCheYearInfo'], cookies, refer, m_proxy, company_uuid, source_id)

    # 股东及出资信息 post
    download_ins_Inv(url_dict['insInvinfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 股权变更信息 post
    download_ins_alter_stock(url_dict['insAlterstockinfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 行政许可信息  post
    download_ins_licence(url_dict['insLicenceinfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 知识产权出质登记信息  post
    download_ins_Pro_Pledge_Reg(url_dict['insProPledgeRegInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 行政处罚信息  post
    download_ins_Punishment(url_dict['insPunishmentinfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 企业简易注销公告信息  get
    download_simple_cancel(url_dict['simpleCancelUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 行政许可信息 POST
    download_other_licence_detail(url_dict['otherLicenceDetailInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 行政处罚信息 POST
    download_punishment_detail(url_dict['punishmentDetailInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    entBusExcepUrl = getJyycKey(ent_type)
    # 列入经营异常名录信息 POST
    download_ent_bus_excep_detail(entBusExcepUrl, cookies, refer, m_proxy, company_uuid, source_id)

    # 列入严重违法失信企业名单（黑名单）信息 POST
    download_Ill_detail(url_dict['IllInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    # 动产抵押登记信息 post
    download_mort_reg_info(url_dict['mortRegInfoUrl'], cookies, refer, m_proxy, company_uuid, source_id)

    update_complete(company_uuid)

def from_webdriver_get_cookies(ip , port):
    web = get_chrome_web_driver(ip, port)
    web.implicitly_wait(20)
    print "go home page"
    web.get("http://www.gsxt.gov.cn/index.html")
    time.sleep(3)
    cookies = formart_selenium_cookies(web.get_cookies())
    if cookies.has_key("JSESSIONID"):
        JSESSIONID = cookies.get("JSESSIONID").replace("n1:0", "n1:-1")
        cookies["JSESSIONID"] = JSESSIONID
    # requests.utils.add_dict_to_cookiejar()
    return cookies, web

@app.task
def download_other_licence_detail(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()
    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage :
        logger.info(u'other_licence_detail response不合法:{}'.format(resHtml))
    else :
        insert_mysql("gsxt_otherlicencedetailinfo", {"page_source": resHtml,
                                                      "company_uuid": company_uuid,
                                                     "source_id": source_id,
                                                      "create_time": now_time()})
        logger.info(u'other_licence_detail 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'other_licence_detail response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_otherlicencedetailinfo", {"page_source": resHtml,
                                                         "company_uuid": company_uuid,
                                                         "source_id": source_id,
                                                         "create_time": now_time()})
            logger.info(u'other_licence_detail 原文为：{}'.format(resHtml))

@app.task
def download_punishment_detail(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'punishment_detail response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_punishmentdetailinfo", {"page_source": resHtml,
                                                     "company_uuid": company_uuid,
                                                   "source_id": source_id,
                                                   "create_time": now_time()})
        logger.info(u'punishment_detail 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'punishment_detail response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_punishmentdetailinfo", {"page_source": resHtml,
                                                       "company_uuid": company_uuid,
                                                       "source_id": source_id,
                                                       "create_time": now_time()})
            logger.info(u'punishment_detail 原文为：{}'.format(resHtml))


@app.task
def download_getDrRaninsResUrl(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "get"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    data = data.replace("length=5", "length=10")
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)

    if not response and not totalPage:
        logger.info(u'getDrRaninsResUrl response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_drraninsres", {"page_source": resHtml,
                                          "company_uuid": company_uuid,
                                          "create_time": now_time()})
        logger.info(u'getDrRaninsResUrl 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'getDrRaninsResUrl response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_drraninsres", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                              "create_time": now_time()})
        logger.info(u'getDrRaninsResUrl 原文为：{}'.format(resHtml))

@app.task
def download_ent_bus_excep_detail(url, cookies, refer, m_proxy, company_uuid, source_id):
    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if response.get("cacheKey")=="0_0":
        retry_get_pictures(m_proxy, cookies)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)

    if not response and not totalPage:
        logger.info(u'ent_bus_excep_detail response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_entbusexcep", {"page_source": resHtml,
                                           "company_uuid": company_uuid,
                                           "create_time": now_time()})
        logger.info(u'ent_bus_excep_detail 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if response.get("cacheKey") == "0_0":
            retry_get_pictures(m_proxy, cookies)
            resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
            response, totalPage = str_to_json(resHtml, func_name)

        if not response and not totalPage:
            logger.info(u'ent_bus_excep_detail response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_entbusexcep", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                              "create_time": now_time()})
            logger.info(u'ent_bus_excep_detail 原文为：{}'.format(resHtml))

@app.task
def download_Ill_detail(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'Ill_detail response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_illinfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "create_time": now_time()})
        logger.info(u'Ill_detail 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'Ill_detail response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_illinfo", {"page_source": resHtml,
                                          "company_uuid": company_uuid,
                                          "create_time": now_time()})

            logger.info(u'Ill_detail 原文为：{}'.format(resHtml))

@app.task
def download_share_holder(url, cookies, refer, m_proxy, company_uuid, source_id):
    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()
    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    share_holder_detail(response, cookies, refer, m_proxy, company_uuid, source_id)
    if not response and not totalPage :
        logger.info(u'share_holder response不合法:{}'.format(resHtml))
    else :
        insert_mysql("gsxt_shareholder", {"page_source": resHtml,
                                          "company_uuid": company_uuid,
                                          "source_id": source_id,
                                          "create_time": now_time()})
        logger.info(u'share_holder 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(10.1)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        share_holder_detail(response, cookies, refer, m_proxy, company_uuid, source_id)
        if not response and not totalPage:
            logger.info(u'share_holder response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_shareholder", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                              "source_id": source_id,
                                              "create_time": now_time()})
            logger.info(u'share_holder 原文为：{}'.format(resHtml))


def share_holder_detail(response, cookies, refer, m_proxy, company_uuid, source_id) :
    func_name = get_func_name()
    datas = response.get("data")
    detail_url = "/corp-query-entprise-info-shareholderDetail-%s.html"

    for data in datas :

        detailCheck = data.get("detailCheck")
        if detailCheck == "true":
            time.sleep(5.1)
            invId = data.get("invId")
            url = detail_url % invId
            resHtml = send_request("get", url, None, refer, cookies, m_proxy, func_name)
            insert_mysql("gsxt_shareholder_detail", {"page_source": resHtml,
                                                      "company_uuid": company_uuid,
                                                      "source_id": source_id,
                                                      "create_time": now_time()})
            print "share_holder_detail: " + resHtml
@app.task
def download_key_person(url, cookies, refer, m_proxy, company_uuid, url_dict, source_id):
    """
    主要人员换信息翻页与分支机构类似。
    翻页之后第一页与首页显示一样。
    所以翻页应该尽可能的直接取第二页。
    """
    mothed = "get"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, None, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)

    if not response and not totalPage:
        logger.info(u'key_person response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_keyperson", {"page_source": resHtml,
                                          "company_uuid": company_uuid,
                                        "source_id": source_id,
                                          "create_time": now_time()})
        logger.info(u'key_person 原文为：{}'.format(resHtml))

    if totalPage > 1 :
        keyPersonAllUrl = url_dict.get("keyPersonAllUrl")
        keyPersonAll_Html = send_request("get", keyPersonAllUrl, None, refer, cookies, m_proxy, func_name)
        soup = bs(keyPersonAll_Html, 'lxml')
        sc = soup.select('div.mainContent script')[0].text.strip()
        keyPersonUrlData = re.search('var keyPersonUrlData =\"(.*?)\";', sc).group(1)
        all_key_person(keyPersonUrlData, cookies, refer, m_proxy, company_uuid, url_dict, totalPage, source_id)

def all_key_person(url, cookies, refer, m_proxy, company_uuid, url_dict, totalPage, source_id):
    func_name = get_func_name()
    data = "start=%s"
    page = 1

    while page < totalPage :
        data = data % (page * 16)
        page = page + 1
        resHtml = send_request("get", url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'key_person response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_keyperson", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                            "source_id": source_id,
                                              "create_time": now_time()})
        logger.info(u'key_person 原文为：{}'.format(resHtml))
        time.sleep(2)

@app.task
def download_liquidation(url, cookies, refer, m_proxy, company_uuid, source_id):
    mothed = "get"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'liquidation response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_liquidation", {"page_source": resHtml,
                                            "company_uuid": company_uuid,
                                          "source_id": source_id,
                                            "create_time": now_time()})
        logger.info(u'liquidation 原文为：{}'.format(resHtml))

    while draw < totalPage and response.get('data'):
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'liquidation response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_liquidation", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                              "source_id": source_id,
                                              "create_time": now_time()})
            logger.info(u'liquidation 原文为：{}'.format(resHtml))

@app.task
def download_branch(url, cookies, refer, m_proxy, company_uuid, url_dict, source_id):

    mothed = "get"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'branch response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_branch", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                     "source_id": source_id,
                                      "create_time": now_time()})
        logger.info(u'branch 原文为：{}'.format(resHtml))

    if totalPage > 1 :
        keyPersonAllUrl = url_dict.get("branchAllUrl")
        keyPersonAll_Html = send_request("get", keyPersonAllUrl, None, refer, cookies, m_proxy, func_name)
        soup = bs(keyPersonAll_Html, 'lxml')
        sc = soup.select('div.mainContent script')[0].text.strip()
        branchUrlData = re.search('var branchUrlData =\"(.*?)\";', sc).group(1)
        all_branch_person_detail(branchUrlData, cookies, refer, m_proxy, company_uuid, url_dict, totalPage, source_id)

def all_branch_person_detail(url, cookies, refer, m_proxy, company_uuid, url_dict, totalPage, source_id):
    func_name = get_func_name()
    data = "start={}"
    page = 1

    while page < totalPage :
        temp = data.format(page * 9)
        page = page + 1
        time.sleep(3)
        resHtml = send_request("get", url, temp, refer, cookies, m_proxy, func_name)
        response, _ = str_to_json(resHtml, func_name)

        if not response and not _:
            logger.info(u'branch_person_detail response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_branch", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                         "source_id": source_id,
                                              "create_time": now_time()})
        logger.info(u'branch_person_detail 原文为：{}'.format(resHtml))

@app.task
def download_alter_info(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)

    if response.get("cacheKey")=="0_0":
        retry_get_pictures(m_proxy, cookies)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)

    if not response and not totalPage:
        logger.info(u'alter_info response不合法:{}'.format(resHtml))
        # raise LogicException(u'变更信息页面response不合法:{}, 重试'.format(resHtml))
    else:
        insert_mysql("gsxt_alterinfo", {"page_source": resHtml,
                                     "company_uuid": company_uuid,
                                        "source_id": source_id,
                                     "create_time": now_time()})

        logger.info(u'alter_info 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(1.5)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)

        if response.get("cacheKey") == "0_0":
            retry_get_pictures(m_proxy, cookies)
            resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
            response, totalPage = str_to_json(resHtml, func_name)

        if not response and not totalPage:
            logger.info(u'alter_info response不合法:{}'.format(resHtml))
            # raise LogicException(u'变更信息页面response不合法:{}, 重试'.format(resHtml))
        else:
            insert_mysql("gsxt_alterinfo", {"page_source": resHtml,
                                            "company_uuid": company_uuid,
                                            "source_id": source_id,
                                            "create_time": now_time()})
        logger.info(u'alter_info 原文为：{}'.format(resHtml))

@app.task
def download_mort_reg_info(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()
    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    time.sleep(3.1)
    response, totalPage = str_to_json(resHtml, func_name)
    mort_reg_detail(response, cookies, refer, m_proxy, company_uuid, source_id)
    if not response and not totalPage:
        logger.info(u'mort_reg_inforesponse不合法 {}'.format(resHtml))
        # raise LogicException(u'mort_reg_inforesponse不合法:{}, 重试'.format(resHtml))
    else:
        insert_mysql("gsxt_mortreginfo", {"page_source": resHtml,
                                            "company_uuid": company_uuid,
                                          "source_id": source_id,
                                            "create_time": now_time()})
    logger.info(u'gsxt_mortreginfo 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(5.1)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        mort_reg_detail(response, cookies, refer, m_proxy, company_uuid, source_id)

        if not response and not totalPage:
            logger.info(u'gsxt_mortreginfo response不合法 {}'.format(resHtml))
        else :
            insert_mysql("gsxt_mortreginfo", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                              "source_id": source_id,
                                              "create_time": now_time()})
        logger.info(u'gsxt_mortreginfo 原文为：{}'.format(resHtml))


def mort_reg_detail(response, cookies, refer, m_proxy, company_uuid, source_id) :
    datas = response.get("data")
    for data in datas :
        morReg_Id = data.get("morReg_Id")
        if morReg_Id :
            mort_reg_regpersoninfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id)
            time.sleep(15)
            mort_reg_creditorRightInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id)
            time.sleep(15)
            mort_reg_guaranteeInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id)
            time.sleep(15)
            mort_reg_regCancelInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id)
            time.sleep(15)
            mort_reg_altItemInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id)
        time.sleep(15)

def mort_reg_regpersoninfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id) :
    regpersoninfo_url = "/corp-query-entprise-info-mortregpersoninfo-%s.html" % morReg_Id
    func_name = get_func_name()
    resHtml = send_request("get", regpersoninfo_url, None, refer, cookies, m_proxy, func_name)
    print "mort_reg_regpersoninfo: " + resHtml

    if "<script>" in resHtml :
        _cookies, web = from_webdriver_get_cookies()
        web.quit()
        resHtml = send_request("get", regpersoninfo_url, None, refer, _cookies, m_proxy, func_name)

    insert_mysql("gsxt_mortreg_regpersoninfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "create_time": now_time()})

def mort_reg_creditorRightInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id) :
    CreditorRightInfo_url = "/corp-query-entprise-info-mortCreditorRightInfo-%s.html" % morReg_Id
    func_name = get_func_name()
    resHtml = send_request("get", CreditorRightInfo_url, None, refer, cookies, m_proxy, func_name)
    print "mort_reg_creditorRightInfo: " + resHtml

    if "<script>" in resHtml :
        _cookies, web = from_webdriver_get_cookies()
        web.quit()
        resHtml = send_request("get", CreditorRightInfo_url, None, refer, _cookies, m_proxy, func_name)

    insert_mysql("gsxt_mortreg_creditorrightinfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "create_time": now_time()})


def mort_reg_guaranteeInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id) :
    GuaranteeInfo_url = "/corp-query-entprise-info-mortGuaranteeInfo-%s.html" % morReg_Id
    func_name = get_func_name()
    resHtml = send_request("get", GuaranteeInfo_url, None, refer, cookies, m_proxy, func_name)
    print "mort_reg_guaranteeInfo: " + resHtml

    if "<script>" in resHtml :
        _cookies, web = from_webdriver_get_cookies()
        web.quit()
        resHtml = send_request("get", GuaranteeInfo_url, None, refer, _cookies, m_proxy, func_name)

    insert_mysql("gsxt_mortreg_guaranteeinfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "create_time": now_time()})


def mort_reg_regCancelInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id):
    RegCancelInfo = "/corp-query-entprise-info-getMortRegCancelInfo-%s.html" % morReg_Id
    func_name = get_func_name()
    resHtml = send_request("get", RegCancelInfo, None, refer, cookies, m_proxy, func_name)
    print "mort_reg_regCancelInfo: " + resHtml

    if "<script>" in resHtml:
        _cookies, web = from_webdriver_get_cookies()
        web.quit()
        resHtml = send_request("get", RegCancelInfo, None, refer, _cookies, m_proxy, func_name)

    insert_mysql("gsxt_mortreg_regcancelinfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "create_time": now_time()})

def mort_reg_altItemInfo(cookies, refer, m_proxy, company_uuid, morReg_Id, source_id) :
    AltItemInfo = "/corp-query-entprise-info-getMortAltItemInfo-%s.html" % morReg_Id
    func_name = get_func_name()
    resHtml = send_request("get", AltItemInfo, None, refer, cookies, m_proxy, func_name)
    print "mort_reg_altItemInfo: " + resHtml

    if "<script>" in resHtml :
        _cookies, web = from_webdriver_get_cookies()
        web.quit()
        resHtml = send_request("get", AltItemInfo, None, refer, _cookies, m_proxy, func_name)

    insert_mysql("gsxt_mortreg_altiteminfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "create_time": now_time()})

@app.task
def download_stak_qualit(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'stak_qualit response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_stakqualitinfo", {"page_source": resHtml,
                                          "company_uuid": company_uuid,
                                             "source_id": source_id,
                                          "create_time": now_time()})
    logger.info(u'stak_qualit 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'stak_qualit response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_stakqualitinfo", {"page_source": resHtml,
                                                 "company_uuid": company_uuid,
                                                 "source_id": source_id,
                                                 "create_time": now_time()})
        logger.info(u'stak_qualit 原文为：{}'.format(resHtml))

@app.task
def download_pro_pledge_reg_info(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'pro_pledge_reg_info response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_inspropledgereginfo", {"page_source": resHtml,
                                             "company_uuid": company_uuid,
                                                  "source_id": source_id,
                                             "create_time": now_time()})
    logger.info(u'pro_pledge_reg_info 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'pro_pledge_reg_info response不合法:{}'.format(resHtml))
        else :
            insert_mysql("gsxt_inspropledgereginfo", {"page_source": resHtml,
                                                      "company_uuid": company_uuid,
                                                      "source_id": source_id,
                                                      "create_time": now_time()})
        logger.info(u'pro_pledge_reg_info 原文为：{}'.format(resHtml))

@app.task
def download_trade_mark(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "get"
    start = 0
    i = 1
    data = ""
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)

    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'trade_mark response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_trademarkinfo", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                            "source_id": source_id,
                                              "create_time": now_time()})
    logger.info(u'trade_mark 原文为：{}'.format(resHtml))

    while i < totalPage:
        start = i * 4
        data = "&start=%s" % start
        time.sleep(2)
        i = i + 1
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'trade_mark response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_trademarkinfo", {"page_source": resHtml,
                                                "company_uuid": company_uuid,
                                                "source_id": source_id,
                                                "create_time": now_time()})
        logger.info(u'trade_mark 原文为：{}'.format(resHtml))

@app.task
def download_spot_check_info(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'spot_check_info response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_spotcheckinfo", {"page_source": resHtml,
                                            "company_uuid": company_uuid,
                                            "source_id": source_id,
                                            "create_time": now_time()})
    logger.info(u'spot_check_info 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'spot_check_info response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_spotcheckinfo", {"page_source": resHtml,
                                                "company_uuid": company_uuid,
                                                "source_id": source_id,
                                                "create_time": now_time()})
        logger.info(u'spot_check_info 原文为：{}'.format(resHtml))

@app.task
def download_assist(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()
    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'assist response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_assist", {"page_source": resHtml,
                                    "company_uuid": company_uuid,
                                     "source_id": source_id,
                                    "create_time": now_time()})
    logger.info(u'assist 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'assist response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_assist", {"page_source": resHtml,
                                         "company_uuid": company_uuid,
                                         "source_id": source_id,
                                         "create_time": now_time()})
        logger.info(u'assist 原文为：{}'.format(resHtml))

@app.task
def download_anche_year(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "get"
    data = ""
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    # try :
    #     _resHtml = resHtml.replace("null", "''")
    #     anche_year_list = eval(_resHtml)
    # except ValueError as e:
    #     logger.error("transform error !!! func_name is :" + func_name + " resopone is :" + resHtml.__str__() + " error_info :" + traceback.format_exc())
    #     raise LogicException('anche_year 下载失败, 重试: {}'.format(str(e)))
    # except Exception as e:
    #     logger.error("New error !!! func_name is :" + func_name + " resopone is :" + resHtml.__str__() + " error_info :" + traceback.format_exc())
    #     raise LogicException('anche_year 下载失败, 重试: {}'.format(str(e)))

    insert_mysql("gsxt_ancheyear", {"page_source": resHtml,
                                 "company_uuid": company_uuid,
                                    "source_id": source_id,
                                 "create_time": now_time()})
    logger.info(u'anche_year 原文为：{}'.format(resHtml))

    # deal_anche_year(resHtml, mothed, url, refer, cookies, m_proxy)

@app.task
def download_ins_Inv(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()
    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'ins_Inv response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_insinvinfo", {"page_source": resHtml,
                                        "company_uuid": company_uuid,
                                         "source_id": source_id,
                                        "create_time": now_time()})
    logger.info(u'ins_Inv 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'ins_Inv response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_insinvinfo", {"page_source": resHtml,
                                             "company_uuid": company_uuid,
                                             "source_id": source_id,
                                             "create_time": now_time()})
        logger.info(u'ins_Inv 原文为：{}'.format(resHtml))

@app.task
def download_ins_alter_stock(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'ins_alter_stock response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_insalterstockinfo", {"page_source": resHtml,
                                        "company_uuid": company_uuid,
                                                "source_id": source_id,
                                        "create_time": now_time()})
    logger.info(u'ins_alter_stock 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'ins_alter_stock response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_insalterstockinfo", {"page_source": resHtml,
                                                    "company_uuid": company_uuid,
                                                    "source_id": source_id,
                                                    "create_time": now_time()})
        logger.info(u'ins_alter_stock 原文为：{}'.format(resHtml))

@app.task
def download_ins_licence(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'ins_licence response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_inslicenceinfo", {"page_source": resHtml,
                                                "company_uuid": company_uuid,
                                             "source_id": source_id,
                                                "create_time": now_time()})
    logger.info(u'ins_licence 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'ins_licence response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_inslicenceinfo", {"page_source": resHtml,
                                                    "company_uuid": company_uuid,
                                                 "source_id": source_id,
                                                    "create_time": now_time()})
        logger.info(u'ins_licence 原文为：{}'.format(resHtml))

@app.task
def download_ins_Pro_Pledge_Reg(url, cookies, refer, m_proxy, company_uuid, source_id):

    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'ins_Pro_Pledge_Reg response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_propledgereginfo", {"page_source": resHtml,
                                                "company_uuid": company_uuid,
                                               "source_id": source_id,
                                                "create_time": now_time()})
    logger.info(u'ins_Pro_Pledge_Reg 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'ins_Pro_Pledge_Reg response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_propledgereginfo", {"page_source": resHtml,
                                                   "company_uuid": company_uuid,
                                                   "source_id": source_id,
                                                   "create_time": now_time()})
        logger.info(u'ins_Pro_Pledge_Reg 原文为：{}'.format(resHtml))

@app.task
def download_ins_Punishment(url, cookies, refer, m_proxy, company_uuid, source_id):
    
    mothed = "post"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()
    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)

    if response.get("cacheKey") == "0_0":
        retry_get_pictures(m_proxy, cookies)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'ins_Punishment response不合法:{}'.format(resHtml))
    else:
        insert_mysql("gsxt_inspunishmentinfo", {"page_source": resHtml,
                                               "company_uuid": company_uuid,
                                                "source_id": source_id,
                                               "create_time": now_time()})
    logger.info(u'ins_Punishment 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)

        if response.get("cacheKey") == "0_0":
            retry_get_pictures(m_proxy, cookies)
            resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
            response, totalPage = str_to_json(resHtml, func_name)

        if not response and not totalPage:
            logger.info(u'ins_Punishment response不合法:{}'.format(resHtml))
        else:
            insert_mysql("gsxt_inspunishmentinfo", {"page_source": resHtml,
                                                    "company_uuid": company_uuid,
                                                    "source_id": source_id,
                                                    "create_time": now_time()})
        logger.info(u'ins_Punishment 原文为：{}'.format(resHtml))

@app.task
def download_simple_cancel(url, cookies, refer, m_proxy, company_uuid, source_id):
    mothed = "get"
    draw = 1
    start = 0
    data = DATA % (draw, start)
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
    response, totalPage = str_to_json(resHtml, func_name)
    if not response and not totalPage:
        logger.info(u'simple_cancel 原文为：{}'.format(resHtml))
    else:
        insert_mysql("gsxt_simplecancel", {"page_source": resHtml,
                                            "company_uuid": company_uuid,
                                           "source_id": source_id,
                                            "create_time": now_time()})
    logger.info(u'simple_cancel 原文为：{}'.format(resHtml))

    while draw < totalPage:
        draw = draw + 1
        start = start + 5
        data = DATA % (draw, start)
        time.sleep(2)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        response, totalPage = str_to_json(resHtml, func_name)
        if not response and not totalPage:
            logger.info(u'simple_cancel 原文为：{}'.format(resHtml))
        else:
            insert_mysql("gsxt_simplecancel", {"page_source": resHtml,
                                               "company_uuid": company_uuid,
                                               "source_id": source_id,
                                               "create_time": now_time()})
        logger.info(u'simple_cancel 原文为：{}'.format(resHtml))


def get_header(refer):
    headers = dict()
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Referer'] = refer
    headers['Origin'] = 'http://www.gsxt.gov.cn'
    return headers

def str_to_json(json_str, func_name):
    try:
        data = json.loads(json_str)
        totalPage = data.get("totalPage")
        return data, totalPage
    except ValueError as e:
        logger.error("transform error !!! func_name is :" +  func_name + " resopone is :" + json_str.__str__() + " error_info :" + traceback.format_exc())
    except Exception as e:
        logger.error("New error !!! func_name is :" + func_name + " resopone is :" + json_str.__str__() + " error_info :" + traceback.format_exc())
    return False, False

# @retry(exceptions=LogicException, tries=3, delay=1, logger=logger)
def send_request(mothed, url, data, refer, cookies, m_proxy, func_name):
    session = get_session()
    session.cookies = cookiejar_from_dict(cookies, 'www.gsxt.gov.cn')
    headers = get_header(refer)
    try :
        if mothed=="get":
            resHtml = session.get(
                headers=headers,
                params = data,
                url='http://www.gsxt.gov.cn' + url,
                proxies=m_proxy
            ).content

        if mothed=="post":
            resHtml = session.post(
                headers=headers,
                url='http://www.gsxt.gov.cn' + url,
                data=data,
                proxies=m_proxy
            ).content

    except Exception as e :
        logger.error("func_name:" + func_name + " send_request func error info " + traceback.format_exc())
        return 0

    return resHtml

def retry_get_pictures(m_proxy, cookies) :
    icon4 = "/image/icon4.jepg"
    icon3 = "/image/icon3.jepg"
    icon2 = "/image/icon2.jepg"
    circle1 = "/image/circle1.jepg"
    user1 = "/image/user1.jepg"
    map1 = "/image/map1.jepg"
    pictures = [icon4, icon3, icon2, circle1, user1, map1]

    print "retry in get picture"
    for pic in pictures :
        send_request("get", pic, None, "http://www.gsxt.gov.cn/", cookies, m_proxy, "retry_get_pictures")

def deal_anche_year(resHtml, mothed, url, refer, cookies, m_proxy, source_id):
    _resHtml = resHtml.replace("null", "''")
    anche_year_list = eval(_resHtml)
    func_name = get_func_name()

    for anche_year in anche_year_list:
        anCheId = anche_year.get("anCheId")
        anCheYear = anche_year.get("anCheYear")
        entType = 1
        data = "anCheId=%s&entType=%s&anCheYear=%s" % (anCheId, entType, anCheYear)
        resHtml = send_request(mothed, url, data, refer, cookies, m_proxy, func_name)
        print "deal_anche_year: " + resHtml
        time.sleep(3)


@retry(exceptions=RuntimeError, tries=3, delay=1, logger=logger)
def insert_mysql(table, model):
    logger.info(u'开始保存数据，table：{}'.format(table))
    db = mysql_pool.connection()
    logger.info('')
    cursor = db.cursor()

    qmarks = ', '.join(['%s'] * len(model))  # 用于替换记录值
    cols = ', '.join(model.keys())  # 字段名
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
    try:
        cursor.execute(sql, model.values())
        db.commit()
        logger.info(u'保存数据成功，table：{}'.format(table))
    except Exception:
        db.rollback()
        db.close()
        logger.error(u"保存数据失败: table_name:" + table.__str__() + " model:" + model.__str__() + " insert_mysql func error info " + traceback.format_exc())
        raise RuntimeError('mysql error')
    db.close()

@retry(exceptions=RuntimeError, tries=3, delay=1, logger=logger)
def update_complete(company_uuid) :
    gsxt_db = CdrcbDb('gsxt_test')
    sql = "update gsxt_company set complete=1 where company_uuid=%s" % company_uuid
    try :
        gsxt_db.execSql(sql)
        logger.info(u'更新complete成功')
    except Exception :
        logger.error(u"更新complete失败")

def get_session():
    from requests.adapters import HTTPAdapter
    session  = requests.session()
    request_retry = HTTPAdapter(max_retries=3)
    session.mount('https://', request_retry)
    session.mount('http://', request_retry)
    return session

def get_func_name():
    return inspect.stack()[1][3].__str__()

def now_time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now_time

def getJyycKey(ent_type):
    defalut_key = 'entBusExcepUrl'
    jyyc_key_map = {
        '16': 'indBusExcepUrl',
        '17': 'argBusExcepUrl',
        '18': 'argBranchBusExcepUrl'
    }
    return jyyc_key_map.get(ent_type, defalut_key)

init('老河口鹏程新型建筑材料有限公司')