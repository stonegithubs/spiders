# coding=utf-8
"""
广州法院庭审直播网
"""


__author__ = 'wu_yong'

import re
import sys
import time
import traceback
from bs4 import BeautifulSoup

from ics.utils.exception_util import LogicException
from ics.utils import get_ics_logger
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase

reload(sys)
sys.setdefaultencoding('utf-8')


class GuangZhouFaYuanTingShenZhiBoWang(KtggIterPageBase):
    """
    广州法院庭审直播网, 对应ktgg项目 368.py 爬虫
    """
    domain = 'gz.sifayun.com'
    ename = 'guang_zhou_fa_yuan_ting_shen_zhi_bo_wang'
    cname = u'广州法院庭审直播网'
    developer = u'吴勇'
    url_pattern = 'http://gz.sifayun.com/new/select?courtId=14&catalogId=0&day=99999&area=null&pageNumber={}&_={}'

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
        super(GuangZhouFaYuanTingShenZhiBoWang, self).__init__(self.seed_dict, self.logger)

    headers = {
        'Accept': '*/*',
        'Host': 'gz.sifayun.com',
        'Proxy-Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def get_total_page(self):
        page = 1
        first_page_url = self.url_pattern.format(page, int(time.time()*1000))
        resp = self.downloader.get(first_page_url, headers=self.headers, retry_cnt=20, timeout=20)
        total_page = ''.join(re.findall(ur'共\s*(\d+)\s*页', resp.text, flags=re.S)).strip()
        return int(total_page)

    def iter_page_list(self, total_page):
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD
        else:
            for page in range(1, total_page + 1):
                page_url = self.url_pattern.format(page, int(time.time()*1000))
                try:
                    resp = self.downloader.get(page_url, headers=self.headers, retry_cnt=20, timeout=20)
                    html = resp.text
                    self.parse_per_page(html, page_url)
                except Exception:
                    err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, page_url, traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(0.5)

    def parse_per_page(self, html, page_url):
        soup = BeautifulSoup(html)
        li_list = soup.select('div#refreshQuery ul#ul li')
        raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
        self.logger.info(self.stat_dict)
        for index, li in enumerate(li_list):
            try:
                case_cause = li.select('div.content_right_case_title2 strong')[0].text
                item_list = li.select('div.hot_case_list2_main > div.index_broadcast_address.OverFlow')
                if len(item_list) < 4:
                    self.logger.error(u'页面出现非预期格式')
                    raise LogicException(u'页面出现非预期格式')

                party_string = item_list[1].text.strip()
                party = re.sub(r'\s{1,}', ' ', party_string, flags=re.S)

                case_number = item_list[0].text.replace('：', ':').split(':', 1)[1].strip()
                court_date = item_list[2].text.replace('：', ':').split(':', 1)[1].strip()
                court_string = item_list[3].text.replace('：', ':').split(':', 1)[1].strip()

                court_string_list = court_string.split(' ', 1)
                if len(court_string_list) == 2:
                    court = court_string_list[0].strip()
                    court_room = court_string_list[1].strip()
                else:
                    court = court_string
                    court_room = ''
                data_dict = {
                    "case_number": case_number,
                    "court_date": court_date,
                    "case_cause": case_cause,
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": self.cname,
                    "court": court,
                    "court_room": court_room,
                    "province": u"广州市",
                    "party": party,
                    "url": page_url,
                    "raw_id": raw_id
                }
                unique_id = "{}_{}_{}".format(self.ename, case_number, court_date)
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
            except Exception:
                err_msg = u'保存数据出现异常,index:{}, page_url: {}, html: {}'.format(index, page_url, html)
                self.logger.error(err_msg)
                raise LogicException(err_msg)
            self.logger.info(u'保存第{}条数据完成'.format(index))
        self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': 'guang_zhou_fa_yuan_ting_shen_zhi_bo_wang', 'is_increment': True, 'page': 1}
    spider = GuangZhouFaYuanTingShenZhiBoWang(None, seed_dict)
    spider.start()

