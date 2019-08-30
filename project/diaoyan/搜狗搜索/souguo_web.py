import json
import time
import requests
from lxml import etree


class KuaiDiSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers)
        return res.text

    def write_html(self, path, content):
        with open(path, 'w', encoding='utf8')as f:
            f.write(content)

    def etree_html(self, content):
        res = etree.HTML(content)
        return res

    def proxies(self):
        proxies = {
            'https': 'https://36.7.26.106:4203'
        }
        return proxies

    def run(self, url):
        all_html = self.get_html(url)
        res = self.etree_html(all_html)
        title_url_list = res.xpath('//div[@class="results"]//h3/a/@href')
        for i in range(1,14):
            title_list = res.xpath('//div[@class="results"]/div['+str(i)+']/h3/a//text()')
            # title_list = res.xpath('//div[@class="results"]/div[4]/h3/a//text()')
            if title_list:
                title = ''
                for i in title_list:
                    title+=i
                print(title)
        # print(title_list)


if __name__ == '__main__':
    url = 'https://news.sogou.com/news?query=%CF%E3%B8%DB'
    kuaidi = KuaiDiSpider()
    kuaidi.run(url)
