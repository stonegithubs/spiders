# coding=utf-8
"""
珠海市中级人民法院
"""

__author__ = 'He_zhen'

import re
import time
import json
import traceback
from bs4 import BeautifulSoup as bs
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException


class ZhuHaiShiZhongJiRenMinFaYuan(KtggIterPageBase):

    """
        珠海市中级人民法院
    """
    domain = 'www.zhcourt.gov.cn'
    ename = 'zhu_hai_shi_zhong_ji_ren_min_fa_yuan'
    cname = u'珠海市中级人民法院'
    developer = u'何振'
    url_detail_prefix = "http://www.zhcourt.gov.cn"
    url_home = 'http://www.zhcourt.gov.cn/courtweb/front/ggxxList/J40-splc-?gglx=kt'
    url_page = "http://www.zhcourt.gov.cn/courtweb/front/ggxxList"
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
              'Accept-Encoding': 'gzip,deflate,br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'www.zhcourt.gov.cn',
              'Referer': 'http://www.zhcourt.gov.cn/',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1'}

    data = {
        "ah":  "",
        "fjm": "J40",
        "gglx": "kt",
        "xszt": "splc",
        "dir": "down",
        "cs_token_flag": "1",
    }

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=True,
            proxy_mode='dly',
            session_keep=False,
            basic_headers = self.header,
            headers_mode=HEADERS_MODEL.UPDATE,
            proxy_strategy=PROXY_STRATEGY.CONTINUITY_USE,
        )
        self.__init_downloader()
        super(ZhuHaiShiZhongJiRenMinFaYuan, self).__init__(self.seed_dict, self.logger)

    def __init_downloader(self):
        def judge_html_invalid(resp, meta):
            if '连接尝试失败' in resp.text:
                self.downloader.change_add_grey_proxy()
                self.update_token()
                return True

        self.downloader.set_retry_solution(judge_html_invalid)

    def parse_per_page(self, html, page=0):
            soup = bs(html, 'lxml')
            details = soup.select('table')[6].select("a")
            for index, detail in enumerate(details):
                href = detail['href']
                case_number = detail.text
                court_date = detail.contents[1].text
                try:
                    resp = self.downloader.get(self.url_detail_prefix + href).content
                    raw_id = self.ktgg_tool.insert_page_source(resp, self.ename, self.cname, self.do_time)
                    self.logger.info(u"第{}页 第{}条 详情抓取成功".format(page, index))
                    soup = bs(resp, 'lxml')
                    table_info = soup.select("table")[5].select("td")
                    # doc = soup.select("table")[5].text.replace('\n','')
                    start_time = table_info[1].text
                    # end_time = table_info[3].text
                    court_room = table_info[5].text
                    presiding_judge = table_info[7].text
                    # judge_use =  table_info[9].text
                    # judge_status = table_info[11].text
                    # doc_id = re.search(r"/(\d+)-", href).group(1)
                    doc_id = "{}_{}".format(case_number, court_date)
                    data_dict = {
                        "case_number": case_number,
                        "court_date": start_time,
                        "case_cause": '',
                        "domain": self.domain,
                        "ename": self.ename,
                        "cname": self.cname,
                        "prosecutor": "",
                        "court_room": court_room,
                        "presiding_judge": presiding_judge,
                        "province": u'广东',
                        "party": "",
                        "url": href,
                        "raw_id": raw_id
                    }
                    unique_id = '{}_{}'.format(self.ename, doc_id)
                    self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
                except Exception:
                    err_msg = u'详情{} 失败：{}'.format(href, traceback.format_exc())
                    self.logger.info(u"第{}页 第{}条 {}".format(page, index, err_msg))
                    raise LogicException(err_msg)

    def get_total_page(self):
        try:
            resp = self.downloader.get(self.url_home, retry_cnt=10)
            html = resp.text
            soup = bs(html, 'lxml')
            pageinfo = soup.select("span.pageinfo")[0].text
            total_cnt = re.search(r"(\d+)", pageinfo).group(0)
            page_cnt = int(total_cnt) / 10 + 1
            self.parse_per_page(html)
            if not page_cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg+'：{}'.format(html))
                raise LogicException(err_msg)
            return int(page_cnt)
        except Exception:
            err_msg = u'下载列表页码失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def update_token(self):
        try:
            token_url = "http://www.zhcourt.gov.cn/courtweb/common/csrfToKen"
            resp = self.downloader.post(token_url)
            token = json.loads(resp.content).get("cs_token")
            self.data.update({"cs_token": token})
        except Exception:
            err_msg = u'更新cs_token出错,原因：{}'.format(traceback.format_exc())
            self.logger.warning(err_msg)
            raise LogicException(err_msg)

    def iter_page_list(self, total_page):
        self.update_token()
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD
        else:
            for page in range(1, total_page+1):
                try:
                    self.data.update({"pagenumber":page})
                    resp = self.downloader.get(self.url_page, params=self.data)
                    html = resp.text
                    self.parse_per_page(html, page)
                except Exception:
                    err_msg = u'下载出错,页码：{}, data：{}, 原因：{}'.format(page, self.data, traceback.format_exc())
                    self.logger.warning(err_msg)
                    self.update_token()
                    raise LogicException(err_msg)
                time.sleep(3)
        print 1


if __name__ == '__main__':
    seed_dict = {'ename': 'zhcourt', 'is_increment': True, 'page': 1}
    ins = ZhuHaiShiZhongJiRenMinFaYuan(None, seed_dict)
    a = ins.start()
    print a
