#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'He_Zhen'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_chrome_web_driver(ip=None, port=None):

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent= Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')

    # chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    if ip and port :
        chrome_options.add_argument("--proxy-server=http:// %s:%s" % (ip, port))

    # executable_path = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    executable_path = "/opt/google/chrome/chromedriver"
    web = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)

    return web


