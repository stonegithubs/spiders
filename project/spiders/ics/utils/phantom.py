#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_web_driver(ip=None, port=None):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.resourceTimeout"] = 10
    dcap["phantomjs.page.settings.loadImages"] = True
    dcap[
        "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

    # PHANTOMJS_SERVICE = [
    #     '--proxy=localhost:8888',
    #     '--proxy-type=http',
    #     # '--proxy-auth=username:password'
    # ]

    PHANTOMJS_SERVICE = [
        '--proxy=%s:%s' % (ip, port),
        '--proxy-type=http'
    ]

    PHANTOMJS_PATH = 'E:/phantomjs/bin/phantomjs.exe'
    # PHANTOMJS_PATH = '/home/ICS/phantomjs'

    if not ip and not port:
        web = webdriver.PhantomJS(service_args=PHANTOMJS_SERVICE, executable_path=PHANTOMJS_PATH,
                                  desired_capabilities=dcap)
    else:
        web = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH, desired_capabilities=dcap)

    web.execute_script('window[\'callPhantom\'] = undefined;')
    web.execute_script('window[\'_phantom\'] = undefined;')
    return web
