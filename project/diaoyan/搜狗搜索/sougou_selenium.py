import time

from selenium import webdriver

class SouGuo(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.page = 1

    def run(self):
        self.driver.get('https://www.sogou.com/')
        self.driver.find_element_by_id("query").send_keys('手机')
        self.driver.find_element_by_id("stb").click()
        while True:
            time.sleep(1)
            title = self.driver.find_elements_by_xpath('//div[@class="results"]')
            print(title[0].text.split())

            # 翻页
            break
            self.driver.find_element_by_id('sogou_next').click()
            self.page+=1
            if self.page==101:
                break


if __name__ == '__main__':
    sougou = SouGuo()
    sougou.run()