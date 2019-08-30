from selenium import webdriver
import time

driver = webdriver.PhantomJS()
driver.get('http://www.renren.com/')

driver.find_element_by_id('email').send_keys('18568453967')
driver.find_element_by_id('password').send_keys('0422.520dong')
driver.find_element_by_id('login').click()
time.sleep(20)

driver.save_screenshot('./renren.png')
driver.close()
