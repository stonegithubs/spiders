import json
import random
import re
import time

import pymysql
import requests
from lxml import etree

class QuNaSpider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self._m = str(int(time.time() * 1000))

    def get_url(self):
        with open('./new_city.txt', 'r', encoding='utf8')as f:
            content = f.read()
        station_list = content.split()

        # for start_station in station_list:
        #     for end_station in station_list:
        #         if start_station == end_station:
        #             continue
        #         else:
        #             self.run(start_station, end_station)
        city = '重庆'
        for i in station_list:
            if i == city:
                continue
            else:
                # print(city,i)
                self.run(city, i)
        for j in station_list:
            if j == city:
                continue
            else:
                # print(city,j)
                self.run(j, city)

    def get_html(self, url):
        res = requests.get(url=url, headers=self.headers)
        return res.text

    def write_html(self, path, content):
        with open(path, 'a', encoding='utf8')as f:
            f.write(content)

    def etree_html(self, content):
        res = etree.HTML(content)
        return res

    def proxies(self):
        ip_list = """115.151.239.149:4217
106.56.90.169:4265
113.103.120.217:4237
114.220.149.111:4236
140.250.123.17:4256
115.205.244.143:4263
125.122.49.79:4217
60.178.27.144:4225
220.165.154.82:4271
115.151.239.179:4218
115.153.8.21:4248
117.94.213.31:4216
112.87.78.28:4250
114.104.235.17:4227
27.152.91.103:4203
114.99.21.244:4276
112.114.165.33:4228
60.166.151.111:4241"""
        ip_list = ip_list.split()
        # print(ip_list)
        i = random.choice(ip_list)
        # for i in ip_list:
        proxies = {
            'http': 'http://' + i
        }
        # print(proxies)
        return proxies

    def all_station_info(self, dptStationName, arrStationName, trainNo, dptDate):
        """
        :param dptStationName: 出发站
        :param arrStationName: 终点站
        :param trainNo: 车次
        :param dptDate: 出发时间
        :return: 写库
        """
        url = 'https://train.qunar.com/dict/open/seatDetail.do?dptStation=' + dptStationName + '&arrStation=' + arrStationName + '&date=' + dptDate + '&trainNo=' + trainNo + '&user=neibu&source=www&needTimeDetail=true'
        while True:
            time.sleep(0.3)
            res = self.get_html(url)
            if json.loads(res).get('ret') == True:
                break

        time.sleep(0.3)
        try:
            city_all_list = json.loads(res)['data']['stationItemList']
            city_list = []
            for x in city_all_list:
                city_list.append(x['stationName'])
            # print('车次：' + trainNo, '所有站点为' + str(city_list))
            a = ','.join(city_list)
        except Exception:
            a = ''
        return a

    def run(self, start_station, end_station):
        url = 'https://train.qunar.com/dict/open/s2s.do?callback=jQuery172012216425254778174_' + self._m + '&dptStation=' + start_station + '&arrStation=' + end_station + '&date=2019-08-09&type=normal&user=neibu&source=site&start=1&num=500&sort=3&_=' + self._m
        all_html = self.get_html(url)
        # time.sleep(1)
        res = re.findall(r'(.*?){', all_html)
        res = all_html.replace(res[0], '').replace(');', '')
        res = json.loads(res)
        # try:
        #     res = res['data']
        # except Exception:
        #     self.run(start_station, end_station)
        # res = res.get('data')
        # print('res',res)
        # print(type(res))
        try:
            res = res['data']
        except Exception:
            print('没有车次')
            return 0
        if res:
            # data = {}
            # time.sleep(1)
            dptStation = res['dptStation']  # 起始站
            arrStation = res['arrStation']  # 终点站
            dptDate = res['dptDate']  # 出发日期
            print('您将于' + dptDate + '从' + dptStation + '到' + arrStation)
            # if res['s2sBeanList']:
            if res.get('s2sBeanList'):
                # print('1',res.get('s2sBeanList'))
                # print('2',type(res.get('s2sBeanList')))
                train_list = res['s2sBeanList']
                for j in train_list:
                    data_info = []
                    trainNo = j['trainNo']  # 车次
                    print('车次',trainNo)
                    startStationName = j['startStationName']  # 车次始发站
                    endStationName = j['endStationName']  # 车次终点站
                    dptStationName = j['dptStationName']  # 出发地
                    arrStationName = j['arrStationName']  # 到达地
                    dptTime = j['dptTime']  # 开车时间
                    arrTime = j['arrTime']  # 到达时间
                    dayDifference = j['dayDifference']  # 是否当日到达
                    if dayDifference == '0':
                        dayDifference = '当日'
                    elif dayDifference == '1':
                        dayDifference = '次日'
                    elif dayDifference == '2':
                        dayDifference = '第三天'
                    else:
                        dayDifference = '暂未查询到第几天到达'
                    all_station = self.all_station_info(dptStationName, arrStationName, trainNo,dptDate)  # 获取全部站点
                    try:
                        one_p = j['seats']['特等座']['price']
                        one_t = j['seats']['特等座']['count']
                    except Exception:
                        one_p = ''
                        one_t = ''
                    try:
                        two_p = j['seats']['商务座']['price']
                        two_t = j['seats']['商务座']['count']
                    except Exception:
                        two_p = ''
                        two_t = ''
                    try:
                        there_t = j['seats']['一等座']['price']
                        there_p = j['seats']['一等座']['count']
                    except Exception:
                        there_t = ''
                        there_p = ''
                    try:
                        four_p = j['seats']['二等座']['price']
                        four_t = j['seats']['二等座']['count']
                    except Exception:
                        four_p = ''
                        four_t = ''
                    try:
                        five_p = j['seats']['无座']['price']
                        five_t = j['seats']['无座']['count']
                    except Exception:
                        five_p = ''
                        five_t = ''
                    try:
                        six_p = j['seats']['一等卧']['price']
                        six_t = j['seats']['一等卧']['count']
                    except Exception:
                        six_p = ''
                        six_t = ''
                    try:
                        seven_p = j['seats']['二等卧']['price']
                        seven_t = j['seats']['二等卧']['count']
                    except Exception:
                        seven_p = ''
                        seven_t = ''
                    try:
                        eight_p = j['seats']['动卧']['price']
                        eight_t = j['seats']['动卧']['count']
                    except Exception:
                        eight_p = ''
                        eight_t = ''
                    try:
                        nine_p = j['seats']['硬卧']['price']
                        nine_t = j['seats']['硬卧']['count']
                    except Exception:
                        nine_p = ''
                        nine_t = ''
                    try:
                        ten_p = j['seats']['硬座']['price']
                        ten_t = j['seats']['硬座']['count']
                    except Exception:
                        ten_p = ''
                        ten_t = ''
                    try:
                        eleven_p = j['seats']['软卧']['price']
                        eleven_t = j['seats']['软卧']['count']
                    except Exception:
                        eleven_p = ''
                        eleven_t = ''
                    try:
                        twelve_p = j['seats']['高级硬卧']['price']
                        twelve_t = j['seats']['高级硬卧']['count']
                    except Exception:
                        twelve_p = ''
                        twelve_t = ''
                    try:
                        thirteen_p = j['seats']['高级软卧']['price']
                        thirteen_t = j['seats']['高级软卧']['count']
                    except Exception:
                        thirteen_p = ''
                        thirteen_t = ''
                    self.connection(trainNo, dptStationName, dptTime, arrStationName, dayDifference + arrTime,
                                    str(all_station), one_p, one_t, two_p, two_t, there_p, there_t, four_p, four_t,
                                    five_p, five_t, six_p, six_t, seven_p, seven_t, eight_p, eight_t, nine_p, nine_t,
                                    ten_p, ten_t, eleven_p, eleven_t, twelve_p, twelve_t, thirteen_p, thirteen_t)

            else:
                print(res['s2sBeanList'], '没有车次')
        else:
            self.run(start_station, end_station)

    def create_file(self):
        keys = ['车次', '出发地', '开车时间', '到达地', '到达时间', '全程站点', '特等座票价', '余票', '商务座票价', '余票', '一等座票价', '余票', '二等座票价', '余票',
                '无座票价', '余票', '一等卧票价', '余票', '二等卧票价', '余票', '动卧票价', '余票', '硬卧票价', '余票', '硬座票价', '余票', '软卧票价', '余票',
                '高级硬卧票价', '余票', '高级软卧票价', '余票']

        a = '#'.join(keys)
        with open('./train.txt', 'w', encoding='utf8')as f:
            f.write(a)

    def connection(self, *args):

        conn = pymysql.connect(host='218.94.82.249',
                               port=8015,
                               user='rhino',
                               passwd="rhino",
                               db='ticket_info')
        cursor = conn.cursor()
        sql = 'insert into table_train (trainNo,dptStationName,dptTime,arrStationName,arrTime,allStationName,teDengZuoPrice,teDengZuoTicket,shangWuZuoPrice,shangWuZuoTicket,yiDengZuoPrice,yiDengZuoTicket,erDengZuoPrice,erDengZuoTicket,wuZuoPrice,woZuoTicket,yiDengWoPrice,yiDengWoTicket,erDengWoPrice,erDengWoTicket,dongWoPrice,dongWoTicket,yingWoPrice,yingWoTicket,yingZuoPrice,yingZuoTicket,ruanWoPrice,ruanWoTicket,gaoJiYingWoPrice,gaoJiYingWoTicket,gaoJiRuanWoPrice,gaoJiRuanWoTicket) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        cursor.execute(sql, list(args))
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    quna = QuNaSpider()
    quna.get_url()
