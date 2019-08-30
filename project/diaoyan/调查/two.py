import time
from lxml import etree

import requests


class NewsSpider(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.num = 474

    def run(self, url):
        # time.sleep(2)
        res1 = requests.get(url, self.headers).content.decode()
        # print(res1)
        res = etree.HTML(res1)
        detail_url_list = res.xpath('//p[@class="view_more"]/a/@href')
        # print(detail_url_list)
        # print(len(detail_url_list))
        for i in detail_url_list:
            time.sleep(2)
            detail = requests.get(i, self.headers).content.decode()
            # with open('news.html','w+',encoding='utf8')as f:
            #     f.write(detail+'\n')
            detail = etree.HTML(detail)
            try:
                title = detail.xpath('//h1[@class="entry-title"]//text()')[0]
            except Exception:
                title=''
            print(title)
            try:
                times = detail.xpath('//a/time/text()')[0]
            except Exception:
                times = ''
            # print(times)
            contents = detail.xpath('//div[@class="entry-content"]//p//text()')
            content = ''
            for j in contents:
                content += j
            content = content.replace('\n', '').replace('\r', '').replace('\r\n', '')
            with open('data_two.txt', 'a+', encoding='utf8')as f:
                self.num += 1
                f.write(str(self.num) + '#' + title + '#' + times + '#' + content + '\n')
            # print(title+'#'+times+'#'+content)
            print('*' * 100)


if __name__ == '__main__':
    new = NewsSpider()
    for i in range(119, 120):
        url = 'https://www.ned.org/category/news/page/{}/'.format(i)
        new.run(url)
        print(i)