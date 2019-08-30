from pprint import pprint

import requests
import re


def f1():
    url = 'http://www.xicidaili.com/wn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    }
    proxies = {
        'http': 'http://80.120.86.242:46771'
    }

    resp = requests.get(url=url, headers=headers, proxies=proxies, timeout=3)
    print(resp.status_code)
    resp = resp.content.decode()
    # ress = resp.find('.*河北衡水市冀州.*',resp)
    print(resp)
    # get_ip(resp)

    # with open('./files/ip1.html', 'w') as file:
    #     file.write(resp)


def get_ip(obj):
    counter = 0
    sec_obj = obj.find('table')
    ip_text = sec_obj.findAll('tr')  # 获取带有IP地址的表格的所有行
    if ip_text is not None:
        with open('./ip2.txt', 'w') as f:  # 保存到本地txt文件中
            for i in range(1, len(ip_text)):
                ip_tag = ip_text[i].findAll('td')
                ip_live = ip_tag[8].get_text()  # 代理IP存活时间
                ip_speed = ip_tag[6].find('div', {'class': 'bar_inner fast'})  # 提取出速度快的IP
                if '天' in ip_live and ip_speed:
                    ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text()  # 提取出IP地址和端口号
                    counter += 1
                    f.write(ip_port + '\n')


def f3():
    url = 'http://www.xicidaili.com/wn'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    }
    proxies = {'http': 'http://124.235.181.175:80'}
    res = requests.get(url=url, headers=headers, proxies=proxies, timeout=3)
    pprint(res.status_code)
    # with open('./代理测试.html', 'w', encoding='utf-8')as ff:
    #     ff.write(res.content.decode())


if __name__ == '__main__':
    # f1()
    f3()
