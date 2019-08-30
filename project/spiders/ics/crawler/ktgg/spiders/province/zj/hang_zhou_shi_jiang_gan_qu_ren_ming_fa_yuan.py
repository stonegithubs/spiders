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


class HangZhouShiJiangGanQuRenMinFaYuan(KtggIterPageBase):

    """
        绍兴市中级人民法院
    """
    domain = 'www.hzjgfy.gov.cn'
    ename = 'hang_zhou_shi_jiang_gan_qu_ren_ming_fa_yuan'
    cname = u'绍兴市中级人民法院'
    developer = u'何振'
    url_pattern = "http://www.hzjgfy.gov.cn/list152.htm"
    header = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
              'Accept-Encoding': 'gzip,deflate,sdch',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'keep-alive',
              'Host': 'www.hzjgfy.gov.cn',
              "Referer": "http://www.hzjgfy.gov.cn/list152.htm",
              'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36('
                            'KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36',
              'Upgrade-Insecure-Requests': '1',}

    _VIEWSTATE = "/wEPDwULLTEwNjg3NDUyMDYPZBYCZg9kFhYCAQ8WAh4LXyFJdGVtQ291bnQCBhYMZg9kFgJmDxUCC2xpc3QxMTYuaHRtDOacrOmZouS7i+e7jWQCAQ9kF\
                  gJmDxUCC2xpc3QxMTcuaHRtDOacuuaehOiuvue9rmQCAg9kFgJmDxUCC2xpc3QxMjguaHRtDOS6uuWRmOS/oeaBr2QCAw9kFgJmDxUCC2xpc3QxNjkuaH\
                  RtDOeuoei+luiMg+WbtGQCBA9kFgJmDxUCC2xpc3QxMjkuaHRtDOiBlOezu+aWueW8j2QCBQ9kFgJmDxUCBmdiLmh0bQzlnKjnur/mnI3liqFkAgIPFgI\
                  fAAIFFgpmD2QWAmYPFQMLbGlzdDE0Ni5odG0FX3NlbGYM6K+J6K685bi46K+GZAIBD2QWAmYPFQMLbGlzdDE0OS5odG0FX3NlbGYY5bi455So6K+J6K68\
                  5paH5pys5qC85byPZAICD2QWAmYPFQMoaHR0cDovL3d3dy56anNmZ2t3LmNuL1JlZmVyZW5jZUNhc2Uvc3NnagZfYmxhbmsM6K+J6K686LS555SoZAIDD\
                  2QWAmYPFQMLbGlzdDE0Ny5odG0FX3NlbGYM6K+J6K685rWB56iLZAIED2QWAmYPFQM8aHR0cDovL3d3dy56anNmZ2t3LmNuL1RyaWFsUHJvY2Vzcy9Db3\
                  VydEhpZ2hlc3RHdWlkZUZpbGVMaXN0Bl9ibGFuaw/mjIflr7zmgKfmlofku7ZkAgMPFgIfAAIHFg5mD2QWAmYPFQMLbGlzdDE1Mi5odG0FX3NlbGYM5by\
                  A5bqt5YWs5ZGKZAIBD2QWAmYPFQMLbGlzdDE1My5odG0FX3NlbGYM57u85ZCI5YWs5ZGKZAICD2QWAmYPFQMLbGlzdDE4Ny5odG0FX3NlbGYM6YCB6L6+\
                  5YWs5ZGKZAIDD2QWAmYPFQM1aHR0cDovL3d3dy56anNmZ2t3LmNuL1RyaWFsUHJvY2Vzcy9UcmlhbFByb2Nlc3NTZWFyY2gGX2JsYW5rGOivieiuvOahi\
                  OS7tuS/oeaBr+afpeivomQCBA9kFgJmDxUDKWh0dHA6Ly93d3cuempzZmdrdy5jbi9UcmlhbFByb2Nlc3MvQWdlbmN5Bl9ibGFuaxjnpL7kvJrkuK3ku4\
                  vmnLrmnoTlkI3lhoxkAgUPZBYCZg8VAxpodHRwOi8vempmeS54aW5zaGl5dW4uY29tLwZfYmxhbmsV5bqt5a6h77yI5b2V77yJ55u05pKtZAIGD2QWAmY\
                  PFQMLbGlzdDE0MC5odG0FX3NlbGYM566h55CG5Yi25bqmZAIEDxYCHwACBBYIZg9kFgJmDxUDC2xpc3QxNDEuaHRtBV9zZWxmDOW3peS9nOaKpeWRimQC\
                  AQ9kFgJmDxUDC2xpc3QxNDIuaHRtBV9zZWxmDOe7n+iuoeaVsOaNrmQCAg9kFgJmDxUDC2xpc3QxODMuaHRtBV9zZWxmEuS4k+mhuee7n+iuoeaVsOaNr\
                  mQCAw9kFgJmDxUDC2xpc3QxODYuaHRtBV9zZWxmGOa2ieahiOasvueJqeS/oeaBr+WFrOW8gGQCBQ8WAh8AAgkWEmYPZBYCZg8VAwtsaXN0MTI1Lmh0bQ\
                  Vfc2VsZgzms5XpmaLopoHpl7tkAgEPZBYCZg8VAwtsaXN0MTIwLmh0bQVfc2VsZgzlm77niYfmlrDpl7tkAgIPZBYCZg8VAwtsaXN0MTU1Lmh0bQVfc2V\
                  sZgzms5Xlrpjpo47ph4dkAgMPZBYCZg8VAwtsaXN0MTY3Lmh0bQVfc2VsZg/mlrDpl7vlj5HluIPkvJpkAgQPZBYCZg8VAwtsaXN0MTY1Lmh0bQVfc2Vs\
                  Zgzop4bpopHngrnmkq1kAgUPZBYCZg8VAwtsaXN0MTQzLmh0bQVfc2VsZg/lhazkvJflvIDmlL7ml6VkAgYPZBYCZg8VAwtsaXN0MTYzLmh0bQVfc2VsZ\
                  g/ouqvovrnnmoTms5XlvotkAgcPZBYCZg8VAwtsaXN0MTYyLmh0bQVfc2VsZgzlqpLkvZPnm7Tlh7tkAggPZBYCZg8VAwtsaXN0MTY0Lmh0bQVfc2VsZg\
                  znkIborrrkuonpuKNkAgYPZBYOAgEPFgIeBFRleHQFDOWuoeWIpOa1geeoi2QCAw8WAh8AAgcWDmYPZBYEZg8VBAtsaXN0MTUyLmh0bQVfc2VsZgRib2x\
                  kDOW8gOW6reWFrOWRimQCAQ8WAh8AZmQCAQ9kFgRmDxUEC2xpc3QxNTMuaHRtBV9zZWxmBm5vcm1hbAznu7zlkIjlhazlkYpkAgEPFgIfAGZkAgIPZBYE\
                  Zg8VBAtsaXN0MTg3Lmh0bQVfc2VsZgZub3JtYWwM6YCB6L6+5YWs5ZGKZAIBDxYCHwBmZAIDD2QWBGYPFQQ1aHR0cDovL3d3dy56anNmZ2t3LmNuL1Rya\
                  WFsUHJvY2Vzcy9UcmlhbFByb2Nlc3NTZWFyY2gGX2JsYW5rBm5vcm1hbBjor4norrzmoYjku7bkv6Hmga/mn6Xor6JkAgEPFgIfAGZkAgQPZBYEZg8VBC\
                  lodHRwOi8vd3d3Lnpqc2Zna3cuY24vVHJpYWxQcm9jZXNzL0FnZW5jeQZfYmxhbmsGbm9ybWFsGOekvuS8muS4reS7i+acuuaehOWQjeWGjGQCAQ8WAh8\
                  AZmQCBQ9kFgRmDxUEGmh0dHA6Ly96amZ5LnhpbnNoaXl1bi5jb20vBl9ibGFuawZub3JtYWwV5bqt5a6h77yI5b2V77yJ55u05pKtZAIBDxYCHwBmZAIG\
                  D2QWBGYPFQQLbGlzdDE0MC5odG0FX3NlbGYGbm9ybWFsDOeuoeeQhuWItuW6pmQCAQ8WAh8AZmQCBQ9kFgICAQ8WAh8AAgcWDmYPZBYCZg8VA0BsaXN0M\
                  TUyLmh0bT9rZXk9MjAxOCVlNiViNSU5OTAxMDQlZTYlYjAlOTElZTUlODglOWQ3NjQyJWU1JThmJWI3GDIwMTjmtZkwMTA05rCR5YidNzY0MuWPtxgyMD\
                  E45rWZMDEwNOawkeWInTc2NDLlj7dkAgEPZBYCZg8VA0BsaXN0MTUyLmh0bT9rZXk9MjAxOCVlNiViNSU5OTAxMDQlZTYlYjAlOTElZTUlODglOWQ3NjQ\
                  xJWU1JThmJWI3GDIwMTjmtZkwMTA05rCR5YidNzY0MeWPtxgyMDE45rWZMDEwNOawkeWInTc2NDHlj7dkAgIPZBYCZg8VA0BsaXN0MTUyLmh0bT9rZXk9\
                  MjAxOCVlNiViNSU5OTAxMDQlZTYlYjAlOTElZTUlODglOWQ2NzA2JWU1JThmJWI3GDIwMTjmtZkwMTA05rCR5YidNjcwNuWPtxgyMDE45rWZMDEwNOawk\
                  eWInTY3MDblj7dkAgMPZBYCZg8VA0BsaXN0MTUyLmh0bT9rZXk9MjAxOCVlNiViNSU5OTAxMDQlZTYlYjAlOTElZTUlODglOWQ0OTkwJWU1JThmJWI3GD\
                  IwMTjmtZkwMTA05rCR5YidNDk5MOWPtxgyMDE45rWZMDEwNOawkeWInTQ5OTDlj7dkAgQPZBYCZg8VA0BsaXN0MTUyLmh0bT9rZXk9MjAxOCVlNiViNSU\
                  5OTAxMDQlZTYlYjAlOTElZTUlODglOWQ5MjUxJWU1JThmJWI3GDIwMTjmtZkwMTA05rCR5YidOTI1MeWPtxgyMDE45rWZMDEwNOawkeWInTkyNTHlj7dk\
                  AgUPZBYCZg8VA0BsaXN0MTUyLmh0bT9rZXk9MjAxOCVlNiViNSU5OTAxMDQlZTYlYjAlOTElZTUlODglOWQ5NDg4JWU1JThmJWI3GDIwMTjmtZkwMTA05\
                  rCR5YidOTQ4OOWPtxgyMDE45rWZMDEwNOawkeWInTk0ODjlj7dkAgYPZBYCZg8VA0lsaXN0MTUyLmh0bT9rZXk9JWU0JWI4JWFkJWU0JWJmJWExJWU2JW\
                  ExJTg4JWU0JWJiJWI2MzIlZTQlYmIlYjYlMmIxNSUyYjE1F+S4reS/oeahiOS7tjMy5Lu2KzE1KzE1F+S4reS/oeahiOS7tjMy5Lu2KzE1KzE1ZAIHDxY\
                  CHwEFDOW8gOW6reWFrOWRimQCCQ8WAh8BBdsBPGEgaHJlZj0iLi8iPummlumhtTwvYT48c3BhbiBzdHlsZT0iZm9udC1mYW1pbHk6QXJpYWw7Zm9udC1z\
                  aXplOjE0cHgiPi0mZ3Q7PC9zcGFuPjxhIGhyZWY9Jy9saXN0MTUxLmh0bSc+5a6h5Yik5rWB56iLPC9hPjxzcGFuIHN0eWxlPSJmb250LWZhbWlseTpBc\
                  mlhbDtmb250LXNpemU6MTRweCI+LSZndDs8L3NwYW4+PGEgaHJlZj0nL2xpc3QxNTIuaHRtJz7lvIDluq3lhazlkYo8L2E+ZAILDxYCHgdWaXNpYmxlaG\
                  QCDw8WAh8CZxYCAgMPZBYCAgEPDxYGHg5DdXN0b21JbmZvVGV4dAWAASZuYnNwO+WFsTxmb250IGNvbG9yPSdyZWQnPjxiPjE3MDg1PC9iPjwvZm9udD7\
                  mnaHorrDlvZUmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDvlvZPliY3pobU6IDxmb250IGNvbG9yPSdyZWQnPjxiPjEvMTEzOTwvYj48L2ZvbnQ+HghQYWdl\
                  U2l6ZQIPHgtSZWNvcmRjb3VudAK9hQFkZAIHDxYCHwACBhYMZg9kFgJmDxUDC2xpc3QxMTYuaHRtBV9zZWxmDOacrOmZouS7i+e7jWQCAQ9kFgJmDxUDC\
                  2xpc3QxMTcuaHRtBV9zZWxmDOacuuaehOiuvue9rmQCAg9kFgJmDxUDC2xpc3QxMjguaHRtBV9zZWxmDOS6uuWRmOS/oeaBr2QCAw9kFgJmDxUDC2xpc3\
                  QxNjkuaHRtBV9zZWxmDOeuoei+luiMg+WbtGQCBA9kFgJmDxUDC2xpc3QxMjkuaHRtBV9zZWxmDOiBlOezu+aWueW8j2QCBQ9kFgJmDxUDBmdiLmh0bQZ\
                  fYmxhbmsM5Zyo57q/5pyN5YqhZAIIDxYCHwACBRYKZg9kFgJmDxUDC2xpc3QxNDYuaHRtBV9zZWxmDOivieiuvOW4uOivhmQCAQ9kFgJmDxUDC2xpc3Qx\
                  NDkuaHRtBV9zZWxmGOW4uOeUqOivieiuvOaWh+acrOagvOW8j2QCAg9kFgJmDxUDKGh0dHA6Ly93d3cuempzZmdrdy5jbi9SZWZlcmVuY2VDYXNlL3NzZ\
                  2oGX2JsYW5rDOivieiuvOi0ueeUqGQCAw9kFgJmDxUDC2xpc3QxNDcuaHRtBV9zZWxmDOivieiuvOa1geeoi2QCBA9kFgJmDxUDPGh0dHA6Ly93d3cuem\
                  pzZmdrdy5jbi9UcmlhbFByb2Nlc3MvQ291cnRIaWdoZXN0R3VpZGVGaWxlTGlzdAZfYmxhbmsP5oyH5a+85oCn5paH5Lu2ZAIJDxYCHwACBxYOZg9kFgJ\
                  mDxUDC2xpc3QxNTIuaHRtBV9zZWxmDOW8gOW6reWFrOWRimQCAQ9kFgJmDxUDC2xpc3QxNTMuaHRtBV9zZWxmDOe7vOWQiOWFrOWRimQCAg9kFgJmDxUD\
                  C2xpc3QxODcuaHRtBV9zZWxmDOmAgei+vuWFrOWRimQCAw9kFgJmDxUDNWh0dHA6Ly93d3cuempzZmdrdy5jbi9UcmlhbFByb2Nlc3MvVHJpYWxQcm9jZ\
                  XNzU2VhcmNoBl9ibGFuaxjor4norrzmoYjku7bkv6Hmga/mn6Xor6JkAgQPZBYCZg8VAylodHRwOi8vd3d3Lnpqc2Zna3cuY24vVHJpYWxQcm9jZXNzL0\
                  FnZW5jeQZfYmxhbmsY56S+5Lya5Lit5LuL5py65p6E5ZCN5YaMZAIFD2QWAmYPFQMaaHR0cDovL3pqZnkueGluc2hpeXVuLmNvbS8GX2JsYW5rFeW6reW\
                  uoe+8iOW9le+8ieebtOaSrWQCBg9kFgJmDxUDC2xpc3QxNDAuaHRtBV9zZWxmDOeuoeeQhuWItuW6pmQCCg8WAh8AAgQWCGYPZBYCZg8VAwtsaXN0MTQx\
                  Lmh0bQVfc2VsZgzlt6XkvZzmiqXlkYpkAgEPZBYCZg8VAwtsaXN0MTQyLmh0bQVfc2VsZgznu5/orqHmlbDmja5kAgIPZBYCZg8VAwtsaXN0MTgzLmh0b\
                  QVfc2VsZhLkuJPpobnnu5/orqHmlbDmja5kAgMPZBYCZg8VAwtsaXN0MTg2Lmh0bQVfc2VsZhjmtonmoYjmrL7niankv6Hmga/lhazlvIBkAgsPFgIfAA\
                  IJFhJmD2QWAmYPFQMLbGlzdDEyNS5odG0FX3NlbGYM5rOV6Zmi6KaB6Ze7ZAIBD2QWAmYPFQMLbGlzdDEyMC5odG0FX3NlbGYM5Zu+54mH5paw6Ze7ZAI\
                  CD2QWAmYPFQMLbGlzdDE1NS5odG0FX3NlbGYM5rOV5a6Y6aOO6YeHZAIDD2QWAmYPFQMLbGlzdDE2Ny5odG0FX3NlbGYP5paw6Ze75Y+R5biD5LyaZAIE\
                  D2QWAmYPFQMLbGlzdDE2NS5odG0FX3NlbGYM6KeG6aKR54K55pKtZAIFD2QWAmYPFQMLbGlzdDE0My5odG0FX3NlbGYP5YWs5LyX5byA5pS+5pelZAIGD\
                  2QWAmYPFQMLbGlzdDE2My5odG0FX3NlbGYP6Lqr6L6555qE5rOV5b6LZAIHD2QWAmYPFQMLbGlzdDE2Mi5odG0FX3NlbGYM5aqS5L2T55u05Ye7ZAIID2\
                  QWAmYPFQMLbGlzdDE2NC5odG0FX3NlbGYM55CG6K665LqJ6bijZGTjn9HKU497olYLVtvbZKdGSP1SGqzGvqLFVlN+0WZLsw=="

    data = {
        "__EVENTTARGET": "ctl00$ContentPlaceHolder1$AspNetPager2",
        "__VIEWSTATE": _VIEWSTATE,
    }

    def __init__(self, logger, seed_dict):
        self.logger = logger or get_ics_logger(self.ename)
        self.seed_dict = seed_dict
        self.status = None
        self.downloader = Downloader(
            logger=self.logger,
            use_proxy=False,
            proxy_mode='dly',
            basic_headers = self.header,
            headers_mode=HEADERS_MODEL.OVERRIDE,
            proxy_strategy=PROXY_STRATEGY.CONTINUITY_USE,
        )
        self.__init_downloader()
        super(HangZhouShiJiangGanQuRenMinFaYuan, self).__init__(self.seed_dict, self.logger)

    def __init_downloader(self):
        def judge_html_invalid(resp, meta):
            if '最近有可疑的攻击行为，请稍后重试' in resp.text:
                self.downloader.change_add_grey_proxy()
                return True

        self.downloader.set_retry_solution(judge_html_invalid)

    def parse_per_page(self, html, href, page=1):
        try:
            soup = bs(html, 'lxml')
            raw_id = self.ktgg_tool.insert_page_source(html, self.ename, self.cname, self.do_time)
            infos = soup.select('div.news_list table tr')[1:]
            for info in infos:
                court_room = info.contents[1].text
                court_date = info.contents[3].text
                case_number = info.contents[5].text
                case_cause = info.contents[7].text
                undertake_dept = info.contents[9].text
                chief_judge = info.contents[11].text
                prosecutor = info.contents[13].text
                defendant = info.contents[15].text

                data_dict = {
                    "case_number": case_number,
                    "court_date": court_date,
                    "case_cause": case_cause,
                    "domain": self.domain,
                    "ename": self.ename,
                    "cname": self.cname,
                    "court_room": court_room,
                    "province": u'浙江',
                    "prosecutor": prosecutor,
                    "defendant": defendant,
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
        resp = self.downloader.get(self.url_pattern)
        html = resp.text
        page_cnt = re.search(ur'当前页: .*\d+/(\d+)', html).group(1)
        self.parse_per_page(html, resp.url, 1)
        return page_cnt

    def iter_page_list(self, total_page):
        if total_page == 0:
            self.logger.info(u'总页码为 total_page: {}, 无此记录'.format(total_page))
            self.status = TASK_STATUS.NO_RECORD
        else:
            for page in range(2, total_page):
                try:
                    self.data.update({"__EVENTARGUMENT": page})
                    self.data.update({"ctl00$ContentPlaceHolder1$AspNetPager2_input": page-1})
                    resp = self.downloader.post(self.url_pattern, data=self.data)
                    html = resp.text
                    self.parse_per_page(html, resp.url, page)
                except Exception:
                    err_msg = u'下载出错,页码：{}, data：{}, 原因：{}'.format(page, self.data, traceback.format_exc())
                    self.logger.warning(err_msg)
                    raise LogicException(err_msg)
                time.sleep(3)


if __name__ == '__main__':
    seed_dict = {'ename': 'hang_zhou_shi_jiang_gan_qu_ren_ming_fa_yuan', 'is_increment': True, 'page': 3}
    ins = HangZhouShiJiangGanQuRenMinFaYuan(None, seed_dict)
    a = ins.start()
    print a