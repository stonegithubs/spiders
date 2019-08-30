import requests
from lxml import etree
import re


class TuBaTuSpider(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'uid=CgoKUF0+aZAubzXWBfsRAg==; to8to_landtime=1564371342; to8tocookieid=9d71d62caf65c03aac12637c6fbd096d328927; tracker2019session=%7B%22session%22%3A%2216c3bcc5459246-0790adaabf17b3-3f385c06-1049088-16c3bcc545a763%22%7D; tracker2019jssdkcross=%7B%22distinct_id%22%3A%2216c3bcc545c4f-08155f9a1a3d08-3f385c06-1049088-16c3bcc545d896%22%7D; to8to_cook=OkOcClPzRWV8ZFJlCIF4Ag==; LXB_REFER=www.baidu.com; to8to_townid=2827; to8to_tcode=nj; to8to_tname=%E5%8D%97%E4%BA%AC; tender_popup_flag=true; layer-popup=true; Hm_lvt_dbdd94468cf0ef471455c47f380f58d2=1564371343,1564371523; sourcepath=r1; to8to_landpage=https%3A//www.to8to.com/yezhu/zxbj.php%3Futm_from%3Dbaidu%26utm_creative%3D31088698599%26utm_network%3D1%26utm_keyword%3D133302796613%26utm_placement%3D%26landpagetype%3D702%26yangshi%3D0%26adpos%3Dcl4; to8to_sourcepage=https%3A//www.baidu.com/baidu.php%3Fsc.af0000aF4eAvq9HI8kk3m-fS23JTvhZe2LqQg_Tgk_hXzxbAV7N4D4AeEB2XLQDnOrUFD6JscPulYOZhQg-1ZjirqtRFlgdYqzkXvOp3RlCKcf1d0JnGf-xPONVWl8ebcWoCXTg1fMLuEJfsAWJPv_6egv4M6Q6ciO1qSpqbal4FkNNL2ou6sRCOahDEV41iSBdcFhJmzztNcvNv1s.Db_a6eufTBjfM9JsfT5wx-qSSa9G4IT1VQ7erQKdsRP5Qjn-h6OlD_TpePh1GLePvOxdsRP5QDh9srhey2S8a9G4XdrW6IPTkgk3tUnMWElXhEWdsRP5QWC_sGYGBCnIpQnNvPMRh9CkGmtUnMgf1hWJXkudu8k8Wm9CqB-muCyr5Hk__R0.U1YY0ZDqdejfLovC__HPSPyS0A7bTgbqdejfLovC__HPSPyS0A7bTgfqnfKspynqnfKY5UQDsTt0pyYqnWcd0ATqTZnz0ZNG5yF9pywd0ZKGujYkrfKWpyfqPHR0UgfqnH0kPdtknjD4g1nvnjD0pvbqn0KzIjYLnWb0uy-b5HcvPHc1g1DYPHIxnWDsrjIxnWbdP19xnWbdnH9xnW6dnH9xnWbsrH-xnWbdPW9xnW63n1PxnWbznW7xnWm1PH00mhbqnHR3g1csP0KVm1Ykrjc4nWb1PWb1g1Dsnj7xn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5H00UMus5H08nj0snj0snj00Ugws5H00uAwETjYs0ZFJ5H00uANv5gKW0AuY5H00TA6qn0KET1Ys0AFL5HDs0A4Y5H00TLCq0A71gv-bm1dsTzdWUfKGuAnqiDFK0ZwdT1YkrjnsrjcdnH0snWR4n1f3rjcd0ZF-TgfqnHRvPjnLnHnYnHndnfK1pyfqrymLm16LnvRsnjD1PAuBnsKWTvYqrRmkrjfYnDc3nRuawDDsPfK9m1Yk0ZwdIjYk0ZK85H00TydY5H00Tyd15H00XMfqn0KVmdqhThqV5HKxn7ts0Aw9UMNBuNqsUA78pyw15HKxn7ts0ZK9I7qhUA7M5H00uAPGujYs0ANYpyfqQHD0mgPsmvnqn0KdTA-8mvnqn0KkUymqnHm0uhPdIjYs0AulpjYs0Au9IjYs0ZGsUZN15H00mywhUA7M5H60UAuW5H00ULfqn0KETMKY5H0WnanWnansc10Wna3snj0snj0WnanWn0KWThnqPjcLnWT%26word%3D%2525E8%2525A3%252585%2525E4%2525BF%2525AE%2525E5%2525BB%2525BA%2525E6%25259D%252590%2525E7%2525BD%252591%2525E7%2525AB%252599%26ck%3D4813.15.139.378.496.456.253.1117%26shh%3Dwww.baidu.com%26sht%3Dbaidu%26us%3D4.39388.3.0.1.301.0%26bc%3D110101; to8tosessionid=s_8cde02a8708beb9383b2f86a80cd09e8; pt_s_30e55b6d=vt=1564371523415&cad=; pt_30e55b6d=uid=f4VqQUarkmPbgbjgEoP7-g&nid=1&vid=2n4QG5PAmLgN3EnJkWt-mg&vn=1&pvn=1&sact=1564371528229&to_flag=0&pl=pv3eX5w3S72TC-tJYHeAGA*pt*1564371523415; to8to_nowpage=http%253A%252F%252Fmall.to8to.com%252Ftemai%252F18479.html; Hm_lpvt_dbdd94468cf0ef471455c47f380f58d2=1564371567; mall_city=326%7C2816',
            'Host': 'mall.to8to.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

    def get_html(self,url):
        res = requests.get(url=url,headers=self.headers).text
        return res

    def run(self):
        res = self.get_html(url)
        res = etree.HTML(res)
        detail_html = res.xpath('//*[@id="goodsList"]/li/div/p[1]/a/@href')
        price=res.xpath('//*[@id="goodsList"]/li/div/p[3]/del/text()')
        print(len(price))
        print(len(detail_html))
        for i in detail_html:
            detail_list = self.get_html(i)
            try:
                img_url = re.findall('value="&lt;img src=&quot;(.*)&quot; alt=&quot;',detail_list)[0]
            except Exception:
                continue
            img_url_list = img_url.split('&quot; alt=&quot;&quot; /&gt;&lt;img src=&quot;')
            # detail_html=etree.HTML(detail_list)
            # detail_title=detail_html.xpath('//*[@id="p_name"]/text()')[1]
            # detail_title=detail_html.xpath('//*[@id="detailContent"]/div[2]/dl[11]/dt/text()')
            # print(detail_title)
            # print(type(detail_title))
            # a = detail_title.split('\n')
            # print(a[1])


if __name__ == '__main__':
    url = 'http://mall.to8to.com/tag/wujin/'
    tu = TuBaTuSpider(url)
    tu.run()
