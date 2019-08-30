import json
import re
import time

import requests
from lxml import etree


class QuNaSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self._m = str(int(time.time() * 1000))

    def get_url(self):
        url = 'https://train.qunar.com/dict/open/s2s.do?callback=jQuery172012216425254778174_' + self._m + '&dptStation=南京&arrStation=上海&date=2019-08-09&type=normal&user=neibu&source=site&start=1&num=500&sort=3&_=' + self._m
        return url

    def get_html(self,url):
        res = requests.get(url=url, headers=self.headers)
        return res.text

    def write_html(self, path, content):
        with open(path, 'a', encoding='utf8')as f:
            f.write(content)

    def etree_html(self, content):
        res = etree.HTML(content)
        return res

    def proxies(self):
        proxies = {
            'https': 'https://36.7.26.106:4203'
        }
        return proxies

    def all_station_info(self,dptStationName,arrStationName,trainNo,dptDate):
        """
        :param dptStationName: 出发站
        :param arrStationName: 终点站
        :param trainNo: 车次
        :param dptDate: 出发时间
        :return: 写库
        """
        url='https://train.qunar.com/dict/open/seatDetail.do?dptStation='+dptStationName+'&arrStation='+arrStationName+'&date='+dptDate+'&trainNo='+trainNo+'&user=neibu&source=www&needTimeDetail=true'
        res = self.get_html(url)
        time.sleep(1)
        city_all_list = json.loads(res)['data']['stationItemList']
        city_list = []
        for x in city_all_list:
            city_list.append(x['stationName'])
        print('车次：'+trainNo,'所有站点为'+str(city_list))

    def run(self):
        all_html = self.get_html(self.get_url())
        res = re.findall(r'(.*?){', all_html)
        res = all_html.replace(res[0], '').replace(');', '')
        res = json.loads(res)
        res = res['data']
        dptStation = res['dptStation']  # 起始站
        arrStation = res['arrStation']  # 终点站
        dptDate = res['dptDate']  # 出发日期
        print('您将于' + dptDate + '从' + dptStation + '到' + arrStation)
        if res['s2sBeanList']:
            train_list = res['s2sBeanList']
            for j in train_list:
                trainNo = j['trainNo']  # 车次
                startStationName = j['startStationName']  # 车次始发站
                endStationName = j['endStationName']  # 车次终点站
                dptStationName = j['dptStationName']  # 出发地
                arrStationName = j['arrStationName']  # 到达地
                dptTime = j['dptTime']  # 开车时间
                arrTime = j['arrTime']  # 到达时间
                dayDifference = j['dayDifference']  # 是否当日到达
                if dayDifference == '0':
                    dayDifference = '当日到达'
                elif dayDifference == '1':
                    dayDifference = '次日到达'
                elif dayDifference == '2':
                    dayDifference = '第三天到达'
                else:
                    dayDifference = '暂未查询到第几天到达'
                print(trainNo)
                if re.findall(r'^G', trainNo):
                    try:
                        vip_price = j['seats']['商务座']['price']
                        vip_ticket = j['seats']['商务座']['count']
                    except Exception:
                        vip_price = '没有商务座'
                        vip_ticket = '没有余票'
                    try:
                        one_price = j['seats']['一等座']['price']
                        one_ticket = j['seats']['一等座']['count']
                    except Exception:
                        one_price = '没有一等座'
                        one_ticket = '没有余票'
                    try:
                        tow_price = j['seats']['二等座']['price']
                        tow_ticket = j['seats']['二等座']['count']
                    except Exception:
                        tow_price = '没有二等座'
                        tow_ticket = '没有余票'
                    try:
                        there_price = j['seats']['无座']['price']
                        there_ticket = j['seats']['无座']['count']
                    except Exception:
                        there_price = '没有无座'
                        there_ticket = '没有余票'
                    try:
                        four_price = j['seats']['特等座']['price']
                        four_ticket = j['seats']['特等座']['count']
                    except Exception:
                        four_price = '没有特等座'
                        four_ticket = '没有余票'
                    print('车次：' + trainNo, '出发地为：' + dptStationName, '开车时间:' + dptTime, '到达地：' + arrStationName,
                          '到达时间：' + arrTime + ',' + dayDifference,
                          '商务座票价：' + str(vip_price), '商务座余票：' + str(vip_ticket),
                          '一等座票价：' + str(one_price), '一等座余票：' + str(one_ticket),
                          '二等座票价：' + str(tow_price), '二等座余票：' + str(tow_ticket),
                          '二等座票价：' + str(tow_price), '二等座余票：' + str(tow_ticket),
                          '无座票价：' + str(there_price), '无座余票：' + str(there_ticket),
                          '特等座票价：' + str(four_price), '特等座余票：' + str(four_ticket))
                elif re.findall(r'^D', trainNo):
                    try:
                        vip_price = j['seats']['一等卧']['price']
                        vip_ticket = j['seats']['一等卧']['count']
                    except Exception:
                        vip_price = '没有一等卧'
                        vip_ticket = '没有余票'
                    try:
                        there_price = j['seats']['二等卧']['price']
                        there_ticket = j['seats']['二等卧']['count']
                    except Exception:
                        there_price = '没有二等卧'
                        there_ticket = '没有余票'
                    try:
                        four_price = j['seats']['动卧']['price']
                        four_ticket = j['seats']['动卧']['count']
                    except Exception:
                        four_price = '没有动卧'
                        four_ticket = '没有余票'
                    try:
                        one_price = j['seats']['无座']['price']
                        one_ticket = j['seats']['无座']['count']
                    except Exception:
                        one_price = '没有无座'
                        one_ticket = '没有余票'
                    try:
                        two_price = j['seats']['二等座']['price']
                        two_ticket = j['seats']['二等座']['count']
                    except Exception:
                        two_price = '没有二等座'
                        two_ticket = '没有余票'
                    print('车次：' + trainNo, '出发地为：' + dptStationName, '开车时间:' + dptTime, '到达地' + arrStationName,
                          '到达时间：' + arrTime + ',' + dayDifference,
                          '一等卧票价：' + str(vip_price),'一等卧余票：' + str(vip_ticket),
                          '无座票价：' + str(one_price), '无座余票：' + str(one_ticket),
                          '二等座票价：' + str(two_price), '二等座余票：' + str(two_ticket),
                          '二等卧票价：' + str(there_price), '二等卧余票：' + str(there_ticket),
                          '动卧票价：' + str(four_price), '动卧余票：' + str(four_ticket))
                else:
                    try:
                        vip_price = j['seats']['硬卧']['price']
                        vip_ticket = j['seats']['硬卧']['count']
                    except Exception:
                        vip_price = '没有硬卧'
                        vip_ticket = '没有余票'
                    one_price = j['seats']['硬座']['price']
                    one_ticket = j['seats']['硬座']['count']
                    try:
                        two_price = j['seats']['软卧']['price']
                        two_ticket = j['seats']['软卧']['count']
                    except Exception:
                        two_price = '没有软卧'
                        two_ticket = '没有余票'
                    there_price = j['seats']['无座']['price']
                    there_ticket = j['seats']['无座']['count']
                    print('车次：' + trainNo, '出发地为：' + dptStationName, '开车时间:' + dptTime, '到达地：' + arrStationName,
                          '到达时间：' + arrTime + ',' + dayDifference,
                          '硬卧票价：' + str(vip_price), '硬卧余票：' + str(vip_ticket),
                          '硬座票价：' + str(one_price), '硬座余票：' + str(one_ticket),
                          '软卧票价：' + str(two_price),'软卧余票：' + str(two_ticket),
                          '无座票价：' + str(there_price), '无座余票：' + str(there_ticket))
                self.all_station_info(dptStationName,arrStationName,trainNo,dptDate)
                # break
        else:
            print(res['s2sBeanList'])


if __name__ == '__main__':
    quna = QuNaSpider()
    quna.run()