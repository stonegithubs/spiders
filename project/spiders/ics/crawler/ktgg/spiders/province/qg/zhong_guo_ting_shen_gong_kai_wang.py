# coding=utf-8


__author__ = 'wu_yong'

import re
import json
import time
import traceback
from retry import retry
from bs4 import BeautifulSoup

from ics.utils import get_ics_logger
from ics.crawler.ktgg.core.ktgg_base import KtggBase
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY


class ZhongGuoTingShenGongKaiWang(KtggBase):
    """
    中国庭审公开网爬虫，对应老爬虫2.py
    根据分析，32省份中，所有省份都只需要抓取高级人民法院，就包括了中级、基层、高级人民法院的信息
    除此之外北京还需抓取最高人民法院
    """

    domain = 'tingshen.court.gov.cn'
    ename = 'zhong_guo_ting_shen_gong_kai_wang'
    cname = u'中国庭审公开网'
    developer = u'吴勇'
    host = 'tingshen.court.gov.cn'

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=True,
            proxy_mode='dly',
            session_keep=True,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.CONTINUITY_USE,
        )
        self.__init_downloader()
        super(ZhongGuoTingShenGongKaiWang, self).__init__(self.seed_dict, self.logger)

    def __init_downloader(self):
        def judge_html_invalid(resp, meta):
            if 'setCookie("acw_sc__v3"' in resp.text:
                self.downloader.change_add_grey_proxy()
                return True

        self.downloader.set_retry_solution(judge_html_invalid)

    @property
    def headers(self):
        return {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'tingshen.court.gov.cn',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Cookie': 'acw_tc={};'.format(int(time.time())),
    }

    def get_court_list(self):
        court_list = [
            {"city_name": u"北京", "area_code": "110000", 'court_id': '0', 'court_level': '1'},       # 最高人民法院
            # {"city_name": u"北京", "area_code": "110000", 'court_id': '1'},       # 北京市高级人民法院
            # {"city_name": u"天津", "area_code": "120000", 'court_id': '51'},      # 天津市高级人民法院
            # {"city_name": u"河北", "area_code": "130000", 'court_id': '100'},     # 河北省高级人民法院
            # {"city_name": u"山西", "area_code": "140000", 'court_id': '300'},     # 山西省高级人民法院
            # {"city_name": u"内蒙古", "area_code": "150000", 'court_id': '451'},   # 内蒙古自治区高级人民法院
            # {"city_name": u"辽宁", "area_code": "210000", 'court_id': '600'},     # 辽宁省高级人民法院
            # {"city_name": u"吉林", "area_code": "220000", 'court_id': '750'},     # 吉林省高级人民法院
            # {"city_name": u"黑龙江", "area_code": "230000", 'court_id': '850'},   # 黑龙江省高级人民法院
            # {"city_name": u"上海", "area_code": "310000", 'court_id': '1100'},    # 上海市高级人民法院
            # {"city_name": u"江苏", "area_code": "320000", 'court_id': '1150'},    # 江苏省高级人民法院
            # {"city_name": u"浙江", "area_code": "330000", 'court_id': '1300'},    # 浙江省高级人民法院
            # {"city_name": u"安徽", "area_code": "340000", 'court_id': '1451'},    # 安徽省高级人民法院
            # {"city_name": u"福建", "area_code": "350000", 'court_id': '1600'},    # 福建省高级人民法院
            # {"city_name": u"江西", "area_code": "360000", 'court_id': '1700'},    # 江西省高级人民法院
            # {"city_name": u"山东", "area_code": "370000", 'court_id': '1850'},    # 山东省高级人民法院
            # {"city_name": u"河南", "area_code": "410000", 'court_id': '2050'},       # 河南省高级人民法院
            # {"city_name": u"湖北", "area_code": "420000", 'court_id': '2250'},       # 湖北省高级人民法院
            # {"city_name": u"湖南", "area_code": "430000", 'court_id': '2400'},    # 湖南省高级人民法院
            # {"city_name": u"广东", "area_code": "440000", 'court_id': '2550'},   # 广东省高级人民法院
            # {"city_name": u"广西", "area_code": "450000", 'court_id': '2750'},    # 广西壮族自治区高级人民法院
            # {"city_name": u"海南", "area_code": "460000", 'court_id': '2900'},    # 海南省高级人民法院
            # {"city_name": u"重庆", "area_code": "500000", 'court_id': '2950'},    # 重庆市高级人民法院
            # {"city_name": u"四川", "area_code": "510000", 'court_id': '3000'},    # 四川省高级人民法院
            # {"city_name": u"贵州", "area_code": "520000", 'court_id': '3250'},    # 贵州省高级人民法院
            # {"city_name": u"云南", "area_code": "530000", 'court_id': '3350'},    # 云南省高级人民法院
            # {"city_name": u"西藏", "area_code": "540000", 'court_id': '3500'},    # 西藏自治区高级人民法院
            # {"city_name": u"陕西", "area_code": "610000", 'court_id': '3600'},    # 陕西省高级人民法院
            # {"city_name": u"甘肃", "area_code": "620000", 'court_id': '3750'},    # 甘肃省高级人民法院
            # {"city_name": u"青海", "area_code": "630000", 'court_id': '3900'},    # 青海省高级人民法院
            # {"city_name": u"宁夏", "area_code": "640000", 'court_id': '4000'},    # 宁夏回族自治区高级人民法院
            # {"city_name": u"新疆", "area_code": "650000", 'court_id': '4050'},    # 新疆维吾尔自治区高级人民法院
            # {"city_name": u"新疆兵团", "area_code": "6650000", 'court_id': '4166'}  # 新疆高级法院生产建设兵团分院
        ]
        return court_list

    def get_review_url_list(self):
        court_list = self.get_court_list()
        for item in court_list:
            if item.get('court_level') == '1': # 最高人民法院
                url_pattern = 'http://tingshen.court.gov.cn/search/a/revmor/full?keywords=&roomId=&label=&courtCode={}&catalogId=&courtLevel=1&pageNumber={}&pageSize=6&dataType=2&extType=&isOts='
            else:
                url_pattern = 'http://tingshen.court.gov.cn/search/a/revmor/full?label=&courtCode={}&catalogId=&pageNumber={}&courtLevel=2&dataType=2&pageSize=6&level=0&extType=&isOts=&keywords='
            item['url_pattern'] = url_pattern
        return court_list

    def get_per_count_total_page(self, court_dict, page):
        url_pattern = court_dict['url_pattern']
        court_id = court_dict['court_id']
        first_page_url = url_pattern.format(court_id, page)
        resp = self.downloader.get(first_page_url, headers=self.headers, retry_cnt=20, timeout=20)
        return self.parse_list(resp.text, court_dict, page)
            
    def parse_list(self, resp_text, court_dict, page):
        court_id = court_dict['court_id']
        city_name = court_dict['city_name']
        try:
            res_json = json.loads(resp_text)
            page_total = res_json['paging'].get('pageTotal')
            result_list = res_json['resultList']
        except Exception:
            err_msg = u'解析列表页详情失败，省份：{}， 页码：{}， court_id：{}, 原因：{}'.\
                format(city_name, page, court_id, traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        return page_total, result_list

    def get_per_court_case_detail(self, court_dict):
        total_page, result_list = self.get_per_count_total_page(court_dict, 1)
        self.logger.info(u'spider_name:{}, 省份：{}， court_id: {}, 实际页码：{}'.\
                         format(self.ename, court_dict['city_name'], court_dict['court_id'], total_page))
        if self.seed_dict.get('is_increment') is True:
            page = self.seed_dict.get('page', 2)  # 默认抓取前20页
            total_page = page if page <= total_page else total_page
            self.logger.info(u'开始增量抓取，spider_name:{}, 省份：{}， court_id: {}, 抓取前{}页'.\
                             format(self.ename, court_dict['city_name'], court_dict['court_id'], total_page))
        else:
            self.logger.info(u'开始全量抓取，spider_name:{}, 省份：{}， court_id: {}, 抓取前{}页'.\
                             format(self.ename, court_dict['city_name'], court_dict['court_id'], total_page))
        for page in range(1, total_page+1):
            _, result_list = self.get_per_count_total_page(court_dict, page)
            self.get_detail(result_list, court_dict, page)

    def get_detail(self, result_list, court_dict, page):
        self.logger.info(u'开始保存省份：{}， court_id:{}, 页码：{}'.\
                         format(court_dict['city_name'], court_dict['court_id'], page))
        for index, item in enumerate(result_list):
            self.downloader_detail(index, court_dict, item)
        self.logger.info(self.stat_dict)

    @retry(exceptions=LogicException, tries=20, delay=1)
    def downloader_detail(self, index, court_dict, item):
        case_url = 'http://tingshen.court.gov.cn/live/{}'.format(item['caseId'])
        resp = self.downloader.get(case_url, headers=self.headers, retry_cnt=20, timeout=20)
        raw_id = self.ktgg_tool.insert_page_source(resp.text, self.ename, self.cname, self.do_time)
        detail_dict = self.parse_case_detail(item, resp.text, case_url, raw_id, court_dict)

        try:
            unique_id = detail_dict.pop('doc_id')
            self.ktgg_tool.insert_ktgg_data(detail_dict, self.stat_dict, '{}_{}'.format(self.ename, unique_id))
        except Exception:
            err_msg = u'保存数据出现异常index:{}, case_url: {}'.format(index, case_url)
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        self.logger.info(u'保存第{}条数据完成'.format(index))

    def parse_case_detail(self, item, html, case_url, raw_id, court_dict):
        try:
            map_key = {
                'court_room': u'庭审地点',
            }
            soup = BeautifulSoup(html)
            case_ul_list = soup.select('div .trial-info ul')

            case_base = case_ul_list[0].select('li')
            result_dict = {}
            for li in case_base:
                text = li.text.strip()
                for k, v in map_key.items():
                    if v in text:
                        val = text.replace(v, '').strip()
                        result_dict[k] = val
            print result_dict

            partyul = ''.join(re.findall(r'\s+var\s+party\s*=\s*"(.+?)"', html, flags=re.S)).strip()
            result_dict['party'] = partyul
            result_dict['presiding_judge'] = item.get('judge')
            result_dict['court'] = item.get('courtName', '')
            result_dict['doc_id'] = item.get('caseId', '')
            result_dict['court_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(item['beginTime'])/1000))
            result_dict['case_number'] = item.get('caseNo', '').strip()
            result_dict['case_cause'] = item.get('title', '').strip()
            result_dict['url'] = case_url
            result_dict['province'] = court_dict['city_name']
            result_dict["domain"] = self.domain
            result_dict["ename"] = self.ename
            result_dict["cname"] = self.cname
            result_dict['raw_id'] = raw_id
            return result_dict
        except Exception as e:
            err_msg = u'解析详情出错：url: {}, e: {}'.format(case_url, str(e))
            self.logger.error(err_msg)
            self.downloader.change_add_grey_proxy()
            raise LogicException(err_msg)

    def start(self):
        """
        http://tingshen.court.gov.cn/live/1382971
        :return:
        """
        self.do_time = self.ktgg_tool.now_date
        self.logger.info(u'开始抓取：name: {}, date: {}'.format(self.ename, self.do_time))
        try:
            self.ktgg_tool.insert_ktgg_spider_status(self.ename, self.cname, self.developer, self.do_time)
            court_list = self.get_review_url_list()
            for court in court_list:
                self.logger.info(u'开始抓取省份：{}, court_id: {}'.format(court['city_name'], court['court_id']))
                self.get_per_court_case_detail(court)
                self.logger.info(u'抓取省份：{}, court_id: {}完成'.format(court['city_name'], court['court_id']))

            self.status = TASK_STATUS.SUCCESS
            self.ktgg_tool.update_ktgg_spider_status(self.ename, self.status, self.do_time)
            self.logger.info('stat_dict: {}'.format(self.stat_dict))
            self.ktgg_tool.update_ktgg_spider_cnt(self.ename, self.stat_dict, self.do_time)
        except Exception:
            err_msg = u'抓取ktgg爬虫异常：爬虫名称: {}, 异常原因: {}'.format(self.ename, traceback.format_exc())
            self.logger.error(err_msg)
            self.status = TASK_STATUS.FAILED
            self.ktgg_tool.update_ktgg_spider_status(self.ename, self.status, self.do_time)
            self.ktgg_tool.update_ktgg_spider_cnt(self.ename, self.stat_dict, self.do_time)
            raise LogicException(err_msg)
        self.logger.info(u'抓取结束：name: {}, date: {}'.format(self.ename, self.do_time))


if __name__ == '__main__':
    seed_dict = {'ename': ZhongGuoTingShenGongKaiWang.ename, 'is_increment': True, 'page': 1}
    ins = ZhongGuoTingShenGongKaiWang(None, seed_dict)
    ins.start()
