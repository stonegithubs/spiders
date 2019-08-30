#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:shang_hai_shi_di_yi_zhong_ji_ren_min_fa_yuan.py
description:
author:crazy_jacky
version: 1.0
date:2018/10/15
"""
import re
import time
import traceback
from lxml import etree

from ics.utils import get_ics_logger

from ics.utils.md5_tool import to_md5
from ics.utils.string_tool import remove_spaces
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.utils.mapfield import map_field
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.captcha.chaojiying.crack_captch import CjyCaptcha
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY


class ShangHaiShiDiYiZhongJiRenMingFaYuan(KtggIterPageBase):
    """
    上海市第一中级人民法院
    """
    domain = 'www.a-court.gov.cn'
    ename = 'shang_hai_shi_di_yi_zhong_ji_ren_ming_fa_yuan'
    cname = u'上海市第一中级人民法院'
    developer = u'郑淇鹏'
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip,deflate,br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'www.a-court.gov.cn',
              'Origin': 'https://www.a-court.gov.cn',
              'Referer': 'https://www.a-court.gov.cn/platformData/infoplat/pub/no1court_2802/homepage_13602/list_lb.jsp',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1'}
    start_url = 'https://www.a-court.gov.cn/platformData/infoplat/pub/no1court_2802/homepage_13602/list_lb.jsp'

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
        super(ShangHaiShiDiYiZhongJiRenMingFaYuan, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        try:
            for case_type in [1, 2, 4, 5, 6]:
                self.paper_type = str(case_type)
                form_data = {'paper_type': self.paper_type,
                             'ktrq': 'thisweek',
                             'type': 'query'}
                resp = self.downloader.post(self.start_url, data=form_data, headers=self.header)
                if not resp:
                    err_msg = u'下载列表页码resp为False'
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                cnt = re.findall(unicode("共查询到\s*(\d+)\s*条记录 "), resp.text, flags=re.S)
                if not cnt:
                    err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
                    self.logger.warning(err_msg + '：{}'.format(resp.text))
                    raise LogicException(err_msg)
                self.parse_per_page(resp.text, self.start_url)
                pages = int(cnt[0])
                if pages > 10:
                    self.iter_page_lst(pages)
        except Exception:
            err_msg = u'下载列表页码失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def iter_page_list(self, total_page):
        pass

    def iter_page_lst(self, total_page):
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD.value
        else:
            pages = total_page / 10 + 1 if total_page % 10 else total_page / 10
            form_data = {
                'ktrq': '',
                'paper_type': self.paper_type,
                'pageCoun': str(pages),
                'count': total_page,
                'type': 'page',
            }
            pages = total_page / 10 + 1 if total_page % 10 else total_page / 10
            for page in range(2, pages + 1):  # TODO just for test
                try:
                    thisPage = (page - 1) * 10
                    thisCoun = thisPage + 9
                    form_data.update({'page': str(page), 'thisCoun': str(thisCoun), 'thisPage': str(thisPage)})
                    resp = self.downloader.post(self.start_url, headers=self.header, data=form_data)
                    self.parse_per_page(resp.text, self.start_url)
                except Exception:
                    err_msg = u'下载出错,页码：{}, url：{}, 原因：{}'.format(page, self.start_url.format(page),
                                                                  traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(0.5)

    def parse_per_page(self, html, url):
        try:
            et = etree.HTML(html)
            collection = []
            data_lst = et.xpath('.//table[@bgcolor="#FFFFFF"]//tr')
            if not data_lst:
                return collection
            self.logger.info(self.stat_dict)
            key_lst = [remove_spaces(k.xpath('string(.)').strip()) for k in data_lst[0].xpath('.//td')]
            cname = u'上海市第一中级人民法院'
            raw_md5 = self.ktgg_tool.insert_page_source(html, self.ename, cname, self.do_time)
            for index, val in enumerate(data_lst[1:-2]):
                val_lst = [v.xpath('string(.)').strip().replace('&nbsp', '') for v in val.xpath('.//td')]
                unique_id = to_md5(''.join(val_lst))
                data_dic = dict(zip(key_lst, val_lst))
                data_dic.pop(u'开庭状态', '')
                data_dic.pop(u'序号', '')
                result_dic = map_field(data_dic)
                result_dic.update({
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": cname,
                    "province": u'上海',
                    "url": url,
                    "unique_id": unique_id,
                    "raw_id": raw_md5
                })
                self.ktgg_tool.insert_ktgg_data(result_dic, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'保存数据出现异常url: {}'.format(url)
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        self.logger.info(u'保存{}数据完成'.format(url))
        self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': 'hshfysh', 'is_increment': False, 'page': None}
    ins = ShangHaiShiDiYiZhongJiRenMingFaYuan(None, seed_dict)
    a = ins.start()
    print a
