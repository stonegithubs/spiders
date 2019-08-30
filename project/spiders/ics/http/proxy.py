# coding=utf-8


__author__ = 'wu_yong'

import time
from ics.utils import get_ics_logger
from ics.proxy_new import IcsProxy, get_fidder_proxy


class Proxy(object):
    def __init__(self, spider_no, from_type, api_num, database_proxy_num, model, grey_time, logger, proxy_model):
        self._ip = None
        self._port = None
        self._proxies = {}

        self._logger = logger
        self._spider_no = spider_no
        self._from_type = from_type
        self._api_num = api_num
        self._database_proxy_num = database_proxy_num
        self._model = model
        self._grey_time = grey_time
        self._proxy_model = proxy_model
        self._proxy_object = IcsProxy(self._proxy_model, logger=logger)

    def __init_proxy(self):
        if self._proxy_model == 'zm':
            self._ip, self._port, self._proxies = self._proxy_object.get_proxy(self._spider_no, self._from_type,
                                                                               self._api_num,
                                                                               self._database_proxy_num, self._model,
                                                                               self._grey_time)
            self._logger.info(u'开始取用芝麻代理, proxy: {}:{}'.format(self._ip, self._port))
        elif self._proxy_model == 'test':
            self._ip, self._port, self._proxies = get_fidder_proxy()
            self._logger.info(u'开始取用test代理, proxy: {}:{}'.format(self._ip, self._port))
        elif self._proxy_model == 'dly':
            self._ip, self._port, self._proxies = self._proxy_object.get_proxy(spider_no=self._spider_no)
            self._logger.info(u'开始取用代理云代理, proxy: {}:{}'.format(self._ip, self._port))
        else:
            self._ip, self._port, self._proxies = None, None, {}
            self._logger.info(u'代理配置关键字proxy_mode为:{}, 无法获取到代理，不使用代理'.format(self._proxy_model))

    def change_proxy(self):
        self._logger.info(u'开始切换代理')
        self.__init_proxy()
        self._logger.info(u'切换代理成功')
        return self._proxies

    @property
    def current_proxy(self):
        proxy = '{}:{}'.format(self._ip, self._port)
        return proxy

    @property
    def current_ip(self):
        return self._ip

    @property
    def current_proxies(self):
        return self._proxies

    def add_black(self):
        self._proxy_object.add_black(self._ip, self._spider_no)

    def add_grey(self):
        self._proxy_object.add_grey(self._ip, self._spider_no)


class VirtualProxy(object):
    def __init__(self):
        pass

    def __init_proxy(self):
        pass

    def change_proxy(self):
        pass

    @property
    def current_proxy(self):
        return "localhost"

    @property
    def current_ip(self):
        return "localhost"

    @property
    def current_proxies(self):
        return None

    def add_black(self):
        pass

    def add_grey(self):
        pass


if __name__ == '__main__':
    logger = get_ics_logger('test')
    ins = Proxy(logger, 'zm', 'zhixing')
    while True:
        # ins.change_proxy()
        print (ins.current_proxy, ins.current_proxies)
        time.sleep(3)
