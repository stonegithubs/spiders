# coding=utf-8
"""
肇庆市鼎湖区人民法院

模板1，直接继承KtggBase 基类， 需要些整个爬虫逻辑
"""

__author__ = 'wu_yong'

import re
import time
import traceback
from lxml import etree
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.crawler.ktgg.utils.tools import remove_words
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.ktgg_base import KtggBase
from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException


class Zqdhfy(KtggBase):
    """
    肇庆市鼎湖区人民法院, 对应ktgg项目 1531.py 爬虫
    """
    ename = 'zqdhfy'
    cname = u'肇庆市鼎湖区人民法院'
    developer = u'吴勇'
    url_pattern = 'http://ssfw.zqdhfy.gov.cn/ktxx.aspx?cateId=15&page={}'

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=False,
            proxy_mode='zm',
            session_keep=True,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.SWITCH_USE,
        )
        super(Zqdhfy, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        try:
            first_url = self.url_pattern.format(1)
            resp = self.downloader.get(first_url, retry_cnt=10)
            html = resp.text
            if not resp:
                err_msg = u'下载列表页码resp为False'
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            page_cnt = re.findall(ur'共\s*(\d+)\s*页', html, flags=re.S)
            if not page_cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg+'：{}'.format(html))
                raise LogicException(err_msg)
            return int(page_cnt[0])
        except Exception:
            err_msg = u'下载列表页码失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def iter_page_list(self, total_page):
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD
        else:
            for page in range(1, total_page+1):   # TODO just for test
                page_url = self.url_pattern.format(page)
                try:
                    resp = self.downloader.get(page_url, retry_cnt=10)
                    html = resp.text
                    self.parse_per_page(html, page_url)
                except Exception:
                    err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, page_url, traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(0.5)

    def parse_per_page(self, html, page_url):
        collection = []
        replace_list = [u"被告人", u"被告", u"原告", u"第三人"]
        et = etree.HTML(html)
        tr_list = et.xpath('.//table[@id="tbData"]/tr')
        if not tr_list:
            return collection
        raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
        for index, tr in enumerate(tr_list):
            td_list = tr.xpath('./td')
            if not td_list:
                continue
            try:
                date_tmp = td_list[0].xpath('string(.)').strip()
                time_tmp = td_list[1].xpath('string(.)').strip()
                court_date = '{} {}'.format(date_tmp, time_tmp).strip()
                fating = td_list[2].xpath('string(.)').strip()
                case_number_tmp = td_list[3].xpath('string(.)').strip()
                case_number = case_number_tmp.replace('（', '(').replace('）', ')').replace('，', ',')
                case_cause = td_list[4].xpath('string(.)').strip()
                party = td_list[6].xpath('string(.)').strip()
                temp_dsr = party.replace(u':', u',').replace(u'：', u',').strip()
                party_parse = remove_words(temp_dsr, replace_list).strip(u',').strip()
                party_parse_flag = 1
                doc = '{} {} {} {} {}'.format(case_number, case_cause, party, court_date, fating)
                data_dict = {
                    'date': self.do_time,
                    "case_number": case_number,
                    "doc": doc,
                    "court_date": court_date,
                    "doc_id": "{}_{}".format(case_number, court_date),
                    "case_cause": case_cause,
                    "name": self.name,
                    "court": u"肇庆市鼎湖区人民法院",
                    "court_room": fating,
                    "province": u"广东",
                    "party": party,
                    "party_parse": party_parse,
                    "party_parse_flag": party_parse_flag,
                    "url": page_url,
                    "raw_id": raw_id
                }
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict)
            except Exception:
                err_msg = u'保存数据出现异常,index:{}, page_url: {}'.format(index, page_url)
                self.logger.error(err_msg)
                self.status = TASK_STATUS.FAILED
                raise LogicException(err_msg)
            self.logger.info(u'保存第{}条数据完成'.format(index))

    def start(self):
        try:
            self.logger.info(u'开始抓取爬虫:{}'.format(self.ename))
            self.do_time = self.ktgg_tool.now_date
            self.ktgg_tool.insert_ktgg_spider_status(self.ename, self.cname, self.developer, self.do_time)
            total_page = self.get_total_page()
            # total_page = 3
            if self.seed_dict.get('is_increment') is True:
                page = self.seed_dict.get('page', 20)  # 默认抓取前20页
                total_page = page if page <= total_page else total_page
                self.logger.info(u'开始增量抓取，spider_name:{}, 抓取前{}页'.format(self.ename, total_page))
            else:
                self.logger.info(u'开始全量抓取，spider_name:{}, 抓取前{}页'.format(self.ename, total_page))
            self.iter_page_list(total_page)

            if self.status != TASK_STATUS.NO_RECORD:
                self.status = TASK_STATUS.SUCCESS

            self.ktgg_tool.update_ktgg_spider_status(self.ename, self.status, self.do_time)
            self.logger.info('ppp: ', self.stat_dict)
            self.ktgg_tool.update_ktgg_spider_cnt(self.ename, self.stat_dict, self.do_time)
        except Exception:
            err_msg = u'抓取ktgg爬虫异常：爬虫名称: {}, 异常原因: {}'.format(self.ename, traceback.format_exc())
            self.logger.error(err_msg)
            self.status = TASK_STATUS.FAILED
            self.ktgg_tool.update_ktgg_spider_status(self.ename, self.status, self.do_time)
            self.ktgg_tool.update_ktgg_spider_cnt(self.name, self.stat_dict, self.do_time)
            raise LogicException(err_msg)

        self.logger.info(u'爬虫抓取完成:{}'.format(self.name))


if __name__ == '__main__':
    ins = Zqdhfy(None, {})
    a = ins.start()
    print a






