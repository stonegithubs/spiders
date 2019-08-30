import requests
from pyquery import PyQuery as pq
from lxml import etree
from time import sleep
import random
import linecache


class GetProxy(object):
    def __init__(self):
        # 代理ip网站
        self.url = 'http://www.xicidaili.com/wn/{}'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self.file = r'./ip.txt'
        # 用于检查代理ip是否可用
        self.check_url = 'https://www.python.org/'
        self.title = 'Welcome to Python.org'
        # self.proxies = {
        #     'http':'http://50.197.139.162:36609'
        # }


    def get_page(self,page_num):
        # response = requests.get(self.url.format(page_num), headers=self.header,proxies=self.proxies)
        response = requests.get(self.url.format(page_num), headers=self.header,)
        # print(response.status_code)
        return response.text

    def page_parse(self, response):
        """只取一页"""
        stores = []
        result = pq(response)('#ip_list')
        for p in result('tr').items():
            if p('tr > td').attr('class') == 'country':
                ip = p('td:eq(1)').text()
                port = p('td:eq(2)').text()
                protocol = p('td:eq(5)').text().lower()
                # if protocol == 'socks4/5':
                #     protocol = 'socks5'
                proxy = '{}://{}:{}'.format(protocol, ip, port)
                stores.append(proxy)
        return stores

    def start(self):
        """只取一页"""
        response = self.get_page(1)
        proxies = self.page_parse(response)
        print(len(proxies))
        file = open(self.file, 'w')
        i = 0
        for proxy in proxies:
            try:
                check = requests.get(self.check_url, headers=self.header, proxies={'http': proxy}, timeout=5)
                check_char = pq(check.text)('head > title').text()
                if check_char == self.title:
                    print('%s is useful'%proxy)
                    file.write(proxy + '\n')
                    i += 1
            except Exception as e:
                continue
        file.close()
        print('Get %s proxies'%i)

    def get_proxiex(self):
        """随机取出IP"""
        i = random.randint(1, 121)
        line = linecache.getline(r'ip.txt', i)
        return line

    def run(self):
        for num in range(1,1674):
            sleep(2)
            res = self.get_page(num)
            print(num)
            res = etree.HTML(res)
            ip_list = res.xpath('//*[@id="ip_list"]//tr/td[2]/text()')
            # print(ip_list)
            port = res.xpath('//*[@id="ip_list"]//tr/td[3]/text()')
            type = res.xpath('//*[@id="ip_list"]//tr/td[6]/text()')
            life = res.xpath('//*[@id="ip_list"]//tr/td[9]/text()')
            time = res.xpath('//*[@id="ip_list"]//tr/td[7]/div/@title')
            delayed = []
            for z in time:
                z = z.split('秒')
                delayed.append(float(z[0]))
            for j, i in enumerate(life):
                if i != '1分钟' and delayed[j] < 3:
                    # print(i)
                    with open('./ip.txt','a',encoding='utf8')as f:
                        f.write(type[j].lower()+'://'+ip_list[j]+':'+port[j]+'\n')

# 732页20048行
if __name__ == '__main__':
    get = GetProxy()
    get.run()
