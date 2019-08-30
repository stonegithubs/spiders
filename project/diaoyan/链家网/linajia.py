import requests
from lxml import etree


class LianJiaSpider(object):
    def __init__(self, url):
        self.url = url
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': '''TY_SESSION_ID=89220a97-c40b-4428-a423-8539ca4695fd; mediav=%7B%22eid%22%3A%22202234%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22v%60(2nESvC%23%3AdQk'H%2Fng7%22%2C%22ctn%22%3A%22%22%7D; select_city=320100; digv_extends=%7B%22utmTrackId%22%3A%2221583074%22%7D; all-lj=979909237fcf62bcb16b5a6dbd3b060f; lianjia_ssid=ec31aab8-0128-4ee3-84ba-c9adf20de0e8; lianjia_uuid=910efb2d-6132-4405-a134-0d061dab6d73; _smt_uid=5d3e4eb1.4357919c; UM_distinctid=16c3b6366b351c-0f2420973d491b-3f385c06-100200-16c3b6366b4798; CNZZDATA1253492138=505308733-1564361008-https%253A%252F%252Fsp0.baidu.com%252F%7C1564361008; CNZZDATA1254525948=379974219-1564360524-https%253A%252F%252Fsp0.baidu.com%252F%7C1564360524; CNZZDATA1255633284=627392219-1564363076-https%253A%252F%252Fsp0.baidu.com%252F%7C1564363076; CNZZDATA1255604082=1672196261-1564359919-https%253A%252F%252Fsp0.baidu.com%252F%7C1564359919; _jzqa=1.3394817871598477000.1564364466.1564364466.1564364466.1; _jzqc=1; _jzqy=1.1564364466.1564364466.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E7%BD%91.-; _jzqckmp=1; _qzjc=1; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216c3b63680a9d-0220270279df23-3f385c06-1049088-16c3b63680b575%22%2C%22%24device_id%22%3A%2216c3b63680a9d-0220270279df23-3f385c06-1049088-16c3b63680b575%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fsp0.baidu.com%2F9q9JcDHa2gU2pMbgoY3K%2Fadrc.php%3Ft%3D06KL00c00fZg9KY0dyPb0nVfAsasHW4I00000PbxQ7C00000VtSvCC.THLKVQ1i1x60UWdBmy-bIfK15ymduWf1nAwhnjKWrjR4n1D0IHdKPjNjwjujrDndfW0krRfknWmswDcvrRuarRNArDm%22%2C%22%24latest_referrer_host%22%3A%22sp0.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E9%93%BE%E5%AE%B6%E7%BD%91%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22sousuo%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; _ga=GA1.2.736178042.1564364468; _gid=GA1.2.300375402.1564364468; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1564364475; Qs_lvt_200116=1564364474; Qs_pv_200116=3730108294450642000%2C3833618644766064600; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1564364491; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiODM1MGIyODUzMWEwOWQyZDJkZjI4YTM0ODlhOTNjMWRlNzQ5OWYxY2EwMTk4ZmZlOTE5YTkyZmExYmIwOTcxNWEwOWM3YmY4OGM4ZmI3YzRiNmY2MjMyOWY0MThhOWNiYjk0ZDE0ZGQzYzk1NDQ0ZjY4Yzc0NTBkMmEwN2RlOWQzZTQ2OTMyMGNmNGVlMmYzZTc2YjNhZmRjYzFjMGJkMTA5MzFkODUyZTg2ZjE1NDc0ZjA1MTc3N2ZhMTMxNDIzNDYyNDI3ZDQyNDFmMWE1NzVlODk0NGFhOWYwNGExMzhiNzU2MmFmNTJkNzFkMzZkMWZjNTg2N2JiNzlkYjhlNzY4YmQ4NGQ3NmU5ZDhiOGY3MjA4M2M5MmY3YzZhMThiNTUwMzAyM2U5Y2IwMTQ3ZjIyZWQ1NmE1MTBlNTkwOGZjOWVjMGJjZjY5NGRlZWZkMDFmMGQ2NjBlY2U2YzVlN1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIyYzA1NTlmZFwifSIsInIiOiJodHRwczovL25qLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvZ3Vsb3UvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _qzja=1.2065536459.1564364466153.1564364466153.1564364466154.1564364475168.1564364491288.0.0.0.3.1; _qzjb=1.1564364466153.3.0.0.0; _qzjto=3.1.0; _jzqb=1.3.10.1564364466.1''',
            'Host': 'nj.lianjia.com',
            'Referer': 'https://nj.lianjia.com/ershoufang/gulou/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers).text
        # with open('./lian.html', 'w', encoding='utf8')as f:
        #     f.write(res)
        return res

    def run(self):
        res = self.get_html(self.url)
        res = etree.HTML(res)
        # hotel_title = res.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[1]/a/text()')
        detail_url = res.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[1]/a/@href')
        for i in detail_url:
            detail_html = self.get_html(i)
            # print(detail_html)
            detail_html = etree.HTML(detail_html)
            detail_title = detail_html.xpath('//h1/text()')[0]
            print(detail_title)


if __name__ == '__main__':
    for i in range(1,101):
        url = 'https://nj.lianjia.com/ershoufang/gulou/pg{}/'.format(i)
    # url = 'https://nj.lianjia.com/ershoufang/gulou/pg2/'
        print(i)
        lian = LianJiaSpider(url)
        lian.run()
