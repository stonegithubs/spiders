import requests
from lxml import etree


class Spiders(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
            'Cache-Control': 'max-age=0',
            'Cookie': '__mta=208969645.1564019937547.1564020536357.1564020558750.3; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=16c23473b6ac8-0333f7f2e95b68-3f385c06-ff000-16c23473b6ac8; _lxsdk=16c23473b6ac8-0333f7f2e95b68-3f385c06-ff000-16c23473b6ac8; _hc.v=f982e933-5e79-e9bf-7ef5-ad70602083de.1563959967; cy=5; cye=nanjing; s_ViewType=10; cityInfo=%7B%22cityId%22%3A5%2C%22cityName%22%3A%22%E5%8D%97%E4%BA%AC%22%2C%22provinceId%22%3A0%2C%22parentCityId%22%3A0%2C%22cityOrderId%22%3A0%2C%22isActiveCity%22%3Afalse%2C%22cityEnName%22%3A%22nanjing%22%2C%22cityPyName%22%3Anull%2C%22cityAreaCode%22%3Anull%2C%22cityAbbrCode%22%3Anull%2C%22isOverseasCity%22%3Afalse%2C%22isScenery%22%3Afalse%2C%22TuanGouFlag%22%3A0%2C%22cityLevel%22%3A0%2C%22appHotLevel%22%3A0%2C%22gLat%22%3A0%2C%22gLng%22%3A0%2C%22directURL%22%3Anull%2C%22standardEnName%22%3Anull%7D; aburl=1; QRCodeBottomSlide=hasShown; wed_user_path=27813|0; _lxsdk_s=16c26bb6e86-c05-f5f-698%7C%7C1995',
            'Host': 'www.dianping.com',
            'If-Modified-Since': 'Thu, 25 Jul 2019 02:37:12 GMT',
            'If-None-Match': '"95643d988708c40cac0194dad6fee4ee"',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.dianping.com/search/keyword/5/10_%E5%AE%B6%E5%B8%B8%E8%8F%9C',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

    def requests_url(self, url):
        res = requests.get(url=url, headers=self.headers).text
        # with open('./jiucan.html','w',encoding='utf8')as f:
        #     f.write(res)
        return res

    def run(self, url):
        for i in range(1, 2):
            res = self.requests_url(url.format(i))
            # print(res)
            res = etree.HTML(res)
            # title = res.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a/h4/text()')
            detail_url = res.xpath('//*[@id="shop-all-list"]/ul/li[1]/div[2]/div[1]/a/@href')
            for i in detail_url:
                detail_html = requests.get(i, self.headers)
                print(detail_html.status_code)
                detail_html = etree.HTML(detail_html.text)
                img_src = detail_html.xpath('//*[@id="shop-tabs"]/div[1]/ul/li[24]/img/@src')
                print(img_src)


if __name__ == '__main__':
    url = 'http://www.dianping.com/search/keyword/5/10_%E5%AE%B6%E5%B8%B8%E8%8F%9C/p{}'
    sp = Spiders()
    sp.run(url)
