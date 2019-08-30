import time

import requests


class IPTest(object):
    def __init__(self):
        self.url='https://www.mingluji.com/'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        self.path='./ip.txt'

    def get_ip(self):
        with open(self.path, 'r')as f:
            for mun in f:
                # print('num',mun)
                a = mun.strip()
                proxies={'https':a}
                print('a',a)
                try:
                    res = requests.get(self.url,self.header,proxies=proxies,timeout=3)
                    with open('./ip1.txt','a',encoding='utf8')as file:
                        file.write(a+'\n')
                    print('响应码',res.status_code,'已写入',a)

                except Exception as e:
                    print('无效',e)
                    continue

if __name__ == '__main__':
    ip = IPTest()
    ip.get_ip()
    # print(a)
