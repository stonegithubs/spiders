# import re
#
# from selenium import webdriver
# import time
#
# # 无界面浏览器
# driver = webdriver.PhantomJS()
# driver.get("https://www.jd.com/")
#
# # 向下滚动10000像素
# js = "document.body.scrollTop=1000000"
# time.sleep(5)
#
# # 查看页面快照
# # driver.save_screenshot("./old_jingdong.png")
#
# # 执行JS语句
# driver.execute_script(js)
# time.sleep(5)
# # 查看页面快照
# driver.save_screenshot("./new_jingdong.png")
#
# # 写入网页
# # with open('./京东.html', 'w')as f:
# #     f.write(driver.page_source)
#
# # 退出
# # driver.quit()
#
# # 打印网页html
# # print(driver.page_source)
#
#
# # res = driver.find_element_by_class_name('more_info_price_txt xh-highlight').text
# # print(type(res))
# # for i in res:
# #     print(i)
#
#
# html_str = driver.page_source
# i = html_str.find_element_by_xpath('//li[@class="more_item more_item_good"]/a/div/p')
# print(i.text)
import csv
import json

import requests

resp = requests.get(
    'https://diviner.jd.com/diviner?p=610009&lid=1&lid=1&pin=&uuid=820685190&lim=100&ec=utf-8&_=1541832169064')
resp = resp.content.decode()
resp = json.loads(resp)
# with open('./jd.json', 'w')as f:
#     f.write(resp)
# print(len(resp['data']))
with open('./jd.csv', 'w')as f:
    f.write('')

for i in range(len(resp['data'])):
    print(resp['data'][i]['t'] + ',' + '¥' + resp['data'][i]['jp'] + ',' + 'https://img13.360buyimg.com/jdcms/s170x170_' + resp['data'][i]['img'] + ',')
    res = resp['data'][i]['t'] + ',' + '¥' + resp['data'][i]['jp'] + ',' + 'https://img13.360buyimg.com/jdcms/s170x170_' + resp['data'][i]['img'] + ','
    with open('./jd.csv', 'a')as f:
        f.write(res + '\n')
