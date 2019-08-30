#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _mysql import OperationalError

__author__ = 'he_zhen/wu_yong'

from retry import retry
from urllib import quote
from bs4 import BeautifulSoup as bs
import requests

import time
import json
import random
import sys
import re
import uuid
import datetime
import traceback
import inspect

from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException
from ics.scheduler import app
from ics.scheduler.new_task import StableTask
from ics.utils.chrome import get_chrome_web_driver
from ics.utils.decorator import stable
from requests.exceptions import ProxyError
from ics.proxy import get_proxy_for_phantom, get_proxy_from_zm
from ics.utils.cookie import formart_selenium_cookies, cookiejar_from_dict
from ics.captcha.jyc2567.crack import get_validate
from ics.task.gsxt.cdrcb.mysql_pool import mysql_pool
from ics.utils.db.mysql_util import MySQLUtil
from ics.settings import default_settings

logger = get_ics_logger(__name__)

reload(sys)
sys.setdefaultencoding('utf-8')


DATA = 'draw=%s&start=%s&length=5'

# task_queue = "queue_cdrcb_normal_gsxt_dev_hezhen"
RETRY_CNT = 5
PROXY = {}

def get_session():
    from requests.adapters import HTTPAdapter
    session  = requests.session()
    request_retry = HTTPAdapter(max_retries=3)
    session.mount('https://', request_retry)
    session.mount('http://', request_retry)
    return session


SESSION = get_session()


def get_proxy():
    """
    ip, port, m_proxy = get_proxy_for_phantom()
    ip, port, m_proxy = get_proxy_for_phantom_test()
    ip, port, m_proxy = get_proxy_from_zm()
    :return:
    """
    global PROXY
    logger.info(u'开始取代理')
    # ip, port, m_proxy = get_proxy_for_phantom()
    ip, port, m_proxy = get_proxy_from_zm(database_proxy_num=5, api_num=6, black_type='gsxt')
    PROXY['ip'] = ip
    PROXY['port'] = port
    PROXY['m_proxy'] = m_proxy
    logger.info(u'取得代理为, {}:{}'.format(ip, port))


def get_headers(refer=None):
    headers = {
        'Host': 'www.gsxt.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'http://www.gsxt.gov.cn/index.html',
        'X-Requested-With': 'XMLHttpRequest',

        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.gsxt.gov.cn',
        'Upgrade-Insecure-Requests': '1'
    }
    if refer:
        headers['Referer'] = refer
    return headers

@retry(exceptions=LogicException, tries=RETRY_CNT, delay=3, logger=logger)
def refresh_cookie():
    time.sleep(1)
    get_proxy()
    cookies, web = from_webdriver_get_cookies(PROXY['ip'], PROXY['port'])
    if not web:
        logger.error(u'刷新cookie，得到web对象不合法')
        raise LogicException("web obj invalid")
    current_url = web.current_url
    current_html = web.page_source
    web.quit()
    if '400 Bad request' in current_html:
        err_msg = u'page source invalid, 400 Bad request'
        logger.warning(err_msg)
        raise LogicException(err_msg)

    if 'spider' in current_url or 'dos' in current_url:
        err_msg = u'刷新cookie，获取到的界面不合法，current_url :{}'.format(current_url)
        logger.error(err_msg)
        raise LogicException(err_msg)

    if not cookies:
        logger.info(u'获取cookie为空')
        raise LogicException("no cookies!!!")
    SESSION.cookies = cookiejar_from_dict(cookies, 'www.gsxt.gov.cn')

@app.task(bind=True, base=StableTask, rate_limit='120/m', ignore_result=True)
# @stable(LogicException, logger=logger)
# @retry(exceptions=LogicException, tries=10, delay=3, logger=logger)
def init(self, keyword):
    try:
        logger.info(u'开始抓取，搜索种子为: {}'.format(keyword))

        refresh_cookie()

        headers = get_headers()
        headers.pop('Host')
        # 打码
        try:
            validate = get_validate(SESSION, headers, PROXY['m_proxy'], logger=logger)
        except Exception as e:
            err_msg = u'打码失败, 结果为: {}, 准备重试'.format(str(e))
            logger.info(err_msg)
            raise LogicException(err_msg)

        time.sleep(2)

        @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
        def get_search_list():
            """
            涉及到打码，不重试太多次数
            :return:
            """
            token = str(random.randint(100000000, 999999999))
            try :
                url = '/corp-query-search-1.html'
                data = 'tab=ent_tab&province=&geetest_challenge={0}&geetest_validate={1}&geetest_seccode={1}%7Cjordan&token={2}&searchword={3}'.format(validate['challenge'], validate['validate'], token, quote(keyword.encode('utf8')))
                html = send_request('post', url=url, data=data, is_json=False, func_name="get_search_list")
                return html
            except Exception as e:
                err_msg = u"获取搜索列表页面失败, 原因: {}".format(traceback.format_exc())
                logger.error(err_msg)
                raise LogicException(err_msg)
        try:
            resHtml = get_search_list()
        except Exception as e:
            raise LogicException(u'获取搜索列表重试失败，从首页开始重试{}'.format(str(e)))

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
            logger.info(u'种子搜索结果为空, 保存种子，结束搜索， 种子为: {}'.format(keyword))
            insert_mysql('gsxt_no_company', {
                'search_key': keyword,
                'create_time': now_time(),
            })
            return

        @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
        def get_jbxx(request_url):
            try :
                html = send_request('get', url=request_url, is_json=False, func_name="get_jbxx")
                return html
            except Exception as e:
                err_msg = u"获取搜索列表页面失败, 原因: {}".format(traceback.format_exc())
                logger.error(err_msg)
                raise LogicException(err_msg)

        refer = url
        try :
            resHtml = get_jbxx(url)
        except:
            err_msg = u"请求基本信息页面失败， 原因: {}".format(traceback.format_exc())
            logger.error(err_msg)
            raise LogicException(err_msg)

        time.sleep(2)

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

        # 股东及出资信息/发起人及出资信息 post
        download_share_holder(url_dict['shareholderUrl'], refer, company_uuid, source_id)

        if '16' == ent_type:
            keyPersonUrl = url_dict['gtKeyPersonUrl']
            alterInfoUrl = url_dict['gtAlertInfoUrl']
        else:
            keyPersonUrl = url_dict['keyPersonUrl']
            alterInfoUrl = url_dict['alterInfoUrl']

        # 主要人员信息 get
        # download_key_person(keyPersonUrl, refer, company_uuid, url_dict, source_id)

        # 变更信息 post
        download_alter_info(alterInfoUrl, refer, company_uuid, source_id)

        # 清算信息 get
        download_liquidation(url_dict['liquidationUrl'], refer, company_uuid, source_id)

        # 双随机抽查结果信息 get
        download_getDrRaninsResUrl(url_dict['getDrRaninsResUrl'], refer, company_uuid, source_id)

        # 分支机构信息 get
        # download_branch(url_dict['branchUrl'], refer, company_uuid, url_dict, source_id)

        time.sleep(3)

        # 股权出质登记信息 post
        download_stak_qualit(url_dict['stakQualitInfoUrl'], refer, company_uuid, source_id)

        # 知识产权出质登记信息 post
        download_pro_pledge_reg_info(url_dict['proPledgeRegInfoUrl'], refer, company_uuid, source_id)

        # 商标注册信息  get
        # download_trade_mark(url_dict['trademarkInfoUrl'], refer, company_uuid, source_id)

        # 抽查检查结果信息 post
        download_spot_check_info(url_dict['spotCheckInfoUrl'], refer, company_uuid, source_id)

        # 司法协助信息 post
        download_assist(url_dict['assistUrl'], refer, company_uuid, source_id)

        time.sleep(3)
        # 企业年报信息 get
        # download_anche_year(url_dict['anCheYearInfo'],  refer, company_uuid, source_id)

        # 股东及出资信息 post
        download_ins_Inv(url_dict['insInvinfoUrl'], refer, company_uuid, source_id)

        # 股权变更信息 post
        download_ins_alter_stock(url_dict['insAlterstockinfoUrl'], refer, company_uuid, source_id)

        # 行政许可信息  post
        download_ins_licence(url_dict['insLicenceinfoUrl'], refer, company_uuid, source_id)

        # 知识产权出质登记信息  post
        download_ins_Pro_Pledge_Reg(url_dict['insProPledgeRegInfoUrl'], refer, company_uuid, source_id)

        # 行政处罚信息  post=
        download_ins_Punishment(url_dict['insPunishmentinfoUrl'], refer, company_uuid, source_id)

        # 企业简易注销公告信息  get
        download_simple_cancel(url_dict['simpleCancelUrl'], refer, company_uuid, source_id)

        # 行政许可信息 POST
        download_other_licence_detail(url_dict['otherLicenceDetailInfoUrl'], refer, company_uuid, source_id)

        # 行政处罚信息 POST
        download_punishment_detail(url_dict['punishmentDetailInfoUrl'], refer, company_uuid, source_id)

        entBusExcepUrl = getJyycKey(ent_type)
        # 列入经营异常名录信息 POST
        download_ent_bus_excep_detail(url_dict[entBusExcepUrl], refer, company_uuid, source_id)

        # 列入严重违法失信企业名单（黑名单）信息 POST
        download_Ill_detail(url_dict['IllInfoUrl'], refer, company_uuid, source_id)

        # 动产抵押登记信息 post
        download_mort_reg_info(url_dict['mortRegInfoUrl'], refer, company_uuid, source_id)

        update_complete(company_uuid)

    except Exception as e:
        err_msg = u'下载公司出错，keyword: {}, e: {}'.format(keyword, str(e))
        logger.error(err_msg)
        insert_mysql("gsxt_fail_record", {"company_name": keyword, "create_time": now_time()})
        raise ProxyError(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_other_licence_detail(url, refer,company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage :
            logger.info(u'other_licence_detail response不合法:{}'.format(resHtml))
        else :
            page_sources.append(resHtml)
            logger.info(u'other_licence_detail 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'other_licence_detail response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)
                logger.info(u'other_licence_detail 原文为：{}'.format(resHtml))
        insert_common("gsxt_otherlicencedetailinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_other_licence_detail error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_punishment_detail(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'punishment_detail response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'punishment_detail 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'punishment_detail response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)
                logger.info(u'punishment_detail 原文为：{}'.format(resHtml))
        insert_common("gsxt_punishmentdetailinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_punishment_detail error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_getDrRaninsResUrl(url, refer, company_uuid, source_id):
    try:
        mothed = "get"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        data = data.replace("length=5", "length=10")
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)

        if not response and not totalPage:
            logger.info(u'getDrRaninsResUrl response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'getDrRaninsResUrl 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'getDrRaninsResUrl response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)
                logger.info(u'getDrRaninsResUrl 原文为：{}'.format(resHtml))
        insert_common("gsxt_drraninsres", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_getDrRaninsResUrl error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_ent_bus_excep_detail(url,refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()
        func_args = {
            'index': 3,
            'retry_cnt': 3,
            'check_key': '0_0',
        }

        resHtml = send_request(mothed, url, data, refer, func_name, check_result_func=check_func,
                               func_args=func_args)
        response, totalPage = str_to_json(resHtml)
        if response.get("cacheKey")=="0_0":
            retry_get_pictures()
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)

        if not response and not totalPage:
            logger.info(u'ent_bus_excep_detail response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'ent_bus_excep_detail 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            func_args['index'] = 3
            resHtml = send_request(mothed, url, data, refer, func_name, check_result_func=check_func,
                                   func_args=func_args)
            response, totalPage = str_to_json(resHtml)
            if response.get("cacheKey") == "0_0":
                retry_get_pictures()
                resHtml = send_request(mothed, url, data, refer, func_name)
                response, totalPage = str_to_json(resHtml)

            if not response and not totalPage:
                logger.info(u'ent_bus_excep_detail response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)

                logger.info(u'ent_bus_excep_detail 原文为：{}'.format(resHtml))
        insert_common("gsxt_entbusexcep", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_ent_bus_excep_detail error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_Ill_detail(url, refer,company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        func_args = {
            'index': 3,
            'retry_cnt': 3,
            'check_key': '0_0',
        }

        resHtml = send_request(mothed, url, data, refer, func_name, check_result_func=check_func, func_args=func_args)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'Ill_detail response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'Ill_detail 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            func_args['index'] = 3
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'Ill_detail response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)
                logger.info(u'Ill_detail 原文为：{}'.format(resHtml))

        insert_common("gsxt_illinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_Ill_detail error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_share_holder(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        data = DATA % (draw, start)
        func_name = get_func_name()
        page_sources = []

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        share_holder_detail(response, refer, company_uuid, source_id)
        if not response and not totalPage :
            logger.info(u'share_holder response不合法:{}'.format(resHtml))
        else :
            page_sources.append(resHtml)
            logger.info(u'share_holder 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(5.1)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            share_holder_detail(response, refer, company_uuid, source_id)
            if not response and not totalPage:
                logger.info(u'share_holder response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)

                logger.info(u'share_holder 原文为：{}'.format(resHtml))
        insert_common("gsxt_shareholder", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_share_holder error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def share_holder_detail(response, refer, company_uuid, source_id) :
    func_name = get_func_name()
    page_sources = []
    datas = response.get("data")
    detail_url = "/corp-query-entprise-info-shareholderDetail-%s.html"

    for data in datas :

        detailCheck = data.get("detailCheck")
        if detailCheck == "true":
            time.sleep(8.1)
            invId = data.get("invId")
            url = detail_url % invId

            resHtml = send_request("get", url, None, refer, func_name)
            page_sources.append(resHtml)
            print "share_holder_detail: " + resHtml
    insert_common("gsxt_shareholder_detail", page_sources, company_uuid, source_id)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_key_person(url, refer, company_uuid, url_dict, source_id):
    """
    主要人员换信息翻页与分支机构类似。
    翻页之后第一页与首页显示一样。
    所以翻页应该尽可能的直接取第二页。
    """
    try:
        mothed = "get"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, None, refer, func_name)
        response, totalPage = str_to_json(resHtml)

        if not response and not totalPage:
            logger.info(u'key_person response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'key_person 原文为：{}'.format(resHtml))

        if totalPage > 1 :
            keyPersonAllUrl = url_dict.get("keyPersonAllUrl")
            keyPersonAll_Html = send_request("get", keyPersonAllUrl, None, refer, func_name, is_json=False)
            soup = bs(keyPersonAll_Html, 'lxml')
            sc = soup.select('div.mainContent script')[0].text.strip()
            keyPersonUrlData = re.search('var keyPersonUrlData =\"(.*?)\";', sc).group(1)
            all_key_person(keyPersonUrlData, refer, company_uuid, url_dict, totalPage, source_id)
        insert_common("gsxt_keyperson", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_key_person error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def all_key_person(url, refer, company_uuid, url_dict, totalPage, source_id):
    data = "start=%s"
    page = 1
    page_sources = []
    func_name = get_func_name()

    while page < totalPage :
        data = data % (page * 16)
        page = page + 1
        resHtml = send_request("get", url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'key_person response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'key_person 原文为：{}'.format(resHtml))
        time.sleep(2)
    insert_common("gsxt_keyperson", page_sources, company_uuid, source_id)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_liquidation(url, refer, company_uuid, source_id):
    try:
        mothed = "get"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'liquidation response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'liquidation 原文为：{}'.format(resHtml))

        while draw < totalPage and response.get('data'):
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'liquidation response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)

                logger.info(u'liquidation 原文为：{}'.format(resHtml))
        insert_common("gsxt_liquidation", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))


    except Exception as e:
        err_msg = 'download_liquidation error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_branch(url, refer, company_uuid, url_dict, source_id):
    try:
        mothed = "get"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'branch response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'branch 原文为：{}'.format(resHtml))

        if totalPage > 1 :
            branchAllUrl = url_dict.get("branchAllUrl")
            branchAll_Html = send_request("get", branchAllUrl, None, refer, func_name, is_json=False)
            soup = bs(branchAll_Html, 'lxml')
            sc = soup.select('div.mainContent script')[0].text.strip()
            branchUrlData = re.search('var branchUrlData =\"(.*?)\";', sc).group(1)
            all_branch_person_detail(branchUrlData, refer, company_uuid, url_dict, totalPage, source_id)

        insert_common("gsxt_branch", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_branch error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)

# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def all_branch_person_detail(url, refer, company_uuid, url_dict, totalPage, source_id):
    data = "start={}"
    page = 1
    func_name = get_func_name()
    page_sources = []

    while page < totalPage :
        temp = data.format(page * 9)
        page = page + 1
        time.sleep(3)
        resHtml = send_request("get", url, temp, refer, func_name)
        response, _ = str_to_json(resHtml)

        if not response and not _:
            logger.info(u'branch_person_detail response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'branch_person_detail 原文为：{}'.format(resHtml))
    insert_common("gsxt_branch", page_sources, company_uuid, source_id)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_alter_info(url, refer, company_uuid, source_id):
    func_name = get_func_name()

    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)

        func_args = {
            'index': 3,
            'retry_cnt': 3,
            'check_key':'0_0',
        }

        resHtml = send_request(mothed, url, data, refer, func_name, check_result_func=check_func, func_args=func_args)
        response, totalPage = str_to_json(resHtml)

        if not response and not totalPage:
            logger.info(u'alter_info response不合法:{}'.format(resHtml))
            # raise LogicException(u'变更信息页面response不合法:{}, 重试'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'alter_info 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(1.5)

            func_args['index'] = 3
            resHtml = send_request(mothed, url, data, refer, func_name, check_result_func=check_func, func_args=func_args)
            response, totalPage = str_to_json(resHtml)

            if not response and not totalPage:
                logger.info(u'alter_info response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)

                logger.info(u'alter_info 原文为：{}'.format(resHtml))
        insert_common("gsxt_alterinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_alter_info error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_mort_reg_info(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        time.sleep(3.1)
        response, totalPage = str_to_json(resHtml)
        mort_reg_detail(response, refer, company_uuid, source_id)
        if not response and not totalPage:
            logger.info(u'mort_reg_inforesponse不合法 {}'.format(resHtml))
            # raise LogicException(u'mort_reg_inforesponse不合法:{}, 重试'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'gsxt_mortreginfo 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(5.1)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            mort_reg_detail(response, refer, company_uuid, source_id)

            if not response and not totalPage:
                logger.info(u'gsxt_mortreginfo response不合法 {}'.format(resHtml))
            else :
                page_sources.append(resHtml)

                logger.info(u'gsxt_mortreginfo 原文为：{}'.format(resHtml))
        insert_common("gsxt_mortreginfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_mort_reg_info error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)

def mort_reg_detail(response, refer, company_uuid, source_id) :
    datas = response.get("data")
    for data in datas :
        morReg_Id = data.get("morReg_Id")
        if morReg_Id :
            mort_reg_regpersoninfo(refer, company_uuid, morReg_Id, source_id)
            time.sleep(10)
            mort_reg_creditorRightInfo(refer, company_uuid, morReg_Id, source_id)
            time.sleep(10)
            mort_reg_guaranteeInfo(refer, company_uuid, morReg_Id, source_id)
            time.sleep(10)
            mort_reg_regCancelInfo(refer, company_uuid, morReg_Id, source_id)
            time.sleep(10)
            mort_reg_altItemInfo(refer, company_uuid, morReg_Id, source_id)
        time.sleep(10)

# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def mort_reg_regpersoninfo(refer,company_uuid, morReg_Id, source_id) :
    func_name = get_func_name()
    regpersoninfo_url = "/corp-query-entprise-info-mortregpersoninfo-%s.html" % morReg_Id

    resHtml = send_request("get", regpersoninfo_url, None, refer, func_name)
    print "mort_reg_regpersoninfo: " + resHtml

    insert_mysql("gsxt_mortreg_regpersoninfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "morReg_Id": morReg_Id,
                                      "create_time": now_time()})

# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def mort_reg_creditorRightInfo(refer, company_uuid, morReg_Id, source_id) :
    CreditorRightInfo_url = "/corp-query-entprise-info-mortCreditorRightInfo-%s.html" % morReg_Id
    func_name = get_func_name()

    resHtml = send_request("get", CreditorRightInfo_url, None, refer, func_name)
    print "mort_reg_creditorRightInfo: " + resHtml

    insert_mysql("gsxt_mortreg_creditorrightinfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "morReg_Id": morReg_Id,
                                      "create_time": now_time()})

# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def mort_reg_guaranteeInfo(refer, company_uuid, morReg_Id, source_id) :
    GuaranteeInfo_url = "/corp-query-entprise-info-mortGuaranteeInfo-%s.html" % morReg_Id
    func_name = get_func_name()

    resHtml = send_request("get", GuaranteeInfo_url, None, refer, func_name)
    print "mort_reg_guaranteeInfo: " + resHtml

    insert_mysql("gsxt_mortreg_guaranteeinfo", {"page_source": resHtml,
                                      "company_uuid": company_uuid,
                                      "source_id": source_id,
                                      "morReg_Id": morReg_Id,
                                      "create_time": now_time()})


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def mort_reg_regCancelInfo(refer, company_uuid, morReg_Id, source_id):
    RegCancelInfo = "/corp-query-entprise-info-getMortRegCancelInfo-%s.html" % morReg_Id
    func_name = get_func_name()

    resHtml = send_request("get", RegCancelInfo, None, refer, func_name)
    print "mort_reg_regCancelInfo: " + resHtml

    insert_mysql("gsxt_mortreg_regcancelinfo", {"page_source": resHtml,
                                                  "company_uuid": company_uuid,
                                                  "source_id": source_id,
                                                  "morReg_Id": morReg_Id,
                                                  "create_time": now_time()})

# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def mort_reg_altItemInfo(refer, company_uuid, morReg_Id, source_id) :
    AltItemInfo = "/corp-query-entprise-info-getMortAltItemInfo-%s.html" % morReg_Id
    func_name = get_func_name()

    resHtml = send_request("get", AltItemInfo, None, refer, func_name)
    print "mort_reg_altItemInfo: " + resHtml

    insert_mysql("gsxt_mortreg_altiteminfo", {"page_source": resHtml,
                                              "company_uuid": company_uuid,
                                              "source_id": source_id,
                                              "morReg_Id": morReg_Id,
                                              "create_time": now_time()})


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_stak_qualit(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'stak_qualit response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)

            logger.info(u'stak_qualit 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'stak_qualit response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)
                logger.info(u'stak_qualit 原文为：{}'.format(resHtml))
        insert_common("gsxt_stakqualitinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_stak_qualit error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_pro_pledge_reg_info(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'pro_pledge_reg_info response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'pro_pledge_reg_info 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'pro_pledge_reg_info response不合法:{}'.format(resHtml))
            else :
                page_sources.append(resHtml)

                logger.info(u'pro_pledge_reg_info 原文为：{}'.format(resHtml))
        insert_common("gsxt_inspropledgereginfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_pro_pledge_reg_info error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_trade_mark(url, refer, company_uuid, source_id):
    try:
        mothed = "get"
        start = 0
        i = 1
        data = ""
        page_sources = []
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)

        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'trade_mark response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'trade_mark 原文为：{}'.format(resHtml))

        while i < totalPage:
            start = i * 4
            data = "&start=%s" % start
            time.sleep(2)
            i = i + 1
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'trade_mark response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)

                logger.info(u'trade_mark 原文为：{}'.format(resHtml))
        insert_common("gsxt_trademarkinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))

    except Exception as e:
        err_msg = 'download_trade_mark error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_spot_check_info(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'spot_check_info response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'spot_check_info 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'spot_check_info response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)
                logger.info(u'spot_check_info 原文为：{}'.format(resHtml))
        insert_common("gsxt_spotcheckinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_spot_check_info error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_assist(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'assist response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)

            logger.info(u'assist 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'assist response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)
                logger.info(u'assist 原文为：{}'.format(resHtml))
        insert_common("gsxt_assist", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_assist error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


def download_anche_year(url, refer, company_uuid, source_id):

    mothed = "get"
    data = ""
    func_name = get_func_name()

    resHtml = send_request(mothed, url, data, refer, func_name)

    insert_mysql("gsxt_ancheyear", {"page_source": resHtml,
                                 "company_uuid": company_uuid,
                                    "source_id": source_id,
                                 "create_time": now_time()})
    logger.info(u'anche_year 原文为：{}'.format(resHtml))


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_ins_Inv(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'ins_Inv response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'ins_Inv 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'ins_Inv response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)

                logger.info(u'ins_Inv 原文为：{}'.format(resHtml))
        insert_common("gsxt_insinvinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_ins_Inv error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_ins_alter_stock(url, refer,company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'download_ins_alter_stock response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)

        logger.info(u'ins_alter_stock 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'download_ins_alter_stock response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)
                logger.info(u'ins_alter_stock 原文为：{}'.format(resHtml))
        insert_common("gsxt_insalterstockinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_ins_alter_stock error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_ins_licence(url, refer,company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'ins_licence response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'ins_licence 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'ins_licence response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)

                logger.info(u'ins_licence 原文为：{}'.format(resHtml))
        insert_common("gsxt_inslicenceinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_ins_licence error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_ins_Pro_Pledge_Reg(url,refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'ins_Pro_Pledge_Reg response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'ins_Pro_Pledge_Reg 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'ins_Pro_Pledge_Reg response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)

                logger.info(u'ins_Pro_Pledge_Reg 原文为：{}'.format(resHtml))
        insert_common("gsxt_propledgereginfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_ins_Pro_Pledge_Reg error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_ins_Punishment(url, refer, company_uuid, source_id):
    try:
        mothed = "post"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        func_args = {
            'index': 3,
            'retry_cnt': 3,
            'check_key': '0_0',
        }
        resHtml = send_request(mothed, url, data, refer, func_name, check_result_func=check_func, func_args=func_args)
        response, totalPage = str_to_json(resHtml)

        if not response and not totalPage:
            logger.info(u'ins_Punishment response不合法:{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'ins_Punishment 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)

            func_args = {
                'index': 3,
                'retry_cnt': 3,
                'check_key': '0_0',
            }
            resHtml = send_request(mothed, url, data, refer, func_name, check_result_func=check_func, func_args=func_args)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'ins_Punishment response不合法:{}'.format(resHtml))
            else:
                page_sources.append(resHtml)

                logger.info(u'ins_Punishment 原文为：{}'.format(resHtml))
        insert_common("gsxt_inspunishmentinfo", page_sources, company_uuid, source_id)

    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_ins_Punishment error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)


# @retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def download_simple_cancel(url, refer,company_uuid, source_id):
    try:
        mothed = "get"
        draw = 1
        start = 0
        page_sources = []
        data = DATA % (draw, start)
        func_name = get_func_name()

        resHtml = send_request(mothed, url, data, refer, func_name)
        response, totalPage = str_to_json(resHtml)
        if not response and not totalPage:
            logger.info(u'simple_cancel 原文为：{}'.format(resHtml))
        else:
            page_sources.append(resHtml)
            logger.info(u'simple_cancel 原文为：{}'.format(resHtml))

        while draw < totalPage:
            draw = draw + 1
            start = start + 5
            data = DATA % (draw, start)
            time.sleep(2)
            resHtml = send_request(mothed, url, data, refer, func_name)
            response, totalPage = str_to_json(resHtml)
            if not response and not totalPage:
                logger.info(u'simple_cancel 原文为：{}'.format(resHtml))
            else:
                page_sources.append(resHtml)

                logger.info(u'simple_cancel 原文为：{}'.format(resHtml))

        insert_common("gsxt_simplecancel", page_sources, company_uuid, source_id)
    except OperationalError as e:
        logger.error(u'操作数据库失败：err_msg: {}'.format(str(e)))
        raise OperationalError(str(e))
    except Exception as e:
        err_msg = 'download_simple_cancel error: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)

def str_to_json(json_str):
    try:
        data = json.loads(json_str)
        totalPage = data.get("totalPage")
        return data, totalPage
    except Exception as e:
        logger.error("New error !!!  resopone is :" + json_str.__str__() + " error_info :" + traceback.format_exc())
    return False, False

def insert_common(table_name, page_sources, company_uuid, source_id):
    for page_source in page_sources :
        insert_mysql(table_name, {"page_source": page_source,
                                   "company_uuid": company_uuid,
                                   "source_id": source_id,
                                   "create_time": now_time()})

@retry(exceptions=LogicException, tries=3, delay=3, logger=logger)
def send_request(method, url, data=None, refer=None, func_name=None, cookies=None, is_json=True, no_context=False, check_result_func=None,func_args={}):
    global SESSION
    if SESSION is None:
        SESSION = get_session()
    if cookies:
        SESSION.cookies = cookiejar_from_dict(cookies, 'www.gsxt.gov.cn')
    headers = get_headers(refer)
    retry_index = 0
    while retry_index < RETRY_CNT:
        try:
            current_url = url if url.startswith('http') else 'http://www.gsxt.gov.cn{}'.format(url)
            ip = PROXY.get('ip', '')
            port = PROXY.get('port', '')
            logger.info(u'进入send_request, 开始下载proxy: {}:{}, method: {}, func_name:{}, url: {}, data: {}'.format(ip, port, method, func_name, current_url, data))
            if method=="get":
                resp = SESSION.get(
                    headers=headers,
                    params = data,
                    url=current_url,
                    proxies=PROXY['m_proxy'],
                    timeout=30
                )

            elif method=="post":
                resp = SESSION.post(
                    headers=headers,
                    url=current_url,
                    data=data,
                    proxies=PROXY['m_proxy'],
                    timeout=30
                )
            else:
                logger.info(u'请求方法不支持')
                break
            if resp.status_code == 521:
                err_msg = u'下载返回状态码不合法, 状态码为： {}'.format(str(resp.status_code))
                logger.warning(err_msg)
                refresh_cookie()
                raise Exception(u'出现加速乐521')

            if resp.status_code >= 400:
                err_msg = u'下载返回状态码不合法, 状态码为： {}'.format(str(resp.status_code))
                logger.warning(err_msg)
                refresh_cookie()
                raise Exception(err_msg)

            res_html = resp.content
            if not res_html and no_context is False:
                logger.warning(u'返回结果为空，重试')
                raise Exception(u'返回结果为空')

            if invalid_link(res_html) is False:
                logger.warning(u'invalid_link，链接不合法，刷新cookie重试')
                refresh_cookie()
                raise Exception(u'invalid_link，链接不合法')
            if assert_404_page(res_html) is False:
                logger.warning(u'404页面出现，重试')
                refresh_cookie()
                raise Exception(u'页面出现404')

            if visit_too_busy(res_html) is False:
                logger.warning(u'访问频繁，刷新cookie')
                refresh_cookie()
                raise Exception(u'访问频繁')

            if is_json is True and assert_is_json(res_html) is False:
                logger.warning(u'返回结果期望是json，但page非json')
                raise Exception(u'返回结果期望是json，但page非json， html: {}'.format(res_html))

            if check_result_func and check_result_func(res_html, func_args) is False:
                logger.warning(u'执行断言函数检查失败，函数为： {}， html为：{}'.format(check_result_func.__name__, res_html))
                raise Exception(u'检查内容失败')
            logger.info(u'send_request, 下载成功 method: {}, url: {}, func_name:{}, data: {}'.format(method, current_url, func_name, data))
            return res_html
        except Exception as e :
            logger.error(u'下载异常, method: {} url: {}, func_name:{}, data: {}, 原因: {}'.format(method, current_url, func_name, data, str(e)))

        retry_index += 1
        if retry_index == RETRY_CNT:
            refresh_cookie()
            raise LogicException(u"重试次数达到最大值")

        time.sleep(1)

def assert_is_json(html):
    flag = False
    try:
        json.loads(html)
        flag = True
    except Exception as e:
        logger.warning(u'模块下载页面非json，重试, {}'.format(str(e)))
    return flag

def get_func_name():
    return inspect.stack()[1][3].__str__()

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


def assert_404_page(html, request_pic=False):
    """
     断言返回页面是否会为404 not found页面，企信网页面偶尔会出现该情况，如果出现需要重试
     :param web:  web对象
     :param html:  网页原文
     :return:
    """

    if u'您访问的页面不存在' in html:
        logger.info(u'响应页面出现404页面: {}'.format(html))
        return False
    return True


def visit_too_busy(html):
    """
    断言返回页面是否合法
    :param html:
    :return:
    """

    if u'操作过于频繁' in html:
        logger.warning(u"操作过于频繁, 切换代理-重试......")
        return False
    return True


def retry_get_pictures() :
    image_uri_list = [
        '/image/map1.jepg',
        '/image/user1.jepg',
        '/image/marker1.jepg',
        '/image/circle1.jepg',
        '/image/icon2.jepg',
        '/image/icon3.jepg',
        '/image/icon4.jepg'
    ]
    print "retry in get picture"
    for pic in image_uri_list :
        send_request("get", pic, None, "http://www.gsxt.gov.cn/",  no_context=True, is_json=False)


def deal_anche_year(resHtml, mothed, url, refer, source_id):
    _resHtml = resHtml.replace("null", "''")
    anche_year_list = eval(_resHtml)

    for anche_year in anche_year_list:
        anCheId = anche_year.get("anCheId")
        anCheYear = anche_year.get("anCheYear")
        entType = 1
        data = "anCheId=%s&entType=%s&anCheYear=%s" % (anCheId, entType, anCheYear)
        resHtml = send_request(mothed, url, data, refer)
        print "deal_anche_year: " + resHtml
        time.sleep(3)


@retry(exceptions=RuntimeError, tries=3, delay=3, logger=logger)
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
    except OperationalError as e:
        raise OperationalError(str(e))
    except Exception:
        db.rollback()
        db.close()
        logger.error(u"保存数据失败: table_name:" + table.__str__() + " model:" + model.__str__() + " insert_mysql func error info " + traceback.format_exc())
        raise RuntimeError('mysql error')
    db.close()


@retry(exceptions=RuntimeError, tries=3, delay=3, logger=logger)
def update_complete(company_uuid) :
    gsxt_db = MySQLUtil('gsxt_test')
    sql = "update gsxt_company set complete=1 where company_uuid='%s'" % company_uuid
    if gsxt_db.execSql(sql):
        logger.info(u'更新complete成功')
    else:
        logger.error(u"更新complete失败, sql: {}".format(sql))


def check_func(html, func_args, max_retry_cnt=3):
    res_json = json.loads(html)
    if res_json.get('cacheKey') == func_args['check_key']:
        if func_args['index'] <= 0:
            func_args['index'] = func_args.get('max_retry_cnt', max_retry_cnt)
            logger.info(u'达到最大重试次数，开始换代理')
            get_proxy()
        logger.info(u'模块出现0_0, 开始获取图片重试')
        retry_get_pictures()
        func_args['index'] -= 1
        return False
    return True


def now_time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now_time


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
    return cookies, web


def getJyycKey(ent_type):
    defalut_key = 'entBusExcepUrl'
    jyyc_key_map = {
        '16': 'indBusExcepUrl',
        '17': 'argBusExcepUrl',
        '18': 'argBranchBusExcepUrl'
    }
    return jyyc_key_map.get(ent_type, defalut_key)

if __name__ == '__main__':
    init(u'四川众和源餐饮管理有限公司  ')