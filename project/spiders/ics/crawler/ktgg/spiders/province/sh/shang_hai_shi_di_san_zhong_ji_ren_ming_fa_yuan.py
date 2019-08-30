#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:shszfy.py
author:mjw
version: 1.0
date:2018-09-29-11:50
"""

import sys
import time
import traceback
from bs4 import BeautifulSoup as bs
from ics.utils.exception_util import LogicException
from ics.utils import get_ics_logger
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.crawler.ktgg.utils.ktgg_data import KtggData

reload(sys)
sys.setdefaultencoding('utf-8')


class ShangHaiShiDiSanZhongJiRenMingFaYuan(KtggIterPageBase):
    """
    上海市第三中级人民法院
    """
    domain = 'www.shszfy.gov.cn'
    ename = 'shang_hai_shi_di_san_zhong_ji_ren_ming_fa_yuan'
    cname = u'上海市第三中级人民法院'
    developer = u'毛靖文'

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=False,
            proxy_mode='dly',
            session_keep=True,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.SWITCH_USE,
        )
        super(ShangHaiShiDiSanZhongJiRenMingFaYuan, self).__init__(self.seed_dict, self.logger)

    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def get_total_page(self):
        return 1

    def iter_page_list(self, total_page):
        for page in range(1, total_page + 1):
            page_url = "http://www.shszfy.gov.cn/list.jhtml?lmdm=ktgg&ds1_p={}".format(page)
            try:
                resp = self.downloader.get(page_url, headers=self.headers, retry_cnt=20, timeout=20)
                self.parse_per_page(resp.content)
            except Exception:
                err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, page_url, traceback.format_exc())
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            time.sleep(0.5)

    def parse_per_page(self, html):
        soup = bs(html, "lxml")
        li_list = soup.select('table#report tr')
        raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
        del (li_list[0])
        for index, li in enumerate(li_list):
            list_td = li.select("td")
            data = KtggData()
            data.raw_id = raw_id
            data.province = "上海市"
            data.domain = self.domain
            data.cname = self.cname
            data.ename = self.ename
            data.court = "上海市第三中级人民法院"
            data.court_room = list_td[1].text
            data.court_date = list_td[2].text
            data.case_number = list_td[3].text
            data.case_cause = list_td[4].text
            data.undertake_dept = list_td[5].text
            data.chief_judge = list_td[6].text
            data.prosecutor = list_td[7].text
            data.defendant = list_td[8].text
            self.ktgg_tool.insert_ktgg_data(data, self.stat_dict, '{}_{}_{}'.format(self.ename, data.case_number, data.court_date))


if __name__ == '__main__':
    seed_dict = {'name': 'shszfy', 'is_increment': True, 'page': 1}
    spider = ShangHaiShiDiSanZhongJiRenMingFaYuan(None, seed_dict)
    spider.start()
