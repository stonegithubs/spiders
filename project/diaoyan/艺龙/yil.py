import json
import time
import requests
from lxml import etree


class YiLongSpider(object):
    def __init__(self,page):
        self.url = 'http://hotel.elong.com/ajax/tmapilist/asyncsearch'
        self.url2='http://fireeye1.elong.com/h5/log?cookieId=0f7fc712-6040-4ca6-a95c-7d530fd739c5&channel=&userAgent=Mozilla%2F5.0%20(Windows%20NT%206.1%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F75.0.3770.142%20Safari%2F537.36&screen=1366*768&dataLen=2050&httpMethod=post&exception=false&requestTime=919&url=http%3A%2F%2Fhotel.elong.com%2Fajax%2Ftmapilist%2Fasyncsearch&type=xhr&time='+str(int(time.time()*1000))+'&pageUrl=http%3A%2F%2Fhotel.elong.com%2Fsearch%2Flist_cn_1101.html'
        self.data = {
            'code': 7006269,
            'listRequest.aBTestNewVersion': 'K',
            'listRequest.aBTestVersion': 'new',
            'listRequest.areaID': 'listRequest.bedLargeTypes:',
            'listRequest.bookingChannel': 1,
            'listRequest.breakfasts': 0,
            'listRequest.cancelFree': 'false',
            'listRequest.cardNo': '192928',
            'listRequest.checkInDate': '2019-07-26 00:00:00',
            'listRequest.checkOutDate': '2019-07-27 00:00:00',
            'listRequest.cityID': 1101,
            'listRequest.cityName': '南京',
            'listRequest.customLevel': 11,
            'listRequest.discountIds': 'listRequest.distance: 20000',
            'listRequest.endLat': 0,
            'listRequest.endLng': 0,
            'listRequest.facilityIds': 'listRequest.highPrice: 0',
            'listRequest.hotelBrandIDs': 'listRequest.isAdvanceSave: false',
            'listRequest.isAfterCouponPrice': 'true',
            'listRequest.isCoupon': 'false',
            'listRequest.isDebug': 'false',
            'listRequest.isLimitTime': 'false',
            'listRequest.isLogin': 'false',
            'listRequest.isMobileOnly': 'true',
            'listRequest.isNeed5Discount': 'true',
            'listRequest.isNeedNotContractedHotel': 'false',
            'listRequest.isNeedSimilarPrice': 'false',
            'listRequest.isReturnNoRoomHotel': 'true',
            'listRequest.isStaySave': 'false',
            'listRequest.isTrace': 'false',
            'listRequest.isUnionSite': 'false',
            'listRequest.isnstantConfirm': 'false',
            'listRequest.keywords': 'listRequest.keywordsType: 0',
            'listRequest.language': 'cn',
            'listRequest.lat': 32.0609158,
            'listRequest.listType': 0,
            'listRequest.lng': 118.7916065,
            'listRequest.lowPrice': 0,
            'listRequest.newABVersion': 'B',
            'listRequest.newVersion': 'true',
            'listRequest.orderFromID': 50793,
            'listRequest.pageIndex': page,
            'listRequest.pageSize': 20,
            'listRequest.payMethod': 0,
            'listRequest.personOfRoom': 0,
            'listRequest.poiId': 0,
            'listRequest.promotionChannelCode': 0000,
            'listRequest.promotionSwitch': -1,
            'listRequest.proxyID': 'ZD',
            'listRequest.rankType': 0,
            'listRequest.returnFilterItem': 'true',
            'listRequest.sectionId': 'listRequest.sellChannel: 1',
            'listRequest.seoHotelStar': 0,
            'listRequest.sortDirection': 1,
            'listRequest.sortMethod': 1,
            'listRequest.standBack': -1,
            'listRequest.starLevels': 'listRequest.startLat: 0',
            'listRequest.startLng': 0,
            'listRequest.taRecommend': 'false',
            'listRequest.themeIds': 'listRequest.traceId: 3290baf2-5fdc-42a3-83f1-07e4e595b108',
            'listRequest.version': 'G',
            'listRequest.wordId': 'listRequest.wordType: 0',
            'listRequest.elongToken': '0c1f3683-0ae4-446c-b719-52ad04d85efd',
        }
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://hotel.elong.com',
            'Referer': 'http://hotel.elong.com/search/list_cn_1101.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.headers2={'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
                       'Referer: http://hotel.elong.com/search/list_cn_1101.html'}

    def get_html(self):
        response = requests.post(url=self.url,headers=self.headers,data=self.data)
        print(response)
        return response.json()

    def get_html2(self):
        requests.get(url=self.url2,headers=self.headers2)
        # print(a.status_code)

    def run(self):
        req_html = self.get_html()
        # self.get_html2()
        result = json.dumps(req_html)
        dic_html = json.loads(result)
        hotel_html = etree.HTML(dic_html['value']['hotelListHtml'])
        # print(dic_html['value']['hotelListHtml'])
        hotel_title = hotel_html.xpath('//div/div[2]/div[3]/p[1]/a/span[2]/text()')
        hotel_price = hotel_html.xpath('//div/div[2]/div[1]/div[1]/a/span[2]/text()')
        print(hotel_title)
        with open('./hotel.txt','a',encoding='utf8')as f:
            f.write(str(hotel_title))
            f.write('\n')
        # print(hotel_price)

        # print(type(res))

if __name__ == '__main__':
    for i in range(1,325):
        yi = YiLongSpider(i)
        print(i)
        yi.run()