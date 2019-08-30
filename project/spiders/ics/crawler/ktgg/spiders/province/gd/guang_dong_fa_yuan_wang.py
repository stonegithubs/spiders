#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:guang_dong_fa_yuan_wang.py
description: 广东法院网
author:crazy_jacky
version: 1.0
date:2018/9/19
"""
import re
import time
import json
import traceback
from lxml import etree

from ics.utils import get_ics_logger

from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.captcha.chaojiying.crack_captch import CjyCaptcha
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY


class GuangDongFaYuanWang(KtggIterPageBase):
    """
    广东法院网
    """
    domain = 'www.gdcourts.gov.cn'
    ename = 'guang_dong_fa_yuan_wang'
    cname = u'广东法院网'
    developer = u'郑淇鹏'
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
              'Accept-Encoding': 'gzip,deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
              'Host': 'www.gdcourts.gov.cn',
              'Origin': 'http://www.gdcourts.gov.cn',
              'Referer': 'http://www.gdcourts.gov.cn/web/search?action=gotoajxxcx&ajlx=sp&flag=first',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'}
    start_url = 'http://www.gdcourts.gov.cn/web/search?action=gotoajxxcx&ajlx=sp&flag=first'
    form_data = {"ajlx": "sp",
                 "fjm": "J00",
                 "pageNum": '',
                 "dsr": "",
                 "ah": "",
                 "csToken": '',
                 "page_randomcode": '',
                 "page_randomcode_submit": ''
                 }

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
        super(GuangDongFaYuanWang, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        try:
            header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'Accept-Encoding': 'gzip,deflate',
                      'Accept-Language': 'zh-CN,zh;q=0.9',
                      'Connection': 'keep-alive',
                      'Host': 'www.gdcourts.gov.cn',
                      'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                                    'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
                      'Upgrade-Insecure-Requests': '1',
                      }
            resp = self.downloader.get(self.start_url, headers=header)
            if not resp:
                err_msg = u'下载列表页码resp为False'
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            page_cnt = re.findall('"bsumpage">(\d+)<', resp.content, flags=re.S)
            token_key = re.findall('{"tokenKey":"(\d+)"}', resp.content, flags=re.S)
            if not page_cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg + '：{}'.format(resp.text))
                raise LogicException(err_msg)
            self.form_data.update({'token_key': token_key[0]})
            return int(page_cnt[0])
        except Exception:
            err_msg = u'下载列表页码失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def update_form_data(self, page):
        try:
            timespan = str(time.time()).replace('.', '')
            url = 'http://www.gdcourts.gov.cn/common/random_codeById/{}-'.format(timespan)
            header = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                      'Accept-Encoding': 'gzip,deflate',
                      'Accept-Language': 'zh-CN,zh;q=0.9',
                      'Connection': 'keep-alive',
                      'Host': 'www.gdcourts.gov.cn',
                      'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                                    'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
                      'Referer': 'http://www.gdcourts.gov.cn/web/search?action=gotoajxxcx&ajlx=sp&flag=first',
                      }
            pic_cont = self.downloader.get(url, headers=header)
            code, report_id = self.captcha.crack_captcha(pic_cont.content, yzm_dir='gdcourts')
            url = 'http://www.gdcourts.gov.cn/common/getToKenTempPutCk'
            form_data = {'tokenKey': self.form_data['token_key']}
            token_cont = self.downloader.post(url, data=form_data, headers=self.header)
            token = token_cont.json().get('tokenVal')
            self.form_data.update({
                "pageNum": page,
                "csToken": token,
                "page_randomcode": code,
                "page_randomcode_submit": timespan
            })
        except Exception:
            err_msg = u'更新form_data失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def iter_page_list(self, total_page):
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD.value
        else:
            post_url = 'http://www.gdcourts.gov.cn/web/search?action=gotoajxxcx'
            detail_url = 'http://www.gdcourts.gov.cn/web/search?action=ajxxxq&ajid={}%20&ah=&dsr=&pageNum=1'
            for page in range(1, total_page + 1):  # TODO just for test
                try:
                    self.update_form_data(page)
                    resp = self.downloader.post(post_url, headers=self.header, data=self.form_data)
                    data_dic_lst = resp.json().get('ajxxlist')
                    for item in data_dic_lst:
                        ajid = item.get('AJID')
                        url = detail_url.format(ajid)
                        self.get_detail_page(url)
                except Exception:
                    err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, self.start_url.format(page),
                                                                  traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(0.5)

    def get_detail_page(self, url):
        header = {'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                  'Accept-Encoding': 'gzip,deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Connection': 'keep-alive',
                  'Host': 'www.gdcourts.gov.cn',
                  'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                                'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
                  }
        try:
            resp = self.downloader.get(url, headers=header)
            if not resp:
                err_msg = u'下载详情页码resp为False'
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            html = resp.content
            self.parse_per_page(html, url)
        except Exception:
            err_msg = u'下载详情出错 url：{}, 原因：{}'.format(url, traceback.format_exc())
            self.logger.warning(err_msg)
            raise LogicException(err_msg)

    def parse_per_page(self, html, url):
        try:
            et = etree.HTML(html)
            collection = []
            print '*'*100
            print et
            print '*'*100
            data_lst = et.xpath('.//div[@id="a1"]')
            if not data_lst:
                return collection
            raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
            self.logger.info(self.stat_dict)
            case_number = ''.join(et.xpath('.//h2//text()')).strip()
            data_lst = [item.xpath('string(.)').strip() for item in et.xpath('.//td')]
            key = data_lst[::2]
            val = data_lst[1::2]
            data_dic = dict(zip(key, val))
            court_room = data_dic.get(u'承办部门')
            case_cause = data_dic.get(u'案由')
            party = data_dic.get(u'当事人')
            temp_lst = party.split()
            prosecutor = temp_lst[0].strip(unicode('申请人:'))
            defendant = temp_lst[1].strip(unicode('被申请人:'))
            # party_parse = prosecutor + ', ' + defendant
            court_date = data_dic.get(u'立案日期')
            presiding_judge = data_dic.get(u'主审法官')
            # doc = '{} {} {} {} {}'.format(case_number, case_cause, party, court_date, court_room)
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
                "prosecutor": prosecutor,
                "defendant": defendant,
                "court_room": court_room,
                "presiding_judge": presiding_judge,
                "province": u'广东',
                "party": party,
                # "party_parse": party_parse,
                # "party_parse_flag": 0,
                "url": url,
                "raw_id": raw_id
            }
            unique_id = '{}_{}_{}'.format(self.ename, case_number, court_date)
            self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'保存数据出现异常url: {}'.format(url)
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        self.logger.info(u'保存{}数据完成'.format(url))
        self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': None, 'is_increment': True, 'page': 1}
    ins = GuangDongFaYuanWang(None, seed_dict)
    a = ins.start()
    print a
