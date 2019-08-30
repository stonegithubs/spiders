# coding=utf-8
from ics.utils.exception_util import DownloaderException

__author__ = 'wu_yong'

import traceback
import urlparse
import requests
import uuid
from ics.utils.exception.http_exception import requests_exception
from requests.adapters import HTTPAdapter
from ics.http.proxy import Proxy, VirtualProxy


class PROXY_STRATEGY(object):
    CONTINUITY_USE = 0  # 连续使用，企信网不用频繁切换ip
    SWITCH_USE = 1  # 每次请求都切换ip，默认策略


class HEADERS_MODEL(object):
    UPDATE = 0  # 更新模式
    OVERRIDE = 1  # 覆盖模式


class Downloader(object):
    def __init__(self, spider_no=None, logger=None,
                 session_keep=True, session_retry_cnt=2, retry_solution_funcs=None, retry_judge_funcs=None,
                 basic_headers=None, headers_mode=HEADERS_MODEL.UPDATE,
                 proxy_strategy=PROXY_STRATEGY.SWITCH_USE, use_proxy=True, from_type='25mintest', api_num=3,
                 database_proxy_num=3, abandon_model='black', grey_time=1, proxy_mode='zm'):
        """
        :param proxy_strategy: 代理策略： 0-连续使用，1-每次请求都会切换
        :param session_keep: session策略： True:下载器永远使用一个session False：下载器每次下载都重置session
        :param proxy_mode: 代理类型：默认芝麻代理
        :param from_type: 25min/25mintest
        :param api_num: 每次从api获取数量
        :param database_proxy_num: 数据库代理补充阈值
        :param abandon_model: black/grey
        :param spider_no: 爬虫包名
        :param grey_time: 加灰维持时间
        :param session_retry_cnt: http request 内置的默认重试次数
        :param retry_solution_funcs: 重试前需要执行的函数
        :param retry_judge_funcs: 判断是否需要重试的函数
        :param http header 传入模式: 更新模式/覆盖模式 默认更新模式
        :param logger:
        """
        self._session = None
        self._logger = logger

        self._spider_no = spider_no
        self._from_type = from_type
        self._api_num = api_num
        self._database_proxy_num = database_proxy_num
        self._abandon_model = abandon_model
        self._grey_time = grey_time
        self._proxy_model = proxy_mode

        self._proxy_strategy = proxy_strategy
        self._use_proxy = use_proxy
        self._session_retry_cnt = session_retry_cnt
        self._session_keep = session_keep
        if use_proxy:
            self._proxy = Proxy(self._spider_no, self._from_type, self._api_num, self._database_proxy_num,
                                self._abandon_model,
                                self._grey_time, self._logger, self._proxy_model)
        else:
            self._proxy = VirtualProxy()
        self._retry_solution_funcs = retry_solution_funcs or {}
        self._retry_judge_funcs = retry_judge_funcs or {}
        self._retry_keys = []
        self._specify_retry_keys = []
        self._normal_retry_keys = []

        self.requests_param = {
            "url": None,
            "params": None,
            "data": None,
            "headers": None,
            "cookies": None,
            "json": None
        }

        default_headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

        self._basic_headers = basic_headers or default_headers

        self._headers_mode = headers_mode
        self._init_session()

    def _init_session(self):
        """
        初始化session
        :return:
        """
        request_retry = HTTPAdapter(max_retries=self._session_retry_cnt)
        self._session = requests.session()
        self._session.mount('https://', request_retry)
        self._session.mount('http://', request_retry)

    def set_cookie(self, cookie):
        """
        :param cookie:  为下载器的session增加cookie。若session_keep=False，设置cookie无意义。
        """
        requests.utils.add_dict_to_cookiejar(self._session.cookies, cookie)

    def request(self, method, url, data=None, headers=None, retry_keys=[], meta={}, **kwargs):
        """
        :param method:
        :param url:
        :param params:
        :param data:
        :param headers:
        :param cookies:
        :param files:
        :param auth:
        :param timeout:
        :param allow_redirects:
        :param hooks:
        :param stream:
        :param verify:
        :param cert:
        :param json:
        :param retry_cnt:
        :param retry_keys:重试方案的key，若传入则使用传入的方案
        :return:
        """

        if not self._session_keep:
            self._init_session()

        params = kwargs.get('params')
        cookies = kwargs.get('cookies')
        files = kwargs.get('files')
        auth = kwargs.get('auth')
        timeout = kwargs.get('timeout', 30)
        allow_redirects = kwargs.get('allow_redirects', True)
        hooks = kwargs.get('hooks')
        stream = kwargs.get('stream')
        verify = kwargs.get('verify')
        cert = kwargs.get('cert')
        json = kwargs.get('json')
        retry_cnt = kwargs.get('retry_cnt', 10)
        self._basic_headers['Host'] = urlparse.urlparse(url).hostname

        if self._headers_mode == HEADERS_MODEL.UPDATE and headers is not None:
            self._basic_headers.update(headers)
            headers = self._basic_headers
        if self._headers_mode == HEADERS_MODEL.OVERRIDE:
            headers = headers or self._basic_headers

        if self._use_proxy:
            if self._proxy_strategy == PROXY_STRATEGY.SWITCH_USE or not self._proxy.current_ip:
                self._proxy.change_proxy()

        index = 0
        while True:
            index += 1
            if index > 1 and not self._session_keep:
                self._init_session()
            if index > 1 and any(self.requests_param.values()):
                self._logger.warning(
                    u"更新requests参数！request_parma:{}".format(self.requests_param))
                if self.requests_param["url"]:
                    url = self.requests_param["url"]
                if self.requests_param["params"]:
                    params = self.requests_param["params"]
                if self.requests_param["data"]:
                    data = self.requests_param["data"]
                if self.requests_param["headers"]:
                    headers = self.requests_param["headers"]
                if self.requests_param["cookies"]:
                    cookies = self.requests_param["cookies"]
                if self.requests_param["json"]:
                    json = self.requests_param["json"]
                # 清空需要更新的param列表以便后续赋值
                self.requests_param = {
                    "url": None,
                    "params": None,
                    "data": None,
                    "headers": None,
                    "cookies": None,
                    "json": None
                }
            if index >= retry_cnt:
                self._logger.info(u'达到最大请求次数:{},url: {}, proxy: {}'.format(index, url, self._proxy.current_proxy))
                raise DownloaderException("max retry:{} url:{} proxy:{}".format(index, url, self._proxy.current_proxy))
            try:
                self._logger.info(u'开始请求url: {}, proxy: {}'.format(url, self._proxy.current_proxy))
                self._logger.info(u"当前下载第{}次，max_retry_cnt: {}".format(index, retry_cnt))
                resp = self._session.request(method, url, params, data, headers, cookies, files, auth, timeout,
                                             allow_redirects, self._proxy.current_proxies, hooks, stream, verify, cert,
                                             json)
                if resp is None:
                    self._logger.error(u'response为None！！url: {}, proxy: {}，开始重试'.format(url, self._proxy.current_proxy))
                    continue

                # 永远使用normal方案
                if self._retry_solutions(self._normal_retry_keys, resp, meta):
                    continue
                # 若传入retry_keys，则只使用retry_keys指定的重试方案
                if retry_keys:
                    if self._retry_solutions(retry_keys, resp, meta):
                        continue
                else:
                    if self._retry_solutions(self._retry_keys, resp, meta):
                        continue
                return resp
            except requests_exception:
                if self._use_proxy:
                    current_ip = self._proxy.current_ip
                    self._logger.warning(u"代理失效, spider_no:{},ip:{}开始加入黑/灰名单,错误原因{}".format(self._spider_no, current_ip,
                                                                                            traceback.format_exc()))

                    # 此种异常必须加黑ip，并更换ip
                    if current_ip:
                        if self._abandon_model == 'black':
                            self._proxy.add_black()
                            self._logger.warning("加入黑名单 ip:" + current_ip)
                        elif self._abandon_model == 'grey':
                            self._proxy.add_grey()
                            self._logger.warning("加入灰名单 ip:" + current_ip)
                        self._proxy.change_proxy()
                else:
                    self._logger.warning(traceback.format_exc())
            except Exception as e:
                err_msg = u'非预期异常: {}'.format(traceback.format_exc())
                self._logger.error(err_msg)
                raise DownloaderException(err_msg)

    def _retry_solutions(self, retry_keys, resp, meta):
        for key in retry_keys:
            retry_judge_func = self._retry_judge_funcs[key]
            retry_solution_func = self._retry_solution_funcs[key]
            if retry_judge_func(resp, meta):
                self._logger.warning(
                    u"retry_judge_func:{} 判断需要重试--------".format(retry_judge_func.__name__))
                if retry_solution_func:
                    self._logger.warning(
                        u"进入retry_solution_func:{} 开始执行".format(retry_solution_func.__name__))
                    retry_solution_func(resp, meta)
                return True
        return False

    def get(self, url, headers=None, retry_keys=[], meta={}, **kwargs):
        """

        :param url:
        :param headers:
        :param retry_keys: 重试方案的key，若传入则使用传入的方案  默认为空list
        :param kwargs:
        :return:
        """
        return self.request('get', url, data=None, headers=headers, retry_keys=retry_keys, meta=meta, verify=False,
                            **kwargs)

    def post(self, url, data=None, headers=None, retry_keys=[], meta={}, **kwargs):
        """

        :param url:
        :param data:
        :param headers:
        :param retry_keys: 重试方案的key，若传入则使用传入的方案 默认为空list
        :param kwargs:
        :return:
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.request('post', url, data=data, headers=headers, retry_keys=retry_keys, meta=meta, verify=False,
                            **kwargs)

    def get_cookie(self):
        """
        获取cookie dict
        :return:
        """
        return requests.utils.dict_from_cookiejar(self._session.cookies)

    def change_proxy(self):
        """
        更换ip
        :return:
        """
        self._proxy.change_proxy()

    def add_black(self):
        """
        加黑当前ip
        :return:
        """
        self._proxy.add_black()

    def add_grey(self):
        """
        加黑当前ip
        :return:
        """
        self._proxy.add_grey()

    def change_add_black_proxy(self):
        """
        加黑当前ip 并更换ip
        :return:
        """
        self.add_black()
        self.change_proxy()

    def change_add_grey_proxy(self):
        """
        加灰当前ip 并更换ip
        :return:
        """
        self.add_grey()
        self.change_proxy()

    def set_retry_solution(self, judge_func=None, solution_func=None, retry_key=None):
        """
        设置判断需要重试方法和重试前执行函数
        :param judge_func:
        :param solution_func:
        :return:
        """
        if retry_key and "normal" in retry_key:
            key = retry_key
            if key not in self._normal_retry_keys:
                self._normal_retry_keys.append(key)
        else:
            if retry_key:
                key = retry_key
                if key not in self._specify_retry_keys:
                    self._specify_retry_keys.append(key)
            else:
                key = str(uuid.uuid4())
                self._retry_keys.append(key)
        self._retry_judge_funcs[key] = judge_func
        self._retry_solution_funcs[key] = solution_func


if __name__ == '__main__':
    from ics.utils import get_ics_logger

    logger_ = get_ics_logger('test')
    downloader = Downloader(spider_no="zhixing", logger=logger_, abandon_model='grey', grey_time=1)


    def test_judge_func(resp):
        if "html" in resp.content:
            return True
        return False


    def test_solution_func(resp, meta):
        downloader.requests_param["url"] = "https://www.baidu.com"


    downloader.set_retry_solution(test_judge_func, test_solution_func)

    for i in range(10):
        downloader.get("https://www.jd.com", update_requests_key="update_cookie").content
