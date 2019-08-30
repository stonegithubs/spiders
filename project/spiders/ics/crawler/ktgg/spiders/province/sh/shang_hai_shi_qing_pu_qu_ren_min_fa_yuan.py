# coding=utf-8
"""
上海市青浦区人民法院
"""

__author__ = 'He_zhen'

import time
import traceback
from bs4 import BeautifulSoup as bs
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException


class ShangHaiShiQingPuQuRenMinFaYuan(KtggIterPageBase):
    domain = 'lawcourt.shqp.gov.cn'
    ename = 'shang_hai_shi_qing_pu_qu_ren_min_fa_yuan'
    cname = u'上海市青浦区人民法院'
    developer = u'何振'
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01,charset=utf-8',
              "Content-Encoding": "gzip",
              'Accept-Language': 'zh-CN,zh;q=0.9',
              "Content-Type":"text/html",
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1'}

    url_start = "http://lawcourt.shqp.gov.cn/gb/special/node_9614.htm"

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=False,
            proxy_mode='dly',
            session_keep=False,
            basic_headers=self.header,
            headers_mode=HEADERS_MODEL.UPDATE,
            proxy_strategy=PROXY_STRATEGY.CONTINUITY_USE,
        )
        super(ShangHaiShiQingPuQuRenMinFaYuan, self).__init__(self.seed_dict, self.logger)

    def parse_per_page(self, html, href, raw_id, page=0):
        try:
            self.do_time = self.ktgg_tool.now_date
            soup = bs(html, 'lxml')
            tab = soup.find("td",{"height":"132"})
            details = tab.find_all("p")[:-1]
            for index, line in enumerate(details):
                body = line.text

                data_dict = {
                    "cname": self.cname,
                    "ename": self.ename,
                    "domain": self.domain,
                    "province": u'上海',
                    "party": "",
                    "body": body,
                    "url": href,
                    "raw_id": raw_id
                }
                unique_id = body + self.ename
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'详情{} 失败：{}'.format(href, traceback.format_exc())
            self.logger.info(u"第{}页 第{}条 {}".format(page, index, err_msg))
            raise LogicException(err_msg)

    def get_total_page(self):
        return 1

    def iter_page_list(self, total_page):
        try:
            resp = self.downloader.get(self.url_start)
            html = resp.text.encode('ISO-8859-1', 'ingore')
            href = resp.url
            raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
            self.parse_per_page(html, href, raw_id, total_page)
        except Exception:
            err_msg = u'下载出错,页码：{}, data：{}, 原因：{}'.format(total_page, traceback.format_exc())
            self.logger.warning(err_msg)
            raise LogicException(err_msg)
        time.sleep(3)


if __name__ == '__main__':
    ins = ShangHaiShiQingPuQuRenMinFaYuan(None, {"is_increment": False, "page": 1})
    a = ins.start()
    print a
