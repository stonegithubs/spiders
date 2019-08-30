#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@copyright: icekredit Tech, LTD
file_name:shang_hai_hai_shi_fa_yuan.py
description:上海海事法院
author:crazy_jacky
version: 1.0
date:2018/10/15
"""
import traceback
from lxml import etree

from urlparse import urljoin
from ics.utils import get_ics_logger

from ics.utils.md5_tool import to_md5
from ics.utils.exception_util import LogicException
from ics.crawler.ktgg.core.constant import TASK_STATUS
from ics.captcha.chaojiying.crack_captch import CjyCaptcha
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY


class ShangHaiHaiShiFaYuan(KtggIterPageBase):
    """
    上海海事法院
    """
    domain = 'shhsfy.gov.cn'
    ename = 'shang_hai_hai_shi_fa_yuan'
    cname = u'上海海事法院'
    developer = u'郑淇鹏'
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept-Encoding': 'gzip,deflate',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'shhsfy.gov.cn',
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1'}
    start_url = 'http://shhsfy.gov.cn/infoplat5/website/hsfyitw/hsfyitw-ktsdgg!toPageAction?page=index&lx=ktgg'

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
        super(ShangHaiHaiShiFaYuan, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        try:
            resp = self.downloader.get(self.start_url, headers=self.header)
            if not resp:
                err_msg = u'下载列表页码resp为False'
                self.logger.warning(err_msg)
                raise LogicException(err_msg)
            # 暂未获取到翻页规则
            # cnt = re.findall(unicode("共查询到\s*(\d+)\s*条记录 "), resp.text, flags=re.S)
            # if not cnt:
            #     err_msg = u'下载列表页获取到的页面，提取不到总页码，请检查列表页html是否正确'
            #     self.logger.warning(err_msg + '：{}'.format(resp.text))
            #     raise LogicException(err_msg)
            self.parse_per_page(resp.text)
            # pages = int(cnt[0])
            # if pages > 1:
            #     self.iter_page_list(pages)
        except Exception:
            err_msg = u'下载列表页码失败：{}'.format(traceback.format_exc())
            self.logger.error(err_msg)
            raise LogicException(err_msg)

    def iter_page_list(self, total_page):
        pass

    def parse_per_page(self, html):
        req_url = ''
        try:
            et = etree.HTML(html)
            url_lst = et.xpath('.//ul[@class="gglist"]//a//@href')
            if not url_lst:
                self.logger.info(u'总记录为 url_lst: {}, 无此记录'.format(url_lst))
                self.status = TASK_STATUS.NO_RECORD.value
                return []
            self.logger.info(self.stat_dict)
            cname = u'上海海事法院'
            for detail_url in url_lst:
                req_url = urljoin(self.start_url, detail_url)
                req = self.downloader.get(req_url, headers=self.header)
                if not req:
                    err_msg = u'下载详情页req为False'
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                detail_html = req.text.replace('&nbsp;', '')
                detail_et = etree.HTML(detail_html)
                court = ''.join(detail_et.xpath('//div[@class="bt1"]//text()'))
                title = court + '\n' + ''.join(detail_et.xpath('//div[@class="bt2"]//text()'))
                body = ''.join(detail_et.xpath('//div[@class="ktnr"]//text()'))
                raw_md5 = self.ktgg_tool.insert_page_source(html, self.ename, cname, self.do_time)
                result_dic = {'court': court, 'title': title, 'body': body}
                unique_id = to_md5(req_url)
                result_dic.update({
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": cname,
                    "province": u'上海',
                    "url": req_url,
                    "unique_id": unique_id,
                    "raw_id": raw_md5
                })
                self.ktgg_tool.insert_ktgg_data(result_dic, self.stat_dict, unique_id)
        except Exception:
            err_msg = u'保存数据出现异常url: {}'.format(req_url)
            self.logger.error(err_msg)
            raise LogicException(err_msg)
        self.logger.info(u'保存{}数据完成'.format(req_url))
        self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': 'hshfysh', 'is_increment': False, 'page': None}
    ins = ShangHaiHaiShiFaYuan(None, seed_dict)
    a = ins.start()
    print a
