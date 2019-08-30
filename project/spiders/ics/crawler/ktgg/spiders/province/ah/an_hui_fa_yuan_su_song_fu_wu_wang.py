# coding=utf-8
"""
安徽法院诉讼服务网
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


class AnHuiFaYuanSuSongFuWuWang(KtggIterPageBase):

    """
        安徽法院诉讼服务网
    """
    domain = 'www.ahgyss.cn'
    ename = 'an_hui_fa_yuan_su_song_fu_wu_wang'
    cname = u'安徽法院诉讼服务网'
    developer = u'何振'
    url_pattern = 'http://www.ahgyss.cn/ktgg/index_{}.jhtml'
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip,deflate,br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'www.ahgyss.cn',
              'Referer': 'http://www.ahgyss.cn/ktgg/index.jhtml',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1'}

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=True,
            basic_headers=self.header,
            proxy_mode='dly',
            session_keep=True,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.CONTINUITY_USE,
        )
        super(AnHuiFaYuanSuSongFuWuWang, self).__init__(self.seed_dict, self.logger)

    def parse_per_page(self, html, page):
        soup = bs(html, 'lxml')
        details = soup.select("div.c1-body a")
        for index, detail in enumerate(details):
            href = detail['href']
            try:
                resp = self.downloader.get(href, retry_cnt=10).content
                self.do_time = self.ktgg_tool.now_date
                raw_id = self.ktgg_tool.insert_page_source(resp, self.ename, self.cname, self.do_time)
                self.logger.info(u"第{}页 第{}条 详情抓取成功".format(page, index))
                dt_soup = bs(resp, 'lxml')
                date_court=dt_soup.find(style="color: grey; margin-top: 10px; margin-bottom: 10px;").text
                court_date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",date_court).group(0)
                court = date_court.split(' ')[1]
                case_number=dt_soup.find(style="font-size: 20pt; padding-top: 10px; border-top: 1px #d6d3d3 dotted;").text
                doc = dt_soup.select("#hiddenTxt")[0]['value']
                doc = doc.replace(u'ሴ','').replace('\r','')
                case_judge = doc.split("。")
                presiding_judge = case_judge[1].split('：')[2]

                data_dict = {
                    # 'date': self.do_time,
                    "case_number": case_number,
                    # "doc": doc,
                    "court_date": court_date,
                    "court": court,
                    # "doc_id": "{}_{}".format(case_number, court_date),
                    "case_cause": "",
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": self.cname,
                    "prosecutor": "",
                    "defendant": "",
                    "court_room": "",
                    "presiding_judge": presiding_judge,
                    "province": u'安徽',
                    "party": "",
                    # "party_parse": "",
                    # "party_parse_flag": 0,
                    "url": href,
                    "raw_id": raw_id
                }
                unique_id = '{}_{}_{}'.format(self.ename, case_number, court_date)
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)

            except Exception:
                err_msg = u'详情{} 失败：{}'.format(href, traceback.format_exc())
                self.logger.info(u"第{}页 第{}条 {}".format(page, index, err_msg))
                raise LogicException(err_msg)

    def get_total_page(self):
        try:
            first_url = self.url_pattern.format(1)
            resp = self.downloader.get(first_url, retry_cnt=10)
            html = resp.text
            soup = bs(html, 'lxml')
            page_cnt = soup.select("div.sswy_sub_turn_page div p a")[4].string
            if not page_cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg+'：{}'.format(html))
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
            for page in range(1, total_page+1):
                page_url = self.url_pattern.format(page)
                try:
                    resp = self.downloader.get(page_url, retry_cnt=10)
                    html = resp.text
                    self.parse_per_page(html, page)
                except Exception:
                    err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, page_url, traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(0.5)

if __name__ == '__main__':
    seed_dict = {'ename': 'an_hui_fa_yuan_su_song_fu_wu_wang', 'is_increment': True, 'page': 1}
    ins = AnHuiFaYuanSuSongFuWuWang(None, seed_dict)
    a = ins.start()
    print a
