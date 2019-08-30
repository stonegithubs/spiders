import re
import time

import pandas as pd
import requests


def get_data(page):
    """"""
    url = "http://hotel.elong.com/ajax/list/asyncsearch"
    data = {
        "code": "7809114",
        "listRequest.areaID": "",
        "listRequest.bookingChannel": 5,
        "listRequest.cardNo": "192928",
        "listRequest.checkInDate": "2018-03-19 00:00:00",
        "listRequest.checkOutDate": "2018-03-20 00:00:00",
        "listRequest.cityID": "0401",
        "listRequest.cityName": "重庆市",
        "listRequest.customLevel": "11",
        "listRequest.distance": "20",
        "listRequest.endLat": 0,
        "listRequest.endLng": 0,
        "listRequest.facilityIds": "",
        "listRequest.highPrice": 0,
        "listRequest.hotelBrandIDs": "",
        "listRequest.isAdvanceSave": "false",
        "listRequest.isAfterCouponPrice": "true",
        "listRequest.isCoupon": "false",
        "listRequest.isDebug": "false",
        "listRequest.isLimitTime": "false",
        "listRequest.isLogin": "false",
        "listRequest.isMobileOnly": "true",
        "listRequest.isNeed5Discount": "true",
        "listRequest.isNeedNotContractedHotel": "false",
        "listRequest.isNeedSimilarPrice": "false",
        "listRequest.isReturnNoRoomHotel": "true",
        "listRequest.isStaySave": "false",
        "listRequest.isTrace": "false",
        "listRequest.isUnionSite": "false",
        "listRequest.keywords": "",
        "listRequest.keywordsType": 0,
        "listRequest.language": "cn",
        "listRequest.listType": 0,
        "listRequest.lowPrice": 0,
        "listRequest.orderFromID": "50793",
        "listRequest.pageIndex": page,
        "listRequest.pageSize": 20,
        "listRequest.payMethod": 0,
        "listRequest.personOfRoom": 0,
        "listRequest.poiId": 0,
        "listRequest.promotionChannelCode": "0000",
        "listRequest.proxyID": "ZD",
        "listRequest.rankType": 0,
        "listRequest.returnFilterItem": "true",
        "listRequest.sellChannel": 1,
        "listRequest.seoHotelStar": 0,
        "listRequest.sortDirection": 1,
        "listRequest.sortMethod": 1,
        "listRequest.starLevels": "",
        "listRequest.startLat": 0,
        "listRequest.startLng": 0,
        "listRequest.taRecommend": "false",
        "listRequest.themeIds": "",
        "listRequest.ctripToken": "815b07a9-3f97-4ae0-965c-e8d9d3b9a57f",
        "listRequest.elongToken": "jeww06u3-7967-4a47-9e59-91d212f31e82",
    }
    header = {
        'code': '7006269',
        'listRequest.aBTestNewVersion': 'K',
        'listRequest.aBTestVersion': 'new',
        'listRequest.areaID': 'listRequest.bedLargeTypes:',
        'listRequest.bookingChannel': '1',
        'listRequest.breakfasts': '0',
        'listRequest.cancelFree': 'false',
        'listRequest.cardNo': '192928',
        'listRequest.checkInDate': '2019-07-26 00:00:00',
        'listRequest.checkOutDate': '2019-07-27 00:00:00',
        'listRequest.cityID': '1101',
        'listRequest.cityName': '南京',
        'listRequest.customLevel': '11',
        'listRequest.discountIds': 'listRequest.distance: 20000',
        'listRequest.endLat': '0',
        'listRequest.endLng': '0',
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
        'listRequest.lat': '32.0609158',
        'listRequest.listType': '0',
        'listRequest.lng': '118.7916065',
        'listRequest.lowPrice': '0',
        'listRequest.newABVersion': 'B',
        'listRequest.newVersion': 'true',
        'listRequest.orderFromID': '50793',
        'listRequest.pageIndex': '3',
        'listRequest.pageSize': '20',
        'listRequest.payMethod': '0',
        'listRequest.personOfRoom': '0',
        'listRequest.poiId': '0',
        'listRequest.promotionChannelCode': '0000',
        'listRequest.promotionSwitch': '-1',
        'listRequest.proxyID': 'ZD',
        'listRequest.rankType': '0',
        'listRequest.returnFilterItem': 'true',
        'listRequest.sectionId': 'listRequest.sellChannel: 1',
        'listRequest.seoHotelStar': '0',
        'listRequest.sortDirection': '1',
        'listRequest.sortMethod': '1',
        'listRequest.standBack': '-1',
        'listRequest.starLevels': 'listRequest.startLat: 0',
        'listRequest.startLng': '0',
        'listRequest.taRecommend': 'false',
        'listRequest.themeIds': 'listRequest.traceId: 3290baf2-5fdc-42a3-83f1-07e4e595b108',
        'listRequest.version': 'G',
        'listRequest.wordId': 'listRequest.wordType: 0',
        'listRequest.elongToken': '0c1f3683-0ae4-446c-b719-52ad04d85efd',
    }

    response = requests.post(url, data=data, headers=header)
    html = response.json()
    hotel_name = re.findall('target="_blank" title="(.*?)"><span class="icon_nmb">', html['value']['hotelListHtml'])
    hotel_price = re.findall('<span class="h_pri_num ">(.*?)</span>', html['value']['hotelListHtml'])
    hotel_address = re.findall('data-hoteladdress="(.*?)" >', html['value']['hotelListHtml'])
    # 返回酒店名称，酒店价格，酒店地址
    return hotel_name, hotel_price, hotel_address


if __name__ == '__main__':
    hotel_name = []
    hotel_price = []
    hotel_address = []
    for i in range(10):
        hotel_name_, hotel_price_, hotel_address_ = get_data(i)
        hotel_name.extend(hotel_name_)
        hotel_price.extend(hotel_price_)
        hotel_address.extend(hotel_address_)
        time.sleep(1)
        print("已完成第" + str(i) + "页爬取")
    dataframe = pd.DataFrame({'酒店名称': hotel_name, '酒店价格': hotel_price, '酒店地址': hotel_address})
    dataframe.to_csv("hotel.csv", index=False, sep=',', encoding="utf_8_sig")
