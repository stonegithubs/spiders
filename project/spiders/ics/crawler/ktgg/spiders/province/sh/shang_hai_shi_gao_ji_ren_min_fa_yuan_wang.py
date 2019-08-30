#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:shang_hai_shi_gao_ji_ren_min_fa_yuan_wang.py
description:上海市高级人民法院网
author:crazy_jacky
version: 1.0
date:2018/9/20
"""

import re
import time
import traceback
from lxml import etree
from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.captcha.chaojiying.crack_captch import CjyCaptcha
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY


class ShangHaiShiGaoJiRenMinFaYuanWang(KtggIterPageBase):
    """
    上海市高级人民法院网
    """
    domain = 'www.hshfy.sh.cn'
    ename = 'shang_hai_shi_gao_ji_ren_min_fa_yuan_wang'
    cname = u'上海市高级人民法院网'
    developer = u'郑淇鹏'

    header = {'Accept': '*/*',
              'Accept-Encoding': 'gzip,deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'www.hshfy.sh.cn',
              'Origin': 'http://www.hshfy.sh.cn',
              'Content-Type': 'application/x-www-form-urlencoded',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Referer': 'http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search.jsp?COLLCC=1275663549&zd=splc',
              'X-Requested-With': 'XMLHttpRequest'}
    start_url = 'http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search_content.jsp'
    form_data = {'yzm': 'EBSp',
                 'ft': '',
                 'ktrqjs': '',
                 'spc': '',
                 'yg': '',
                 'bg': '',
                 'ah': ''}

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.captcha = CjyCaptcha(self.logger)
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=True,
            proxy_mode='dly',
            session_keep=True,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.SWITCH_USE,
        )
        super(ShangHaiShiGaoJiRenMinFaYuanWang, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        try:
            curr_date = time.strftime('%Y-%m-%d', time.localtime())
            self.form_data.update({'ktrqks': curr_date, 'ktrqjs': curr_date})
            self.form_data.update({'pagesnum': '1'})
            resp = self.downloader.post(self.start_url, headers=self.header, data=self.form_data)
            if not resp:
                err_msg = u'下载列表页码resp为False'
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            cnt = re.findall('<strong>(\d+)<', resp.content, flags=re.S)
            if not cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg + '：{}'.format(resp.text))
                raise LogicException(err_msg)
            cnt = int(cnt[0])
            page_cnt = cnt / 15 + 1 if cnt % 15 else cnt / 15
            self.parse_per_page(resp.content, self.start_url)
            return int(page_cnt)
        except Exception:
            err_msg = u'下载列表页码失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def iter_page_list(self, total_page):
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD.value
        else:
            for page in range(2, total_page + 1):  # TODO just for test
                try:
                    self.form_data.update({'pagesnum': str(page)})
                    resp = self.downloader.post(self.start_url, headers=self.header, data=self.form_data)
                    html = resp.content
                    self.parse_per_page(html, self.start_url)
                except Exception:
                    err_msg = u'下载出错页码：{}, url：{}, 原因：{}'.format(page, self.start_url, traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(0.5)

    def parse_per_page(self, html, url):
        html = html.decode('gb18030')
        et = etree.HTML(html)
        collection = []
        data_lst = et.xpath('.//table[@id="report"]//tr')
        if not data_lst:
            return collection
        raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
        self.logger.info(self.stat_dict)
        key = [''.join(x.xpath('string(.)')).strip() for x in data_lst[0].xpath('.//td')]
        for index, value in enumerate(data_lst[1:]):
            try:
                val = [''.join(x.xpath('string(.)')).strip() for x in value.xpath('.//td')]
                dic = dict(zip(key, val))
                case_number = dic.get(u'案号')
                case_cause = dic.get(u'案由')
                responsible_court = dic.get(u'承办部门')
                presiding_judge = dic.get(u'审判长/主审人')
                prosecutor = dic.get(u'原告/上诉人')
                defendant = dic.get(u'被告/被上诉人')
                court = dic.get(u'法院')
                court_room = dic.get(u'法庭')
                court_date = dic.get(u'开庭日期')
                # party_parse = prosecutor + ', ' + defendant
                # doc = '{} {} {} {} {}'.format(case_number, case_cause, party_parse, court_date, court_room)
                data_dict = {
                    # 'date': self.do_time,
                    "case_number": case_number,
                    # "doc": doc,
                    "court_date": court_date,
                    # "doc_id": "{}_{}".format(case_number, court_date),
                    "case_cause": case_cause,
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": self.cname,
                    "court": court,
                    "responsible_court": responsible_court,
                    "prosecutor": prosecutor,
                    "defendant": defendant,
                    "court_room": court_room,
                    "presiding_judge": presiding_judge,
                    "province": u'上海',
                    # "party_parse": party_parse,
                    # "party_parse_flag": 0,
                    "url": url,
                    "raw_id": raw_id
                }
                unique_id = "{}_{}_{}".format(self.ename, case_number, court_date)
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
                self.logger.info(u'保存第{}条数据完成'.format(index))
            except Exception:
                err_msg = u'保存第{}条数据出现异常'.format(index)
                self.logger.error(err_msg)
                raise LogicException(err_msg)
        self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': 'hshfysh', 'is_increment': True, 'page': 1}
    ins = ShangHaiShiGaoJiRenMinFaYuanWang(None, seed_dict)
    a = ins.start()
    print a
