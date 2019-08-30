import requests
from lxml import etree


class ZhongGuanCunSpider(object):
    def __init__(self):
        self.url_1='http://detail.zol.com.cn'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Cookie': 'ip_ck=7sWH5fz1j7QuOTI2MjYyLjE1NjIyODgyNDQ%3D; lv=1564487862; vn=4; Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0=1562288249,1562672508,1563262415,1564487862; z_pro_city=s_provice%3Djiangsu%26s_city%3Dnanjing; gr_user_id=c1b54581-be03-4a55-b35e-db6321e3cc6a; gr_session_id_9b437fe8881a7e19=6854bf20-744c-4e4b-bce6-1217426bfff0; visited_serachKw=cpu; gr_session_id_9b437fe8881a7e19_6854bf20-744c-4e4b-bce6-1217426bfff0=true; Adshow=4; Hm_lpvt_ae5edc2bc4fc71370807f6187f0a2dd0=1564487913; visited_subcateId=28|383; visited_subcateProId=28-0|383-0; userProvinceId=25; userCityId=123; userCountyId=0; userLocationId=23; realLocationId=23; userFidLocationId=23; z_day=izol101693=2&ixgo20=1&rdetail=4; listSubcateId=5; questionnaire_pv=1564444808'
        }

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers)
        return res.text

    def run(self, url):
        res = self.get_html(url)
        res = etree.HTML(res)
        title = res.xpath('//*[@id="J_PicMode"]/li/h3/a/@href')
        for i in title:
            detail_html = self.get_html(self.url_1 + i)
            detail_html = etree.HTML(detail_html)
            detail_url = detail_html.xpath('//*[@id="_j_tag_nav"]/ul/li[2]/a/@href')[0]
            self.get_html('')
            print(detail_url)


if __name__ == '__main__':
    url = 'http://detail.zol.com.cn/motherboard/?search_keyword=%D6%F7%B0%E5'
    tu = ZhongGuanCunSpider()
    tu.run(url)
