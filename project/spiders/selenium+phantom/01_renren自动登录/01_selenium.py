from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('/home/zhang/chromedriver')
driver.get('http://www.renren.com/')
# driver.save_screenshot("baidu.png")
print(driver.title)
driver.find_element_by_id("email").send_keys(u"18568453967")
driver.find_element_by_id("password").send_keys(u"0422.520dong")
driver.find_element_by_id("login").click()


# driver.quit()
