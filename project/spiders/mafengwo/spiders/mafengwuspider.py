import requests
from lxml import etree
import re


class MaFengWoSpider(object):

    def __init__(self, city, page_num):
        self.city = city
        self.page_num = page_num
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Host': 'www.mafengwo.cn'
        }

    def url_list(self):
        pass

    def run(self):
        data_list = []
        # 1.准备url
        for i in range(1, 6):
            start_url = 'http://www.mafengwo.cn/search/s.php?q=' + self.city + '&p={}&t=poi&kt=1'.format(i)
            # start_url.format(i)
            print(start_url)
            # 2.请求
            cont = requests.get(start_url, headers=self.headers)
            # print(cont.content.decode())
            response = etree.HTML(cont.text)
            li_list = response.xpath('//div[@id="_j_search_result_left"]//ul/li')
            for li in li_list:
                # item = {}
                title = li.xpath('./div/div[2]/h3/a/text()')
                if title:
                    title = re.findall('景点',title[0])
                    # str = title.replace('景点 - ', '')
                    # data_list.append(item)
                    print(title)


if __name__ == '__main__':
    mfw = MaFengWoSpider('驻马店', 1)
    mfw.run()
