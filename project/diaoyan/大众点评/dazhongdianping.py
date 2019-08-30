import requests
from lxml import etree


class Spiders(object):
    def __init__(self ):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Cookie': '_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16c23473b6ac8-0333f7f2e95b68-3f385c06-ff000-16c23473b6ac8; _lxsdk=16c23473b6ac8-0333f7f2e95b68-3f385c06-ff000-16c23473b6ac8; _hc.v=f982e933-5e79-e9bf-7ef5-ad70602083de.1563959967; cy=5; cye=nanjing; s_ViewType=10; cityInfo=%7B%22cityId%22%3A5%2C%22cityName%22%3A%22%E5%8D%97%E4%BA%AC%22%2C%22provinceId%22%3A0%2C%22parentCityId%22%3A0%2C%22cityOrderId%22%3A0%2C%22isActiveCity%22%3Afalse%2C%22cityEnName%22%3A%22nanjing%22%2C%22cityPyName%22%3Anull%2C%22cityAreaCode%22%3Anull%2C%22cityAbbrCode%22%3Anull%2C%22isOverseasCity%22%3Afalse%2C%22isScenery%22%3Afalse%2C%22TuanGouFlag%22%3A0%2C%22cityLevel%22%3A0%2C%22appHotLevel%22%3A0%2C%22gLat%22%3A0%2C%22gLng%22%3A0%2C%22directURL%22%3Anull%2C%22standardEnName%22%3Anull%7D; _lxsdk_s=16c26bb6e86-c05-f5f-698%7C%7C456',
        }

    def requests_url(self,url):
        res = requests.get(url=url, headers=self.headers).text
        return res

    def run(self,url):
        for i in range(1,51):
            res = self.requests_url(url.format(i))
            res = etree.HTML(res)
            hotel_name = res.xpath('//*[@id="poi-list"]/div[3]/div/div[1]/div[1]/ul/li/div[1]/div[1]/h2/a[1]/text()')
            area = res.xpath('//*[@id="poi-list"]/div[3]/div/div[1]/div[1]/ul/li/div[1]/div[1]/p/a/text()')
            area_m = res.xpath('//*[@id="poi-list"]/div[3]/div/div[1]/div[1]/ul/li/div[1]/div[1]/p/span/text()')
            pares = res.xpath('//*[@id="poi-list"]/div[3]/div/div[1]/div[1]/ul/li/div[1]/div[2]/div[1]/p/strong/text()')
            # print(hotel_name)
            # print(len(hotel_name))
            with open('./hotel_name.txt','a',encoding='utf8')as f:
                for j,i in enumerate(hotel_name):
                    f.write('店名:'+hotel_name[j]+'\t'+'地区:'+area[j]+area_m[j]+'\t'+'价格:'+pares[j]+'\n')


if __name__ == '__main__':
    url = 'http://www.dianping.com/nanjing/hotel/p{}'
    sp = Spiders()
    sp.run(url)
