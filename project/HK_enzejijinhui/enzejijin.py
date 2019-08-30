import requests
from lxml import etree


def parse_url(i):
    url = 'http://www.en-ze.cn/pc/zhuyang/list1/lb/a_f71d0d79/p/{}.html'
    res = requests.get(url.format(i)).text
    return res


def detail_html():
    for i in range(1,85):
        html = parse_url(i)
        html = etree.HTML(html)
        for i in range(1, 5):
            title = html.xpath('//div[@id="section"]/dl/dd[' + str(i) + ']/h4//text()')[0]
            year = html.xpath('//*[@id="section"]/dl/dd[' + str(i) + ']/p[1]//text()')
            title = title.replace('﻿', '')
            with open('text.csv', 'a', encoding='utf-8')as f:
                f.write(title + '\n')
            # print(year)
            for i in year:
                i = i.replace('\n          ', '')
                with open('text.csv', 'a', encoding='utf-8')as f:
                    f.write(i + '\n')

            with open('text.csv', 'a', encoding='utf-8')as f:
                f.write('\n')


if __name__ == '__main__':
    detail_html()
