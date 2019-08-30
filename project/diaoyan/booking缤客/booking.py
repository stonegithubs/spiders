import requests
from lxml import etree


class BooKingSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36', }
        self.base_url = 'https://www.booking.com'

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers)
        return res.text

    def write_html(self,path,content):
        with open(path,'w',encoding='utf8')as f:
            f.write(content)

    def run(self, url):
        res = self.get_html(url)
        res = etree.HTML(res)
        url_list = res.xpath('//*[@id="hotellist_inner"]//h3/a/@href')
        for detail_url_list in url_list:
            # break
            # detail_url = self.base_url+detail_url_list
            # print(detail_url)
            a = detail_url_list.split()
            # print(a)
            c = ''
            for i in a:
                c += i
            d = self.base_url+c
            print(d)
            detail_html = self.get_html(d)
            self.write_html('./booking.html', detail_html)
            detail_content = etree.HTML(detail_html)
            hotel_title = detail_content.xpath('//*[@id="hotellist_inner"]/div[2]/div[2]/div[1]/div[1]/div[1]/h3/a/span[1]/text()')
            print(hotel_title)


if __name__ == '__main__':
    url = 'https://www.booking.com/searchresults.zh-cn.html?aid=334565&label=baidu-brandzone_booking-brand-list1&sid=69db5ac6a68e89c8031cbf4c68953961&tmpl=searchresults&class_interval=1&dest_id=-1919548&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=index&src_elem=sb&srpvid=a8af0973c3b30097&ss=%E5%8D%97%E4%BA%AC&ss_all=0&ssb=empty&sshis=0&rows=15'
    tu = BooKingSpider()
    tu.run(url)
