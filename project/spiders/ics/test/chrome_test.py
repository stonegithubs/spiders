#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'MaoJingwen'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options



chrome_options = Options()
# 无头模式启动
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
# 谷歌文档提到需要加上这个属性来规避bug
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
chrome_options.add_argument('Accept=image/webp,image/apng,image/*,*/*;q=0.8')
chrome_options.add_argument('encoding=gzip, deflate, br')
chrome_options.add_argument('lang=zh-CN,zh;q=0.9')
# 初始化实例
path = "/opt/google/chrome/chromedriver"
chrome_options.binary_location = '/opt/google/chrome/chrome'

# 禁止加载图片
prefs = {
    'profile.default_content_setting_values' : {
        'images' : 2
    }
}
chrome_options.add_experimental_option('prefs',prefs)

web= webdriver.Chrome(executable_path=path,chrome_options=chrome_options)
# 请求百度
web.get("http://www.baidu.com")



web.quit()
