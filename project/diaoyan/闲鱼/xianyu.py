import json
import time

import requests
from lxml import etree


class KuaiDiSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'cookie': 'miid=508263721001231958; t=0f7e8f73488da6f95b67d3805a3478a4; hng=CN%7Czh-CN%7CCNY%7C156; cna=1l1/FRo5AikCAbfPtqIfa5gc; thw=cn; lgc=dd1358792063; tracknick=dd1358792063; _cc_=WqG3DMC9EA%3D%3D; tg=0; enc=9sCu8EvLHu%2Fyll91AjOjWgFq%2FVia2XMl0Gkc71PZzeStw33u67ZDOESeJB21pYOT2a3z07Pesr5e3wZ%2B%2Fbs7fA%3D%3D; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _lang=zh_CN; cookie2=17993000af4cd52d2177eefdae96f3d4; v=0; _tb_token_=7d83bfa863bde; _m_h5_tk=8271d5a4ff8990d5188037a6bc2c2ba2_1565091967341; _m_h5_tk_enc=afe75d95d11dc58e1bf749eb92773c5b; UM_distinctid=16c664d2bd74c3-0b69d7e4dd4b6f-3f385c06-100200-16c664d2bd834c; uc3=id2=UoYaibHU7gsJjg%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dBy32ghOW65Y%2FZw9I%3D&nk2=B0b8TA7HQ2aKcDOf; csg=adf96469; dnk=dd1358792063; skt=9e3052022c8f9fe8; existShop=MTU2NTA4NjgwMQ%3D%3D; uc4=nk4=0%40BQUFo%2FtZUS9%2Bq%2FDb2K4wYvALdf2OVo8%3D&id4=0%40UO6TEV%2FB5R53qm%2BsLUsU5wHp2XmI; uc1=cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie21=VFC%2FuZ9aiKCaj7AzMHh1&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTaHY75OeMsXQ%3D%3D&tag=8&lng=zh_CN; mt=ci=0_1; isg=BBsbLkfcwut6az5vrfh0ZAekqn-F8C_y1Ekyew1Y95ox7DvOlcC_QjluhgxHV4fq; l=cBSoBiGgqM1nUHJzBOCanurza77OSIRYYuPzaNbMi_5pv6T_ADbOk5iw3F96VjWd_2TB4sdB3eJ9-etkZ-PPSIok11sh.',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }

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
        # all_html = all_html.json()
        # res = json.dumps(all_html)
        print(all_html)


if __name__ == '__main__':
    url = "https://h5api.m.taobao.com/h5/mtop.taobao.idle.home.nextfresh/3.0/?jsv=2.5.0&appKey=12574478&t="+str(int(time.time()*1000))+"&sign=793f9e09377991cf686e0b0176178fc0&api=mtop.taobao.idle.home.nextfresh&v=3.0&type=jsonp&dataType=jsonp&callback=mtopjsonp3&data=%7B%22spmPrefix%22%3A%22a2170.7897990.6801272.%22%2C%22trackName%22%3A%22Feed1%22%2C%22needBanner%22%3A%22true%22%2C%22abtag%22%3A%22style_masonryLayouts_1.0_mamaAD%22%2C%22pageNumber%22%3A1%7D"
    kuaidi = KuaiDiSpider()
    kuaidi.run(url)
