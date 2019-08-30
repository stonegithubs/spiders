import time

import requests
from lxml import etree


class NewsSpider(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.proxies={
            'https':'https://42.3.138.236:62176'
        }

    def get_html(self, url):
        try:
            res = requests.get(url, self.headers).content.decode()
        except Exception as err:
            time.sleep(2)
            res = ''
            self.get_html(url)
        return res

    def run(self, url):
        res = self.get_html(url)
        res = etree.HTML(res)
        next_page_url = res.xpath('//*[@id="wrapper"]/main/div[2]/div[2]/div/div/div[5]/div/a/@href')[0]
        if next_page_url.split('?')[0]:
            detail_url_list = res.xpath('//*[@id="wrapper"]/main//p[2]/a/@href')
            for i in detail_url_list:
                detail_html = self.get_html(i)
                # print(detail_html)
                detail_html = etree.HTML(detail_html)
                title = detail_html.xpath('//h1[@class="entry-title"]/text()')[0]
                times = detail_html.xpath('//a/time/text()')[0]
                contents = detail_html.xpath('//div[@class="entry-content"]//p//text()')
                content = ''
                # print('1',title)
                # print('2',times)
                for j in contents:
                    content += j
                content = content.replace('         ','').replace('\n','')
                with open('data.txt','a+',encoding='utf8')as f:
                    f.write(title+'#'+times+'#'+content+'\n')
                print(next_page_url.split('?')[0])
                self.run(next_page_url.split('?')[0])


if __name__ == '__main__':
    news = NewsSpider()
    url = 'https://www.ned.org/category/news/'
    news.run(url)
