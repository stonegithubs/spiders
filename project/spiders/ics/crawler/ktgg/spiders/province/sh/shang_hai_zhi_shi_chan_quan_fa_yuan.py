# coding=utf-8
"""
上海知识产权法院
"""

__author__ = 'He_zhen'

import re
import time
import traceback
from bs4 import BeautifulSoup as bs
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException


class ShangHaiZhiShiChanQuanFaYuan(KtggIterPageBase):
    url_home = "http://www.shzcfy.gov.cn/ktgg.jhtml?lmdm=ktgg"
    domain = 'www.shzcfy.gov.cn'
    ename = 'shang_hai_zhi_shi_chan_quan_fa_yuan'
    cname = u'上海知识产权法院'
    developer = u'何振'
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
              'Accept-Encoding': 'gzip,deflate,br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1'}

    data = dict()

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
            proxy_strategy=PROXY_STRATEGY.SWITCH_USE,
        )
        super(ShangHaiZhiShiChanQuanFaYuan, self).__init__(self.seed_dict, self.logger)

    def parse_per_page(self, html, href, raw_id, page=0):
        try:
            self.do_time = self.ktgg_tool.now_date
            soup = bs(html, 'lxml')
            tab = soup.select("#report tr")[1:]
            for index, line in enumerate(tab):
                data = line.select("b")
                court_room = data[0].text
                court_date = data[1].text
                case_number = data[2].text
                case_cause = data[3].text
                undertake_dept = data[4].text
                chief_judge = data[5].text
                prosecutor = data[6].text
                defendant = data[7].text

                data_dict = {
                    # 'date': self.do_time,
                    "case_number": case_number,
                    "case_cause": case_cause,
                    # "doc_id": "{}_{}".format(case_number, court_date),
                    "undertake_dept": undertake_dept,
                    "cname": self.cname,
                    "ename": self.ename,
                    "domain": self.domain,
                    "chief_judge": chief_judge,
                    "prosecutor": prosecutor,
                    "court_room": court_room,
                    "defendant": defendant,
                    "province": u'上海',
                    "party": "",
                    # "party_parse": "",
                    # "party_parse_flag": 0,
                    "url": href,
                    "raw_id": raw_id
                }
                unique_id = case_number + self.ename
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'详情{} 失败：{}'.format(href, traceback.format_exc())
            self.logger.info(u"第{}页 第{}条 {}".format(page, index, err_msg))
            raise LogicException(err_msg)

    def get_total_page(self):
        try:
            resp = self.downloader.get(self.url_home, retry_cnt=10)
            html = resp.text
            page_cnt = re.search(ur'共(\d+)页', html).group(1)
            if not page_cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg + '：{}'.format(html))
                raise LogicException(err_msg)
            return int(page_cnt)
        except Exception:
            err_msg = u'下载列表页码失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def iter_page_list(self, total_page):
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD
        else:
            for page in range(total_page, total_page - 5, -1):
                try:
                    self.data.update({"ds_p": page})
                    resp = self.downloader.get(self.url_home, params=self.data)
                    html = resp.text
                    href = resp.url
                    raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
                    self.parse_per_page(html, href, raw_id, page)
                except Exception:
                    err_msg = u'下载出错,页码：{}, data：{}, 原因：{}'.format(page, self.data, traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(3)


if __name__ == '__main__':
    ins = ShangHaiZhiShiChanQuanFaYuan(None, {"is_increment": True, "page": 1})
    a = ins.start()
    print a
