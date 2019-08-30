import json
import os
import time

import pymysql
import requests
from lxml import etree


class KuaiDiSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        if not os.path.exists('image'):
            os.mkdir('image')

    def get_html(self, url, num):
        self.data = {
            '__VIEWSTATEGENERATOR': 'DB1FBB6D',
            'cityName': '%E9%87%8D%E5%BA%86',
            'StartTime': '2019-08-20',
            'DepTime': '2019-08-21',
            'RoomGuestCount': '1,1,0',
            'operationtype': 'NEWHOTELORDER',
            'IsOnlyAirHotel': 'F',
            'cityId': '4',
            'cityPY': 'chongqing',
            'cityCode': '023',
            'cityLat': '29.5693030786',
            'cityLng': '106.5579918074',
            'htlPageView': '0',
            'hotelType': 'F',
            'hasPKGHotel': 'F',
            'requestTravelMoney': 'F',
            'isusergiftcard': 'F',
            'useFG': 'F',
            'priceRange': '-2',
            'promotion': 'F',
            'prepay': 'F',
            'IsCanReserve': 'F',
            'OrderBy': '99',
            'checkIn': '2019-08-15',
            'checkOut': '2019-08-16',
            'hidTestLat': '0%7C0',
            'AllHotelIds': '33344529%2C6238298%2C17324394%2C744324%2C28677349%2C435664%2C6424389%2C3484522%2C1719173%2C1451725%2C2295624%2C2638694%2C17491688%2C39697263%2C1214343%2C1691030%2C39032036%2C29783584%2C5256381%2C8553506%2C5982675%2C12785272%2C18005108%2C31099499%2C19088258',
            'isfromlist': 'T',
            'ubt_price_key': 'htl_search_result_promotion',
            'isHuaZhu': 'False',
            'traceAdContextId': 'v2_H4sIAAAAAAAAAD3Ouw0CMRAEUJFRAzERwpL3v0szJ853jukSeiBDIqQHkO0jfRrNzP59f34e6fDaKQXzVG5lYhJVnuDCZzAMtKaIIYqDgTNFY9CATLlxcERXCUc16WF2FGjs4r8a3VgCG4exuXdVlDHIhARoWzoyaD%2BSFQRklBs7%2FG%2BbZ6Hm4oYyOCO08OlIS62zF0tL5ZK4RqQrrZ5g1lUEVHShvPsCAhFmLxQBAAA%3D',
            'allianceid': '0',
            'sid': '0',
            'pyramidHotels': '435664_6%7C2295624_11%7C1691030_16%7C5982675_21',
            'hotelIds': '33344529_1_1,6238298_2_1,17324394_3_1,744324_4_1,28677349_5_1,435664_6_1,6424389_7_1,3484522_8_1,1719173_9_1,1451725_10_1,2295624_11_1,2638694_12_1,17491688_13_1,39697263_14_1,1214343_15_1,1691030_16_1,39032036_17_1,29783584_18_1,5256381_19_1,8553506_20_1,5982675_21_1,12785272_22_1,18005108_23_1,31099499_24_1,19088258_25_1',
            'markType': '0',
            'a': '0',
            'contrast': '0',
            'page': num,
            'contyped': '0',
        }
        res = requests.post(url=url, headers=self.headers, data=self.data)
        return res.content.decode()

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
        num = 700
        while num < 720:
            print('第' + str(num) + '页')
            self.write_html('./爬取进度2.txt','第' + str(num) + '页')
            # time.sleep(1)
            all_html = self.get_html(url, num)
            try:
                all_json = json.loads(all_html)
            except Exception:
                print('该打码了')
                print('该打码了')
                print('该打码了')
                print('该打码了')
                print('该打码了')
                print('该打码了')
                print('该打码了')
                print('该打码了')
                print('该打码了')
                print('该打码了')
                input()
                all_html = self.get_html(url, num)
                all_json = json.loads(all_html)
            hotelList = all_json.get('hotelPositionJSON')
            url_list = []
            for i in hotelList:
                url_list.append(i['id'])
            detail_url = 'https://hotels.ctrip.com/hotel/{}.html?isFull=F&checkIn=2019-08-15&checkOut=2019-08-16'
            detail_url_list = []
            for j in url_list:
                detail_url1 = detail_url.format(j)
                detail_url_list.append(detail_url1)
            # print(detail_url_list)
            # a = 1
            for k in detail_url_list:
                # time.sleep(1)
                detail_html = requests.get(k, self.headers).content.decode()
                detail_html = etree.HTML(detail_html)
                try:
                    hotel_name = detail_html.xpath('//h2[@class="cn_n"]/text()')[0]
                except Exception:
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    print('该打码了')
                    input()
                    detail_html = requests.get(k, self.headers).content.decode()
                    detail_html = etree.HTML(detail_html)
                    hotel_name = detail_html.xpath('//h2[@class="cn_n"]/text()')[0]
                hotel_name = hotel_name.strip()  # 酒店名
                print(hotel_name)
                # print(a)
                # a += 1
                address_list = detail_html.xpath('//div[@class="adress"]//text()')[:6]
                address = ''  # 酒店地址
                for add in address_list:
                    address += add.strip()
                # print(address)
                hotel_info = \
                    detail_html.xpath('//span[@id="ctl00_MainContentPlaceHolder_hotelDetailInfo_lbDesc"]/text()')[
                        0]
                hotel_info = hotel_info.replace('\r\n','').replace('　　','')  # 酒店简介
                # print(hotel_info)
                internets = detail_html.xpath('//tr[1]//ul/li/@title')  # 网络设施
                internet=''
                if internets:
                    for inter in internets:
                        internet += inter+' '
                # print(internet)
                servers = detail_html.xpath('//tr[3]//ul/li/@title')  # 前台服务
                server = ''
                if servers:
                    for serv in servers:
                        server += serv+' '
                # print(server)
                cafe_servers = detail_html.xpath('//tr[4]//ul/li/@title')  # 餐饮服务
                cafe_server = ''
                if cafe_servers:
                    for cafe in cafe_servers:
                        cafe_server += cafe
                # print(cafe_server)
                business_affairs_servers = detail_html.xpath('//tr[5]//ul/li/@title')  # 商务服务
                business_affairs_server = ''
                if business_affairs_servers:
                    for busin in business_affairs_servers:
                        business_affairs_server+=busin+' '
                # print(business_affairs_server)
                in_out = detail_html.xpath('//*[@id="hotel_info_comment"]//tr[1]/td/text()')[0]  # 入离时间
                in_out = in_out.replace('     ', '')
                children_list = detail_html.xpath('//*[@id="hotel_info_comment"]/div/div[7]//tr[2]/td//text()')
                children = ''
                if children_list:
                    for child in children_list:
                        children += child.replace('•', ' ')
                else:
                    children = ''
                # print(children)
                food = detail_html.xpath('//*[@id="hotel_info_comment"]/div/div[7]//tr[3]/td//text()')
                foods = ''  # 早餐信息
                if food:
                    for foo in food:
                        foods += foo.strip() + '\t'
                # print(foods)
                try:
                    pet = detail_html.xpath('//*[@id="hotel_info_comment"]/div/div[7]//tr[4]/td/text()')[0]
                except Exception:
                    pet = ''
                # print(rb)
                img_url_list = detail_html.xpath('//div[@class="forward"]//@src')
                # print(img_url_list)
                num_1 = 1
                for img_url in img_url_list:
                    # imgurl = img_url.replace('//','')
                    img_content = requests.get('http:' + img_url, self.headers).content
                    if not os.path.exists('image/' + hotel_name.replace('/','')):
                        os.mkdir('image/' + hotel_name.replace('/',''))
                    with open('image/' + hotel_name.replace('/','') + '/%s.jpg' % str(num_1), 'wb')as f:
                        f.write(img_content)
                    num_1 += 1
                self.connection(hotel_name, address, hotel_info, str(internet), str(server), str(cafe_server),
                                str(business_affairs_server), in_out, children, foods, pet, 'image/' + hotel_name)
            num += 1

    def connection(self, *args):
        conn = pymysql.connect(host='218.94.82.249',
                               port=8015,
                               user='rhino',
                               passwd="rhino",
                               db='ticket_info')
        cursor = conn.cursor()
        sql = 'insert into table_hotel (hotel_name,address,hotel_info,internet,server,cafe_server,business_affairs_server,in_out,children,foods,pet,imgs) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        cursor.execute(sql, list(args))
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    url = 'https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
    kuaidi = KuaiDiSpider()
    kuaidi.run(url)
