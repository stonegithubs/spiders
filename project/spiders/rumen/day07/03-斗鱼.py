from selenium import webdriver

# 有界面浏览器
# driver = webdriver.Chrome('/home/zhang/chromedriver')
# 无界面浏览器
driver = webdriver.PhantomJS()
driver.get('https://www.douyu.com/directory/all')

all_data = driver.find_element_by_xpath('//ul[@id="live-list-contentbox"]/li')

for i in all_data:
    data = {}
    data['btitle'] = i.driver.find_element_by_xpath