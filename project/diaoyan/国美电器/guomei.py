import json

import requests


class GuoMeiSpider(object):
    def __init__(self):
        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
            'referer': 'https://search.gome.com.cn/search?question=%E7%94%B5%E5%99%A8',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.cookie = {
            'uid': 'CjoWyl0//Si/VZoZmmIUAg==',
            'sajssdk_2015_cross_new_user': '1',
            'atgregion': '11010200%7C%E5%8C%97%E4%BA%AC%E5%8C%97%E4%BA%AC%E5%B8%82%E6%9C%9D%E9%98%B3%E5%8C%BA%E6%9C%9D%E5%A4%96%E8%A1%97%E9%81%93%7C11010000%7C11000000%7C110102002',
            's_cc': 'true',
            'gpv_p22': 'no%20value',
            'cartnum': '0_0-1_0',
            'DSESSIONID': '04f827386c4948199ddba19b189d9d27',
            '_idusin': '81257323763',
            's_ev13': '''%5B%5B'sem_baidu_pinpai_yx_pc_bt'%2C'1564474663789'%5D%5D''',
            'headerSearchHistory': '%5B%22%E7%94%B5%E5%99%A8%22%5D',
            'route': 'd0f4111aa9842ebeec03a646eac8fbad',
            'compare': '',
            '_index_ad': '0',
            'gradeId': '-1',
            'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2216c41f4daed6f0-01baf0fa69d84d-3f385c06-1049088-16c41f4daee8bb%22%2C%22%24device_id%22%3A%2216c41f4daed6f0-01baf0fa69d84d-3f385c06-1049088-16c41f4daee8bb%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22_latest_cmpid%22%3A%22sem_baidu_pinpai_yx_pc_bt%22%7D%7D',
            'gpv_pn': 'no%20value',
            's_ppv': '-%2C100%2C18%2C7193',
            's_getNewRepeat': '1564474709708-New',
            's_sq': 'gome-prd%3D%2526pid%253Dhttps%25253A%25252F%25252Fsearch.gome.com.cn%25252Fsearch%25253Fquestion%25253D%252525E7%25252594%252525B5%252525E5%25252599%252525A8%2526oid%253Dfunctiononclick(event)%25257Bjavascript%25253AdoPageNumSearch(3)%25253Breturnfalse%25253B%25257D%2526oidt%253D2%2526ot%253DA',
        }

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers,cookies=self.cookie)
        print(res.text)
        return res.text

    def run(self, url):
        res = self.get_html(url)
        res = json.loads(res)
        with open('./guomei.json','w',encoding='utf8')as f:
            f.write(str(res))
        print(res['content']['prodInfo']['products'][0]['name'])


if __name__ == '__main__':
    url = 'https://search.gome.com.cn/search?question=%E7%94%B5%E5%99%A8&&page=2&type=json&aCnt=0'
    tu = GuoMeiSpider()
    tu.run(url)
