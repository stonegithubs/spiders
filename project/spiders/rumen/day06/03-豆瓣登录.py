"""
from selenium import webdriver
import time
import requests
from yundama import discern

# 无界面浏览器
# driver = webdriver.PhantomJS()

# 有界面浏览器
driver = webdriver.Chrome('/home/zhang/chromedriver')

# 访问url
driver.get('https://www.douban.com/')

# 填写账号
driver.find_element_by_id('form_email').send_keys('3118870566@qq.com')
# 填写密码
driver.find_element_by_id('form_password').send_keys('hello123')

# 获取验证码url
img_path = driver.find_element_by_id('captcha_image').get_attribute('src')

# 访问验证码url地址
resp = requests.get(url=img_path)
resp = resp.content
# 写入验证码
with open('./yanzhengma.jpg', 'wb')as f:
    f.write(resp)

recode = discern('./yanzhengma.jpg', 3000)

# 填写验证码
driver.find_element_by_id('captcha_field').send_keys(recode)

time.sleep(10)

# 点击登录
driver.find_element_by_class_name('bn-submit').click()

# dtitle = driver.find_element_by_xpath('//div[@id="content"]/h1/text()')
# print(driver.title)
if driver.title == '登录豆瓣':
    # 获取验证码url
    img_path = driver.find_element_by_id('captcha_image').get_attribute('src')

    # 访问验证码url地址
    resp = requests.get(url=img_path)
    resp = resp.content
    # 写入验证码
    with open('./yanzhengma.jpg', 'wb')as f:
        f.write(resp)

    recode = discern('./yanzhengma.jpg', 3000)

    # 填写验证码
    driver.find_element_by_id('captcha_field').send_keys(recode)
    driver.find_element_by_class_name('btn-submit').click()

# 写入网页
with open('./豆瓣.html', 'w')as f:
    f.write(driver.page_source)
# driver.close()"""

from selenium import webdriver
import time
import requests
from yundama import discern


class DoubanLoginSpider():

    def __init__(self):
        self.url = 'https://www.douban.com/'

    def set_user_info(self, driver):
        """填写账号密码"""
        # 填写账号
        driver.find_element_by_id('form_email').send_keys('3118870566@qq.com')
        # 填写密码
        driver.find_element_by_id('form_password').send_keys('hello123')

    def set_recode(self, driver):
        """获取验证码"""
        # 获取验证码url
        img_path = driver.find_element_by_id('captcha_image').get_attribute('src')

        # 访问验证码url地址
        resp = requests.get(url=img_path)
        resp = resp.content

        # 写入验证码
        with open('./yanzhengma.jpg', 'wb')as f:
            f.write(resp)

        # 调用云打印API识别验证码
        recode = discern('./yanzhengma.jpg', 3000)

        # 填写验证码
        driver.find_element_by_id('captcha_field').send_keys(recode)

        time.sleep(5)

    def run(self):
        # 1.访问url

        # 无界面浏览器
        # driver = webdriver.PhantomJS()

        # 有界面浏览器
        driver = webdriver.Chrome('/home/zhang/chromedriver')

        # 访问url
        driver.get(self.url)

        # 2.写入用户名密码
        self.set_user_info(driver)

        # 3.写入验证码
        self.set_recode(driver)
        # 点击登录
        driver.find_element_by_class_name('bn-submit').click()

        # 判断是否登陆成功
        # 如果登录失败
        if driver.title == '登录豆瓣':
            # 再次填写验证码
            self.set_recode(driver)
            # 再次登录
            driver.find_element_by_class_name('btn-submit').click()

        # 写入网页
        with open('./豆瓣.html', 'w')as f:
            f.write(driver.page_source)

        # 关闭连接
        # driver.close()


if __name__ == '__main__':
    dbs = DoubanLoginSpider()
    dbs.run()
