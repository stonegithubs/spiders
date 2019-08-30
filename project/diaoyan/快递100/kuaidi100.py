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
            'https':'https://36.7.26.106:4203'
        }
        return proxies

    def run(self, url, danhao):
        all_html = self.get_html(url)
        res = json.loads(all_html)
        post_type = res['auto'][0]['comCode']
        print(post_type)
        # phone_url = 'https://m.kuaidi100.com/query'
        # headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36'}
        # data = {
        #     'postid': danhao,
        #     'id': 1,
        #     'valicode': '',
        #     'temp': 0.11227234573852751,
        #     'type': post_type,
        #     'phone': '',
        #     'token': '',
        #     'platform': 'MWWW'
        # }
        # content = requests.post(url=phone_url, headers=headers, data=data, proxies=self.proxies()).content.decode()
        # content = json.loads(content)
        # for i in content['data']:
        #     # print(i)
        #     print('快递于' + i['time'] + '在' + i['context'])
        # com_url='https://www.kuaidi100.com/query?type='+post_type+'&postid='+danhao+'&temp=0.9210675893058222&phone='
        com_url = 'https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/channel/data/asyncqury?cb=jQuery110205566413472862644_{}&appid=4001&com='+post_type+'&nu='+danhao+'&vcode=&token=&_={}'.format(int(time.time() * 100),int(time.time() * 100))
        res = self.get_html(com_url)
        # res = json.loads(res)
        print(res.replace('/**/jQuery110205566413472862644_(',''))
        # for i in res['data']:
        #     print('快递于' + i['time'] + '在' + i['context'])


if __name__ == '__main__':
    # danhao = '822250542489'
    danhao = '3102657956320'
    url = 'https://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={}'.format(danhao)
    kuaidi = KuaiDiSpider()
    kuaidi.run(url, danhao)