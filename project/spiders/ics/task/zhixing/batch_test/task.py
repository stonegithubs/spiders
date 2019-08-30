#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'wu_yong'

import re
import sys
import json
import time
import random
import requests
import traceback
from lxml import etree
from uuid import uuid4
from ics.utils import get_ics_logger
from ics.utils.task_util.batch_test.task_util import *
from ics.scheduler.new_task import StableTask
from ics.utils.decorator import stable
from ics.utils.exception_util import LogicException
from ics.scheduler import app
from ics.proxy import get_proxy_from_zm, get_proxy_for_phantom_test
from ics.utils.md5_tool import to_md5
from ics.task.zhixing.batch_test.etl_zhixing import zhixing_parse
# from ics.captcha.juhe.verification_code import get_code_by_content
from ics.captcha.chaojiying.crack_captch import CjyCaptcha
from ics.settings.default_settings import ZHIXING_DATA_TABLE, BATCH_TEST_ZHIXING_NORMAL_TASK_QUEUE

reload(sys)
sys.setdefaultencoding('utf-8')

RETRY_CNT = 30
G_YZM_CODE = None
G_CAPTCHA_ID = None


class STATUS(object):
    YZM_ERROR = 101
    CONTENT_ERROR = 102
    PROXY_ERROR = 103
    RESPONSE_CODE_ERROR = 104
    DOWNLOADER_ERROR = 105


logger = get_ics_logger('zhixing')

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'zhixing.court.gov.cn',
    'Origin': 'http://zhixing.court.gov.cn',
    'Referer': 'http://zhixing.court.gov.cn/search/newsearch',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

chaojiying = CjyCaptcha(logger)

@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def start(self, seed_dict):
    """
    富阳
    (mysql_db, rabbit_db, table_name, seed_dict, result_queue_name, error_msg=None, is_detail=True ,logger=None)
    破解验证码并请求第一页数据，获取总页数
    """

    self.error_callback = search_error_callback
    self.callback_param = {
        'seed_dict': seed_dict,
        'logger': logger,
        'table_name': ZHIXING_DATA_TABLE,
    }

    global G_YZM_CODE
    logger.info(u'搜索种子为： {}'.format(json.dumps(seed_dict, ensure_ascii=False)))
    get_yzm(self)
    res = get_page_list(self, seed_dict, G_CAPTCHA_ID, G_YZM_CODE, page=1)
    if res in STATUS.__dict__.values():
        err_msg = u'请求第一页搜索列表失败: 状态为status: {}, 准备重试'.format(res)
        logger.error(err_msg)
        raise LogicException(err_msg)
    context = res.text
    try:
        total_cnt = int(re.findall(r'共\s*(\d+)\s*条', context.encode('utf-8'), flags=re.S)[0])
    except Exception as e:
        err_msg = u'获取总页码失败： e: {}'.format(str(e))
        logger.error(err_msg)
        raise LogicException(err_msg)
    if total_cnt == 0:
        logger.info(u'搜索结果为空, task_id:{}, seed: {}'.format(seed_dict['task_id'], seed_dict))  # TODO
        send_no_record(seed_dict=seed_dict, logger=logger, table_name=ZHIXING_DATA_TABLE)
        return

    total_page = (total_cnt - 1) / 10 + 1
    seed_dict['total_cnt'] = total_cnt
    logger.info(u'task_id{}, 总页数为: {}，总条数为: {}'.format(seed_dict['task_id'], total_page, total_cnt))
    for page in range(1, total_page + 1):
        app.send_task('ics.task.zhixing.batch_test.task.visit_page_list', [seed_dict, page, total_cnt],
                      queue=BATCH_TEST_ZHIXING_NORMAL_TASK_QUEUE, priority=2)
    logger.info(u'send_task to visit_page_list 成功')


@app.task(bind=True, base=StableTask, default_retry_delay=2, max_retries=5, ignore_result=True)
@stable(LogicException, logger=logger)
def visit_page_list(self, seed_dict, page, total_cnt):
    """
    获取搜索列表每一页数据
    """
    global G_YZM_CODE
    global G_CAPTCHA_ID
    self.error_callback = error_callback
    self.callback_param = {
        'seed_dict': seed_dict,
        'logger': logger,
        'table_name': ZHIXING_DATA_TABLE,
        'lose_cnt': get_current_page_cnt(total_cnt, 10, page)
    }
    if G_YZM_CODE is None:
        get_yzm(self)
    logger.info(u'开始迭代翻页数据，seed: {} page: {}'.format(json.dumps(seed_dict, ensure_ascii=False), page))
    resp = get_page_list(self, seed_dict, G_CAPTCHA_ID, G_YZM_CODE, page)
    retry_cnt = RETRY_CNT
    if resp in STATUS.__dict__.values():
        current_cnt = 1
        while current_cnt < retry_cnt:
            try:
                if resp == STATUS.YZM_ERROR:
                    logger.info(u'验证码识别错误，开始重新获取验证码')
                    get_yzm(self)
                resp = get_page_list(self, seed_dict, G_CAPTCHA_ID, G_YZM_CODE, page)
                if resp not in STATUS.__dict__.values():
                    break
                else:
                    logger.info(u'visit_page_list结果非法: {}'.format(resp))
            except Exception as e:
                logger.warning(u'visit_page_list 出现异常{}，开始第{}次重试'.format(str(e), current_cnt))
                resp = STATUS.DOWNLOADER_ERROR
            current_cnt += 1
            time.sleep(1)
        else:
            raise LogicException(u'resp不符合预期，重试{}次失败，需要检查原因'.format(retry_cnt))

    context = resp.text
    et = etree.HTML(context)
    detail_id_list = et.xpath('.//table[@id="Resultlist"]//tr/td[5]/a/@id')
    for detail_id in detail_id_list:
        app.send_task('ics.task.zhixing.batch_test.task.visit_detail_list',
                      [seed_dict, detail_id, total_cnt],
                      queue=BATCH_TEST_ZHIXING_NORMAL_TASK_QUEUE,
                      priority=3)
    logger.info(u'send_task to visit_detail_list 成功')


@app.task(bind=True, base=StableTask, default_retry_delay=10, max_retries=3, ignore_result=True)
@stable(LogicException, logger=logger)
def visit_detail_list(self, seed_dict, detail_id, total_cnt):
    """
    获取搜索列表每一页数据
    """
    global G_YZM_CODE
    global G_CAPTCHA_ID
    self.error_callback = error_callback
    self.callback_param = {
        'seed_dict': seed_dict,
        'logger': logger,
        'table_name': ZHIXING_DATA_TABLE,
        'lose_cnt': 1
    }
    if G_YZM_CODE is None:
        get_yzm(self)
    res_dic = {}
    resp = get_detail(self, G_CAPTCHA_ID, G_YZM_CODE, detail_id)
    retry_cnt = RETRY_CNT
    if resp in STATUS.__dict__.values():
        current_cnt = 1
        while current_cnt < retry_cnt:
            try:
                if resp == STATUS.YZM_ERROR:
                    logger.info(u'验证码识别错误，开始重新获取验证码')
                    get_yzm(self)
                resp = get_detail(self, G_CAPTCHA_ID, G_YZM_CODE, detail_id)
                if resp not in STATUS.__dict__.values():
                    break
                else:
                    logger.info(u'visit_detail_list结果非法: {}'.format(resp))
            except Exception as e:
                logger.warning(u'get_detail 出现异常{}，开始第{}次重试'.format(str(e), current_cnt))
                resp = STATUS.DOWNLOADER_ERROR
            current_cnt += 1
            time.sleep(1)
        else:
            raise LogicException(u'get_detail操作，resp不符合预期，重试{}次失败，需要检查原因'.format(retry_cnt))

    context = resp.text
    source_id = str(uuid4())
    res_dic['source_id'] = source_id
    res_dic['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res_dic['detail_id'] = detail_id
    res_dic['page_source'] = context.decode('utf-8', "ignore")

    # err_msg = None
    try:
        # raise SoftTimeLimitExceeded('xxxxxxxxxx')
        etl_dict = zhixing_parse(res_dic['page_source'], logger)
        format_old = u'%Y年%m月%d日'
        format_new = '%Y-%m-%d %H:%M:%S'
        case_create_time = etl_dict.get('caseCreateTime')
        if case_create_time:
            etl_dict['caseCreateTime'] = time.strftime(format_new, time.strptime(case_create_time, format_old))
        add_common_key(etl_dict, seed_dict, source_id=source_id, page_source=res_dic['page_source'],
                       total_cnt=total_cnt, status=TASK_STATUS.SUCCESS)
        insert_mysql(ZHIXING_DATA_TABLE, etl_dict, logger)

        check_result_and_send_msg(ZHIXING_DATA_TABLE, total_cnt, seed_dict['task_id'], logger)
    except Exception as e:
        err_msg = 'save data to mysql failed {} \n{}'.format(e, traceback.format_exc())
        logger.error(err_msg)
        etl_dict = {}
        add_common_key(etl_dict, seed_dict, err_msg=err_msg, status=TASK_STATUS.FAILED)
        insert_mysql(ZHIXING_DATA_TABLE, etl_dict, logger)
        check_result_and_send_msg(ZHIXING_DATA_TABLE, total_cnt, seed_dict['task_id'], logger, err_msg=err_msg)
        # 检查是否抓取完成，是否需要发送结束信息


def get_yzm(self):
    global G_YZM_CODE
    global G_CAPTCHA_ID
    current_cnt = 1
    G_CAPTCHA_ID = to_md5('{}{}'.format(time.time() * 1000, random.choice(range(1, 10000))))
    while current_cnt < 10:
        try:
            logger.info(u'开始打码')
            yzm_url = 'http://zhixing.court.gov.cn/search/captcha.do?captchaId={}'.format(G_CAPTCHA_ID)
            # resp = requests.get(yzm_url, headers=headers)
            resp = download_page(self, 'get', yzm_url, headers, timeout=40, proxies={}, data=None)
            if resp.status_code == 200:
                start_time = time.time()
                # code = get_code_by_content(resp.content, logger=logger, yzm_dir='zhixing')
                code, code_id = chaojiying.crack_captcha(resp.content, yzm_dir='zhixing')
                if code:
                    G_YZM_CODE = code
                    end_time = time.time()
                    logger.info(u'打码完成，破解值为： {}, code_id: {}, 打码耗时:{}'.format(code, code_id, end_time - start_time))
                    break
                logger.info(u'打码结果为空: {}'.format(code))
            else:
                logger.info(u'请求验证码返回状态码不正确:{}'.format(resp.status_code))
        except Exception as e:
            logger.warning(u'visit_page_list 出现异常{}，开始第{}次重试'.format(str(e), current_cnt))

        current_cnt += 1
        time.sleep(1)


def download_page(self, method, url, headers, timeout=40, proxies={}, data=None):
    proxy = get_proxy_from_zm(database_proxy_num=5, api_num=6, black_type='zhixing')

    # from ics.proxy import get_proxy_for_phantom_test
    # proxy = '', '', {}
    if not proxy:
        raise LogicException(u'代理为空: {}'.format(proxy))
    ip, port, proxies = proxy
    if ip:
        self.abandon_ip = ip
    logger.info(u'使用代理{}:{}，请求url: {}'.format(ip, port, url))

    if method.lower() == 'get':
        resp = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
    elif method.lower() == 'post':
        resp = requests.post(url, headers=headers, timeout=timeout, proxies=proxies, data=data)
    else:
        logger.info(u'请求方法不支持, method: {}'.format(method))
        resp = None
    if resp:
        logger.info(u'请求完成，status_code：{}, proxy:{}:{}, url: {}'.format(resp.status_code, ip, port, url))
    return resp


def get_page_list(self, seed_dict, captcha_id, yzm_code, page):
    """
    请求搜索列表页码功能函数
    """

    data = {
        'currentPage': page,
        'searchCourtName': u'全国法院（包含地方各级法院）',
        'selectCourtId': '',
        'selectCourtArrange': '1',
        'pname': '',
        'cardNum': '',
        'j_captcha': yzm_code,
        'captchaId': captcha_id
    }

    pname = seed_dict.get('target_name', '')
    card_num = seed_dict.get('target_id', '')
    if card_num:
        data['cardNum'] = card_num
    else:
        data['pname'] = pname

    url = 'http://zhixing.court.gov.cn/search/newsearch'
    resp = download_page(self, 'post', url, headers, timeout=40, proxies={}, data=data)

    if not resp:
        logger.error(u'搜索种子: {}, 执行列表第{}页，内容为空'.format(json.dumps(seed_dict, ensure_ascii=False), page))
        return STATUS.CONTENT_ERROR

    if resp.status_code != 200:
        logger.error(u'搜索种子: {}, 执行列表第{}页，返回状态吗不合法'.format(json.dumps(seed_dict, ensure_ascii=False), page))
        return STATUS.RESPONSE_CODE_ERROR

    content = resp.text
    if not content:
        logger.error(u'搜索种子: {}, 执行列表第{}页，内容为空'.format(json.dumps(seed_dict, ensure_ascii=False), page))
        return STATUS.CONTENT_ERROR

    if u'验证码错误，请重新输入' in content:
        logger.warning(u'搜索种子: {}, 执行列表第{}页，验证码错误'.format(json.dumps(seed_dict, ensure_ascii=False), page))
        logger.error(content)
        return STATUS.YZM_ERROR

    if u'验证码错误或验证码已过期，请重新输入' in content:
        logger.warning(u'搜索种子: {}, 执行列表第{}页，验证码错误或验证码已过期'.format(json.dumps(seed_dict, ensure_ascii=False), page))
        logger.error(content)
        return STATUS.YZM_ERROR

    return resp


def get_detail(self, captcha_id, yzm_code, detail_id):
    detail_url = 'http://zhixing.court.gov.cn/search/newdetail?id={}&j_captcha={}&captchaId={}&_={}'.format(detail_id,
                                                                                                            yzm_code,
                                                                                                            captcha_id,
                                                                                                            int(
                                                                                                                time.time() * 1000))
    headers['Referer'] = 'http://zhixing.court.gov.cn/search/'
    headers['Accept'] = '*/*'
    resp = download_page(self, 'get', detail_url, headers, timeout=40, proxies={})
    if resp.status_code != 200:
        return STATUS.RESPONSE_CODE_ERROR

    content = resp.text

    if u'{}' == content:
        return STATUS.YZM_ERROR

    if not resp or not content:
        return STATUS.CONTENT_ERROR

    if u'验证码错误，请重新输入' in content:
        return STATUS.YZM_ERROR
    return resp
