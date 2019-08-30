from selenium import webdriver
import time
import requests


driver = webdriver.Chrome('/home/zhang/chromedriver')

driver.get('https://mail.qq.com/cgi-bin/loginpage')

driver.switch_to.frame('login_frame')
try:
    driver.find_element_by_id('u').send_keys('31926990')
    driver.find_element_by_id('p').send_keys('2005426.')
    time.sleep(1)
except:
    print('111')
driver.find_element_by_id('login_button').click()
