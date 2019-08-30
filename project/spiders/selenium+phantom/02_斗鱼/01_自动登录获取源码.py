from selenium import webdriver


driver = webdriver.Chrome('/home/zhang/chromedriver')
driver.get('https://www.douyu.com/directory/all')
driver.find_elements_by_class_name("u-login fl").click()
