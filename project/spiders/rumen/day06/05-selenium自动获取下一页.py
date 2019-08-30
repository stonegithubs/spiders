from selenium import webdriver
import requests

# driver = webdriver.PhantomJS()

driver = webdriver.Chrome('/home/zhang/chromedriver')

page_num = input('吧名:')
link = 'http://tieba.baidu.com/f?kw={}'.format(page_num)
while True:
    print(link)
    driver.get(link)
    try:
        # print(1111, driver.find_element_by_link_text('下一页>').get_attribute('href'))
        link = driver.find_element_by_link_text('下一页>').get_attribute('href')
    except:
        link = None
        print('没有下一页了')
    # print(driver.find_element_by_xpath('//div[@id="frs_list_pager"]/span').text)
    if link:
        continue
    else:
        break

driver.quit()
