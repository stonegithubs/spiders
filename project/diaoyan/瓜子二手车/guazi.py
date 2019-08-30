import requests
from lxml import etree


class GuaZiSpider(object):
    def __init__(self):
        self.headers = {
            'Cookie': 'uuid=f991946e-8e4c-4d69-fd2c-e09d3bef8679; antipas=7622P9Ge71n3v22316g051739X912G; cityDomain=nj; clueSourceCode=10103000312%2300; user_city_id=65; ganji_uuid=5088370033020682685555; sessionid=4259f0ec-58f3-41c6-cb54-ed9949be2758; lg=1; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22%22%2C%22ca_campaign%22%3A%22%22%2C%22ca_kw%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22ca_transid%22%3A%22%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22ca_i%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22f991946e-8e4c-4d69-fd2c-e09d3bef8679%22%2C%22sessionid%22%3A%224259f0ec-58f3-41c6-cb54-ed9949be2758%22%7D; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A51192019538%7D; preTime=%7B%22last%22%3A1564468038%2C%22this%22%3A1564467166%2C%22pre%22%3A1564467166%7D',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers).content.decode()
        return res

    def run(self, url):
        res = self.get_html(url)
        # print(res)
        res = etree.HTML(res)
        detail_list = res.xpath('//ul/li/a[@class="car-a"]/@href')
        for i in detail_list:
            detail_html=self.get_html('https://www.guazi.com'+i)
            detail_html=etree.HTML(detail_html)
            title = detail_html.xpath('/html/body/div[4]/div[3]/div[2]/h2/text()')[0].split()
            price = detail_html.xpath('/html/body/div[4]/div[3]/div[2]/div[1]/span[1]/text()')[0].split()[0]
            ccc = detail_html.xpath('//tr/td[@class="td2"]/text()')
            # print(ccc)
            # print(price)
            c = ''
            for j in title:
                c +=j
            # print(c)
            with open('./car.txt','a',encoding='utf8')as f:
                f.write(c+'\n')


if __name__ == '__main__':
    for i in range(1,51):
        url = 'https://www.guazi.com/nj/buy/o{}/'.format(i)
        tu = GuaZiSpider()
        tu.run(url)
