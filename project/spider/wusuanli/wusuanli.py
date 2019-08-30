# import datetime
# import json
# import random
# import re
# import time
# import pymysql
# import requests
# from lxml import etree
#
#
# class WuSuSpider(object):
#     def __init__(self):
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
#             'Cookie': 'Hm_lvt_e496ad63f9a0581b5e13ab0975484c5c=1566438073; Hm_lvt_bc6f194cb44b24b9f44f1c8766c28008=1566438073; showSubSiteTip=false; _t=bdb3679f-1566-4bce-a515-ddc4568a1118; sessionId=6187bf70-947e-46e9-be80-89c2403a4235; subSiteCode=bj; _u=49fb2c48-90eb-4039-b2ec-b763b0075796; _i=c7076e05-e93d-489e-bf20-7e489e16ee94; _p=84c671c9-d83a-49ba-a9df-200f905f8047; Hm_lpvt_bc6f194cb44b24b9f44f1c8766c28008=1566438374; Hm_lpvt_e496ad63f9a0581b5e13ab0975484c5c=1566438374',
#             'Pragma': 'no-cache',
#
#         }
#         self.url_list_page = 'https://www.itslaw.com/api/v1/caseFiles?startIndex=40&countPerPage=20&sortType=1&conditions=searchWord%2B%E5%85%AC%E7%9B%8A%E8%AF%89%E8%AE%BC%2B1%2B%E5%85%AC%E7%9B%8A%E8%AF%89%E8%AE%BC'
#
#     def get_html(self, url):
#         try:
#             # time.sleep(1)
#             res = requests.get(url=url, headers=self.headers).text
#         except Exception:
#             res=''
#             # time.sleep(1)
#             self.get_html(url)
#         return res
#
#     def write_html(self, path, content):
#         """写入文本"""
#         with open(path, 'a', encoding='utf8')as f:
#             f.write(content)
#
#     def etree_html(self, content):
#         """转为html"""
#         res = etree.HTML(content)
#         return res

#     def proxies(self):
#         """代理"""
#         proxies = {
#             'http': 'http://183.38.30.221:2736'
#         }
#         return proxies

#     def run(self,):
#         all_html = self.get_html(self.url_list_page)
#         print(all_html)

#     def connection(self, *args):
#         """连接mysql"""
#         try:
#             conn = pymysql.connect(host='218.94.82.249',
#                                    port=8015,
#                                    user='rhino',
#                                    passwd="rhino",
#                                    db='ticket_info')
#         except Exception:
#             conn = ''
#             self.connection(self, *args)
#         cursor = conn.cursor()
#         # sql = 'insert into table_all_train (trainNo,dptStationName,dptTime,arrStationName,arrTime,allStationName,dptDate,teDengZuoPrice,teDengZuoTicket,shangWuZuoPrice,shangWuZuoTicket,yiDengZuoPrice,yiDengZuoTicket,erDengZuoPrice,erDengZuoTicket,wuZuoPrice,woZuoTicket,yiDengWoPrice,yiDengWoTicket,erDengWoPrice,erDengWoTicket,dongWoPrice,dongWoTicket,yingWoPrice,yingWoTicket,yingZuoPrice,yingZuoTicket,ruanWoPrice,ruanWoTicket,gaoJiYingWoPrice,gaoJiYingWoTicket,gaoJiRuanWoPrice,gaoJiRuanWoTicket) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
#         # cursor.execute(sql, list(args))
#         conn.commit()
#         cursor.close()
#         conn.close()


# if __name__ == '__main__':
#     wusu = WuSuSpider()
#     wusu.run()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Pragma': 'no-cache',
}
cookie = {
    'Cookie:Hm_lvt_e496ad63f9a0581b5e13ab0975484c5c': '1566438073',
    'Hm_lvt_bc6f194cb44b24b9f44f1c8766c28008': '1566438073',
    'showSubSiteTip': 'false',
    '_t': 'bdb3679f-1566-4bce-a515-ddc4568a1118',
    'sessionId': '6187bf70-947e-46e9-be80-89c2403a4235',
    'subSiteCode': 'bj',
    '_u': '49fb2c48-90eb-4039-b2ec-b763b0075796',
    '_i': 'c7076e05-e93d-489e-bf20-7e489e16ee94',
    '_p': '84c671c9-d83a-49ba-a9df-200f905f8047',
    'Hm_lpvt_bc6f194cb44b24b9f44f1c8766c28008': '1566438374',
    'Hm_lpvt_e496ad63f9a0581b5e13ab0975484c5c': '1566438374',
}
url = 'https://www.itslaw.com/api/v1/caseFiles?startIndex=40&countPerPage=20&sortType=1&conditions=searchWord%2B%E5%85%AC%E7%9B%8A%E8%AF%89%E8%AE%BC%2B1%2B%E5%85%AC%E7%9B%8A%E8%AF%89%E8%AE%BC'
import requests

res = requests.get(url, headers=headers, cookies=cookie)
print(res)
