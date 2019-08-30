#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:shang_hai_shi_pu_dong_xin_qu_ren_min_fa_yuan.py
description:上海市浦东新区人民法院
author:crazy_jacky
version: 1.0
date:2018/10/16
"""
import re
import time
import json
import traceback

from ics.utils import get_ics_logger

from ics.utils.md5_tool import to_md5
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.captcha.chaojiying.crack_captch import CjyCaptcha
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY


class ShangHaiShiPuDongXinQuRenMinFaYuan(KtggIterPageBase):
    """
    上海市浦东新区人民法院
    """
    domain = 'www.pdfy.gov.cn'
    ename = 'shang_hai_shi_pu_dong_xin_qu_ren_min_fa_yuan'
    cname = u'上海市浦东新区人民法院'
    developer = u'郑淇鹏'
    header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
              'Accept-Encoding': 'gzip,deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'www.a-court.gov.cn',
              'Origin': 'http://www.pdfy.gov.cn',
              'Referer': 'http://www.pdfy.gov.cn/sfgk/getKtgg',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36'
              }
    start_url = 'http://www.pdfy.gov.cn/sfgk/getKtgg'
    post_url = 'http://www.pdfy.gov.cn/sfgk/pageinfo_ktgg'
    form_data = {'PAGING': '1',
                 'S_KTRQ1': '2018-01-01',
                 'S_KTRQ2': '',
                 'S_SPZ': '',
                 'S_YG': '',
                 'S_BG': '',
                 'csrf_token_random': ''
                 }

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.paper_type = None
        self.captcha = CjyCaptcha(self.logger)
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=True,
            proxy_mode='dly',
            session_keep=True,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.SWITCH_USE,
        )
        super(ShangHaiShiPuDongXinQuRenMinFaYuan, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        try:
            today = time.strftime('%Y-%m-%d', time.localtime())
            resp = self.downloader.get(self.start_url, headers=self.header)
            if not resp:
                err_msg = u'下载首页码resp为False'
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            rand_str = ''.join(re.compile('csrf_token_random:\"(\w+)\"').findall(resp.text))
            self.form_data.update({'csrf_token_random': rand_str, 'S_KTRQ2': today})
            json_req = self.downloader.post(self.post_url, headers=self.header, data=self.form_data)
            if not json_req:
                err_msg = u'下载列表页码json_req为False'
                self.logger.warning(err_msg)
                self.downloader.change_add_grey_proxy()
                raise LogicException(err_msg)
            dic = json.loads(json_req.text.replace('null', '\"\"'))
            pages = dic.get('totalPage')
            self.parse_per_page(dic)
            if pages > 1:
                self.iter_page_list(pages)
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
                    self.form_data.update({'PAGING': str(page)})
                    resp = self.downloader.post(self.post_url, headers=self.header, data=self.form_data)
                    if not resp:
                        err_msg = u'下载列表页{} 码resp为False'.format(page)
                        self.logger.warning(err_msg)
                        self.downloader.change_add_grey_proxy()
                        raise LogicException(err_msg)
                    self.parse_per_page(json.loads(resp.text.replace('null', '\"\"')))
                except Exception:
                    err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, self.start_url.format(page),
                                                                  traceback.format_exc())
                    self.logger.warning(err_msg)
                    self.downloader.change_add_grey_proxy()
                    raise LogicException(err_msg)
                time.sleep(0.5)

    def parse_per_page(self, html):
        try:
            collection = []
            data_lst = html.get('listData', [])
            if not data_lst:
                return collection
            self.logger.info(self.stat_dict)
            result_dic = {}
            cname = u'上海市浦东区人民法院'
            raw_md5 = self.ktgg_tool.insert_page_source(json.dumps(html, ensure_ascii=False), self.ename, cname,
                                                        self.do_time)
            for item in data_lst:
                tmp = item.get('KTSJ')
                sj = ' ' + tmp[:2] + ':' + tmp[2:]
                result_dic['court'] = u'浦东'
                result_dic['court_room'] = item.get('FT')
                result_dic['court_date'] = item.get('KTRQ') + sj
                result_dic['case_number'] = item.get('AH')
                result_dic['case_cause'] = item.get('AYMC')
                result_dic['undertake_dept '] = item.get('CBBMMC')
                result_dic['prosecutor'] = item.get('YG')
                result_dic['defendant'] = item.get('BG')
                result_dic['chief_judge'] = item.get('SPCMC')
                unique_id = to_md5(
                    ''.join([item.get('AH', ''), result_dic['court_date']]))
                result_dic.update({
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": cname,
                    "province": u'上海',
                    "url": self.post_url,
                    "unique_id": unique_id,
                    "raw_id": raw_md5
                })
                self.ktgg_tool.insert_ktgg_data(result_dic, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'保存数据出现异常url: {} \n:{}'.format(self.post_url, traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        self.logger.info(u'保存{}数据完成'.format(self.post_url))
        self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': 'hshfysh', 'is_increment': False, 'page': None}
    ins = ShangHaiShiPuDongXinQuRenMinFaYuan(None, seed_dict)
    a = ins.start()
    print a
