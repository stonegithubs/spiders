# !/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import random
import traceback
from urllib import quote
from lxml import etree
from ics.captcha.jyc2567.crack import jiyan_validate
from ics.task.gsxt.cdrcb.util import *
from ics.utils.exception_util import LogicException

__author__ = 'wu_yong'


from ics.task.gsxt.cdrcb.constant import *


def init_home():
    global page_dict
    page_dict = {}
    url = 'http://www.gsxt.gov.cn/index.html'
    params = {
        'method': 'get',
        'url': url,
        'is_json': False,
    }
    resp = send_request(**params)
    # print resp.text


@retry(exceptions=LogicException, tries=8, delay=1, logger=logger)
def get_validate():
    try:
        yzm_url = 'http://www.gsxt.gov.cn/SearchItemCaptcha?t={}'.format(current_timestamp())
        params = {
            'method': 'get',
            'url': yzm_url,
        }
        resp = send_request(**params)
        result = jiyan_validate(resp.text, logger)
        if not result:
            raise Exception(u'极验打码失败, 返回值为空：{}'.format(result))
        value_dict['validate'] = result
    except Exception as e:
        err_msg = u'极验打码失败， e:{}'.format(str(e))
        logger.info(err_msg)
        raise LogicException(err_msg)


@retry(exceptions=LogicException, tries=3, delay=1, logger=logger)
def init_search_list():
    """
    涉及到打码，不重试太多次数
    :return:
    """
    try:
        token = str(random.randint(100000000, 999999999))
        url = '{}/corp-query-search-1.html'.format(host)
        validate = value_dict['validate']
        seed_dict = value_dict['seed_dict']
        data = 'tab=ent_tab&province=&geetest_challenge={0}&geetest_validate={1}&geetest_seccode={1}%7Cjordan&token={2}&searchword={3}'.\
            format(validate['challenge'], validate['validate'], token, quote(seed_dict['company_key'].encode('utf8')))
        params = {
            'method': 'post',
            'url': url,
            'data': data,
            'is_json': False,
        }
        resp = send_request(**params)
        page_dict['search_html'] = resp.text

        search_list = parse_search(resp.text)
        value_dict['search_list'] = search_list
        value_dict['search_html'] = resp.text
    except Exception as e:
        err_msg = u"获取搜索列表页面失败, 原因: {}".format(traceback.format_exc())
        logger.error(err_msg)
        raise LogicException(err_msg)


@retry(exceptions=LogicException, tries=3, delay=1, logger=logger)
def init_jbxx(item):
    try:
        page_dict['snapshot_html'] = item['snapshot_html']
        url = '{}{}'.format(host, item['jbxx_uri'])
        resp = send_request('get', url=url, is_json=False)      # TODO 保存原文
        uri_dict = parse_jbxx(resp.text)
        if not uri_dict:
            raise LogicException(u'获取基本信息页面失败，解析不出url_dict, html:{}'.format(resp.text))
        value_dict['uri_dict'] = uri_dict
        page_dict['jbxx'] = {
            'html': resp.text
        }
    except Exception as e:
        err_msg = u"获取搜索列表页面失败, 原因: {}".format(traceback.format_exc())
        logger.error(err_msg)
        raise LogicException(err_msg)


def parse_jbxx(html=None):
    url_dict = {}
    if not html:
        return url_dict
    et = etree.HTML(html)
    ent_type = ''.join(et.xpath('.//input[@id="entType"]/@value')).strip()
    value_dict["ent_type"] = ent_type

    # 16 表示个体公司 ， bgxx_key = gtAlertInfoUrl,
    if '16' == ent_type:
        bgxx_key = 'gtAlertInfoUrl'
        baxx_key = 'gtKeyPersonUrl'
    else:
        bgxx_key = 'alterInfoUrl'
        baxx_key = 'keyPersonUrl'

    def get_jyyc_key(ent_type):
        defalut_key = 'entBusExcepUrl'
        jyyc_key_map = {
            '16': 'indBusExcepUrl',
            '17': 'argBusExcepUrl',
            '18': 'argBranchBusExcepUrl'
        }
        return jyyc_key_map.get(ent_type, defalut_key)
    map_key_dict = {
        "gdxx_uri": "shareholderUrl",                   # 股东信息
        "bgxx_uri": bgxx_key,                           # 变更信息
        "baxx_uri": baxx_key,                           # 备案信息
        "sbxx_uri": "trademarkInfoUrl",                 # 商标信息
        "fzjg_uri": "branchUrl",                        # 分支机构
        "dcdy_uri": "mortRegInfoUrl",                   # 动产抵押
        'gqcz_uri': 'stakQualitInfoUrl',                # 股权出资
        "sfxz_uri": "assistUrl",                        # 司法协助
        "xzxktop_uri": "otherLicenceDetailInfoUrl",     # 行政许可
        "xzcftop_uri": "punishmentDetailInfoUrl",       # 行政违法黑名单
        'jyyctop_uri': get_jyyc_key(ent_type),          # 经营异常
        'hmdtop_uri': 'IllInfoUrl',                     # 黑名单
        'qsxx_uri': 'liquidationUrl',                   # 清算信息
        'ccjc_uri': 'spotCheckInfoUrl',                 # 抽查检查
        'xzxkbottom_uri': 'insLicenceinfoUrl',          # 行政许可bottom  (年报下面的部分)
        'xzcfbottom_uri': 'insPunishmentinfoUrl',       # 行政处罚bottom  (年报下面的部分)
        'zscqbottom_uri': 'insProPledgeRegInfoUrl',     # 知识产权bottom  (年报下面的部分)
        'sjxx_uri': 'getDrRaninsResUrl',                # 双随机抽查结果信息
        'sfxz_xq_uri': 'judiciaryAltershareholderUrl',  # 司法协助详情，(没有抓取)
        'gdxxbottom_uri': 'insInvinfoUrl',              # 股东及出资信息，(年报下面的部分)
        'gqbgbottom_uri': 'insAlterstockinfoUrl',       # 股权变更信息    (年报下面的部分)
        'zxggbottom_uri': 'simpleCancelUrl',            # 注销公告
    }
    for k, v in map_key_dict.items():
        uri = ''.join(re.findall(r'var\s+{}\s*=\s*"(.+?)"'.format(v), html, flags=re.S))
        if uri:
            url_dict[k] = uri
    for k, v in url_dict.items():
        logger.info('{}===> {}'.format(k, v))
    return url_dict


def parse_search(html):
    et = etree.HTML(html)
    search_et_list = et.xpath('.//a[@class="search_list_item db"]')
    search_result_div_list = et.xpath('.//div[contains(@class, "search_result")]')
    non_company_flag = False
    if search_result_div_list:
        for search_result in search_result_div_list:
            result_text = search_result.xpath('string(.)')
            if result_text and u'查询到0条信息' in result_text:
                non_company_flag = True
    if non_company_flag:
        logger.info(u'搜索结果为空: {}'.format(value_dict['seed_dict']))
        page_dict['status'] = Status.NON_COMPANY
        page_dict['error_msg'] = '查询到0条信息'
    search_list = []
    for item in search_et_list:
        try:
            tmp_dict = {}
            jbxx_uri = item.xpath('./@href')[0].strip()
            company_name = item.xpath('string(./h1)').strip()
            company_status = item.xpath('//*[@id="advs"]/div/div[2]/a[1]/div[1]/span')[0].text
            reg_no_str = item.xpath('string(./div[@class="f14 g9 pt10"]/div[@class="div-map2"])').strip()
            reg_no = reg_no_str.replace('：', ':').split(':')[1]
            tmp_dict['company_status'] = company_status
            tmp_dict['jbxx_uri'] = jbxx_uri
            tmp_dict['company_name'] = company_name
            tmp_dict['company_zch'] = reg_no.strip()
            html = etree.tostring(item)
            item_et = etree.HTML(html) # utf8 会造成历史名称乱码
            history_name = item_et.xpath('string(.//div[@class="div-info-circle3"]/span[@class="g3"])').strip()
            # history_name_list = filter(lambda x: x,
            #                            map(lambda x: x.strip(), history_name.replace(u'；', ';').split(';')))
            # tmp_dict['history_name_list'] = history_name_list
            tmp_dict['history_name'] = history_name # 历史名称存在特殊情况，不做任何处理
            tmp_dict['snapshot_html'] = html
            tmp_dict['status'] = 0
            search_list.append(tmp_dict)
        except Exception as e:
            logger.info(u'解析搜索列表失败: {}'.format(str(e)))
    return search_list


def init_params(item):
    """
    :return:
    """
    logger.info(u'开始抓取公司: {}, 注册号：{}'.format(item['company_name'], item['company_zch']))
    global_value_key = ['seed_dict', ]
    for key in value_dict.keys():               # 首尾清理一次，避免搜索列表有多条数据的情况下，出现公司数据错位的情况
        if key not in global_value_key:
            del value_dict[key]

    page_dict['company_name'] = item['company_name']
    page_dict['company_zch'] = item['company_zch']
    page_dict['search_item'] = item
    page_dict['status'] = Status.SUCCESS     # 抓取状态，默认0 成功， 其它值为失败


def init_module_page(module_name, method, length=5, *args, **kwargs):
    if method.lower() == 'post':
        url = '{}{}'.format(host, value_dict['uri_dict']['{}_uri'.format(module_name)])
        data = {
            "draw": 1,
            "start": 0,
            "length": length
        }
    else:
        url = '{}{}'.format(host, value_dict['uri_dict']['{}_uri'.format(module_name)])
        data = None
    logger.info(u'开始抓取模块页码列表, module: {}'.format(module_name))
    resp = send_request(method, url, data, *args, **kwargs)
    page_list = get_total_page(resp.text)
    value_dict['{}_page_list'.format(module_name)] = page_list
    logger.info(u'抓取模块页码完成列表, module: {}, 列表为：{}'.format(module_name, page_list))


def iter_module_page(module_name, method, length=5, *args, **kwargs):
    page_dict[module_name] = []
    init_module_page(module_name, method, length, *args, **kwargs)
    page_list = value_dict['{}_page_list'.format(module_name)]
    logger.info(u'开始抓取模块翻页信息, module: {}'.format(module_name))
    for page in page_list:
        if method.lower() == 'post':
            url = value_dict['uri_dict']['{}_uri'.format(module_name)]
            data = {
                "draw": page,
                "start": (page - 1) * length,
                "length": length
            }
        else:
            url = '{}?start={}'.format(value_dict['uri_dict']['{}_uri'.format(module_name)], (page - 1) * length)
            data = None
        logger.info(u'开始抓取模块{}翻页, 页码: {}, method:{}, url:{}, data:{}'.\
                    format(module_name, page, method, url, data))
        resp = send_request(method, '{}{}'.format(host, url), data, *args, **kwargs)
        logger.info(u'翻页完成, 页码: {} 响应为：{}'.format(page, resp.text))
        page_dict[module_name].append({
            'page': page,
            'html': resp.text
        })
        time.sleep(1)
    logger.info(u'抓取模块翻页信息完成, module: {}'.format(module_name))


def get_module_detail_id_list(module_name, from_module, key_id):
    """
    提取模块详情id
    :param module_name:
    :param json_key:
    :return:
    """
    collection = []
    html_list = page_dict[from_module]
    for page in html_list:
        try:
            res_list = json.loads(page['html'])
            for item in res_list['data']:
                try:
                    xq_id = item.get(key_id)
                    if xq_id:
                        collection.append(xq_id)
                except:
                    logger.error(traceback.format_exc())
        except:
            logger.error(traceback.format_exc())
    value_dict['{}_id_list'.format(module_name)] = collection


def iter_module_detail_list(module_name, url_pattern, *args, **kwargs):
    page_dict['{}_page_list'.format(module_name)] = []
    xq_id_list = value_dict.get('{}_id_list'.format(module_name), [])
    for i, detail_id in enumerate(xq_id_list):
        try:
            url = url_pattern.format(host, detail_id)
            logger.info(u'迭代模块详情第{}条，模块：{}， url：{}'.format(i+1, module_name, url))
            resp = send_request('get', url, *args, **kwargs)
            page_dict['{}_page_list'.format(module_name)].append({
                'id': detail_id,
                'html': resp.text
            })
            time.sleep(3)
            logger.info(u'模块详情请求成功，原文为：{}'.format(resp.text))
        except Exception as e:
            err_msg = u'迭代模块详情出错，module:{}, e: {}'.format(module_name, str(e))
            logger.error(err_msg)
            page_dict['status'] = Status.EXCEPTION
            raise Exception(err_msg)


def iter_dcdyxq_list():
    page_dict['dcdy_xq_list'] = []
    for dcdyxq_id in value_dict['dcdyxq_id_list']:
        dcdy_xq_key_list = [
            'mortregpersoninfo',
            'mortCreditorRightInfo',
            'mortGuaranteeInfo',
            'getMortAltItemInfo',
            'getMortRegCancelInfo'
        ]
        for xq_key in dcdy_xq_key_list:
            xq_url = '{}/corp-query-entprise-info-{}-{}.html'.format(host, xq_key, dcdyxq_id)
            resp = send_request('get', xq_url)
            page_dict['dcdy_xq_list'].append({
                'html': resp.text,
                'id': dcdyxq_id,
                'xq_key': xq_key,
            })
            time.sleep(3)


def init_gdxx():
    iter_module_page(module_name='gdxx', method='post', length=5)
    gdxq_url_pattern = '{}/corp-query-entprise-info-shareholderDetail-{}.html'
    get_module_detail_id_list('gdxq', 'gdxx', 'invId')
    iter_module_detail_list('gdxq', gdxq_url_pattern, cache_key_switch=False)

# def init_sbxx():
#     iter_module_page(module_name='sbxx', method='get', length=4)

def init_baxx():
    iter_module_page(module_name='baxx', method='post', length=16)


def init_bgxx():
    iter_module_page(module_name='bgxx', method='post', length=5)


def init_fzjg():
    iter_module_page(module_name='fzjg', method='get', length=9)


def init_dcdy():
    iter_module_page(module_name='dcdy', method='post', length=5)
    get_module_detail_id_list('dcdyxq', 'dcdy', 'morReg_Id')


def init_gqcz():
    iter_module_page(module_name='gqcz', method='post', length=5)       # TODO 没找到详情


def init_sfxz():
    iter_module_page(module_name='sfxz', method='post', length=5)


def init_xzxktop():
    iter_module_page(module_name='xzxktop', method='post', length=5)


def init_xzcftop():
    iter_module_page(module_name='xzcftop', method='post', length=5)


def init_jyyctop():
    iter_module_page(module_name='jyyctop', method='post', length=5)


def init_hmdtop():
    iter_module_page(module_name='hmdtop', method='post', length=5)


def init_qsxx():
    iter_module_page(module_name='qsxx', method='post', length=5)


def init_ccjc():
    iter_module_page(module_name='ccjc', method='post', length=5)


def init_xzxkbottom():
    iter_module_page(module_name='xzxkbottom', method='post', length=5)


def init_xzcfbottom():
    iter_module_page(module_name='xzcfbottom', method='post', length=5)


def init_zscqbottom():
    iter_module_page(module_name='zscqbottom', method='post', length=5)


def init_sjxx():
    iter_module_page(module_name='sjxx', method='get', length=10) # # 网页返回json，每页10条，不同于其他模块


def init_gdxxbottom():
    iter_module_page(module_name='gdxxbottom', method='post', length=5)


def init_gqbgbottom():
    iter_module_page(module_name='gqbgbottom', method='post', length=5)

def init_zxggbottom():
    iter_module_page(module_name='zxggbottom', method='get', length=5)


def iter_search_list():
    search_list = copy.deepcopy(value_dict['search_list'])  # 深拷贝出来，因为后面会对value_dict进行清理
    if not search_list:
        logger.info(u'搜索列表解析结果为空，无此公司,company_key:{}'.format(value_dict['seed_dict']['company_key']))
        page_dict['status'] = Status.NON_COMPANY
        insert_error_record(page_dict, value_dict)
        # TODO 无此公司的情况，是否需要记录存入空数据
        save_html()

    for item in search_list[:1]:      # 只抓取第一条信息
        # if item.get("company_status") == u"已吊销":
        #     page_dict['status'] = Status.REVOVATION
        #     save_html()
        #     return
        try:
            init_params(item)

            # ====================== 模块名====================案例公司=============

            init_jbxx(item)         # 基本信息

            init_gdxx()             # 股东信息                 四川众和源餐饮管理有限公司

            init_baxx()             # 备案信息                 长沙银行股份有限公司

            init_bgxx()             # 变更信息                 贵州银行股份有限公司

            init_fzjg()             # 分支机构                 贵州银行股份有限公司

            init_dcdy()             # 动产抵押                 山西立恒钢铁集团股份有限公司
            iter_dcdyxq_list()      # 动产抵押详情

            init_gqcz()             # 股权出质                 山西立恒钢铁集团股份有限公司

            init_sfxz()             # 司法协助                 山西立恒钢铁集团股份有限公司  # TODO 司法协助没抓详情(需求文档中没有要求)

            init_xzxktop()          # 行政许可top              山西立恒钢铁集团股份有限公司

            init_xzcftop()          # 行政处罚top              山西立恒钢铁集团股份有限公司

            init_jyyctop()          # 经营异常top              秦皇岛广瀚水利技术咨询服务有限公司

            init_hmdtop()           # 黑名单top                四川省南江宏益矿业有限公司

            init_qsxx()             # 清算信息top              四川省南江宏益矿业有限公司

            init_ccjc()             # 抽查检查信息              庆阳诚盛钻井工程有限公司

            # init_sbxx()             # 商标信息

            init_xzxkbottom()       # 行政许可bottom           东营利源环保科技有限公司

            init_xzcfbottom()       # 行政处罚bottom           古田县鸿安液化气有限责任公司

            init_zscqbottom()       # 知识产权bottom           郑州都森环保科技有限公司

            init_gdxxbottom()       # 股东信息bottom           深圳市富满电子集团股份有限公司

            init_gqbgbottom()       # 股权变更信息bottom        江西华业消防器材有限公司

            init_sjxx()             # 随机信息                 遂宁市惟思安防设备有限公司  # 不抓取 # 没找到存储的数据

            init_zxggbottom()       # 注销信息


        except Exception as e:
            error_msg = u'抓取公司: {}异常, 原因：{}'.format(value_dict.get('seed_dict').get('company_key'), str(e))
            logger.error(error_msg)
            page_dict['status'] = Status.EXCEPTION
            page_dict['error_msg'] = error_msg
            insert_error_record(page_dict, value_dict)
            raise LogicException(str(e))
        # TODO 看抓取正确和抓取异常怎么存储
        save_html()


def save_html():
    global value_dict
    global page_dict
    page_dict['uuid'] = str(uuid)
    # TODO save source to db
    page_dict['seed_dict'] = value_dict['seed_dict']
    insert_page_json(page_dict)
    logger.info(u'完成了:{}'.format(value_dict))
    logger.info(u'完成了:{}'.format(page_dict))
    value_dict.clear()
    page_dict.clear()





