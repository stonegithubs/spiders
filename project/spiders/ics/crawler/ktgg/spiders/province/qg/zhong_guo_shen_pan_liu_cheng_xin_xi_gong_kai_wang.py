#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:zhong_guo_shen_pan_liu_cheng_xin_xi_gong_kai_wang.py
description:中国审判流程信息公开网
author:crazy_jacky
version: 1.0
date:2018/9/18
"""
import re
import time
import json
import traceback

from ics.utils import get_ics_logger
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase


class ZhongGuoShenPanLiuChengXinXiGongKaiWang(KtggIterPageBase):
    """
    中国审判流程信息公开网
    """
    domain = 'splcgk.court.gov.cn'
    ename = 'zhong_guo_shen_pan_liu_cheng_xin_xi_gong_kai_wang'
    cname = u'中国审判流程信息公开网'
    developer = u'郑淇鹏'
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
              'Accept-Encoding': 'gzip,deflate,br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
              'Host': 'splcgk.court.gov.cn',
              'Origin': 'https://splcgk.court.gov.cn',
              'Referer': 'https://splcgk.court.gov.cn/gzfwww/ktgg',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'}
    start_url = 'https://splcgk.court.gov.cn/gzfwww/ktgglist?pageNo={}'
    form_data = {'bt': '', 'fydw': '', 'pageNum': ''}

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
        super(ZhongGuoShenPanLiuChengXinXiGongKaiWang, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        try:
            first_url = self.start_url.format(1)
            self.form_data.update({'pageNum': str(1)})
            resp = self.downloader.post(first_url, data=self.form_data, headers=self.header)
            data_dic = resp.json()
            if not resp:
                err_msg = u'下载列表页码resp为False'
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            page_cnt = data_dic.get('page').get('pages')
            self.parse_per_page(data_dic, first_url)
            if not page_cnt:
                err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                self.logger.warning(err_msg + '：{}'.format(resp.text))
                raise LogicException(err_msg)
            return page_cnt
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
                self.form_data.update({'pageNum': str(page)})
                try:
                    resp = self.downloader.post(self.start_url.format(page), headers=self.header, data=self.form_data)
                    data_dic = resp.json()
                    self.parse_per_page(data_dic, self.start_url.format(page))
                except Exception:
                    err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, self.start_url.format(page),
                                                                  traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(0.5)

    def parse_per_page(self, dic, page_url):
        collection = []
        data_lst = dic.get('data')
        if not data_lst:
            return collection
        source = json.dumps(dic, ensure_ascii=False)
        raw_id = self.ktgg_tool.insert_page_source(source, self.ename, self.cname, self.do_time)
        self.logger.info(self.stat_dict)
        for index, data_dic in enumerate(data_lst):
            try:
                # party_parse_flag = 1
                case_number = data_dic.get('cah')
                court_date = ''.join(
                    re.compile('\d{4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{1,2}').findall(data_dic.get('cggbt'))).strip()
                court_room = data_dic.get('ccbftBh')
                court = data_dic.get('cfymc')
                province = data_dic.get('sf')
                prosecutor = data_dic.get('cygMc')
                defendant = data_dic.get('cbgMc')
                party_parse = prosecutor.strip(u'原告:') + ',' + defendant.strip(u'被告')
                title = data_dic.get('cggbt')
                case_cause = ''
                if defendant in title:
                    case_cause = title.split(defendant)[-1].strip(';').strip(u'。').strip(u'一案').strip(u'的')
                    if u'的' in case_cause:
                        case_cause = case_cause.split(u'的')[-1]
                doc = '{} {} {} {} {}'.format(case_number, case_cause, party_parse, court_date, court)
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
                    "court_room": court_room,
                    "prosecutor": prosecutor,
                    "province": province,
                    "defendant": defendant,
                    # "party_parse": party_parse,
                    # "party_parse_flag": party_parse_flag,
                    "url": page_url,
                    "raw_id": raw_id
                }
                unique_id = "{}_{}_{}".format(self.ename, case_number, court_date)
                self.ktgg_tool.insert_ktgg_data(data_dict, self.stat_dict, unique_id)
            except Exception:
                err_msg = u'保存数据出现异常,index:{}, page_url: {}'.format(index, page_url)
                self.logger.error(err_msg)
                raise LogicException(err_msg)
            self.logger.info(u'保存第{}条数据完成'.format(index))
        self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': 'splcgk', 'is_increment': True, 'page': 1}
    ins = ZhongGuoShenPanLiuChengXinXiGongKaiWang(None, seed_dict)
    a = ins.start()
    print a
