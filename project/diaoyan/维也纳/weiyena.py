import time
from lxml import etree
from selenium import webdriver
import requests
chromeOptions = webdriver.ChromeOptions()


def req_html(url):
    chromeOptions.add_argument("--proxy-server=http://119.132.61.12:4272")
    driver=webdriver.Chrome()

    driver.get(url)
    time.sleep(2)
    # with open('./weiyena.html','wb')as f:
    #     f.write(driver.page_source.encode("utf8", "ignore"))  # 忽略非法字符
    return driver

def get_detail_hotel(url):
    driver = req_html(url)
    html = driver.page_source
    res = etree.HTML(html)
    hotel_list = res.xpath('//div/div[1]/div[2]/div/div/div[1]/span/a/@href')
    # print(hotel_list)
    driver.close()
    return hotel_list

def get_next_page(url):
    driver = req_html(url)
    driver.find_element_by_link_text('下一页').click()
    # print(hotel_list)
    # driver.close()
    return driver

def detail_list(url):
    hotel_list=get_detail_hotel(url)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    for i in hotel_list:
        # req_html(i)
        # print(i)
        detail_html = requests.get(url=i,headers=headers).text
        detail_html = etree.HTML(detail_html)
        title = detail_html.xpath('//p[@class="ht3"]/text()')[0]
        with open('./totel_name.txt','a',encoding='utf8')as f:
            f.write(title+'\n')
    driver = get_next_page(url)
    url = driver.current_url
    print(url)
    driver.close()
    detail_list(url)


if __name__ == '__main__':
    url='http://www.wyn88.com/resv/newResvDataInit.html'
    detail_list(url)