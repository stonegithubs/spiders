# coding=utf-8
"""
绍兴市中级人民法院
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


class ShaoXingShiZhongJiRenMinFaYuan(KtggIterPageBase):
    """
        绍兴市中级人民法院
    """
    domain = 'www.sxcourt.gov.cn'
    ename = 'shao_xing_shi_zhong_ji_ren_ming_fa_yuan'
    cname = u'绍兴市中级人民法院'
    developer = u'何振'
    url_pattern = "http://www.sxcourt.gov.cn/E_ktgg.asp"
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
              'Accept-Encoding': 'gzip,deflate,sdch',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'www.sxcourt.gov.cn',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1', }

    data = {
        "ah": "",
        "ay": "",
        "dsr": "",
        "spz": "",
        "ktsj": "",
    }

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
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.CONTINUITY_USE,
        )
        super(ShaoXingShiZhongJiRenMinFaYuan, self).__init__(self.seed_dict, self.logger)

    def parse_per_page(self, html, href, page=1):
        try:
            soup = bs(html, 'lxml')
            raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
            infos = soup.select('div.list_hdcnt table tr')[2:]
            for info in infos:
                case_number = info.contents[1].text
                case_cause = info.contents[3].text
                party = info.contents[5].text
                court_date = info.contents[7].text
                court_room = info.contents[9].text
                undertake_dept = info.contents[11].text
                chief_judge = info.contents[13].text

                data_dict = {
                    "case_number": case_number,
                    "court_date": court_date,
                    "case_cause": case_cause,
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": self.cname,
                    "court_room": court_room,
                    "province": u'浙江',
                    "party": party,
                    "undertake_dept": undertake_dept,
                    "chief_judge": chief_judge,
                    "url": href,
                    "raw_id": raw_id
                }
                unique_id = '{}_{}'.format(self.ename, case_number)
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'详情{} 失败：{}'.format(href, traceback.format_exc())
            self.logger.info(u"第{}页 出错{}".format(page, err_msg))
            raise LogicException(err_msg)

    def get_total_page(self):
        try:
            self.data.update({"page": 1})
            resp = self.downloader.get(self.url_pattern, params=self.data, retry_cnt=10)
            html = resp.text.encode('ISO-8859-1').decode('gbk')
            page_cnt = re.search(ur'共(\d+)页', html).group(1)
            if not page_cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg + '：{}'.format(html))
                raise LogicException(err_msg)
            self.parse_per_page(html, resp.url)
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
            for page in range(1, total_page):
                try:
                    self.data.update({"page": page})
                    resp = self.downloader.get(self.url_pattern, params=self.data)
                    html = resp.text
                    self.parse_per_page(html, resp.url, page)
                except Exception:
                    err_msg = u'下载出错,页码：{}, data：{}, 原因：{}'.format(page, self.data, traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(3)


if __name__ == '__main__':
    seed_dict = {'ename': 'shao_xing_shi_zhong_ji_ren_ming_fa_yuan', 'is_increment': False, 'page': 1}
    ins = ShaoXingShiZhongJiRenMinFaYuan(None, seed_dict)
    a = ins.start()
    print a
