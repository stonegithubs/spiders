# coding=utf-8
"""
上海市松江区人民法院
"""

__author__ = 'He_zhen'

import time
import traceback
from bs4 import BeautifulSoup as bs
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException


class ShangHaiShiSongJiangQuRenMinFaYuan(KtggIterPageBase):
    url_home = "http://dj.evideocloud.com/gf/pc/web/video/getListByCategory"
    domain = 'http://dj.evideocloud.com'
    ename = 'shang_hai_shi_song_jiang_qu_ren_min_fa_yuan'
    cname = u'上海市松江区人民法院'
    developer = u'何振'
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
              'Accept-Encoding': 'gzip,deflate,br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1'}

    data = {
        "categoryId":  0,
        "tenantId": 9,
        "courtId": 10,
    }

    trans = {"审判长": "chief_judge",
             "主审法官": "presiding_judge",
             "法官": "judiciary", }

    judge_man = dict()

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
        super(ShangHaiShiSongJiangQuRenMinFaYuan, self).__init__(self.seed_dict, self.logger)

    def parse_per_page(self, html):
        self.do_time = self.ktgg_tool.now_date
        soup = bs(html, 'lxml')
        lis = soup.select("div.left.fixpos ul li")

        for line in lis:
            href = self.domain + line.contents[1]['href']
            self.parse_detail_page(href)

    def parse_detail_page(self, detail_url):
        try:
            resp = self.downloader.get(detail_url)
            html = resp.text
            raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
            soup = bs(html, 'lxml')
            court = soup.select('div.name h3')[0].text[5:]
            case_introduction = soup.select('div.produce .pro p')[0].text

            base_info = soup.select('div.basebox span.cont')
            case_number = base_info[0].text
            court_date = base_info[1].text
            case_cause = base_info[2].text
            court_room = base_info[3].text
            position_str = base_info[4].text
            self.transfrom_position(position_str)
            prosecutor = base_info[5].text.split(u"：")[1] if base_info[5].text else u''
            defendant = base_info[6].text.split(u"：")[1] if base_info[6].text else u''
            party = base_info[5].text + base_info[6].text

            data_dict = {
                "court": court,
                "case_introduction": case_introduction,
                "court_date": court_date,
                "case_number": case_number,
                "case_cause": case_cause,
                "cname": self.cname,
                "ename": self.ename,
                "domain": self.domain,
                "prosecutor": prosecutor,
                "court_room": court_room,
                "defendant": defendant,
                "province": u'上海',
                "party": party,
                "url": detail_url,
                "raw_id": raw_id
            }
            data_dict.update(self.judge_man)
            self.judge_man.clear()
            unique_id = case_number + self.ename
            self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'下载出错, 详情链接：{}, data：{}, 原因：{}'.format(detail_url, self.data, traceback.format_exc())
            self.logger.warning(err_msg)
            raise LogicException(err_msg)


    def get_total_page(self):
        return 1

    def iter_page_list(self, total_page):
        try:
            self.data.update({"page": total_page})
            resp = self.downloader.get(self.url_home, params=self.data)
            html = resp.text
            self.parse_per_page(html)
        except Exception:
            err_msg = u'下载出错data：{}, 原因：{}'.format(self.data, traceback.format_exc())
            self.logger.warning(err_msg)
            raise LogicException(err_msg)
        time.sleep(3)

    def transfrom_position(self, position_str):
        positions = list()
        if position_str.find(u',') > 0:
            positions = position_str.split(u',')

        if positions:
            for text in positions:
                position_name = self.get_position_name(text)
                name = text.split(u'：')[1]
                self.judge_man[position_name] = name
            return

        if position_str:
            name = position_str.split(u'：')[1]
            text = position_str.split(u'：')[0]
            position_name = self.get_position_name(text)
            self.judge_man[position_name] = name

    def get_position_name(self, text):
        for k, v in self.trans.iteritems():
            if k in text:
                return v

if __name__ == '__main__':
    ins = ShangHaiShiSongJiangQuRenMinFaYuan(None, {"is_increment": True, "page": 1})
    a = ins.start()
    print a
