import time
import random
import requests
from lxml import etree

from faker import Factory

class DangDangSpider(object):
    def __init__(self):
        # self.f = Factory.create()
        # self.ua = f.user_agent()
        self.headers = {
            'User-Agent': Factory.create().user_agent(),
            'Cookie': 'from=460-5-biaoti; order_follow_source=P-460-5-bi%7C%231%7C%23sp0.baidu.com%252F9q9JcDHa2gU2pMbgoY3K%252Fadrc.php%253Ft%253D06KL00c00fZ-jkY0h0G-0KGwAsjknY-I00000rNUrNC00000VtSvCC%7C%230-%7C-; ddscreen=2; __permanent_id=20190806161533559315735406156904033; __visit_id=20190806161533561304615533315653580; __out_refer=1565079334%7C!%7Csp0.baidu.com%7C!%7C%25E5%25BD%2593%25E5%25BD%2593; __ddc_1d=1565079334%7C!%7C_utm_brand_id%3D11106; __ddc_24h=1565079334%7C!%7C_utm_brand_id%3D11106; __ddc_15d=1565079334%7C!%7C_utm_brand_id%3D11106; __ddc_15d_f=1565079334%7C!%7C_utm_brand_id%3D11106; pos_1_end=1565079443238; pos_1_start=1565079446594; priceab=b; NTKF_T2D_CLIENTID=guest693FFB4B-4465-A1C6-483A-6616C8B37793; nTalk_CACHE_DATA={uid:dd_1000_ISME9754_guest693FFB4B-4465-A1,tid:1565080864946422}; MDD_channelId=70000; MDD_fromPlatform=307; __rpm=%7Cs_112100.94003212839%2C94003212840.7.1565081593098; pos_9_end=1565081816385; pos_0_start=1565081816406; pos_0_end=1565081816413; ad_ids=2614197%2C2677950%2C3258059%2C3258055%2C3258054%2C3258053%7C%233%2C3%2C3%2C3%2C2%2C1; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D1%26district_id%3D1110101%26town_id%3D-1; __trace_id=20190806165658548911805398324197287; producthistoryid=1900652264%2C27859582'}

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers, proxies=self.proxies())
        return res.text

    def proxies(self):
        ip = '''14.134.200.107:4272
115.153.169.88:4236
220.189.109.109:4268
122.231.115.182:4265
218.66.247.195:4235
218.23.128.154:4254
60.182.78.110:4221
182.105.227.207:4276
60.189.146.134:4274
153.99.8.56:4260
113.117.109.102:4237
222.188.48.85:4232
118.79.9.189:4225
114.239.123.9:4292
114.226.133.35:4275
114.229.86.249:4216
36.33.54.91:4254
49.76.55.47:4224
122.4.47.229:4264
220.165.29.251:4226'''
        ip = ip.split('\n')
        # print(ip)
        proxies = {
            'https': 'https://'+random.choice(ip)
        }
        return proxies

    def write_html(self, path, content):
        with open(path, 'w', encoding='utf8')as f:
            f.write(content)

    def etree_html(self, content):
        res = etree.HTML(content)
        return res

    def run(self, url):
        all_html = self.get_html(url)
        all_html = self.etree_html(all_html)
        href_list = all_html.xpath('//ul[@class="bigimg"]/li/a/@href')
        # print(href_list)
        # print(len(href_list))
        for i in href_list:
            detail_html = self.get_html(i)
            self.write_html('./dangdang.html',detail_html)
            break
            detail_html = self.etree_html(detail_html)
            try:
                title = detail_html.xpath('//h1//@title')[0]
            except Exception:
                title = ''
            print(title)
            # time.sleep(1)


if __name__ == '__main__':
    for i in range(14, 101):
        url = 'http://search.dangdang.com/?key=python&act=input&page_index={}'.format(i)
    #     url = 'http://search.dangdang.com/?key=python&act=input&page_index=1'
        print('第', i, '页')
        kuaidi = DangDangSpider()
        kuaidi.run(url)
        # kuaidi.proxies()
        break