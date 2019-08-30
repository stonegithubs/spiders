from selenium import webdriver

driver = webdriver.PhantomJS()

driver.get('https://www.liepin.com/user/login')

driver.save_screenshot('./liepin.png')

driver.find_element_by_class_name('text input-xlarge').send_keys('18336217025')
driver.find_element_by_class_name('text input-xlarge').send_keys('217025')
driver.find_element_by_class_name('btn btn-login').click()

import time

time.sleep(10)

driver.save_screenshot('./liepin.png')
driver.close()