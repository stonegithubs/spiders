from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class PinDuoDuo(object):
    def first(self):
        driver=webdriver.Chrome()
        url = 'http://mobile.yangkeduo.com/classification.html?refer_page_name=index&refer_page_id=10002_1563931825148_wFM8cVWX3w&refer_page_sn=10002'
        driver.get(url)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/div/div/span[1]').send_keys('足球')
        time.sleep(4)
        driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/span').click()
        time.sleep(4)
        driver.refresh()
        driver.refresh()
        driver.refresh()
        driver.refresh()

        time.sleep(4)
        page_html = driver.page_source
        self.write_html(page_html)
        driver.find_element_by_xpath('')


    def write_html(self,page_html):
        with open('pinduoduo_html.html','a',encoding='utf8')as f:
            f.write(page_html)


if __name__ == '__main__':
    pin = PinDuoDuo()
    pin.first()