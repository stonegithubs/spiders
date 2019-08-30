import json
import time
import requests
from lxml import etree


class WiPinHuiSpider(object):
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
        self.write_html('./weipinhui.html',all_html)


if __name__ == '__main__':
    url = 'https://category.vip.com/suggest.php?keyword=%E7%89%99%E8%86%8F&page=2'
    kuaidi = WiPinHuiSpider()
    kuaidi.run(url)
