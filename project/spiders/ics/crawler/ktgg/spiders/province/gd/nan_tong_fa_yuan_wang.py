# coding=utf-8
import re

__author__ = 'li_bao_ling'

import sys
import chardet
import logging
from lxml import etree
from ics.utils.string_tool import *
from ics.utils import get_ics_logger
from ics.crawler.ktgg.utils.ktgg_data import KtggData
from ics.crawler.ktgg.core.iter_page_base import KtggIterPageBase
from ics.http.http_downloader import Downloader, HEADERS_MODEL, PROXY_STRATEGY

reload(sys)
sys.setdefaultencoding('utf-8')


class NanTongFaYuanWang(KtggIterPageBase):
    domain = 'www.ntfy.gov.cn'
    ename = 'nan_tong_fa_yuan_wang'
    cname = u'南通法院网'
    developer = u'李保领'
    url_pattern = 'http://www.ntfy.gov.cn/channels/65.html'
    url_pattern_1 = 'http://www.ntfy.gov.cn/channels/65_{}.html'
    headers = {
        'Host': 'www.ntfy.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    }
    headers_1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q= 0.9',
        'Connection': 'keep-alive',
        'Host': 'www.ntfy.gov.cn',
        'If-None-Match': "60ff95182fbcd31:0",
        'Referer': 'http://www.ntfy.gov.cn/channels/65.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            spider_no='nan_tong_fa_yuan_wang',
            logger=self.logger,
            use_proxy=False,
            proxy_mode='dly',
            session_keep=True,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.SWITCH_USE,
        )
        super(NanTongFaYuanWang, self).__init__(self.seed_dict, self.logger)

    def get_total_page(self):
        html = self.downloader.get(self.url_pattern, headers=self.headers, retry_cnt=20, timeout=3)
        HTML = html.content
        charset = chardet.detect(HTML)['encoding']
        resq = HTML.decode(charset, 'ignore')
        page_re = re.compile(r'<span class="lanmu_b">(.*?)</span>')
        page_str = page_re.findall(resq)[3]
        if page_str:
            page = int(page_str)
        else:
            page = 1
        return page

    def page_detail(self, request_url, detail_urls):
        response = self.downloader.get(url=request_url, headers=self.headers, retry_cnt=20, timeout=3)
        HTML = response.content
        charset = chardet.detect(HTML)["encoding"]
        detail_text = HTML.decode(charset, 'ignore')
        self.parse_list(detail_text, detail_urls)

    def iter_page_list(self, total_page):
        # 请求list
        detail_urls = []
        for page_num in range(1, total_page + 1):
            print page_num
            if page_num >= 2:
                request_url = self.url_pattern_1.format(page_num)
                self.page_detail(request_url, detail_urls)
            else:
                request_url = self.url_pattern
                self.page_detail(request_url, detail_urls)

        # 请求detail
        for detail_url in detail_urls:
            response = self.downloader.get(url=detail_url, headers=self.headers_1, retry_cnt=20, timeout=3)
            HTML = response.content
            detail_text = HTML.decode('gbk')
            self.parse_detail(detail_text, detail_url)

    def parse_list(self, response_text, detail_urls):
        # 解析list
        html = etree.HTML(response_text)
        html_data = html.xpath('//table[@class="innercontent"]//table//a/@href')
        for url_num in html_data:
            if 'contents' in url_num:
                detail_url = 'http://www.ntfy.gov.cn/' + url_num
                print detail_url
                detail_urls.append(detail_url)

    def parse_detail(self, response_text, request_url):
        # 解析detail
        content = response_text
        html = etree.HTML(content)
        raw_id = self.ktgg_tool.insert_page_source(response_text, self.ename, self.cname, self.do_time)
        data_dicts = []
        try:
            data = re.compile(r'<td align="left">(.*?)</td>')
            data_1 = re.compile(r'<td align="left" class="linekt">(.*?)</td>')
            temp_publish_date = data.findall(content)
            temp_publish_date_1 = data_1.findall(content)
            data_nu = KtggData()
            # 发布时间
            data_nu.publish_date = re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}', content).group()
            data_nu.raw_id = raw_id
            # 开庭日期
            data_nu.court_date = temp_publish_date[0]

            # 法 庭
            data_nu.court_room = temp_publish_date[1].decode("utf-8")

            # 审判长
            data_nu.chief_judge = temp_publish_date[2].decode("utf-8")

            # 合议庭
            data_nu.court_member = temp_publish_date[3].decode("utf-8")

            # 书记员
            data_nu.court_clerk = temp_publish_date_1[1].decode("utf-8")

            # title
            title = html.xpath('//div[@id="artibodyTitle"]/h1/text()')[0]
            if "测试数据" not in title:
                data_nu.title = title

            data_nu.court = u'南通市中级人民法院'
            data_nu.domain = self.domain
            data_nu.ename = self.ename
            data_nu.cname = self.cname
            data_nu.province = u'江苏'
            data_nu.url = request_url
            print data_nu.court_date, data_nu.court_room, data_nu.chief_judge, data_nu.court_member, data_nu.court_clerk
            print data_nu.title, data_nu.publish_date
            self.logger.info("{} {} {} {} {}".format(data_nu.court_date, data_nu.court_room, data_nu.chief_judge,
                                                     data_nu.court_member, data_nu.court_clerk))
            self.logger.info("{} {}".format(data_nu.title, data_nu.publish_date))

            data_dicts.append(data_nu)
        except Exception:
            logging.warning('============== 解析异常 ============== {}'.format(content))

        if data_dicts:
            try:
                self.ktgg_tool.insert_ktgg_data(data_dicts, self.stat_dict, unique_key='unique_id')
                self.logger.info(u'保存数据成功')
            except:
                self.logger.error('保存数据出现异常')
            self.logger.info(self.stat_dict)


if __name__ == '__main__':
    seed_dict = {'ename': 'nan_tong_fa_yuan_wang', 'is_increment': True, 'page': 18}
    spider = NanTongFaYuanWang(None, seed_dict)
    spider.start()
