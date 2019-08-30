
#coding=utf-8
import copy
import json
import os
import re
import sys
import time
import logging
import traceback

import requests
from requests.cookies import cookiejar_from_dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from lxml import etree
from retry import retry

from captcha.jyc2567 import get_validate
# from task.gsxt.task import get_session
from proxy import get_proxy_for_phantom_test
from utils.cookie import formart_selenium_cookies

reload(sys)
sys.setdefaultencoding('utf-8')

formatter = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=formatter)

NEED_RETRY_CNT = 10
DELAY = 3
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

executable_path = 'C:\install\chromedriver.exe'
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=executable_path)


class RetryException(Exception):
    def __init__(self, msg):
        if isinstance(msg, Exception):
            self.message = str(msg)

headers = dict()
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
headers['Referer'] = 'http://www.gsxt.gov.cn/index.html'
headers['Upgrade-Insecure-Requests'] = '1'
m_proxy = {}


def get_session():
    from requests.adapters import HTTPAdapter
    session  = requests.session()
    request_retry = HTTPAdapter(max_retries=3)
    session.mount('https://', request_retry)
    session.mount('http://', request_retry)
    return session

session = get_session()

entType = '101'


def get_print_item(session):
    ent_type = '101'
    url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-printByEnttype.html?entType={}'.format(ent_type)
    resp = session.get(url, headers=headers, proxies=m_proxy)
    _list = json.loads(resp.text).get('data', [])
    _list = map(lambda x: x.get('codeValue', '').strip(), _list)
    st = ''
    for i in _list:
        st += 'print_item={}&'.format(i)
    print st.strip('&')
    return st, _list

def get_json(session, url):
    url = 'http://www.gsxt.gov.cn/corp-query-entprise-info-printByEnttype.html'
    data = {
        "draw": "1",
        "start":"0",
        "length": "5"
    }

    resp = session.post(url, data=json.dumps(data), headers=headers, proxies=m_proxy)


def get_html(baogao_url, st, g, item_list):
    # st = {u'status': u'ok', u'challenge': u'2f12e13c3dfd0a189309a361a8cd932c', u'validate': u'73617ae0609c49044330843e7875a1b0'}
    geet_dict = {
        'geetest_challenge': g.get('challenge'),
        'geetest_validate': g.get('validate'),
        'geetest_seccode': '{}|jordan'.format(g.get('validate')),
        'print_item': item_list
    }

    geet_st = 'geetest_challenge={}&geetest_validate={}&geetest_seccode={}&{}'.format(geet_dict['geetest_challenge'], geet_dict['geetest_validate'], geet_dict['geetest_seccode'], st)
    geet_st = geet_st.replace('|', '%7C').strip('&')
    # resp = session.post(baogao_url, data=geet_st, headers=headers, proxies=m_proxy)
    test_url = '{}?{}'.format(baogao_url, geet_st)
    resp1 = session.get(test_url, headers=headers, proxies=m_proxy)
    pass


@retry(RetryException, tries=NEED_RETRY_CNT, delay=DELAY)
def get_jbxx():
    global m_proxy
    ip, port, m_proxy = get_proxy_for_phantom_test()
    et = etree.HTML(open('search_list.html').read())
    search_urls = et.xpath('.//div[@id="advs"]//a[@class="search_list_item db"]/@href')
    host = 'http://www.gsxt.gov.cn'
    first_company_url = '{}{}'.format(host, search_urls[0])
    driver.set_page_load_timeout(20)
    try:
        driver.implicitly_wait(30)
        driver.get(first_company_url)
        locator = (By.ID, 'btn_print')
        WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located(locator))
        driver_cookies = driver.get_cookies()
        cookies = formart_selenium_cookies(driver_cookies)
        if cookies.has_key("JSESSIONID"):
            JSESSIONID = cookies.get("JSESSIONID").replace("n1:0", "n1:-1")
            cookies["JSESSIONID"] = JSESSIONID
        # session.cookies = cookiejar_from_dict(cookies, 'www.gsxt.gov.cn')
        requests.utils.add_dict_to_cookiejar(session.cookies,cookies)
        html = driver.execute_script("return document.documentElement.outerHTML")
        baogao_url = '{}{}'.format(host, re.findall(r'id=\s*"f-form"\s+action="(.+?)"', html, flags=re.S)[0])

        # insInvinfoUrl = '{}{}'.format(host, re.findall(r'var\s+insInvinfoUrl\s*=\s*"(.+?)"', html, flags=re.S)[0])
        # r = get_json(session, insInvinfoUrl)
        st, item_list = get_print_item(session)

        validate = get_validate(session, headers, m_proxy)

        s = get_html(baogao_url, st, validate, item_list)



        pass
        # cookie_str = "; ".join([item["name"] + "=" + item["value"] for item in cookies])


        # driver.find_element_by_id('btn_print').click()
        #
        # headers = dict()
        # headers[
        #     'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        # headers['Accept-Encoding'] = 'gzip, deflate'
        # headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
        # headers['Referer'] = 'http://www.gsxt.gov.cn/index.html'
        # headers['X-Requested-With'] = 'XMLHttpRequest'


        # def get_session():
        #     from requests.adapters import HTTPAdapter
        #     session = requests.session()
        #     request_retry = HTTPAdapter(max_retries=3)
        #     session.mount('https://', request_retry)
        #     session.mount('http://', request_retry)
        #     return session
        # session = get_session()
        # # session.cookies = cookiejar_from_dict({}, 'www.gsxt.gov.cn')
        # # 打码
        # current_html = driver.execute_script("return document.documentElement.outerHTML")
        # if 'http://geenew.geetest.com/static/' in current_html:
        #     try:
        #         validate = get_validate(session, headers, {})
        #     except ValueError as e:
        #         driver.quit()
        #         print "validata has error : " + e.message
        #         return
        #
        #     except Exception as e:
        #         driver.quit()
        #         # app.send_task('ics.task.gsxt.task.init', [keyword], queue='task_queue')
        #         print e
        #         return

        # driver.implicitly_wait(30)
        # locator = (By.ID, 'pop-captcha-print')
        # WebDriverWait(driver, 30, 1).until(EC.presence_of_element_located(locator))
        # driver.find_element_by_id('pop-captcha-print').click()
        #
        # driver.implicitly_wait(30)
        # html = driver.execute_script("return document.documentElement.outerHTML")
        # print driver.current_url
    except TimeoutException:
        logging.error('time out after 10 seconds when loading page')
        driver.execute_script('window.stop()')
        err_msg = u'持续操作 get_login_page 失败，重试， 失败原因: {}'.format(traceback.format_exc())
        logging.error(err_msg)
        raise RetryException(err_msg)





if __name__ == '__main__':
    get_jbxx()