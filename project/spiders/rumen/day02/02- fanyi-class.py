import json
import sys

import requests


class BaiduFanyi():
    def __init__(self, trans_str):
        self.trans_str = trans_str
        self.lang_detect_url = 'https://fanyi.baidu.com/langdetect'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1', }
        self.trans_url = 'https://fanyi.baidu.com/basetrans'

    def parse_url(self, url, data):
        """发送post请求,获取相应"""
        r = requests.post(url, data=data, headers=self.headers)
        return json.loads(r.content.decode())

    def get_ret(self, dict_r):
        """提取翻译结果"""
        ret = dict_r['trans'][0]['dst']
        print(self.trans_str + ':' + ret)

    def run(self):
        """实现主要逻辑"""
        # 1.获取语言类型
        # 1.准备post的url地址,post_data
        lang_detect_data = {'query': self.trans_str}
        # 2.发送post请求,获取相应
        # 3.提取语言类型
        lang = self.parse_url(self.lang_detect_url, lang_detect_data)['lan']
        # print(lang)
        # 2.准备post的数据
        trans_data = {'query': self.trans_str, 'from': 'zh', 'to': 'en'} if lang == 'zh' else {'query': self.trans_str,
                                                                                               'from': 'en', 'to': 'zh'}
        # 3.发送请求,获取相应
        dict_r = self.parse_url(self.trans_url, trans_data)
        # 4.提取翻译的结果
        self.get_ret(dict_r)


if __name__ == '__main__':
    trans_str = sys.argv[1]
    # trans_str = '建筑'
    baiduFanyi = BaiduFanyi(trans_str)
    baiduFanyi.run()
